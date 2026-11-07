/**
 * TrixieStorm Viewer - Stadt NexVerse destination policy.
 * Copyright (C) 2026 OpenGenesisLINK contributors.
 * Licensed under the GNU Lesser General Public License, version 2.1.
 *
 * This is a client-side product restriction, not authentication or an
 * authorization boundary. Never trust viewer identity at the grid server.
 */
#ifndef OGL_NEXVERSE_GRID_POLICY_H
#define OGL_NEXVERSE_GRID_POLICY_H

#include <string>

namespace OGLNexVerse
{
// Gen1 is the currently operated OpenSim/ROBUST endpoint. OpenSim login
// is XML-RPC over HTTP on the grid's published port 80. Do not replace
// HTTP with HTTPS: the current Gen1 grid endpoint does not support TLS.
// A live credentialed login/redirect smoke test is still required.
inline constexpr const char* GEN1_GRID = "hg.stadt-nexverse.de";
inline constexpr const char* GEN1_LOGIN_URI = "http://hg.stadt-nexverse.de:80/";
inline constexpr const char* GEN1_LABEL = "Stadt NexVerse - Generation 1";
inline constexpr const char* GEN1_REALM = "G1";

// Generation 2 is intentionally unavailable until its actual login URL,
// protocol, server trust, and realm isolation have been validated. The
// hostname alone is not permission to attempt a Beta login.
inline constexpr const char* GEN2_GRID = "beta.stadt-nexverse.de";
inline constexpr bool GEN2_ENABLED = false;

inline bool isAllowedGrid(const std::string& grid)
{
    return grid == GEN1_GRID;
}

// Exact endpoint pinning prevents alternate ports, userinfo, fragments,
// query strings, encoded authorities and subdomain lookalikes. The
// login implementation must use the same check before any auth request.
inline bool isAllowedLoginURI(const std::string& uri)
{
    return uri == GEN1_LOGIN_URI;
}

// A region name containing a foreign-grid separator must not be transformed
// into a Hypergrid teleport. Ordinary internal regions and home/last use
// the active NexVerse grid, never another grid.
inline bool isAllowedTravel(const std::string& grid,
                            const std::string& region,
                            bool hypergrid)
{
    return !hypergrid &&
           (grid.empty() || isAllowedGrid(grid)) &&
           region.find("://") == std::string::npos &&
           region.find('@') == std::string::npos &&
           region.find(':') == std::string::npos;
}

// Security-sensitive services must be negotiated over region capabilities;
// arbitrary URL redirects, CAP endpoints and HTTP proxying are NOT allowed
// by this helper. Services such as media and assets are separate from LOGIN.
}
#endif // OGL_NEXVERSE_GRID_POLICY_H
