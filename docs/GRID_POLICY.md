# Stadt NexVerse-only grid policy

**Product:** TrixieStorm Viewer  
**Decision date:** 2026-10-31  
**Status:** Specification only; restrictions are NOT yet implemented in the C++ viewer.

## 1. Allowed deployment generations

| Mode | Identity | Provided hostname | Rollout |
|---|---|---|---|
| Generation 1 | Stadt NexVerse Gen 1 | `hg.stadt-nexverse.de` | Current Stable |
| Generation 2 | Stadt NexVerse Gen 2 | `beta.stadt-nexverse.de` | Future Beta; disabled until enabled |

These hostnames identify the user-requested grid deployments; **do not assume they are actual viewer login endpoints**. In OpenSim, a Hypergrid entry address and the login-service URL can differ. For each generation, operations must verify the actual `login_uri` including scheme, port and route, server certificate and redirect behavior. Do not guess or silently substitute `http://host:80` or `http://host:8002`.

The provisional machine-readable manifest `config/nexverse-generations.json` intentionally contains `login_uri: null` until that verification is completed. The mere presence of this manifest does not configure Firestorm.

## 2. Exclusive application behavior

1. The released viewer allows login **only** to authorized Gen1 or Gen2 endpoints. No "Add Grid", custom login URL or third-party grid manager in the public client.
2. Validate every effective login destination, including the initial command-line arguments, programmatic invocation, imported viewer/grid settings, deep links, SSO paths, redirects and alternative login UI controls.
3. Do not expose external Hypergrid teleport in TrixieStorm. Region teleports inside the active NexVerse generation remain functional. Ensure the grid server enforces the intended outbound travel policy rather than relying solely on an editable local viewer.
4. Restrict only grid login/travel destinations. Authorized asset CDN, CAPTCHA, media, voice, CAPS, marketplace and update URLs may be on other hosts; validate and authorize those services separately.
5. The Generation 2 Beta profile must be hidden or disabled until its actual endpoint and security configuration are confirmed and released.

## 3. Session segregation

Treat Gen1 and Gen2 as separate security realms until proven otherwise. Allocate independent user settings, caches, credential/session storage, logs, installation/update channels where relevant. Never carry CAP URLs, JWTs, cookies or inventory IDs across generations implicitly. Remove all generation-scoped capabilities on logout or mode switch.

## 4. Validation gates (M2)

- Correct Gen1 login and subsequent asset/inventory/teleport/voice in a real build.
- Gen2 profile hidden/unavailable before launch; after launch, real login only to verified Gen2 endpoint.
- Negative tests for external login via UI, CLI, `secondlife://` links, HG URLs, saved grid configuration, redirects and code-level alternate entry points.
- Ensure that allowed non-login services still work (authorized CAPS, assets, voice, marketplace).
- No mixing Gen1 and Gen2 session tokens, cache, settings or inventory namespace.
- Feature flags, updater and error messages identify the active generation.
- Client restrictions are not a security boundary: server authorization and network-side policy are necessary where exclusivity/security is required.

## 5. License clarification

LGPL-2.1 source code remains modifiable and redistributable subject to its license. A distributed **official TrixieStorm Viewer application** can restrict the visible login choices to NexVerse, but the project cannot ensure forks of published source cannot change a client-side restriction. The server must not trust application/channel strings as proof of authentic TrixieStorm software.
