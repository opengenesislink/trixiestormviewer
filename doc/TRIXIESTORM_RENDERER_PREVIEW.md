# TrixieStorm graphics backends (Linux)

## OpenGL (default)
The original Firestorm / TrixieStorm rendering pipeline, using the Mesa
OpenGL driver. This remains the supported recovery path.

## Vulkan preview through Mesa Zink
This is a **working OpenGL-to-Vulkan translation** through Mesa Zink and a
compatible Vulkan driver (RADV on the Ryzen 7 2700U test PC).
It is **not a native Vulkan rewrite of Firestorm**. The same scene/shaders
are rendered, so do not expect an entirely different world appearance.

Tested on PC-Bomlitz: Mesa 25.2.8, Radeon Vega RADV Vulkan 1.4.
The GLX probe needed `LIBGL_KOPPER_DRI2=true`. The successful probe showed
`OpenGL renderer string: zink Vulkan 1.4(AMD Radeon Vega ... RADV)`.
A real Viewer-inworld test is still necessary to verify stability, shaders,
FPS, media playback and crash/recovery behavior.

To select:
1. Preferences > Graphics > Graphics Engine.
2. Choose **OpenGL** or **Vulkan via Mesa Zink (experimental, Linux)**.
3. Close and restart the viewer. The new setting applies before window creation.

To recover if the Zink graphics initialization prevents the viewer from
starting, force the reliable backend for a single launch:

```bash
TRIXIESTORM_FORCE_OPENGL=1 ./trixiestormviewer
```

Then return to Graphics Engine and select OpenGL. The override only affects
the current launch and does not overwrite user settings.

Requirements for Zink: compatible Linux Mesa DRI, Vulkan loader, physical
Vulkan GPU, correct X11/Wayland integration. Some combinations do not
support it. Use standard OpenGL or the one-launch recovery when unsure.
Display the Vulkan trademark in startup ONLY when Mesa reports an actual
Zink OpenGL renderer. Do not claim Vulkan conformance for TrixieStorm.

## Native Vulkan roadmap (future, NOT implemented)
A native Vulkan engine requires a different rendering architecture:
swapchain and lifetime, Vulkan descriptor/pipeline/resource management,
SPIR-V shader support, GL state isolation, avatar/mesh/terrain/particles
and UI rendering port, CEF/video path, lighting/PBR parity, shader caching,
error recovery, and extensive platform/GPU testing. This cannot be achieved
with driver selection or the Zink preview alone.

## Benchmarking
Compare exactly the same location, time of day, avatar load, camera angle,
render distance, graphics preset and resolution. Measure frame times
(CPU/GPU) and 1% lows in addition to average FPS. On integrated GPUs Zink
may be slower or less stable than direct OpenGL.

## Enhanced weather visuals in Zink (v2)
With `TrixieStormEnhancedClouds` and `TrixieStormZinkVisualBoost` both
selected, the active Mesa Zink renderer samples additional cloud-noise
octaves for more varied cloud edges and frontal forms. Rain fronts are
blue-charcoal; snow systems are diffuse grey-white. Density and tint follow
smoothed OGLWeather intensity; wind speed controls the approximate cloud
front drift. Toggle `TrixieStormZinkVisualBoost` to compare, and compare
to OpenGL using the same EEP preset and precipitation intensity.

This changes **cloud appearance only**, not reflections, terrain, PBR
materials or the underlying Firestorm rendering pipeline. The optional
Zink path will not always outperform native OpenGL, especially on small
integrated GPUs. TrixieStorm still has no native Vulkan rasterizer.
