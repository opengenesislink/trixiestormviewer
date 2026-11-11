# TrixieStorm Linux build profiles

TrixieStorm supports two distinct x86_64 compiler profiles.

## Portable ReleaseOS (default)
- x86_64 baseline with SSE2, as in upstream Firestorm.
- `-DUSE_AVX2_OPTIMIZATION:BOOL=OFF`
- `-DUSE_LTO:BOOL=OFF`
- Suitable for older CPUs and broadly distributed packages.

## Targeted AVX2 + LTO
Use only for a machine whose CPU supports AVX2. On PC-Bomlitz, the
AMD Ryzen 7 2700U supports AVX2.

To request the optimized profile with the existing Autobuild toolchain,
configure the ReleaseOS build with:

```bash
autobuild configure -A 64 -c ReleaseOS -- \
  -DOPENSIM:BOOL=ON \
  -DROOT_PROJECT_NAME:STRING=TrixieStorm \
  -DPACKAGE:BOOL=ON \
  -DLL_TESTS:BOOL=OFF \
  -DUSE_AVX2_OPTIMIZATION:BOOL=ON \
  -DUSE_LTO:BOOL=ON

cmake --build build-linux-x86_64 --parallel 2
```

The Autobuild variables file and Python environment must already be
configured, as described in the standard Linux build guide.

**Warning:** Changing these flags requires substantial recompilation.
LTO also makes the final link considerably more memory intensive.
AVX2-only binaries do not run on processors without AVX2; keep a
portable ReleaseOS build for general distribution.

AVX2/LTO may reduce CPU time in specific workloads; it does not by
itself resolve a GPU-bound frame-rate limit. Benchmark equivalent
scenes, graphics settings, resolution, and cache state before claiming
a performance improvement.

Audio note: FMOD Studio is a separately licensed/installed audio
backend and is not part of the generic open-source ReleaseOS build;
OpenAL remains the available audio engine. WebRTC/Vivox concern
voice transport and are not substitutes for FMOD/OpenAL.
