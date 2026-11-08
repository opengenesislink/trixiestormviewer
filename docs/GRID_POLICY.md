# Stadt NexVerse grid policy — source implementation

**Source status: 8 November 2026.** Changes are committed to `feature/firestorm-source-import` ([PR #1](https://github.com/opengenesislink/trixiestormviewer/pull/1)), not verified by a full Windows/Linux ReleaseOS build or integrated into `main`.

## Approved login realms

| Realm | Grid ID | Login | Current availability |
|---|---|---|---|
| Gen1 (G1) | `hg.stadt-nexverse.de` | `http://hg.stadt-nexverse.de:80/` | Hardcoded source candidate; full runtime login and redirects unverified |
| Gen2 (G2 Beta) | `beta.stadt-nexverse.de` | None | Disabled; separate testing and release required |

`indra/newview/oglnexversegridpolicy.h` defines the canonical allowlist. It rejects foreign grid ID aliases, alternate authorities/ports and Hypergrid locations. The policy is called from grid-manager selection, add-grid, login connect/reconnect, startup URL and external teleport handlers. The main login UI disables manual server changes, and the old remote Firestorm grid-list downloader is no longer started.

`config/nexverse-generations.json` mirrors the current source policy, **not** a trusted runtime configuration source. The G1 program profile/cache namespace is `TrixieStormViewer_G1_x64` (or G1 without x64); G2 has no active realm or credentials. Do not auto-migrate user passwords/cookies, account credentials, inventory caches or region caps across generations.

## OGL discovery, authentication and security

The ROBUST server source provides public, read-only `GET http://hg.stadt-nexverse.de/ogl/v1/grid-info` with schema `org.opengenesislink.viewer.grid-info.v1`. The viewer sends a credential-free GET when the login panel opens and validates schema, version, advertised legacy login and product identity. On failure it does not pick another grid; discovery must not supply a new login URI. The server documentation explicitly lists `ogl_native_login: false`; native OGL login and OAuth are **not** implemented in this patch.

**Release blocker:** the only currently specified Gen1 legacy endpoint is plain HTTP port 80. Passwords sent via this protocol are not protected against network eavesdropping unless an authenticated TLS front end or separate secure login is deployed and verified. A public release must resolve this issue; changing just the Viewer to HTTPS without a working server is not a fix. Never send World API bearer tokens, API keys or LiveKit signing secrets over public HTTP.

Client restrictions are not cryptographic server authorization. Real operator-side viewer access/allowlists, permission checks, login audit, account bans and parcel/group enforcement remain in OpenGenesisLINK. A modified open-source client can change this product policy.

## Capability-safe voice and services

OGLVoice's media bridge is **server-side** Pion/LiveKit. When the region exposes standard `ProvisionVoiceAccountRequest` and `VoiceSignalingRequest` CAPS, `llvoiceclient.cpp` prefers its existing WebRTC implementation. Voice still requires a deployed bridge, valid server provisions, HTTPS where applicable, reachable ICE/TURN and live voice tests. No private `/internal/webrtc/v1/exchange` requests or LiveKit service secrets are made from the Viewer.

OGL World API data (maps, profiles, NV$, Marketplace, IAR/OAR, weather, registration) require their documented versioned OAuth/capability contracts, rights and running services. No client-side fake ownership or private backend tokens are introduced.

## Safety and test gates

- Isolated C++17 allowlist tests: `tests/nexverse_grid_policy_test.cpp`.
- Static wiring audit: `python3 scripts/audit_nexverse_runtime.py`.
- CI: `.github/workflows/nexverse-policy.yml` and branding audit.
- Required staging: passwordless discovery; authorized G1 login; failed foreign CLI/UI/SLURL/HG/redirect login attempts; region teleports; asset/inventory/PBR/mesh; server-owned ownership and NV$ calculations; end-to-end WebRTC voice; Gen1 cache isolation.
- **Not proven**: full C++ binary linking, native credentials protection, redirects, real live sessions, region access after login, all language locales, full 3D experience or future Gen2.

Do not confuse **server-side Hypergrid access for visiting users** with TrixieStorm's client product restriction: regular authorized visitors to Stadt NexVerse must still be able to move legitimately purchased transferable content to their own home grids if server policy permits. No server-wide asset export lockdown is part of this change.

## Server civil time is not an authentication feature

TrixieStorm's status clock reads optional UTC epoch, server timezone and effective
UTC offset from the **same pinned public, credential-free** OGL discovery URL.
The response never changes the allowed grid, login URI or authorization policy.
Old ROBUST deployments without the extension show UTC (not guessed Berlin or
Pacific time). The published extension is tracked in OpenGenesisLINK PR #405.
