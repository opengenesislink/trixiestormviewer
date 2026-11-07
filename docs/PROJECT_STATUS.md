# TrixieStorm Viewer – verified project status

Updated: 2026-11-08. Source branch: [feature/firestorm-source-import](https://github.com/opengenesislink/trixiestormviewer/tree/feature/firestorm-source-import); [Draft PR #1](https://github.com/opengenesislink/trixiestormviewer/pull/1) targets `main`.

| Item | Status | Evidence |
|---|---|---|
| Pinned Firestorm source (7.2.4) | **Imported into source branch; not yet merged to main** | Upstream commit `10bd3c9f930c76e1427ddd4ecece6cdf36b4406d` retained as ancestor |
| LGPL-2.1 and copyright attribution | Preserved | Original source headers, Firestorm & Linden Lab credits, `LICENSE` |
| Product/channel name | **Patched in CMake/manifests/UI** | `TrixieStorm Viewer`, `TrixieStorm` |
| Windows executable/product metadata | **Patched in source** | `TrixieStormViewer.exe` identity, Windows .rc metadata; actual build unverified |
| Linux launcher/desktop/installer | **Patched in source** | `trixiestormviewer`, desktop entry, unique application paths |
| Separate installer/user/cache/crash identifiers | **Partially implemented in source** | Windows registry, profile/cache/crash names; requires runtime validation |
| Windows/Linux/runtime UI icons | **Generated and committed** | ICO/PNG/BMP/login icon, generated via `scripts/build_brand_assets.py` |
| Icon quality | Development-grade | Compact WebP rendition (64×64) committed; full 1254×1254 original should replace it before release |
| Main application UI labels (English and German) | **Patched** | Login, settings, Help, support URLs, notifications; other locale review pending |
| Static branding consistency, Python, selected XML | **Passed CI** | `scripts/audit_branding.py`, branding audit workflow |
| Windows x64 ReleaseOS C++ build | **Not verified** | No build artifact or installer smoke test |
| Linux x64 ReleaseOS C++ build | **Not verified** | No build artifact or launcher smoke test |
| Exclusive NexVerse Gen1/Gen2 product scope | Specified, **not security-enforced** | `docs/GRID_POLICY.md`, provisional JSON; hiding a UI checkbox is not a login restriction |
| Actual Gen1/Gen2 login URI and port | Not verified | Hypergrid/service hostnames are not necessarily login URIs |
| Gen1/Gen2 cache/session isolation | Not complete | Separate per-generation credentials, cache and CAP cleanup still needed |
| OpenGenesisLINK services and renderer upgrades | Not implemented | Roadmap phases M3+ |
| Release | **Not available** | No compiled/tested viewer and no signed install artifacts |

**Status distinction:** A static XML/branding script that passes does not prove the C++ viewer compiles. The imported code on a draft pull request does not imply it is on `main`.

**Next release gates:** Review/merge import PR; run Linux/Windows `ReleaseOS` builds; test product identity, icon, installer data isolation, login/inventory/teleport/mesh/PBR; implement verified NexVerse-only Gen1/Gen2 login and security restrictions; complete license/dependency audit and source attribution.
