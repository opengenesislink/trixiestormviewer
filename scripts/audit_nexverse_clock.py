#!/usr/bin/env python3
"""Structural tests for the viewer's server-authoritative clock wiring."""
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
clock = (root / "indra/newview/oglnexverseclock.cpp").read_text()
status = (root / "indra/newview/llstatusbar.cpp").read_text()
login = (root / "indra/newview/fspanellogin.cpp").read_text()
cmake = (root / "indra/newview/CMakeLists.txt").read_text()

for needle in (
    'org.opengenesislink.viewer.clock.v1',
    'OGLNexVerse::GEN1_LOGIN_URI',
    'org.opengenesislink.viewer.grid-info.v1',
    'std::chrono::steady_clock',
    'state.unixSeconds +',
    'berlinUtcOffset(utcEpoch)',
    'std::chrono::seconds(60)',
    'std::chrono::hours(24)',
    'void OGLNexVerseClock::refreshIfDue()',
):
    assert needle in clock, f"Missing clock implementation: {needle}"

for needle in (
    'OGLNexVerseClock::refreshIfDue()',
    'OGLNexVerseClock::now(',
    'std::regex_replace(pattern, slt_token, ", utc]")',
    'LLStringUtil::replaceString(pattern, "OGLSERVERCLOCKZONE", zone_label)',
    'Never revert to raw UTC on network errors.',
):
    assert needle in status, f"Missing status-bar integration: {needle}"

assert 'oglnexverseclock.cpp' in cmake
assert 'oglnexverseclock.h' in cmake
assert 'OGLNexVerseClock::refreshIfDue();' in login
assert 'std::regex_replace(pattern, timezone_token,' in status

zone = ZoneInfo('Europe/Berlin')
for date, expected_offset, label in (
    (datetime(2026, 1, 15, 12, tzinfo=timezone.utc), 3600, 'MEZ'),
    (datetime(2026, 7, 15, 12, tzinfo=timezone.utc), 7200, 'MESZ'),
    (datetime(2026, 3, 29, 0, 59, tzinfo=timezone.utc), 3600, 'MEZ'),
    (datetime(2026, 3, 29, 1, 1, tzinfo=timezone.utc), 7200, 'MESZ'),
    (datetime(2026, 10, 25, 0, 59, tzinfo=timezone.utc), 7200, 'MESZ'),
    (datetime(2026, 10, 25, 1, 1, tzinfo=timezone.utc), 3600, 'MEZ'),
):
    local = date.astimezone(zone)
    assert int(local.utcoffset().total_seconds()) == expected_offset
    assert ('MESZ' if local.dst().total_seconds() else 'MEZ') == label

checked = 0
for locale in ('az','da','de','en','es','fr','it','ja','pl','pt','ru','tr','zh'):
    path = root / f'indra/newview/skins/default/xui/{locale}/panel_status_bar.xml'
    if path.exists():
        document = ET.parse(path).getroot()
        time_elements = [element for element in document.iter() if element.get('name') == 'TimeText']
        assert len(time_elements) == 1, (locale, len(time_elements))
        label = time_elements[0]
        assert 'PST' not in ''.join(label.itertext()), f'{locale}: old PST status placeholder'
        assert 'Pacific' not in label.get('tool_tip',''), f'{locale}: hardcoded Pacific tooltip'
        assert 'Pazifik' not in label.get('tool_tip',''), f'{locale}: hardcoded Pacific tooltip'
        checked += 1
assert checked == 13, checked
print("NexVerse OGL server clock source, 13 locales and Berlin DST fixtures passed.")
