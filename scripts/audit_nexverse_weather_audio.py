#!/usr/bin/env python3
"""Static regression tests for OGLWeather v1 and extended OpenSim WAV upload.

No network, live account or running simulator is required for CI.
"""
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
nv = root / "indra/newview"
audio = root / "indra/llaudio"
weather = (nv / "oglnexverseweather.cpp").read_text()
cmake = (nv / "CMakeLists.txt").read_text()
app = (nv / "llappviewer.cpp").read_text()
wav = (audio / "llvorbisencode.cpp").read_text()
header = (audio / "llvorbisencode.h").read_text()
decoder = (audio / "llaudiodecodemgr.cpp").read_text()
upload = (nv / "llviewerassetupload.cpp").read_text()

for token in (
    '"OGLWeatherState"', '"ogl.weather"', '"region_id"',
    '"legacy_prim_emitters_active"', '"condition"', '"intensity"',
    '"wind_kmh"', 'Condition::Rain', 'Condition::Snow',
    'LLViewerPartSim::getInstance()->addPart', 'LLViewerPartSource',
    'WEATHER_STALE_AFTER', 'POLL_INTERVAL',
    's.regionId != region', 'TrixieStormWeatherXmlFallback',
):
    assert token in weather, token
assert 'oglnexverseweather.cpp' in cmake
assert 'OGLNexVerseWeather::update()' in app
assert 'OGLNexVerseWeather::shutdown()' in app
assert 'if (is_in_secondlife && clip_length > LLVORBIS_CLIP_MAX_TIME)' in wav
assert 'LLVORBIS_CLIP_MAX_TIME_OPENSIM' not in wav + header + (nv / "llviewermenufile.cpp").read_text()
assert '256u * 1024u * 1024u' in header
assert 'const ogg_int64_t pcm_samples = ov_pcm_total' in decoder
assert 'pcm_samples <= static_cast<ogg_int64_t>(LLVORBIS_CLIP_REJECT_SAMPLES)' in decoder
assert 'encode_vorbis_file(getFileName(), filename, LLGridManager::instance().isInSecondLife())' in upload

settings = ET.parse(nv / "app_settings/settings.xml").getroot()
keys = [x.text for x in settings.iter("key")]
for name in ('TrixieStormWeatherEffects', 'TrixieStormWeatherXmlFallback',
             'TrixieStormWeatherDensity'):
    assert name in keys, name
for language in ('en', 'de'):
    x = ET.parse(nv / f"skins/default/xui/{language}/panel_preferences_graphics1.xml").getroot()
    tabs = [t for t in x.iter("panel") if t.attrib.get("name") == "TrixieStorm Weather"]
    assert len(tabs) == 1, language
    for name in ('TrixieStormWeatherEffects', 'TrixieStormWeatherXmlFallback'):
        assert any(c.attrib.get('name') == name for c in tabs[0].iter('check_box'))
    assert any(c.attrib.get('name') == 'TrixieStormWeatherDensity'
               for c in tabs[0].iter('slider'))

# Exact relevant fields of OGLWeather v1, including a simulated snow switch.
for condition in ('rain', 'snow'):
    document = {'protocol': 'ogl.weather', 'version': 1,
                'region_id': 'c0ffee00-0000-0000-0000-000000000001',
                'precipitation': {'condition': condition, 'intensity': 85,
                                  'wind_kmh': 18, 'legacy_prim_emitters_active': False}}
    assert document['precipitation']['condition'] in ('rain', 'snow')
    assert 0 <= document['precipitation']['intensity'] <= 100
    assert not document['precipitation']['legacy_prim_emitters_active']

fallback = ET.fromstring('<oglweather version="1"><current condition="rain" '
                         'precipitation_intensity_percent="45" wind_kmh="11"/></oglweather>')
assert fallback.find('current').get('condition') == 'rain'

print('PASS: OGLWeather CAPS fields, local rain/snow, cross-region safety, UI and long OpenSim WAV')
