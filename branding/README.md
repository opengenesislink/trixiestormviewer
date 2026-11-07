# TrixieStorm Viewer application artwork

The application's own neon-pink TrixieStorm graphic is supplied by the project.

- `branding/source/trixiestorm-logo.webp`: compact 64×64 preliminary rendition of the project-uploaded original, included so that source checkouts can build against real project artwork. It is **not the original full-resolution image**.
- `branding/source/trixiestorm-logo.png`: preferred replacement input for final releases (the original 1254×1254 PNG). Place the rights-cleared original here and regenerate all icons.
- `scripts/build_brand_assets.py`: creates multi-size ICO, Linux PNG, login image, optional ICNS and the platform resources consumed by the viewer.
- `indra/newview/res/trixiestormviewer.ico`: Windows resource and installer icon.
- `indra/newview/res/trixiestormviewer.png`: Linux application icon.
- `indra/newview/skins/default/textures/windows/trixiestorm_login.png`: login/startup logo.

The GitHub workflow `.github/workflows/generate-brand-assets.yml` generates/commits the concrete runtime icons when source artwork changes. Build/publish jobs must use the committed generated assets. Do not let upstream Firestorm CMake override TrixieStorm icons at configure time.

The binary identity may not replace the original authorship notices. Distribution rights for project-provided artwork must be documented separately in `branding/ASSET_LICENSE.md`.
