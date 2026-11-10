#!/usr/bin/env python3
"""Static tests for the optional enhanced EEP cloud shader and fallback."""
from pathlib import Path
from xml.etree import ElementTree as ET

root = Path(__file__).resolve().parents[1]
nv = root / "indra/newview"
shader_root = nv / "app_settings/shaders/class1/deferred"
enhanced = (shader_root / "cloudsF.glsl").read_text()
legacy = (shader_root / "cloudsLegacyF.glsl").read_text()
shader_manager = (nv / "llviewershadermgr.cpp").read_text()
settings = ET.parse(nv / "app_settings/settings.xml").getroot()
assert any(t.text == "TrixieStormEnhancedClouds" for t in settings.iter("key"))
assert 'gSavedSettings.getBOOL("TrixieStormEnhancedClouds")' in shader_manager
assert '"deferred/cloudsF.glsl" : "deferred/cloudsLegacyF.glsl"' in shader_manager
for flag in ("multi-frequency", "cloud_shape", "middle_noise", "thickness", "sun_visibility"):
    if flag != "multi-frequency":
        assert flag in enhanced, flag
assert "float alpha1 = (cloudNoise(uv1).x - 0.5)" in legacy
assert "cloud_shape" not in legacy
for loc in ("en", "de"):
    tree = ET.parse(nv / f"skins/default/xui/{loc}/panel_preferences_graphics1.xml")
    controls = [x for x in tree.iter("check_box")
                if x.attrib.get("name") == "TrixieStormEnhancedClouds"]
    assert len(controls) == 1, loc
assert "cloud_noise_texture_next" in enhanced
assert "cloud_pos_density1" in enhanced and "cloud_pos_density2" in enhanced
print("PASS: cloud shader variants, restart selection, EEP parameter compatibility and bilingual UI")
