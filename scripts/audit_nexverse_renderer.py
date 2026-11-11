#!/usr/bin/env python3
"""Structural guard for TrixieStorm's experimental Linux Zink renderer selection."""
from pathlib import Path
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
viewer = root / "indra/newview"
settings = ET.parse(viewer / "app_settings/settings.xml").getroot()
keys = [item.text for item in settings.iter("key")]
assert "TrixieStormGraphicsBackend" in keys
for locale in ("en", "de"):
    panel = ET.parse(viewer / f"skins/default/xui/{locale}/panel_preferences_graphics1.xml").getroot()
    tabs = [e for e in panel.iter("panel") if e.attrib.get("name") == "TrixieStorm Renderer"]
    assert len(tabs) == 1, locale
    if locale == "en":
        selectors = [e for e in tabs[0].iter("combo_box") if e.get("name") == "TrixieStormBackend"]
        assert len(selectors) == 1
        assert selectors[0].get("control_name") == "TrixieStormGraphicsBackend"
        assert {e.get("value") for e in selectors[0].findall("combo_box.item")} == {"opengl", "zink"}

app = (viewer / "llappviewer.cpp").read_text()
for token in ("TRIXIESTORM_FORCE_OPENGL", "MESA_LOADER_DRIVER_OVERRIDE",
              "LIBGL_KOPPER_DRI2", 'graphics_backend == "zink"'):
    assert token in app, token

progress = (viewer / "llprogressview.cpp").read_text()
for token in ("webrtc_logo.png", "vulkan_logo.png", 'mGLRenderer.find("zink")',
              "#ifdef LL_FMODSTUDIO", "vivox_logo.png"):
    assert token in progress, token

for name in ("webrtc_logo.png", "vulkan_logo.png", "fmod_logo.png"):
    data = (viewer / "skins/default/textures/3p_icons" / name).read_bytes()
    assert data.startswith(b"\x89PNG\r\n\x1a\n"), name

im = (viewer / "llimview.cpp").read_text()
assert "mP2PAsAdhocCall = mStartedAsIMCall &&" in im
assert 'No ChatSessionRequest CAP for an outgoing voice call' in im
assert "if (!url.empty())" in im
assert "start_deprecated_conference_chat" in im
print("PASS: TrixieStorm text IM split, Zink backend UI/driver guard and conditional startup logos")
