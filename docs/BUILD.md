# Build and source import

**Current state:** Foundation only. There is no bundled C++ viewer in this repository yet.

## 1. Import pinned Firestorm code into a review branch

```bash
git clone https://github.com/opengenesislink/trixiestormviewer.git
cd trixiestormviewer
bash scripts/import_firestorm.sh
```

The import uses official Firestorm `Firestorm_7.2.4` at SHA `10bd3c9f930c76e1427ddd4ecece6cdf36b4406d`; it never changes `main` or pushes remotely. Existing files and the upstream history must be reviewed. Resolve merge conflicts manually if prompted; do not blindly replace license headers or notice files.

## 2. Establish reproducible baseline

On a reviewed import branch follow the **upstream instructions for the exact pinned version**:
- Linux: https://github.com/FirestormViewer/phoenix-firestorm/blob/Firestorm_7.2.4/doc/building_linux.md
- Windows: https://github.com/FirestormViewer/phoenix-firestorm/blob/Firestorm_7.2.4/doc/building_windows.md

Upstream's Linux guide specifies Ubuntu 22.04 LTS x86_64, GCC 11, at least 16 GB RAM, 64 GB disk, and glibc 2.34+. These are upstream baseline requirements, not proof of a working TrixieStorm build. Check autobuild/versioned dependency requirements and compile OpenSimulator `ReleaseOS`, not Second Life-only profiles.

Record commit SHA, exact SDK/compiler/autobuild versions, dependency revisions, build log, hashes and platform.

## 3. Rebrand after baseline works

Set executable/product/channel IDs to `TrixieStorm Viewer`. Keep TrixieStorm paths, settings, cache, crash reports and updater independent from Firestorm. Use icons produced by `scripts/generate_icons.py` for installers, desktop files and executable resources.

OpenGenesisLINK additions must remain optional on other OpenSim grids. Do not disable HTTPS certificate verification or trust arbitrary server-supplied URLs without authorization.

## 4. Test/release gate

A real installable Linux/Windows build must pass login, avatar appearance, inventory/permissions, Teleport/Hypergrid, voice, mesh/PBR, camera/build controls, region crossing, clean uninstall and side-by-side installation with Firestorm. Run tests on NexVerse *and* a standard OpenSimulator grid. See `ROADMAP.md`.
