# TrixieStorm Viewer rebranding - source-level change

## Product identity for the Firestorm 7.2.4 source import

Once the pinned source tree is imported, `python3 scripts/rebrand_firestorm.py` updates the application identity while preserving upstream copyright and the separate Firestorm/Second Life software origins.

| Surface | Expected result |
|---|---|
| Viewer/channel | `TrixieStorm Viewer` |
| CMake root project | `TrixieStorm` |
| CMake internal binary | `trixiestorm-bin` |
| Windows public executable name | `TrixieStormViewer.exe` (verify installer manifest) |
| Windows installer display name | `TrixieStorm Viewer` |
| Linux launcher | `trixiestormviewer` |
| Linux desktop entry | `trixiestormviewer.desktop` |
| Profile directories (x64) | `TrixieStormViewer_x64` |
| Profile directories (other) | `TrixieStormViewer` |
| Windows resources | `TrixieStorm Viewer` product/file description |
| Crash logger | `TrixieStorm Viewer`; isolated crash reports |
| Icon assets | Original logo integration still pending; see `docs/BRANDING.md` |

The script is *not* a global case-insensitive find-and-replace. Names such as `FSL*` classes, `fs_*` module identifiers, `#Firestorm` system inventory folder IDs, third-party URLs in attribution, and copyright notices must not be rewritten. Old Firestorm-specific resources and internal file names may remain and require separate audits before release.

### How to run after import

```bash
python3 scripts/rebrand_firestorm.py
python3 scripts/rebrand_firestorm.py --check
git diff --stat
git diff --check
```

The import GitHub workflow applies this script to its **review branch** before opening a PR. No automatic merge or executable release takes place.

The login lock to Stadt NexVerse G1 and G2 is a separate implementation, documented in `docs/GRID_POLICY.md`, and is not automatically completed by branding.
