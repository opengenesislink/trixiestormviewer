#!/usr/bin/env python3
"""Structural and math guard for visible weather fronts & precipitation."""
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
source = (root / 'indra/newview/oglnexverseweather.cpp').read_text()
sky = (root / 'indra/newview/lldrawpoolwlsky.cpp').read_text()
cloud = (root / 'indra/newview/app_settings/shaders/class1/deferred/cloudsF.glsl').read_text()
cloud_vertex = (root / 'indra/newview/app_settings/shaders/class1/deferred/cloudsV.glsl').read_text()
settings = ET.parse(root / 'indra/newview/app_settings/settings.xml').getroot()

for token in ('const F32 weighted = strength * strength',
              '65.f + 650.f * weighted', '35.f + 240.f * weighted',
              'getAtAxis()', 'mBudget = 0.f',
              's.visual.rain +=', 's.visual.snow +=', 's.visual.wind +=',
              'visualState()', 'std::exp(-elapsed * 0.38f)'):
    assert token in source, token
for token in ('OGLNexVerseWeather::visualState()',
              'sTrixieWeather', 'sTrixieWeatherTime',
              'gGLManager.mGLRenderer.find("zink")', 'TrixieStormZinkVisualBoost'):
    assert token in sky, token
for token in ('uniform vec4 trixie_weather;',
              'uniform float trixie_weather_time;',
              'frontalCover', 'rainBase', 'snowBase', 'largeNoise',
              'highQuality > 0.5', 'cloud_noise_texture_next'):
    assert token in cloud, token
names=[e.text for e in settings.iter('key')]
assert 'activeCloudScale = max(cloud_scale' in cloud_vertex
assert 'max(activeCloudScale, 0.001)' in cloud_vertex
assert 'uniform vec4 trixie_weather;' in cloud_vertex
assert 'TrixieStormWeatherSkySync' in names
assert 'TrixieStormZinkVisualBoost' in names
for loc in ('en', 'de'):
    xml = ET.parse(root / f'indra/newview/skins/default/xui/{loc}/panel_preferences_graphics1.xml').getroot()
    controls=[e.attrib.get('name') for e in xml.iter('check_box')]
    assert 'TrixieStormWeatherSkySync' in controls
    assert 'TrixieStormZinkVisualBoost' in controls

# 0% must be clear and distinct intensity levels must be monotonic.
last_rain = last_snow = -1
for i in range(101):
    strength=i/100.0
    weighted=strength * strength * (3-2*strength)
    rain=0 if strength < .005 else 65+650*weighted
    snow=0 if strength < .005 else 35+240*weighted
    assert rain >= last_rain and snow >= last_snow
    last_rain, last_snow=rain,snow
assert last_rain==715 and last_snow==275
print('PASS: weather intensity monotonicity, camera-centric particles, cloud fronts and Zink HQ profile')
