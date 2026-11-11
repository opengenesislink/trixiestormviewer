#!/usr/bin/env python3
"""Structural regression checks for TrixieStorm's NexVerse chat and voice policy.

These tests do not replace a full Linux build or in-world regression testing.
"""
from pathlib import Path

root = Path(__file__).resolve().parents[1]

def source(name):
    return (root / "indra/newview" / name).read_text(encoding="utf-8")

chat = source("fschathistory.cpp")
legacy_chat = source("llchathistory.cpp")
nearby = source("fsfloaternearbychat.cpp")
log = source("lllogchat.cpp")
clock = source("oglnexverseclock.cpp")
voice = source("llvoiceclient.cpp")
cmake = (root / "indra/cmake/00-Common.cmake").read_text(encoding="utf-8")

assert "appendText(chat.mFromName, prependNewLineState, name_params)" in chat
assert "appendText(std::string(name_params.link_href)" not in chat
assert "mEditor->appendText(chat.mFromName + delimiter," in legacy_chat
assert "mEditor->appendText(std::string(link_params.link_href)" not in legacy_chat

for text, name in ((nearby, "nearby"), (log, "IM and log")):
    assert "OGLNexVerseClock::civilTimeFromUTC" in text, name
    assert 'std::regex_replace(timeStr, slt_token, ", utc]")' in text, name

assert "berlinUtcOffset(utcEpoch)" in clock
assert 'tick - state.lastSample <= MAX_STALE_AGE' in clock
assert 'voiceServerType != WEBRTC_VOICE_SERVER_TYPE' in voice
assert "legacy Vivox fallback disabled" in voice
assert "Legacy Vivox authorization is only needed for non-NexVerse builds." in voice

assert "TRIXIESTORM_COMPILER_HAS_AVX2" in cmake
assert "add_compile_options(-mavx2)" in cmake
assert "set(USE_LTO OFF CACHE BOOL" in cmake
print("PASS: NexVerse chat names, timestamps, clock fallback, WebRTC policy and AVX2/LTO build options")
