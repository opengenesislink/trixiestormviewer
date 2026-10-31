# Architecture principles

TrixieStorm Viewer is a Firestorm-derived OpenSimulator/Hypergrid client, **not** a new game engine or an OpenGenesisLINK-exclusive client.

- Maintain upstream Firestorm viewer login, avatar, inventory, assets, networking, script/build and teleport behavior; adapt before rewriting.
- Implement an optional per-grid/per-region OpenGenesisLINK capability manager; validate feature announcements and permissions, handle timeouts and clear all tokens/URLs on grid switch.
- Keep economy, purchase, permissions, transfer and ownership decisions server-side. Treat the viewer as an untrusted client.
- Introduce detachable UI panels, scalable dark/light interfaces and creator tools without breaking established UI workflows.
- Measure baseline OpenGL/PBR first; optimize visibility/LOD/texture/cache and frame pacing before introducing new backends.
- A future Vulkan path remains experimental and must have OpenGL fallback. No renderer features are claimed implemented yet.
- Provide separate executable, cache, settings, crashlog and update channels from Firestorm.

See `ROADMAP.md` for phase ordering, benchmark gates and compatibility matrix.
