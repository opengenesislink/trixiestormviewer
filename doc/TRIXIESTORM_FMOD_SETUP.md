# FMOD Studio SDK – TrixieStorm local Linux build

The user-supplied FMOD Studio 2.03.15 Linux x86_64 SDK has been installed
locally on PC-Bomlitz:

`~/Projekte/TrixieStorm/fmod-sdk-2.03.15/`

The SDK supplies `libfmod.so.14.15`, `libfmodstudio.so.14.15`,
their Linux SONAME aliases and the C/C++ headers.

Install or refresh the local SDK from the user-provided archive:

```bash
cd ~/Projekte/TrixieStorm/trixiestormviewer
bash scripts/install_fmod_local.sh \
    ~/Downloads/TrixieStorm-FMOD-2.03.15-Linux-x64-SDK.tar.gz
```

The installer keeps proprietary binaries outside Git tracking. It stages
the SONAME symlink chain inside both local build directories for packaging.
The viewer itself links only to the FMOD Core library required by the
existing `LLAudioEngine_FMODSTUDIO`; the Studio library is staged as a
compatible optional runtime dependency, not evidence that Studio banks
have been integrated.

Configure with these exact existing CMake options:

```text
-DUSE_FMODSTUDIO:BOOL=ON
-DUSE_OPENAL:BOOL=ON
-DFMODSTUDIO_INCLUDE_DIR:PATH=/home/slmm/Projekte/TrixieStorm/fmod-sdk-2.03.15/include
-DFMODSTUDIO_LIBRARY:FILEPATH=/home/slmm/Projekte/TrixieStorm/fmod-sdk-2.03.15/lib/libfmod.so
```

For the optimized local profile also enable:

```text
-DUSE_AVX2_OPTIMIZATION:BOOL=ON
-DUSE_LTO:BOOL=ON
```

The viewer tries FMOD first and falls back to OpenAL if FMOD device
initialization fails. Voice chat (WebRTC) is a separate subsystem.

**Licensing:** This third-party SDK is proprietary. Keep it out of
GitHub, CI artifacts and public ReleaseOS downloads unless the specific
distribution use is authorized under FMOD licensing. Confirm license
terms at https://www.fmod.com/licensing and attribution requirements
at https://www.fmod.com/attribution before public distribution.
