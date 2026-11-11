# Build and source import

**Current state (2026-11-08):** Firestorm C++ source and TrixieStorm rebranding are present in `feature/firestorm-source-import` ([PR #1](https://github.com/opengenesislink/trixiestormviewer/pull/1)), but **not merged to main**. No compiled viewer has been verified.

## 1. Pinned Firestorm source (already imported into review branch)

```bash
git clone https://github.com/opengenesislink/trixiestormviewer.git
cd trixiestormviewer
bash scripts/import_firestorm.sh
```

The completed review-branch import uses official Firestorm `Firestorm_7.2.4` at SHA `10bd3c9f930c76e1427ddd4ecece6cdf36b4406d`; it never changes `main` or pushes remotely. Existing files and the upstream history must be reviewed. Resolve merge conflicts manually if prompted; do not blindly replace license headers or notice files.

## 2. Establish reproducible baseline

On a reviewed import branch follow the **upstream instructions for the exact pinned version**:
- Linux: https://github.com/FirestormViewer/phoenix-firestorm/blob/Firestorm_7.2.4/doc/building_linux.md
- Windows: https://github.com/FirestormViewer/phoenix-firestorm/blob/Firestorm_7.2.4/doc/building_windows.md

Upstream's Linux guide specifies Ubuntu 22.04 LTS x86_64, GCC 11, at least 16 GB RAM, 64 GB disk, and glibc 2.34+. These are upstream baseline requirements, not proof of a working TrixieStorm build. Check autobuild/versioned dependency requirements and compile OpenSimulator `ReleaseOS`, not Second Life-only profiles.

Record commit SHA, exact SDK/compiler/autobuild versions, dependency revisions, build log, hashes and platform.

## 3. Confirm source-level rebranding after baseline works

Executable/product/channel IDs, principal menus and generated icons have been patched. Run `python3 scripts/audit_branding.py` to validate static identity and asset links. Verify **real** installed executable filename, app icons, Windows registration, cache isolation and Linux desktop launcher in the built packages before shipping. The original supplied high-resolution icon must replace the compact rendition.

OpenGenesisLINK integration is available only when connected to Stadt NexVerse Generation 1 or Generation 2. The public TrixieStorm build must not expose arbitrary grid management, login URL overrides or foreign Hypergrid travel. Do not disable HTTPS certificate verification or trust arbitrary server-supplied URLs without authorization.

## 4. Test/release gate

A real installable Linux/Windows build must pass login, avatar appearance, inventory/permissions, Teleport/Hypergrid, voice, mesh/PBR, camera/build controls, region crossing, clean uninstall and side-by-side installation with Firestorm. Run tests on NexVerse Generation 1 and (once deployed) Generation 2, including rejection of foreign grid login and external HG teleport attempts. See `ROADMAP.md`.

## Exclusive login target integration

The source-level implementation must enforce the [grid policy](GRID_POLICY.md) when Firestorm is imported. The [manifest](../config/nexverse-generations.json) only documents target hostnames; `login_uri: null` is intentional because the real OpenSim login URL/port is not verified. The final client must safely reject unknown grid URLs, bypasses through CLI/deep links and foreign HG teleport. Distinguish authorized non-login services (CAPs/assets/media/voice) from login destinations. On Gen1↔Gen2 switch, securely invalidate session URLs/tokens and isolate cache and settings.
