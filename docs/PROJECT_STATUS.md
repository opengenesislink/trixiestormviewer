# TrixieStorm Viewer – verified status (2026-11-08)

The Firestorm 7.2.4 source is present with TrixieStorm rebranding in the **feature branch** `feature/firestorm-source-import` ([draft PR #1](https://github.com/opengenesislink/trixiestormviewer/pull/1)), **not yet on main**.

**Implemented at source level:**
- Branding and generated Windows/Linux/login icon references; German/English viewer text.
- Gen1-only canonical target `hg.stadt-nexverse.de`, legacy login URI `http://hg.stadt-nexverse.de:80/`, with exact-match checks from grid manager, login/reconnect, startup/SLURL and teleport, remote grid-list download disabled.
- Gen2 Beta `beta.stadt-nexverse.de` explicitly disabled, future isolated generation.
- Gen1 profile/cache/crash namespace isolated from original Firestorm.
- Read-only OGL v1 JSON public discovery attempt on the login panel, with schema/product/version validation and immutable login destination.
- Existing Firestorm WebRTC used preferentially when OpenSim region advertises the standard voice provisioning/signaling capabilities for server-side OGLVoice.
- A dedicated German/English Stadt NexVerse service hub menu opens public Portal, WorldMap, Marketplace, OGL public grid discovery, releases and support in an external browser. No privileged World API calls or credentials are embedded.
- Existing Firestorm OXP export improved to abort and report failure for missing requested assets, timeouts and incomplete disk writes; ownership/permission checks retained.

**Passed:** independent native C++17 grid-policy tests; static branding, XML and Python syntax workflows at their latest completed commits. Static C++ wiring audit is also included. **Not proved:** full Firestorm C++ ReleaseOS build, runtime login/teleport/assets/voice/export tests, redirect/login transport safety.

**Critical security gate:** current Gen1 login URI is HTTP port80. Authenticating with password over unencrypted public HTTP can expose credentials. Server-side [OGL discovery](https://github.com/opengenesislink/opengenesislinkserver/blob/main/doc/NexVerse/OGL_VIEWER_DISCOVERY.md) confirms the legacy route but explicitly requires TLS for new credentialed login. No private tokens are sent by the added read-only discovery. A secure deployed login strategy is required before public release.

**Not yet delivered:** mesh/animesh/PBR export/import, full WebAPI profile/groups/economy marketplace UI, maps, weather dashboard, native IAR, Discord account linking, modern docks, Vulkan/raytracing and Recast navigation. See [function matrix](OGL_FEATURE_MATRIX.md). Every feature remains gated by correct server contract, authorization and full staging verification.

## Grid server wall-clock display (OGL Viewer Clock v1)

The viewer source now polls the pinned public Gen1 discovery endpoint for the
optional `clock` contract supplied in **OpenGenesisLINK server PR #405**.
It converts the server's UTC epoch plus current configured time-zone offset
into status-bar civil time, independently of the viewer's local PC time zone.
It preserves the 12/24-hour display settings, shows the server-supplied label
(e.g. MEZ/MESZ when ROBUST `DSTZone` is Europe/Berlin), and refreshes the
server sample at approximately 60-second intervals to follow DST changes.
A missing or stale clock falls back to visibly labelled UTC, never PST/PDT.
The server feature must be merged, built and deployed to ROBUST first; its
mere presence in a PR does **not** change a running production server. Full
Linux/Windows viewer runtime integration is not yet proven.
