# TrixieStorm Viewer

**TrixieStorm Viewer** is an independent OpenSimulator/Hypergrid viewer project based on the [Firestorm](https://github.com/FirestormViewer/phoenix-firestorm) C++ viewer, with optional [OpenGenesisLINK](https://github.com/opengenesislink/opengenesislinkserver) integrations.

**Status (2026-10-31): repository foundation only.** Firestorm source has **not** yet been imported or compiled here. There is no verified downloadable TrixieStorm Viewer build.

## Product goals
- Preserve standard OpenSimulator and Hypergrid login, inventory, avatar, building, teleport and communications.
- Provide a unique TrixieStorm Viewer application/channel identity and separate settings, cache and installation paths; coexist with upstream Firestorm.
- Offer configurable, modern UI, accessible layouts, and optional OpenGenesisLINK services (World API, weather, voice, marketplace and economy) through safely negotiated capabilities.
- Optimize the existing OpenGL/PBR rendering path first; evaluate Vulkan, advanced weather, water and lighting only later with measurements and OpenGL fallback.

## Firestorm source baseline

- Upstream: https://github.com/FirestormViewer/phoenix-firestorm
- Release branch: `Firestorm_7.2.4`
- Pinned commit: `10bd3c9f930c76e1427ddd4ecece6cdf36b4406d`
- First targets: Windows x86_64 and Linux x86_64, OpenSimulator `ReleaseOS` profile

```bash
git clone https://github.com/opengenesislink/trixiestormviewer.git
cd trixiestormviewer
bash scripts/import_firestorm.sh
```

This script creates `feature/firestorm-source-import`, fetches and verifies the pinned upstream commit and attempts to merge it, preserving upstream Git ancestry. It may stop for manual conflict resolution. **Review licensing and build requirements before any merge or distribution.** No script force-pushes to `main`.

## Documentation
- [German NextGen roadmap and acceptance criteria](ROADMAP.md)
- [Current, evidence-based status](docs/PROJECT_STATUS.md)
- [Developer and build instructions](docs/BUILD.md)
- [Branding and application icons](docs/BRANDING.md)
- [Architecture and compatibility principles](docs/ARCHITECTURE.md)
- [Licenses, attribution and distribution gate](docs/LEGAL.md)
- [Contribution guide](CONTRIBUTING.md)

## License and attribution

Code in this project is intended to follow the **GNU Lesser General Public License v2.1** (`LICENSE`), subject to original file notices and third-party dependencies. Firestorm and Second Life are separate projects and retain their respective attribution and trademarks. Original TrixieStorm branding assets are separately addressed in `branding/ASSET_LICENSE.md`; the code license does not automatically grant trademark rights.

**TrixieStorm Viewer – Powered by OpenGenesisLINK.** Not an official Firestorm or Second Life release.
