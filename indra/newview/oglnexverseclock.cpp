/**
 * TrixieStorm Viewer — OGL grid clock synchronization.
 * Copyright (C) 2026 OpenGenesisLINK contributors.
 * SPDX-License-Identifier: LGPL-2.1-only
 */
#include "llviewerprecompiledheaders.h"
#include "oglnexverseclock.h"

#include "oglnexversegridpolicy.h"
#include "fsgridhandler.h"
#include "fscorehttputil.h"
#include "llcorehttputil.h"
#include "llsdjson.h"

#include <boost/json.hpp>
#include <chrono>
#include <cctype>
#include <cmath>
#include <cstdint>
#include <mutex>

namespace
{
using MonotonicClock = std::chrono::steady_clock;
constexpr auto REFRESH_INTERVAL = std::chrono::seconds(60);
constexpr auto MAX_STALE_AGE = std::chrono::minutes(5);
constexpr size_t MAX_RESPONSE_BYTES = 65536;

struct ServerClock
{
    std::mutex mutex;
    MonotonicClock::time_point lastAttempt{};
    MonotonicClock::time_point lastSample{};
    std::int64_t unixSeconds = 0;
    std::int32_t utcOffsetSeconds = 0;
    std::string abbreviation;
    std::string zone;
    std::uint64_t serial = 0;
    bool requested = false;
    bool valid = false;
};

ServerClock& clock()
{
    static ServerClock instance;
    return instance;
}

bool validZone(const std::string& id)
{
    if (id.empty() || id.size() > 128)
        return false;
    for (unsigned char ch : id)
    {
        if (!std::isalnum(ch) && ch != '/' && ch != '_' &&
            ch != '-' && ch != '+' && ch != ' ' && ch != '.')
            return false;
    }
    return true;
}

bool validLabel(const std::string& value)
{
    if (value.empty() || value.size() > 16)
        return false;
    for (unsigned char ch : value)
    {
        if (!std::isalnum(ch) && ch != '+' && ch != '-' && ch != ':')
            return false;
    }
    return true;
}

void onClockFailure(std::uint64_t request, const char* reason)
{
    ServerClock& state = clock();
    std::lock_guard<std::mutex> lock(state.mutex);
    if (request != state.serial)
        return; // Late response from superseded request.
    LL_DEBUGS("NexVerseClock") << reason << "; retained prior valid clock until expiry"
                             << LL_ENDL;
}

void onClockSuccess(std::uint64_t request, const LLSD& response)
{
    const LLSD::Binary& raw = response[
        LLCoreHttpUtil::HttpCoroutineAdapter::HTTP_RESULTS_RAW].asBinary();
    if (raw.empty() || raw.size() > MAX_RESPONSE_BYTES)
    {
        onClockFailure(request, "Missing or excessive grid-info body");
        return;
    }
    try
    {
        const std::string json(raw.begin(), raw.end());
        const LLSD root = LlsdFromJson(boost::json::parse(json));
        if (root["schema"].asString() != "org.opengenesislink.viewer.grid-info.v1" ||
            root["protocol_version"].asInteger() != 1 ||
            root["server"]["product"].asString() != "OpenGenesisLINK" ||
            !root["features"]["legacy_login"].asBoolean() ||
            !root["features"]["ogl_grid_info_v1"].asBoolean())
        {
            onClockFailure(request, "Unrecognized OGL grid-info response");
            return;
        }

        const std::string login = root["endpoints"]["legacy_login"].asString();
        if (login != OGLNexVerse::GEN1_LOGIN_URI &&
            login != "http://hg.stadt-nexverse.de/")
        {
            onClockFailure(request, "Untrusted login endpoint in discovery");
            return; // Clock data can never change the fixed login authority.
        }

        const LLSD& data = root["clock"];
        if (!data.isMap() ||
            data["schema"].asString() != "org.opengenesislink.viewer.clock.v1")
        {
            onClockFailure(request, "Server does not advertise clock v1");
            return;
        }
        const std::string zone = data["timezone"].asString();
        const std::string label = data["abbreviation"].asString();
        const std::int32_t offset = data["utc_offset_seconds"].asInteger();
        const double epoch = data["unix_time"].asReal();

        if (!validZone(zone) || !validLabel(label) ||
            offset < -14 * 3600 || offset > 14 * 3600 ||
            !std::isfinite(epoch) || epoch < 1577836800.0 ||
            epoch > 4102444800.0 || std::floor(epoch) != epoch)
        {
            onClockFailure(request, "Invalid clock zone, epoch or UTC offset");
            return;
        }

        const auto received = MonotonicClock::now();
        ServerClock& state = clock();
        std::lock_guard<std::mutex> lock(state.mutex);
        if (request != state.serial)
            return;
        state.unixSeconds = static_cast<std::int64_t>(epoch);
        state.utcOffsetSeconds = offset;
        state.abbreviation = label;
        state.zone = zone;
        state.lastSample = received;
        state.valid = true;
        LL_DEBUGS("NexVerseClock") << "Server civil clock synchronized: "
                                 << zone << " " << label << LL_ENDL;
    }
    catch (const std::exception& err)
    {
        LL_DEBUGS("NexVerseClock") << "Invalid OGL clock JSON: "
                                 << err.what() << LL_ENDL;
    }
}
} // namespace

void OGLNexVerseClock::refreshIfDue()
{
    if (!OGLNexVerse::isAllowedGrid(LLGridManager::getInstance()->getGrid()))
        return;

    std::uint64_t request;
    ServerClock& state = clock();
    const auto now = MonotonicClock::now();
    {
        std::lock_guard<std::mutex> lock(state.mutex);
        if (state.requested && now - state.lastAttempt < REFRESH_INTERVAL)
            return;
        state.requested = true;
        state.lastAttempt = now;
        request = ++state.serial;
    }

    FSCoreHttpUtil::callbackHttpGetRaw(
        "http://hg.stadt-nexverse.de:80/ogl/v1/grid-info",
        [request](const LLSD& data) { onClockSuccess(request, data); },
        [request](const LLSD&) {
            onClockFailure(request, "OGL clock discovery unavailable");
        });
}

bool OGLNexVerseClock::now(std::time_t& civilEpoch,
                           std::string& abbreviation, std::string& zoneId)
{
    ServerClock& state = clock();
    const auto tick = MonotonicClock::now();
    std::lock_guard<std::mutex> lock(state.mutex);
    if (!state.valid || tick < state.lastSample ||
        tick - state.lastSample > MAX_STALE_AGE)
        return false;
    const auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
        tick - state.lastSample).count();
    civilEpoch = static_cast<std::time_t>(
        state.unixSeconds + elapsed + state.utcOffsetSeconds);
    abbreviation = state.abbreviation;
    zoneId = state.zone;
    return true;
}
