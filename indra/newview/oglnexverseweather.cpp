/**
 * TrixieStorm native OpenGenesisLINK precipitation.
 *
 * This consumes the per-region OGLWeatherState CAPS and renders local
 * precipitation without temporary in-world prims. When an older simulator
 * does not advertise the CAPS, the global /weather/xml endpoint may be used
 * as an explicitly configurable compatibility fallback.
 *
 * SPDX-License-Identifier: LGPL-2.1-only
 */
#include "llviewerprecompiledheaders.h"
#include "oglnexverseweather.h"

#include "oglnexversegridpolicy.h"
#include "fsgridhandler.h"
#include "fscorehttputil.h"
#include "llcorehttputil.h"
#include "llsdjson.h"
#include "llagent.h"
#include "llappviewer.h"
#include "llstartup.h"
#include "llviewercontrol.h"
#include "llviewerregion.h"
#include "llviewercamera.h"
#include "llviewerobject.h"
#include "llvoavatar.h"
#include "llviewerpartsim.h"
#include "llviewerpartsource.h"
#include "llviewertexture.h"
#include "llrand.h"
#include "llrender.h"

#include <boost/json.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <mutex>
#include <sstream>
#include <string>

namespace
{
using Clock = std::chrono::steady_clock;
constexpr auto POLL_INTERVAL = std::chrono::seconds(45);
constexpr auto WEATHER_STALE_AFTER = std::chrono::minutes(10);
constexpr size_t MAX_BODY = 65536;
constexpr char GLOBAL_WEATHER_URL[] = "https://world.stadt-nexverse.de/weather/xml";

enum class Condition { Clear, Cloud, Rain, Snow };

struct WeatherSnapshot
{
    Condition condition = Condition::Clear;
    int intensity = 0;
    int windKmh = 0;
    int cloudBase = 250;
    bool legacyEmitters = false;
    bool valid = false;
    Clock::time_point received{};
};

class WeatherPartSource;

struct WeatherState
{
    std::mutex mutex;
    LLUUID regionId;
    Clock::time_point lastAttempt{};
    std::uint64_t serial = 0;
    WeatherSnapshot weather;
    OGLNexVerseWeather::VisualState visual;
    Clock::time_point lastVisualUpdate{};
    LLPointer<WeatherPartSource> emitter;
};

WeatherState& state()
{
    static WeatherState s;
    return s;
}

Condition parseCondition(const std::string& name)
{
    if (name == "rain") return Condition::Rain;
    if (name == "snow") return Condition::Snow;
    if (name == "cloud") return Condition::Cloud;
    return Condition::Clear;
}

const char* conditionLabel(Condition condition)
{
    switch (condition)
    {
    case Condition::Rain: return "rain";
    case Condition::Snow: return "snow";
    case Condition::Cloud: return "cloud";
    default: return "sun";
    }
}

WeatherSnapshot currentWeather()
{
    WeatherState& s = state();
    std::lock_guard<std::mutex> lock(s.mutex);
    WeatherSnapshot current = s.weather;
    if (current.valid && Clock::now() - current.received > WEATHER_STALE_AFTER)
        current.valid = false;
    return current;
}

class WeatherPartSource final : public LLViewerPartSource
{
public:
    WeatherPartSource() : LLViewerPartSource(LL_PART_SOURCE_NULL)
    {
        mImagep = LLViewerFetchedTexture::sDefaultParticleImagep;
    }

