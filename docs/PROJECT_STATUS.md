# TrixieStorm Viewer – Verified project status
Updated: 2026-10-31.

| Item | Status | Evidence |
|---|---|---|
| New GitHub project | Initialized | Repository foundation commit(s) |
| Source license | Included | Upstream Firestorm `LICENSE`, LGPL-2.1 |
| Branding name | Decided | TrixieStorm Viewer |
| Exclusive NexVerse product scope | Decided, not implemented | Gen1 `hg.stadt-nexverse.de`, Gen2 beta `beta.stadt-nexverse.de` |
| Real login URI/port per generation | Not verified | Service domains are not necessarily login endpoints |
| External grid and Hypergrid travel blocking | Not implemented | Must cover UI, CLI, deep links and redirects |
| Gen1/Gen2 cache/profile separation | Not implemented | Required before Gen2 activation |
| App icon pipeline | Prepared | `scripts/generate_icons.py` (source image must be present) |
| Firestorm branch/commit | Verified | `Firestorm_7.2.4` → `10bd3c9f930c76e1427ddd4ecece6cdf36b4406d` |
| Firestorm C++ code in repo | **Not yet** | Local import script + on-demand GitHub Actions PR workflow available; no import executed |
| Linux x64 ReleaseOS build | Not verified | No build artifact |
| Windows x64 ReleaseOS build | Not verified | No build artifact |
| TrixieStorm executable/channel | Not implemented | Needs Firestorm code customization |
| Separate cache/config/install | Not implemented | Phase M2 |
| OpenGenesisLINK service adapters | Not implemented | Phase M3 |
| NextGen UI / renderer | Not implemented | Phases M4/M5 |
| Release | Not available | Requires full test matrix |

**Important:** A successful foundation workflow checks documentation/scripts only, not a compiled C++ viewer. Do not advertise features or releases before their evidence is linked here.

Next gate: import upstream to a reviewed feature branch, audit dependencies, verify the actual NexVerse Gen1 login URI, build `ReleaseOS` on Linux/Windows, then implement/test an exclusive Gen1 login and Gen2-ready mode without access to foreign grids.

Current product policy: [GRID_POLICY.md](GRID_POLICY.md); initial config: [`config/nexverse-generations.json`](../config/nexverse-generations.json). The JSON is a planning manifest, **not** an active Firestorm restriction.
