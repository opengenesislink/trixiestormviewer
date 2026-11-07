# TrixieStorm Viewer

**TrixieStorm Viewer** is a Stadt-NexVerse-exclusive viewer project based on the [Firestorm](https://github.com/FirestormViewer/phoenix-firestorm) C++ viewer, with integrated [OpenGenesisLINK](https://github.com/opengenesislink/opengenesislinkserver) support.

**Status (2026-11-08): complete Firestorm source imported and TrixieStorm product rebranding applied on [`feature/firestorm-source-import`](https://github.com/opengenesislink/trixiestormviewer/tree/feature/firestorm-source-import) / [PR #1](https://github.com/opengenesislink/trixiestormviewer/pull/1).** Windows/Linux runtime icons are generated from a compact representation of the project-supplied logo. Source/branding checks pass; **no verified Windows or Linux C++ `ReleaseOS` build exists yet**, and the NexVerse-only login policy is not yet enforced at runtime.

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

**Source import:** the pinned Firestorm source and original Git ancestry have already been imported into the linked review branch. Do **not** rerun the import workflow while that branch exists. Review and merge [PR #1](https://github.com/opengenesislink/trixiestormviewer/pull/1) only after relevant checks.

**Grid configuration:** `config/nexverse-generations.json` describes the allowed deployment targets; it is not yet wired into the Firestorm source. The real login URI, TLS/port and redirects for each generation must be verified before shipping, and the Gen2 profile remains disabled until operational.

The script above is for reproducing the initial import from a clean repository, not a routine update. **Review licensing and build requirements before any merge or distribution.** No script force-pushes to `main`.

## TrixieStorm rebranding

The [product-name patch](scripts/rebrand_firestorm.py) and additional reviewed commits have **already rebranded the imported source** in the feature branch: channel, CMake targets, NSIS/Velopack metadata, Linux launcher, settings/cache identifiers, primary UI labels and links. [Generated platform artwork](branding/README.md) is present and referenced by the Windows resources, Linux desktop launcher, and login UI. [Static branding audit](scripts/audit_branding.py) and generated-icon workflow pass. Original Firestorm/Linden Lab copyright and internal FS* symbols are preserved. **A successful C++ build, actual Windows/Linux runtime behavior, and strict NexVerse login enforcement remain unverified.** See [rebranding details](docs/REBRANDING.md).

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