    void update(const F32 dt) override
    {
        const WeatherSnapshot w = currentWeather();
        if (!w.valid || w.legacyEmitters ||
            (w.condition != Condition::Rain && w.condition != Condition::Snow) ||
            !gSavedSettings.getBOOL("TrixieStormWeatherEffects"))
            return;

        if (mImagep.isNull())
            mImagep = LLViewerFetchedTexture::sDefaultParticleImagep;
        if (mImagep.isNull() || !gAgent.getRegion())
            return;

        const bool snow = w.condition == Condition::Snow;
        const F32 quality = llclamp(
            static_cast<F32>(gSavedSettings.getF32("TrixieStormWeatherDensity")),
            0.1f, 2.0f);
        const F32 strength = llclamp(w.intensity / 100.f, 0.f, 1.f);
        if (strength < 0.005f)
        {
            mBudget = 0.f;
            return;
        }
        // Intensity governs particle counts nonlinearly: light showers stay
        // sparse, heavy rain fills the near field. Per-frame and scene limits
        // guard frame time on integrated GPUs (including Radeon Vega).
        const F32 weighted = strength * strength * (3.f - 2.f * strength);
        const F32 rate = (snow ? 35.f + 240.f * weighted
                               : 65.f + 650.f * weighted) * quality;
        mBudget = llmin(mBudget + llclamp(dt, 0.f, 0.12f) * rate, 64.f);
        const S32 count = llmin(static_cast<S32>(mBudget), 40);
        mBudget -= static_cast<F32>(count);

        // Populate the camera's visible volume rather than a wide square
        // largely behind the player. The source still creates no inworld prim.
        LLViewerCamera* camera = LLViewerCamera::getInstance();
        mPosAgent = camera->getOrigin();
        LLVector3 forward = camera->getAtAxis();
        forward.mV[VZ] = 0.f;
        if (forward.magVecSquared() < 0.01f)
            forward = LLVector3(1.f, 0.f, 0.f);
        forward.normalize();
        const LLVector3 side(-forward.mV[VY], forward.mV[VX], 0.f);
        // Weather v1 specifies wind speed only, so drift direction is a
        // consistent visual approximation until the CAPS adds a wind vector.
        const F32 wind = llclamp(static_cast<F32>(w.windKmh), 0.f, 100.f) / 3.6f;
        for (S32 i = 0; i < count; ++i)
        {
            if (!LLViewerPartSim::shouldAddPart())
            {
                mBudget = 0.f;
                break;
            }
            const F32 depth = snow ? 1.5f + ll_frand(13.f)
                                   : 1.5f + ll_frand(15.f);
            const F32 breadth = (ll_frand(2.f) - 1.f) * (2.8f + depth * 0.58f);
            LLViewerPart* particle = new LLViewerPart;
            particle->init(this, mImagep.get(), nullptr);
            particle->mPosAgent = mPosAgent + forward * depth + side * breadth +
                LLVector3(0.f, 0.f, snow ? (1.5f + ll_frand(7.f))
                                          : (2.f + ll_frand(9.f)));
            particle->mMaxAge = snow ? 4.0f + ll_frand(2.f)
                                     : 0.85f + ll_frand(0.45f);
            particle->mVelocity = LLVector3(
                wind * (snow ? 0.32f : 0.48f) +
                    (snow ? ll_frand(1.4f) - 0.7f : 0.f),
                wind * 0.12f + (snow ? ll_frand(1.2f) - 0.6f : 0.f),
                snow ? -1.2f - ll_frand(0.8f) : -12.f - ll_frand(8.f));
            particle->mAccel = LLVector3(0.f, 0.f, snow ? -0.08f : -2.0f);
            particle->mFlags = LLPartData::LL_PART_INTERP_COLOR_MASK |
                (snow ? 0 : LLPartData::LL_PART_FOLLOW_VELOCITY_MASK);
            particle->mStartColor = snow ? LLColor4(0.96f, 0.98f, 1.f, 0.94f)
                                        : LLColor4(0.77f, 0.85f, 0.95f,
                                                   0.60f + weighted * 0.18f);
            particle->mEndColor = particle->mStartColor;
            particle->mEndColor.mV[3] = 0.0f;
            particle->mColor = particle->mStartColor;
            particle->mScale = snow
                ? LLVector2(0.14f + ll_frand(0.17f), 0.14f + ll_frand(0.17f))
                : LLVector2(0.055f, 0.66f + weighted * 0.64f);
            particle->mStartScale = particle->mScale;
            particle->mEndScale = particle->mScale;
            particle->mStartGlow = 0.f;
            particle->mEndGlow = 0.f;
            particle->mBlendFuncSource = LLRender::BF_SOURCE_ALPHA;
            particle->mBlendFuncDest = LLRender::BF_ONE_MINUS_SOURCE_ALPHA;
            LLViewerPartSim::getInstance()->addPart(particle);
        }
    }

private:
    F32 mBudget = 0.f;
};

bool parseCap(const LLSD& data, const LLUUID& expectedRegion, WeatherSnapshot& result)
{
    if (data["protocol"].asString() != "ogl.weather" ||
        data["version"].asInteger() != 1 ||
        data["region_id"].asUUID() != expectedRegion)
        return false;
    const LLSD& prec = data["precipitation"];
    if (!prec.isMap())
        return false;
    const std::string name = prec["condition"].asString();
    if (name != "rain" && name != "snow" && name != "sun" && name != "cloud")
        return false;
    result.condition = parseCondition(name);
    result.intensity = llclamp(prec["intensity"].asInteger(), 0, 100);
    result.windKmh = llclamp(prec["wind_kmh"].asInteger(), 0, 120);
    result.cloudBase = llclamp(prec["cloud_base_m"].asInteger(), 64, 2048);
    result.legacyEmitters = prec["legacy_prim_emitters_active"].asBoolean();
    result.valid = true;
    return true;
}

bool parseGlobalXml(const std::string& body, WeatherSnapshot& result)
{
    try
    {
        std::istringstream stream(body);
        boost::property_tree::ptree xml;
        boost::property_tree::read_xml(stream, xml);
        const auto& current = xml.get_child("oglweather.current.<xmlattr>");
        const std::string cond = current.get<std::string>("condition", "");
        if (cond != "rain" && cond != "snow" && cond != "sun" && cond != "cloud")
            return false;
        result.condition = parseCondition(cond);
        result.intensity = llclamp(
            current.get<int>("precipitation_intensity_percent", 0), 0, 100);
        result.windKmh = llclamp(current.get<int>("wind_kmh", 0), 0, 120);
        result.cloudBase = 250;
        result.legacyEmitters = false; // Not advertised by the grid-wide XML.
        result.valid = true;
        return true;
    }
    catch (const std::exception& error)
    {
        LL_WARNS("NexVerseWeather") << "Invalid weather XML: "
                                    << error.what() << LL_ENDL;
        return false;
    }
}

void applyResponse(std::uint64_t serial, LLUUID region,
                   bool globalXml, const LLSD& response)
{
    const LLSD::Binary& bytes = response[
        LLCoreHttpUtil::HttpCoroutineAdapter::HTTP_RESULTS_RAW].asBinary();
    if (bytes.empty() || bytes.size() > MAX_BODY)
    {
        LL_WARNS("NexVerseWeather") << "Empty or excessive weather response"
                                    << LL_ENDL;
        return;
    }
    WeatherSnapshot incoming;
    try
    {
        const std::string payload(bytes.begin(), bytes.end());
        bool valid = false;
        if (globalXml)
            valid = parseGlobalXml(payload, incoming);
        else
            valid = parseCap(LlsdFromJson(boost::json::parse(payload)), region, incoming);
        if (!valid)
        {
            LL_WARNS("NexVerseWeather") << "Unrecognized weather response" << LL_ENDL;
            return;
        }
    }
    catch (const std::exception& error)
    {
        LL_WARNS("NexVerseWeather") << "Weather decoding failed: "
                                    << error.what() << LL_ENDL;
        return;
    }
    WeatherState& s = state();
    std::lock_guard<std::mutex> lock(s.mutex);
    if (serial != s.serial || s.regionId != region)
        return; // Reject delayed responses from a previous region.
    incoming.received = Clock::now();
    s.weather = incoming;
    LL_INFOS("NexVerseWeather") << "OGLWeather condition="
                                << conditionLabel(incoming.condition)
                                << " intensity=" << incoming.intensity
                                << " wind_kmh=" << incoming.windKmh
                                << " legacy_emitters=" << incoming.legacyEmitters
                                << (globalXml ? " source=grid-xml" : " source=region-caps")
                                << LL_ENDL;
}

void cancelWeather(WeatherState& s)
{
    if (s.emitter.notNull())
    {
        s.emitter->setDead();
        s.emitter = nullptr;
    }
    s.weather = WeatherSnapshot{};
    s.visual = OGLNexVerseWeather::VisualState{};
    s.lastVisualUpdate = Clock::time_point{};
}

} // namespace

