# Architecture principles

TrixieStorm Viewer is a Firestorm-derived, **Stadt-NexVerse-exclusive** OpenSimulator client, not a new game engine.

## Target deployments

- **Generation 1 (Stable):** `hg.stadt-nexverse.de`.
- **Generation 2 (future Beta):** `beta.stadt-nexverse.de`, disabled until provisioned and verified.
- These are **target hostnames**, not assumed fully qualified OpenSim login URIs. Login scheme, port, path and redirects need verification for each deployment before binding them into the executable.

## Runtime boundaries

- Keep Firestorm login/network/asset/teleport/inventory implementations as a protocol basis, but restrict login destinations to authorized Stadt NexVerse generation endpoints. Do not expose free third-party grid entry in the production UI, CLI, deep links or imported settings.
- Distinguish **login grid targets** from authorized CAPS, asset, media, voice and marketplace hosts. Do not break required content downloads by indiscriminately blocking other domains.
- Block direct outbound Hypergrid teleport to foreign grids as a product requirement; additionally enforce relevant rules server-side. Incoming Hypergrid avatars on the NexVerse server are a server policy, not a reason to add foreign client login destinations.
- On Gen1↔Gen2 switching clear authenticated tokens/CAP URLs and isolate settings, caches, inventory mappings, logs and credentials. Treat them as separate security realms unless the server explicitly establishes a shared identity contract.
- Keep economy, purchase, permissions, transfer and ownership decisions exclusively server-side. The viewer is an untrusted client and its apparent branding or channel is not authentication.
- Integrate OGL World API, weather, voice, NV$, marketplace and update services only via versioned, trusted, authorized capabilities appropriate to the active generation.
- Provide modern detachable panels, accessibility and performance telemetry without breaking standard Firestorm UX workflows.
- Optimize baseline OpenGL/PBR first; optional Vulkan later with documented benchmarks and mandatory OpenGL fallback.
- Keep executable, settings, crashes and update channels independent of official Firestorm installations.

See [GRID_POLICY.md](GRID_POLICY.md), [config manifest](../config/nexverse-generations.json) and [ROADMAP.md](../ROADMAP.md).
