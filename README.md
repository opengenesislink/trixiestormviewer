# TrixieStorm Viewer

**TrixieStorm Viewer** is a Stadt-NexVerse-exclusive viewer project based on the [Firestorm](https://github.com/FirestormViewer/phoenix-firestorm) C++ viewer, with integrated [OpenGenesisLINK](https://github.com/opengenesislink/opengenesislinkserver) support.

**Status (2026-10-31): repository foundation only.** Firestorm source has **not** yet been imported or compiled here. There is no verified downloadable TrixieStorm Viewer build.

## Product goals
- **Exclusively connect to Stadt NexVerse.** Generation 1: `hg.stadt-nexverse.de`; upcoming Generation 2 beta: `beta.stadt-nexverse.de`. These are service hostnames, not yet verified full viewer login URLs.
- Remove public third-party grid addition/selection. Any external Hypergrid teleport must be blocked in the final released client and enforced on the grid server where required; protocol compatibility is retained internally.
- Provide a unique TrixieStorm Viewer application/channel identity and separate settings, cache and installation paths; coexist with upstream Firestorm.
- Offer configurable, modern UI, accessible layouts, and OpenGenesisLINK services (World API, weather, voice, marketplace and economy) through safely negotiated capabilities.
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

**Optional GitHub Actions import:** [Run the reviewed Firestorm import workflow](https://github.com/opengenesislink/trixiestormviewer/actions/workflows/import-firestorm.yml) via **Run workflow**. It attempts to create a source-import pull request, not a release, and requires Actions write permissions. No automatic merge into `main`.

**Grid configuration:** `config/nexverse-generations.json` describes the allowed deployment targets; it is not yet wired into the Firestorm source. The real login URI, TLS/port and redirects for each generation must be verified before shipping, and the Gen2 profile remains disabled until operational.

This script creates `feature/firestorm-source-import`, fetches and verifies the pinned upstream commit and attempts to merge it, preserving upstream Git ancestry. It may stop for manual conflict resolution. **Review licensing and build requirements before any merge or distribution.** No script force-pushes to `main`.

## TrixieStorm rebranding

The pinned-source import workflow applies [the audited product-name patch](scripts/rebrand_firestorm.py) on its **review branch**. The patch changes the visible app/channel identity, launcher, internal executable name, metadata and profile paths; it preserves original Firestorm/Linden Lab copyright and internal FS* symbols. **It is not yet a tested C++ build, and the custom application icons still need binary integration.** See [the rebranding plan](docs/REBRANDING.md).

## Documentation
- [German NextGen roadmap and acceptance criteria](ROADMAP.md)
- [Current, evidence-based status](docs/PROJECT_STATUS.md)
- [Developer and build instructions](docs/BUILD.md)
- [Branding and application icons](docs/BRANDING.md)
- [Source-level rename and testing](docs/REBRANDING.md)
- [Stadt NexVerse Generation 1/Generation 2 exclusive-grid policy](docs/GRID_POLICY.md)
- [Architecture principles](docs/ARCHITECTURE.md)
- [Licenses, attribution and distribution gate](docs/LEGAL.md)
- [Contribution guide](CONTRIBUTING.md)

## License and attribution

Code in this project is intended to follow the **GNU Lesser General Public License v2.1** (`LICENSE`), subject to original file notices and third-party dependencies. Firestorm and Second Life are separate projects and retain their respective attribution and trademarks. Original TrixieStorm branding assets are separately addressed in `branding/ASSET_LICENSE.md`; the code license does not automatically grant trademark rights.

**TrixieStorm Viewer – Powered by OpenGenesisLINK.** Not an official Firestorm or Second Life release.
