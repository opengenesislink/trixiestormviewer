/**
 * TrixieStorm / OpenGenesisLINK weather state and client precipitation.
 * SPDX-License-Identifier: LGPL-2.1-only
 */
#ifndef OGL_NEXVERSE_WEATHER_H
#define OGL_NEXVERSE_WEATHER_H

namespace OGLNexVerseWeather
{
    // Smoothed values in 0..1 for the EEP cloud shader. These are visual
    // parameters, not simulator-wide environment overrides.
    struct VisualState
    {
        float rain = 0.f;
        float snow = 0.f;
        float wind = 0.f;
    };
    VisualState visualState();

    // Call from the main viewer loop only. Networks and native local particle
    // rendering are disabled outside the approved Stadt NexVerse grid.
    void update();
    void shutdown();
}

#endif // OGL_NEXVERSE_WEATHER_H
