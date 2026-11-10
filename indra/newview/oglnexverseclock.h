/**
 * TrixieStorm Viewer — read-only server-authoritative civil wall clock.
 * Copyright (C) 2026 OpenGenesisLINK contributors.
 * SPDX-License-Identifier: LGPL-2.1-only
 *
 * The original Firestorm time formatting remains intact for other purposes.
 * This API only supplies the NexVerse clock shown in the status bar.
 */
#ifndef OGL_NEXVERSE_CLOCK_H
#define OGL_NEXVERSE_CLOCK_H

#include <ctime>
#include <string>

namespace OGLNexVerseClock
{
// Rate-limited, public, credential-free grid-info GET. Safe to call every
// second from status-bar refresh and once at login screen construction.
void refreshIfDue();

// A valid server sample is extrapolated using a monotonic timer, so it
// remains correct even when the user's operating-system clock is wrong.
// Continues using a recent server sample when discovery is temporarily down.
// Without a usable sample, falls back to Europe/Berlin with EU DST rules;
// no Pacific/UTC-only fallback is displayed on the NexVerse status bar.
bool now(std::time_t& civilEpoch, std::string& abbreviation,
         std::string& zoneId);

// Convert an arbitrary UTC instant (including historical chat timestamps)
// to the grid's civil time. On NexVerse this is MEZ/MESZ with DST.
std::time_t civilTimeFromUTC(std::time_t utcEpoch);
}
#endif
