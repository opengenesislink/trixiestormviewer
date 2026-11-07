# TrixieStorm Viewer branding

| Item | Value |
|---|---|
| Product display name | **TrixieStorm Viewer** |
| Short name | **TrixieStorm** |
| Viewer channel (source) | `TrixieStorm Viewer` |
| Technology caption | Powered by OpenGenesisLINK |
| Windows exe (planned packaging) | `TrixieStormViewer.exe` |
| Linux launcher | `trixiestormviewer` |
| Internal CMake executable | `trixiestorm-bin` |
| Windows app paths, x64 | `TrixieStormViewer_x64` |
| App bundle identifier (provisional) | `de.opengenesislink.trixiestormviewer` |

The product is **exclusively intended for Stadt NexVerse** Generation 1 (`hg.stadt-nexverse.de`) and upcoming Gen 2 Beta (`beta.stadt-nexverse.de`). Actual login endpoints and runtime restrictions are *not* yet validated. See [GRID_POLICY.md](GRID_POLICY.md).

## Original artwork and generated icons

The user supplied a 1254×1254 neon pink/violet TrixieStorm Viewer design. A compact development rendition is committed at `branding/source/trixiestorm-logo.webp`, with source processing in `scripts/build_brand_assets.py`. Before the final release, import the original rights-cleared PNG at `branding/source/trixiestorm-logo.png` and regenerate.

```bash
python3 -m pip install Pillow
python3 scripts/build_brand_assets.py
python3 scripts/audit_branding.py
```

The GitHub Actions workflow `.github/workflows/generate-brand-assets.yml` has generated and committed actual icon assets. They include Windows ICO, Linux PNG, SDL BMP, Windows/Linux installer and login UI resources. Their file existence, XML references and icon build inputs are statically audited. macOS support remains out of the initial build scope.

## Branding boundaries

Product/UI, executable, installer, desktop, cache and update identities may be replaced. **Do not overwrite** Firestorm/Linden Lab copyright and contributor credits, third-party license notices, or internal C++ identifiers such as `fs*` and inventory integration names without a compatibility audit. Do not imply the official Firestorm team endorses TrixieStorm.

The LGPL code license does not automatically authorize redistribution or trademark usage of the project logo; see `branding/ASSET_LICENSE.md`. Platform packaging and parallel-install behavior still require real OS tests.
