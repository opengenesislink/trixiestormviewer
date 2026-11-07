#!/usr/bin/env python3
"""Static TrixieStorm source branding verification (not a compilation)."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "indra/CMakeLists.txt": ['ROOT_PROJECT_NAME "TrixieStorm"', 'VIEWER_CHANNEL "TrixieStorm Viewer"'],
    "indra/lib/python/indra/util/llmanifest.py": ["CHANNEL_VENDOR_BASE = 'TrixieStorm Viewer'"],
    "indra/newview/CMakeLists.txt": ['VIEWER_BINARY_NAME "trixiestorm-bin"', "res/trixiestormviewer.ico"],
    "indra/newview/res/viewerRes.rc": ['"TrixieStorm Viewer"', '"TrixieStormViewer.exe"', '"trixiestormviewer.ico"'],
    "indra/newview/viewer_manifest.py": ['return "TrixieStorm Viewer"', 'trixiestormviewer.ico', 'trixiestormviewer.png'],
    "indra/newview/fs_viewer_manifest.py": ["TrixieStormViewer_", "trixiestorm-bin.pdb"],
    "indra/newview/linux_tools/wrapper.sh": ["do-not-directly-run-trixiestorm-bin"],
    "indra/newview/linux_tools/refresh_desktop_app_entry.sh": ["Name=TrixieStorm Viewer", "trixiestormviewer.desktop", "trixiestormviewer.png"],
    "indra/newview/skins/default/xui/en/strings.xml": ['name="APP_NAME">TrixieStorm Viewer'],
    "indra/newview/skins/default/textures/textures.xml": ['login_trixiestorm_logo', 'windows/trixiestorm_login.png'],
    "indra/newview/installers/windows/installer_template.nsi": ["OpenGenesisLINK\\TrixieStormViewer", "trixiestormviewer.ico"],
    "indra/newview/llappviewer.cpp": ['initAppDirs("TrixieStormViewer_x64")'],
    "indra/llcrashlogger/llcrashlogger.cpp": ['"TrixieStormViewer_x64"'],
    "indra/newview/llvelopack.cpp": ['return L"TrixieStorm Viewer";'],
}
ASSETS = [
    "branding/source/trixiestorm-logo.webp",
    "indra/newview/res/trixiestormviewer.ico",
    "indra/newview/res/trixiestormviewer.png",
    "indra/newview/res-sdl/trixiestormviewer.BMP",
    "indra/newview/skins/default/textures/windows/trixiestorm_login.png",
]
errors = []
for path, needles in REQUIRED.items():
    f = ROOT / path
    if not f.is_file():
        errors.append(f"Missing source file: {path}")
        continue
    text = f.read_text("utf-8", errors="replace")
    for needle in needles:
        if needle not in text:
            errors.append(f"{path}: missing {needle}")
for path in ASSETS:
    f = ROOT / path
    if not f.exists() or not f.stat().st_size:
        errors.append(f"Missing generated artwork: {path}")

for path in ("indra/newview/skins/default/textures/textures.xml",
             "indra/newview/skins/default/xui/en/panel_login.xml",
             "indra/newview/skins/default/xui/en/strings.xml",
             "indra/newview/skins/default/xui/en/floater_about.xml"):
    try:
        ET.parse(ROOT / path)
    except Exception as err:
        errors.append(f"{path}: XML parse error: {err}")

cmake = (ROOT / "indra/newview/CMakeLists.txt").read_text()
# Upstream Firestorm icon must never be copied *onto* TrixieStorm ICO.
if re.search(r"icons/\$\{ICON_PATH\}/firestorm_icon\.ico\x22\s*\x22\$\{CMAKE_CURRENT_SOURCE_DIR\}/res/trixiestormviewer.ico", cmake):
    errors.append("CMake may overwrite the TrixieStorm icon with upstream artwork")

# Display a bounded report of remaining old branding for manual triage.
report = []
for path in sorted((ROOT / "indra/newview/skins/default/xui/en").rglob("*.xml")):
    if path.name == "floater_about.xml":
        continue  # Original Firestorm credits deliberately retained here.
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if ("Firestorm" in line or "Phoenix" in line) and len(report) < 80:
            report.append(f"{path.relative_to(ROOT)}:{n}: {line.strip()[:160]}")
print("Remaining visible text candidates (copyright/feature names may be intentional):")
print("\n".join(report) or "None in sampled UI")
if errors:
    print("\nBranding validation FAILED:")
    print("\n".join(f"  - {e}" for e in errors))
    sys.exit(1)
print("\nSource branding/static XML/asset checks passed.")
print("No claim made about successful C++ build, runtime behavior or closed-grid enforcement.")
