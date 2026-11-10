# FMOD Studio for TrixieStorm (optional, SDK required)

TrixieStorm's ReleaseOS Linux build currently uses OpenAL for world audio,
sound effects and streaming audio. WebRTC is a separate spatial voice client;
it does not replace FMOD or OpenAL.

The source contains an FMOD Studio backend and already includes the official
`skins/default/textures/3p_icons/fmod_logo.png` startup mark. That mark is
displayed only when the C++ target was actually compiled with
`LL_FMODSTUDIO=1` via `USE_FMODSTUDIO=ON`.

The official FMOD SDK is proprietary and was not found on PC-Bomlitz.
Do not bundle or download unauthorized SDK copies, and do not claim FMOD is
active without a working library. Before distribution, review the licensing
terms and attribution requirements at:

- https://www.fmod.com/licensing
- https://www.fmod.com/attribution
- https://www.fmod.com/download

Once the correct licensed **Linux x64 FMOD Studio Engine API** has been
obtained and unpacked, configure a *separate* ReleaseOS build, pointing
CMake at the complete installed SDK:

```bash
# Replace the examples with paths to your legitimate SDK installation.
FMOD_INCLUDE_DIR="/path/to/fmod/api/core/inc"
FMOD_LIBRARY="/path/to/fmod/api/core/lib/x86_64/libfmod.so"

# These options are appended after the standard autobuild configure -- flags:
-DUSE_FMODSTUDIO:BOOL=ON \
-DFMODSTUDIO_INCLUDE_DIR:PATH="$FMOD_INCLUDE_DIR" \
-DFMODSTUDIO_LIBRARY:FILEPATH="$FMOD_LIBRARY"
```

Verify the actual SDK path and sonames first; the FMOD packaging step needs
the matching `libfmod.so` copied into the Linux viewer's `lib` directory,
with its dependent libraries if applicable. Test audio startup, sound
playback, streaming and viewer shutdown before enabling this profile.

If the SDK is absent, retain `-DUSE_FMODSTUDIO=OFF` and OpenAL; never force
the FMOD mark to appear purely for branding. Licensing and attribution remain
the responsibility of the distributor.
