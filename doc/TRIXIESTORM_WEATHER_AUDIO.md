# TrixieStorm / OpenGenesisLINK – native precipitation and extended sound upload

## Weather protocol
This viewer uses the server's per-region, per-avatar capability
`OGLWeatherState`, registered by `addons/OGLWeather/OglWeatherRegionModule.cs`.
It expects read-only `ogl.weather` JSON, version 1, with:

- `region_id`: must match the currently connected region
- `precipitation.condition`: `sun`, `cloud`, `rain` or `snow`
- `precipitation.intensity`: 0–100
- `precipitation.wind_kmh` and `precipitation.cloud_base_m`
- `precipitation.legacy_prim_emitters_active`

The viewer polls at most every 45 seconds, drops delayed responses after a
region crossing and stops using stale readings after 10 minutes. New weather
never rezzes prims, edits region terrain, or changes server inventory.

Rain and snow use the existing Firestorm GPU-batched particle renderer with
locally created particles near the camera. Density scales with intensity,
wind and a user multiplier. The viewer suppresses its own particles while
the CAP says a live legacy emitter already operates in the region.

When the region does not advertise `OGLWeatherState`, optional fallback
uses only the fixed trusted grid endpoint:
`https://world.stadt-nexverse.de/weather/xml`, element
`oglweather/current`, attributes `condition`,
`precipitation_intensity_percent` and `wind_kmh`.
The XML is grid-wide and does not report legacy emitter state. It can
duplicate older inworld weather; disable the fallback if needed.

Controls: Preferences → Graphics → Weather (`TrixieStorm Weather`).
They allow toggling native precipitation, toggling XML fallback and
selecting density (0.1–2.0). Changes are live. Effect rendering requires
that particles are enabled in the main viewer graphics preferences.

The grid must remain the authorized Stadt NexVerse grid. Only the
server-provisioned per-region capability is used for region-specific weather;
the XML fallback never supplies region identity.

### Known renderer limitations
- Existing GPU-batched billboard particles; not a new compute-shader system.
- No roof / building-occlusion raycast or indoor precipitation shielding yet.
- Weather v1 provides wind speed but not wind direction.
- Cloud-base height from the server is retained but the viewer creates
  precipitation a short distance above the camera for usable visual density.
- Sky/cloud darkening is managed by server OGLWeather EEP and the optional
  enhanced client-side EEP cloud shader. The weather renderer does not
  override personal EEP settings.
- No rain/snow audio has been added.

## WAV upload changes
Firestorm previously limited WAV files to 30s (SL) or 60s (OpenSim).
TrixieStorm retains Second Life compatibility while removing the
**fixed time-based rejection on OpenGenesisLINK/OpenSim**.
It still requires an uncompressed 8/16-bit PCM WAV at 44,100 Hz,
one or two channels; files are converted to Vorbis Ogg on upload.

The decoder now validates 64-bit Vorbis sample counts before arithmetic,
and rejects an asset if decompressed PCM exceeds 256 MiB. That prevents
untrusted audio assets from allocating arbitrary memory. The simulator,
CAPS uploader, RIFF container and the actual playback engine may have
additional file-size, compatibility and resource limits. Therefore it is
not a promise of literally unlimited file size or RAM use.

Recommended acceptance checks:
1. Upload and play mono/stereo PCM test WAVs of 15, 60, 120 and 300 seconds.
2. Verify inventory asset persistence and playback after viewer restart.
3. Test llPlaySound, llLoopSound and llStopSound with a longer Ogg asset.
4. Verify the FMOD Studio backend starts, and the OpenAL fallback works.
5. Reject intentionally malformed WAV headers and oversized decoded Ogg data.

## FMOD
FMOD Studio 2.03.15 was provided by the user and installed privately in
`~/Projekte/TrixieStorm/fmod-sdk-2.03.15`. Source is compiled with
`USE_FMODSTUDIO=ON`, `USE_AVX2_OPTIMIZATION=ON`, `USE_LTO=ON`.
The privately supplied SDK binaries must never be checked into this public
repository. `scripts/install_fmod_local.sh` stages the correct Linux x64
SONAME aliases (`libfmod.so.14`) into both local build trees. Distribute
FMOD-enabled packages only when the applicable FMOD rights are verified.
