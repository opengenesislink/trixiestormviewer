# TrixieStorm Viewer branding

- **Product name:** TrixieStorm Viewer
- **Short name:** TrixieStorm
- **Proposed viewer channel:** `TrixieStorm Viewer` (to be implemented in the Firestorm C++ build and checked against OGL server compatibility filters)
- **Caption:** Powered by OpenGenesisLINK
- **Application ID convention (proposal):** `de.opengenesislink.trixiestormviewer`, subject to per-platform validation
- **Linux executable (proposal):** `trixiestormviewer`
- **Windows executable (proposal):** `TrixieStormViewer.exe`

The project supplied a square neon pink/violet TrixieStorm Viewer graphic featuring its character, globe and "Powered by OpenGenesisLINK" text. It should be retained without replacement by generic Firestorm/Second Life logos.

## Icon generation

Place the provided original image at `branding/source/trixiestorm-logo.png`, then run:

```bash
python3 -m pip install Pillow
python3 scripts/generate_icons.py
```

Generated in `branding/generated`: Linux PNGs (16, 32, 48, 64, 128, 256, 512), Windows multi-resolution ICO, and an optimized 256px icon for metadata.

**Generation is not yet integration.** After importing upstream, wire the images into Windows resource/packaging, Linux desktop launchers and installers; replace the original Firestorm icon references, and make caches/profiles/updaters separate.

Icons and naming are application assets, distinct from the program license. See `branding/ASSET_LICENSE.md`.

The source graphic should be distributed only by or with permission of its rights holder. Do not claim rights beyond those granted.