void OGLNexVerseWeather::update()
{
    WeatherState& s = state();
    LLViewerRegion* region = gAgent.getRegion();
    const bool weatherNeeded = gSavedSettings.getBOOL("TrixieStormWeatherEffects") ||
        gSavedSettings.getBOOL("TrixieStormWeatherSkySync");
    const bool allowed = !gDisconnected &&
        LLStartUp::getStartupState() == STATE_STARTED &&
        OGLNexVerse::isAllowedGrid(LLGridManager::getInstance()->getGrid()) &&
        region && weatherNeeded;
    const LLUUID regionId = allowed ? region->getRegionID() : LLUUID::null;
    const auto now = Clock::now();

    std::string requestedUrl;
    bool globalXml = false;
    std::uint64_t serial = 0;
    {
        std::lock_guard<std::mutex> lock(s.mutex);
        if (regionId != s.regionId)
        {
            s.regionId = regionId;
            ++s.serial;
            s.lastAttempt = Clock::time_point{};
            cancelWeather(s);
        }
        if (!allowed)
        {
            cancelWeather(s);
            return;
        }
        if (s.weather.valid && now - s.weather.received > WEATHER_STALE_AFTER)
            s.weather.valid = false;
        // Smooth weather fronts so abrupt updates don't flash the skydome.
        const F32 elapsed = s.lastVisualUpdate == Clock::time_point{}
            ? 0.0f : llclamp(
                std::chrono::duration<F32>(now - s.lastVisualUpdate).count(),
                0.f, 1.0f);
        s.lastVisualUpdate = now;
        const F32 blend = 1.f - std::exp(-elapsed * 0.38f);
        const F32 strength = s.weather.valid
            ? llclamp(s.weather.intensity / 100.f, 0.f, 1.f) : 0.f;
        const F32 targetRain = s.weather.condition == Condition::Rain ? strength : 0.f;
        const F32 targetSnow = s.weather.condition == Condition::Snow ? strength : 0.f;
        const F32 targetWind = s.weather.valid
            ? llclamp(s.weather.windKmh / 100.f, 0.f, 1.f) : 0.f;
        s.visual.rain += (targetRain - s.visual.rain) * blend;
        s.visual.snow += (targetSnow - s.visual.snow) * blend;
        s.visual.wind += (targetWind - s.visual.wind) * blend;
        const bool display = gSavedSettings.getBOOL("TrixieStormWeatherEffects") &&
            s.weather.valid && !s.weather.legacyEmitters &&
            (s.weather.condition == Condition::Rain ||
             s.weather.condition == Condition::Snow);
        if (display && s.emitter.isNull())
        {
            s.emitter = new WeatherPartSource();
            LLViewerPartSim::getInstance()->addPartSource(s.emitter);
        }
        else if (!display && s.emitter.notNull())
        {
            s.emitter->setDead();
            s.emitter = nullptr;
        }
        if (now - s.lastAttempt < POLL_INTERVAL)
            return;
        s.lastAttempt = now;
        serial = ++s.serial;
        requestedUrl = region->getCapability("OGLWeatherState");
        if (requestedUrl.empty() &&
            gSavedSettings.getBOOL("TrixieStormWeatherXmlFallback"))
        {
            globalXml = true;
            requestedUrl = GLOBAL_WEATHER_URL;
        }
    }
    if (requestedUrl.empty())
        return;

    FSCoreHttpUtil::callbackHttpGetRaw(
        requestedUrl,
        [serial, regionId, globalXml](const LLSD& data)
        {
            applyResponse(serial, regionId, globalXml, data);
        },
        [serial, regionId](const LLSD&)
        {
            WeatherState& s = state();
            std::lock_guard<std::mutex> lock(s.mutex);
            if (s.serial == serial && s.regionId == regionId)
                LL_DEBUGS("NexVerseWeather") << "Weather CAPS temporarily unavailable" << LL_ENDL;
        });
}

void OGLNexVerseWeather::shutdown()
{
    WeatherState& s = state();
    std::lock_guard<std::mutex> lock(s.mutex);
    ++s.serial;
    s.regionId = LLUUID::null;
    cancelWeather(s);
}

OGLNexVerseWeather::VisualState OGLNexVerseWeather::visualState()
{
    WeatherState& s = state();
    std::lock_guard<std::mutex> lock(s.mutex);
    return s.visual;
}
