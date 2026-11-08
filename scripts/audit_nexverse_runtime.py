#!/usr/bin/env python3
"""Structural guard for TrixieStorm NexVerse-only source integration.

Does not compile Firestorm, prove login TLS, audit HTTP redirects, or test
server-side access control. Those need full ReleaseOS and staging tests.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    "indra/newview/oglnexversegridpolicy.h": [
        'GEN1_GRID = "hg.stadt-nexverse.de"',
        'GEN1_LOGIN_URI = "http://hg.stadt-nexverse.de:80/"',
        'GEN2_ENABLED = false',
        'isAllowedGrid(', 'isAllowedLoginURI(', 'isAllowedTravel(',
    ],
    "indra/newview/fsgridhandler.cpp": [
        '#include "oglnexversegridpolicy.h"',
        'addSystemGrid(OGLNexVerse::GEN1_LABEL',
        'void LLGridManager::setGridChoice(', 'isAllowedGrid(grid)',
        'void LLGridManager::getLoginURIs(',
        'uris.emplace_back(OGLNexVerse::GEN1_LOGIN_URI)',
        'void LLGridManager::initCmdLineGrids()',
        'void LLGridManager::saveGridList()',
    ],
    "indra/newview/lllogininstance.cpp": [
        '#include "oglnexversegridpolicy.h"',
        'Authentication to a non-NexVerse login URI blocked',
        '!OGLNexVerse::isAllowedLoginURI(uri)',
        'Reconnect refused: no trusted login URI',
    ],
    "indra/newview/llstartup.cpp": [
        '#include "oglnexversegridpolicy.h"',
        'sGridListRequestReady = true;',
        'Blocked foreign grid or Hypergrid startup URL',
    ],
    "indra/newview/llurldispatcher.cpp": [
        '#include "oglnexversegridpolicy.h"',
        'Rejected external SLURL',
        'Rejected foreign region teleport',
        'Rejected external app teleport',
    ],
    "indra/newview/fspanellogin.cpp": [
        'server_choice_combo->setEnabled(false)',
        'bool show_server = false',
        'OGLNexVerseClock::refreshIfDue()',
    ],
    "indra/newview/oglnexverseclock.cpp": [
        'org.opengenesislink.viewer.clock.v1',
        'clock', 'utc_offset_seconds',
        'MAX_STALE_AGE', 'REFRESH_INTERVAL',
        'std::chrono::steady_clock',
        'http://hg.stadt-nexverse.de:80/ogl/v1/grid-info',
        'OGLNexVerse::GEN1_LOGIN_URI',
    ],
    "indra/newview/llstatusbar.cpp": [
        'OGLNexVerseClock::refreshIfDue()',
        'OGLNexVerseClock::now(',
        'civil_epoch = time_corrected()',
        'std::regex_replace(pattern, slt_token, ", utc]")',
        'zone_id',
    ],
    "indra/newview/llvoiceclient.cpp": [
        '"VoiceServerType"',
        '"ProvisionVoiceAccountRequest"',
        '"VoiceSignalingRequest"',
        'voiceServerType = WEBRTC_VOICE_SERVER_TYPE;',
        'setSpatialVoiceModule(voiceServerType);',
    ],
    "indra/newview/fsfloaterexport.cpp": [
        'canExportNode', 'NexVerseExport',
        'mAborted = true;',
        'LLNotificationsUtil::add("ExportFailed");',
    ],
}
errors = []
for path, needles in CHECKS.items():
    source = ROOT / path
    if not source.is_file():
        errors.append(f"Missing {path}")
        continue
    content = source.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in content:
            # Marker text in the log may differ in capitalization; no aliasing for policy guards.
            if path.endswith("fspanellogin.cpp") and needle == "Legacy G1 login policy unchanged":
                if 'legacy G1 login policy unchanged' in content:
                    continue
            errors.append(f"{path}: missing {needle!r}")

startup = (ROOT / "indra/newview/llstartup.cpp").read_text()
if 'FSCoreHttpUtil::callbackHttpGet(url, last_modified,' in startup:
    errors.append("Old remote Firestorm grid-list HTTP download is still wired into startup")
for path in ("indra/newview/llstartup.cpp", "indra/newview/llurldispatcher.cpp"):
    if "slurl.getHypergrid()" in (ROOT / path).read_text():
        errors.append(f"{path}: LLSLURL has no getHypergrid() method")
if 'grid_entry->grid[GRID_VALUE]' not in (ROOT / "indra/newview/fsgridhandler.cpp").read_text():
    errors.append("Grid manager no longer has an identifiable grid key")

manifest = json.loads((ROOT / "config/nexverse-generations.json").read_text())
if manifest["allow_custom_grids"] or manifest["allow_external_grid_logins"] or manifest["allow_outbound_external_hypergrid_teleports"]:
    errors.append("Product manifest accidentally enables third-party grid travel")
gens = manifest["generations"]
if len(gens) != 2 or gens[0]["hostname"] != "hg.stadt-nexverse.de" or gens[1]["hostname"] != "beta.stadt-nexverse.de":
    errors.append("Generation identities do not match approved hostnames")
if gens[1]["state"] != "future-disabled" or gens[1]["login_uri"] is not None:
    errors.append("Gen2 must remain unavailable pending separate certification")
if gens[0]["login_uri"] != "http://hg.stadt-nexverse.de:80/":
    errors.append("Gen1 manifest login endpoint differs from compiled target")

grids = ET.parse(ROOT / "indra/newview/app_settings/grids.xml").getroot()
names = [k.text for k in grids.iter("key") if k.text and "." in k.text and k.text in
         ("hg.stadt-nexverse.de", "beta.stadt-nexverse.de")]
if names != ["hg.stadt-nexverse.de"]:
    errors.append(f"Runtime packaged grids.xml contains unexpected generation identities: {names}")
for file in ("indra/newview/skins/default/xui/en/menu_viewer.xml",
             "indra/newview/skins/default/xui/de/menu_viewer.xml"):
    try:
        ET.parse(ROOT / file)
    except ET.ParseError as exc:
        errors.append(f"Invalid UI XML {file}: {exc}")

print("NexVerse runtime-source policy audit:")
if errors:
    for err in errors:
        print("ERROR:", err)
    sys.exit(1)
print("PASS: canonical Gen1, disabled Gen2, app/link/login guards, OGL JSON discovery,")
print("      WebRTC CAP choice, fail-closed export markers, manifest and UI XML.")
print("LIMITS: no C++ link/build, no operational TLS or redirect test, no security")
print("        guarantee from client-side restrictions. Staging E2E is mandatory.")
