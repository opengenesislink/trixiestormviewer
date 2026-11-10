/**
 * TrixieStorm / OpenGenesisLINK weather state and client precipitation.
 * SPDX-License-Identifier: LGPL-2.1-only
 */
#ifndef OGL_NEXVERSE_WEATHER_H
#define OGL_NEXVERSE_WEATHER_H

namespace OGLNexVerseWeather
{
    // Call from the main viewer loop only. Networks and native local particle
    // rendering are disabled outside the approved Stadt NexVerse grid.
    void update();
    void shutdown();
}

#endif // OGL_NEXVERSE_WEATHER_H
