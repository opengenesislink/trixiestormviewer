# TrixieStorm Viewer – Verified project status
Updated: 2026-10-31.

| Item | Status | Evidence |
|---|---|---|
| New GitHub project | Initialized | Repository foundation commit(s) |
| Source license | Included | Upstream Firestorm `LICENSE`, LGPL-2.1 |
| Branding name | Decided | TrixieStorm Viewer |
| App icon pipeline | Prepared | `scripts/generate_icons.py` (source image must be present) |
| Firestorm branch/commit | Verified | `Firestorm_7.2.4` → `10bd3c9f930c76e1427ddd4ecece6cdf36b4406d` |
| Firestorm C++ code in repo | **Not yet** | Import script exists, import not executed |
| Linux x64 ReleaseOS build | Not verified | No build artifact |
| Windows x64 ReleaseOS build | Not verified | No build artifact |
| TrixieStorm executable/channel | Not implemented | Needs Firestorm code customization |
| Separate cache/config/install | Not implemented | Phase M2 |
| OpenGenesisLINK service adapters | Not implemented | Phase M3 |
| NextGen UI / renderer | Not implemented | Phases M4/M5 |
| Release | Not available | Requires full test matrix |

**Important:** A successful foundation workflow checks documentation/scripts only, not a compiled C++ viewer. Do not advertise features or releases before their evidence is linked here.

Next gate: import upstream to a reviewed feature branch, audit licenses/third parties, build the unmodified `ReleaseOS` baseline on Linux and Windows, test login/inventory/teleport/Hypergrid on OpenGenesisLINK and a standard OpenSim grid.
