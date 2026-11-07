# TrixieStorm Viewer × OpenGenesisLINK function implementation matrix

**Status: 2026-11-08 — only code actually committed to the feature branch is marked source-implemented.** This is not a release checklist, compilation report or proof of deployed server APIs. Real-time deployed endpoints and server authorization must be checked separately.

| Function / requirement | Actual source status | Remaining gate |
|---|---|---|
| App/installer/login identity | Implemented in imported C++ source and generated icons | Linux/Windows ReleaseOS binaries and install tests |
| Exclusive Stadt NexVerse G1 | Runtime guard code in grid manager, login and SLURL/teleport paths; isolated native policy tests pass | Full C++ build; redirects and alternate network entry points; real G1 login |
| G2 Beta (`beta.stadt-nexverse.de`) | Disabled and reserved | Verified port, service, realm-isolated tokens and regression suite |
| Per-generation caches/accounts | G1 process namespace and Windows cleanup; G2 reserved | Account credential store, CAP reset and cross-generation leak tests |
| Public OGL JSON discovery | Read-only client request/validation integrated; fallback keeps pinned login | Running ROBUST v1 endpoint and network test |
| Existing OpenSim XML-RPC/CAPS | Retained | Staging; plain HTTP credential transport is currently insecure |
| OGLVoice (WebRTC/LiveKit) | Standard viewer WebRTC selected when server CAPS advertised; server bridge remains independent | Pion/LiveKit production deployment, multiple-user audio and ICE/TURN tests |
| Authorized OXP export (objects, textures, animations, sounds, scripts) | Firestorm OXP path retained, improved abort/error-on-missing-assets and timeout handling | Runtime test of every asset class and permissions |
| **Mesh/animesh export + LOD/PBR materials** | **Not implemented**; existing Firestorm OXP code explicitly aborts on mesh | New format/serializer, upload/import cost and rights checks |
| Grid WebAPI profiles, groups, friends | API exists on server; no viewer-specific authenticated client | OAuth/PKCE and token storage over verified HTTPS; user-scope data |
| Weather/Seasons and PBR environment | Existing viewer EEP/PBR path retained | Verified simulator feature schema and OGLWeather UI/asset bindings |
| OGL FastRez/FastMap | Primarily server-side; baseline viewer protocols retained | Live latency/map tests; documented CAPS only |
| NV$ economy and marketplace | Existing viewer economy/currency UI retained; OGL website links present | Actual authenticated payments and Marketplace backend API contract |
| WorldMap/land portal | Existing worldmap UI and links; no native OGL map overlay | Region API, tile protocol, owner/permissions and spatial coordinate tests |
| IAR/OAR import and export | Server admin/service API with signed per-node feature rights; no new viewer client | Explicit user-scope OAuth and job lifecycle endpoints, never bypass policy |
| Discord presence/chat/roles | Firestorm Discord bridge exists; no OGL account/role linking | OAuth mapping and consent with server connector |
| LiveKit/Discord voice arbitration | Not built | SDK interoperability, privacy controls and fallback tests |
| HUD, detachable dock, modern UX, performance monitor | Original Firestorm UI controls retained | NextGen UI implementation and accessibility regression |
| Renderer Vulkan/GPU raytracing | Not implemented | Backend architecture, hardware support and OpenGL fallback |
| Recast/Detour pathfinding | Not implemented | Server-compatible navmesh/CAPS and sandboxed movement tests |
| CI release packages | Static and isolated native policy tests only | Linux/Windows ReleaseOS toolchain/deps, package signing and e2e |

## Core architectural constraints

The server and Viewer operate on separate permission domains. The viewer is always an untrusted client; never embed node HMAC, LiveKit API secret, World API machine-key, simulator ES256 key or user/admin impersonation credentials in published code or installation assets. Never claim a read-only discovery or launcher link is a transactional integration.

Reference server source: `opengenesislink/opengenesislinkserver` `doc/NexVerse/OGL_VIEWER_DISCOVERY.md`, `services/oglvoice-media/README.md`, `doc/NexVerse/WORLD_API.md`, `doc/NexVerse/OGL_FEATURE_CONTROL_09312.md`. Confirm the actual running version before release.
