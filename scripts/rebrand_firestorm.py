#!/usr/bin/env python3
"""Apply TrixieStorm app identity to the pinned Firestorm 7.2.4 source.

This deliberately does NOT rewrite copyright, license headers, upstream URLs,
internal FS* C++ classes, or Firestorm-specific feature identifiers.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = "10bd3c9f930c76e1427ddd4ecece6cdf36b4406d"
PRODUCT = "TrixieStorm Viewer"
APPID = "TrixieStormViewer"
EXEC = "trixiestorm-bin"
CHANGES: list[tuple[str, int]] = []


def edit(relative: str, swaps: list[tuple[str, str]]) -> None:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(f"Missing required upstream file: {relative}")
    old_text = path.read_text(encoding="utf-8")
    text = old_text
    for old, new in swaps:
        if old not in text:
            if new in text:
                continue  # repeatable after a successful first rebrand
            raise ValueError(f"{relative}: required source fragment not found: {old[:100]!r}")
        text = text.replace(old, new)
    if text != old_text:
        path.write_text(text, encoding="utf-8")
        CHANGES.append((relative, len(swaps)))


def expression(relative: str, pattern: str, replacement: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE | re.DOTALL)
    if count != 1:
        if replacement in text:
            return
        raise ValueError(f"{relative}: required replacement pattern not found")
    path.write_text(updated, encoding="utf-8")
    CHANGES.append((relative, 1))


def edit_language_strings() -> None:
    # Source name keys are public text; other string IDs and Firestorm-specific
    # internal tokens (e.g. #Firestorm virtual inventory folder) must remain.
    base = ROOT / "indra/newview/skins"
    found = 0
    for path in base.glob("*/xui/*/strings.xml"):
        original = path.read_text(encoding="utf-8")
        result = original
        names = {
            "APP_NAME": "TrixieStorm Viewer",
            "CAPITALIZED_APP_NAME": "TRIXIESTORM VIEWER",
            "APP_NAME_ABBR": "TS",
            "SUPPORT_SITE": "TrixieStorm Viewer Support",
        }
        for key, new in names.items():
            patt = r'(<string\s+name="' + re.escape(key) + r'"[^>]*>).*?(</string>)'
            result, n = re.subn(patt, lambda m: m.group(1) + new + m.group(2),
                                result, count=1, flags=re.DOTALL)
            if key == "APP_NAME" and n:
                found += 1
        if path.as_posix().endswith("/en/strings.xml"):
            result = result.replace("https://www.firestormviewer.org/choose-your-platform/",
                                    "https://github.com/opengenesislink/trixiestormviewer/releases")
        if result != original:
            path.write_text(result, encoding="utf-8")
            CHANGES.append((str(path.relative_to(ROOT)), 1))
    if found == 0:
        raise ValueError("No localized APP_NAME string found")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebrand pinned Firestorm source")
    parser.add_argument("--check", action="store_true", help="Only verify previously applied branding")
    args = parser.parse_args()
    if not (ROOT / "indra/newview/CMakeLists.txt").exists():
        raise SystemExit("Firestorm C++ source not imported; run source import first.")

    if not args.check:
        edit("indra/CMakeLists.txt", [
            ('set(ROOT_PROJECT_NAME "Firestorm" CACHE STRING\n    "The root project/makefile/solution name. Defaults to Firestorm.")',
             'set(ROOT_PROJECT_NAME "TrixieStorm" CACHE STRING\n    "TrixieStorm root project / solution name.")'),
            ("include(Variables)\ninclude(BuildVersion)",
             'include(Variables)\n# TrixieStorm product identity must be set before BuildVersion.\nset(VIEWER_CHANNEL "TrixieStorm Viewer" CACHE STRING "Viewer Channel Name" FORCE)\ninclude(BuildVersion)'),
        ])
        edit("indra/newview/CMakeLists.txt", [
            ('set(VIEWER_BINARY_NAME "firestorm-bin" CACHE STRING',
             'set(VIEWER_BINARY_NAME "trixiestorm-bin" CACHE STRING'),
            ('set(product "Firestorm")', 'set(product "TrixieStormViewer")'),
            ('set(MACOSX_EXECUTABLE_NAME "Firestorm")', 'set(MACOSX_EXECUTABLE_NAME "TrixieStormViewer")'),
            ('set(MACOSX_BUNDLE_INFO_STRING "Firestorm Viewer")', 'set(MACOSX_BUNDLE_INFO_STRING "TrixieStorm Viewer")'),
            ('set(MACOSX_BUNDLE_GUI_IDENTIFIER "org.firestormviewer.firestorm")',
             'set(MACOSX_BUNDLE_GUI_IDENTIFIER "de.opengenesislink.trixiestormviewer")'),
            ('set(MACOSX_BUNDLE_BUNDLE_NAME "Firestorm")',
             'set(MACOSX_BUNDLE_BUNDLE_NAME "TrixieStorm Viewer")'),
        ])
        # The generated package/installer name cannot inherit Firestorm's
        # Release/OS suffix: the new product is always TrixieStorm Viewer.
        expression("indra/newview/viewer_manifest.py",
            r"    def app_name\(self\):\n.*?(?=\n    def exec_name\(self\):)",
            '    def app_name(self):\n        return "TrixieStorm Viewer"\n')
        edit("indra/newview/viewer_manifest.py", [
            ("return CHANNEL_VENDOR_BASE\n    # </FS:Ansariel>",
             'return "TrixieStorm Viewer"\n    # </FS:Ansariel>'),
            ("self.path(src='%s/firestorm-bin.exe' % self.args['configuration'], dst=self.final_exe())",
             "self.path(src='%s/trixiestorm-bin.exe' % self.args['configuration'], dst=self.final_exe())"),
            ('self.path("wrapper.sh","firestorm")', 'self.path("wrapper.sh","trixiestormviewer")'),
            ('self.path("firestorm-bin","do-not-directly-run-firestorm-bin")',
             'self.path("trixiestorm-bin","do-not-directly-run-trixiestorm-bin")'),
            ('firestorm-bin\\..*', 'trixiestorm-bin\\..*'),
        ])
        edit("indra/newview/fs_viewer_manifest.py", [
            ('return "Phoenix-%(app_name)s_%(optimized)s-%(version_dashes)s" % substitution_strings',
             'return "TrixieStormViewer_%(optimized)s-%(version_dashes)s" % substitution_strings'),
            ('return self.channel().replace("Firestorm", "").strip()',
             'return self.channel().replace("TrixieStorm", "").strip()'),
            ("installer_name_components = ['Phoenix',self.app_name(),self.args.get('arch'),'.'.join(self.args['version'])]",
             "installer_name_components = ['TrixieStormViewer',self.args.get('arch'),'.'.join(self.args['version'])]"),
            ("components = ['Phoenix',self.app_name(),self.args.get('arch'),'.'.join(self.args['version'])]",
             "components = ['TrixieStormViewer',self.args.get('arch'),'.'.join(self.args['version'])]"),
            ('"firestorm-bin.pdb"', '"trixiestorm-bin.pdb"'),
            ('"firestorm-bin-public.pdb"', '"trixiestorm-bin-public.pdb"'),
            ('Firestorm-bin.exe', 'trixiestorm-bin.exe'),
            ('"firestorm-bin.exe"', '"trixiestorm-bin.exe"'),
        ])
        expression("indra/newview/llvelopack.cpp",
            r"static std::wstring get_app_name\(\)\n\{.*?\n\}\n(?=\nstatic std::wstring get_app_name_oneword\(\))",
            'static std::wstring get_app_name()\n{\n    return L"TrixieStorm Viewer";\n}\n')
        edit("indra/newview/llvelopack.cpp", [
            ('L"The Phoenix Firestorm Project, Inc."', 'L"OpenGenesisLINK"'),
            ('L"https://www.firestormviewer.org/support"',
             'L"https://github.com/opengenesislink/trixiestormviewer/issues"'),
            ('L"https://www.firestormviewer.org/downloads"',
             'L"https://github.com/opengenesislink/trixiestormviewer/releases"'),
            ('L"https://www.firestormviewer.org"',
             'L"https://github.com/opengenesislink/trixiestormviewer"'),
        ])
        edit("indra/newview/res/viewerRes.rc", [
            ('LTEXT           "Loading Firestorm ..."', 'LTEXT           "Loading TrixieStorm Viewer ..."'),
            ('VALUE "FileDescription", "Firestorm"', 'VALUE "FileDescription", "TrixieStorm Viewer"'),
            ('VALUE "InternalName", "Firestorm"', 'VALUE "InternalName", "TrixieStormViewer"'),
            ('VALUE "OriginalFilename", "Firestorm.exe"',
             'VALUE "OriginalFilename", "TrixieStormViewer.exe"'),
            ('VALUE "ProductName", "Firestorm"', 'VALUE "ProductName", "TrixieStorm Viewer"'),
            ('VALUE "CompanyName", "The Phoenix Firestorm Project, Inc."',
             'VALUE "CompanyName", "OpenGenesisLINK"'),
        ])
        edit("indra/llcrashlogger/llcrashlogger.cpp", [
            ('"Firestorm_x64"', '"TrixieStormViewer_x64"'),
            ('initAppDirs("Firestorm")', 'initAppDirs("TrixieStormViewer")'),
            ('"FirestormCrashReport"', '"TrixieStormCrashReport"'),
            ('mProductName = "Firestorm";', 'mProductName = "TrixieStorm Viewer";'),
        ])
        edit("indra/newview/llappviewer.cpp", [
            ('gDirUtilp->initAppDirs(APP_NAME + "_x64");',
             'gDirUtilp->initAppDirs("TrixieStormViewer_x64");'),
            ('gDirUtilp->initAppDirs(APP_NAME);',
             'gDirUtilp->initAppDirs("TrixieStormViewer");'),
            ('return LLTrans::getString( "APP_NAME" ) + "_x64";',
             'return "TrixieStormViewer_x64";'),
            ('return LLTrans::getString("APP_NAME");',
             'return "TrixieStormViewer";'),
            ('We are sorry, but Firestorm has crashed', 'We are sorry, but TrixieStorm Viewer has crashed'),
        ])
        edit("indra/newview/linux_tools/wrapper.sh", [
            ('bin/do-not-directly-run-firestorm-bin',
             'bin/do-not-directly-run-trixiestorm-bin'),
        ])
        edit("indra/newview/linux_tools/install.sh", [
            ('Firestorm Viewer', 'TrixieStorm Viewer'),
            ('DEFAULT_SYSTEM_INSTALL_DIR="/opt/firestorm"',
             'DEFAULT_SYSTEM_INSTALL_DIR="/opt/trixiestormviewer"'),
            ('DEFAULT_USER_INSTALL_DIR="$HOME/firestorm"',
             'DEFAULT_USER_INSTALL_DIR="$HOME/trixiestormviewer"'),
        ])
        edit("indra/newview/linux_tools/refresh_desktop_app_entry.sh", [
            ('Name=Firestorm Viewer', 'Name=TrixieStorm Viewer'),
            ('/firestorm\\n', '/trixiestormviewer\\n'),
            ('do-not-directly-run-firestorm-bin', 'do-not-directly-run-trixiestorm-bin'),
            ('firestorm-viewer.desktop', 'trixiestormviewer.desktop'),
        ])
        edit("indra/newview/installers/windows/installer_template.nsi", [
            (r'\AppData\Roaming\Firestorm', r'\AppData\Roaming\TrixieStormViewer'),
            (r'\AppData\Local\FirestormOS_x64', r'\AppData\Local\TrixieStormViewer_x64'),
            (r'\AppData\Local\FirestormOS', r'\AppData\Local\TrixieStormViewer'),
            (r'\AppData\Local\Firestorm_x64', r'\AppData\Local\TrixieStormViewer_x64'),
            (r'\AppData\Local\Firestorm', r'\AppData\Local\TrixieStormViewer'),
            (r'ProgramData\Firestorm', r'ProgramData\TrixieStormViewer'),
            ('RMDir /r "$0\\Firestorm"', 'RMDir /r "$0\\TrixieStormViewer"'),
            ('"Publisher" "The Phoenix Firestorm Project, Inc."',
             '"Publisher" "OpenGenesisLINK"'),
            ('"URLInfoAbout" "https://www.firestormviewer.org"',
             '"URLInfoAbout" "https://github.com/opengenesislink/trixiestormviewer"'),
            ('"URLUpdateInfo" "https://www.firestormviewer.org/downloads"',
             '"URLUpdateInfo" "https://github.com/opengenesislink/trixiestormviewer/releases"'),
            ('"HelpLink" "https://www.firestormviewer.org/support"',
             '"HelpLink" "https://github.com/opengenesislink/trixiestormviewer/issues"'),
        ])
        edit_language_strings()

    must = {
        "indra/CMakeLists.txt": 'set(VIEWER_CHANNEL "TrixieStorm Viewer"',
        "indra/newview/CMakeLists.txt": 'set(VIEWER_BINARY_NAME "trixiestorm-bin"',
        "indra/newview/llappviewer.cpp": 'initAppDirs("TrixieStormViewer_x64")',
        "indra/llcrashlogger/llcrashlogger.cpp": '"TrixieStormViewer_x64"',
        "indra/newview/res/viewerRes.rc": 'VALUE "ProductName", "TrixieStorm Viewer"',
        "indra/newview/viewer_manifest.py": 'return "TrixieStorm Viewer"',
        "indra/newview/fs_viewer_manifest.py": 'return "TrixieStormViewer_%(optimized)s',
        "indra/newview/linux_tools/refresh_desktop_app_entry.sh": 'Name=TrixieStorm Viewer',
        "indra/newview/linux_tools/wrapper.sh": 'do-not-directly-run-trixiestorm-bin',
    }
    for rel, needle in must.items():
        if needle not in (ROOT / rel).read_text(encoding="utf-8"):
            raise SystemExit(f"Branding verification FAILED: {rel}: {needle}")
    print(f"TrixieStorm branding verified. Edited {len(CHANGES)} files.")
    if CHANGES:
        for path, _ in CHANGES:
            print(f"  {path}")
    print("Upstream license/credit headers intentionally preserved.")
    print("This is a source change, not proof of a successful build.")


if __name__ == "__main__":
    main()
