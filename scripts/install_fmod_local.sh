#!/usr/bin/env bash
# Install the user's own FMOD Studio API 2.03.15 into a private local SDK.
# Do not commit or publicly upload the proprietary SDK or its binaries.
set -euo pipefail

BASE="${HOME}/Projekte/TrixieStorm"
ARCHIVE="${1:-${HOME}/Downloads/TrixieStorm-FMOD-2.03.15-Linux-x64-SDK.tar.gz}"
SDK="${BASE}/fmod-sdk-2.03.15"
REPO="${BASE}/trixiestormviewer"

if [[ ! -f "${ARCHIVE}" ]]; then
  printf 'FMOD archive not found: %s\nDownload the SDK attachment from the chat into ~/Downloads.\n' "${ARCHIVE}" >&2
  exit 2
fi
if [[ ! -d "${REPO}/indra/cmake" ]]; then
  echo "Viewer repository not found at ${REPO}" >&2; exit 3
fi

# The uploaded official archive and the smaller x86_64-only archive have
# the same directory layout. Reject unsafe archive paths.
if tar -tzf "${ARCHIVE}" | grep -Eq '(^/|(^|/)\.\./)'; then
  echo "Refusing archive with unsafe paths" >&2; exit 4
fi

mkdir -p "${SDK}/include/fmodstudio" "${SDK}/lib"
TMP="$(mktemp -d "${BASE}/fmod-extract.XXXXXXXX")"
trap 'rm -rf "${TMP}"' EXIT
tar -xzf "${ARCHIVE}" -C "${TMP}"
ROOT="${TMP}/fmodstudioapi20315linux"
CORE="${ROOT}/api/core"
STUDIO="${ROOT}/api/studio"
test -s "${CORE}/inc/fmod.hpp"
test -s "${CORE}/lib/x86_64/libfmod.so.14.15"
test -s "${STUDIO}/lib/x86_64/libfmodstudio.so.14.15"

cp -a "${CORE}/inc/." "${SDK}/include/fmodstudio/"
cp -a "${STUDIO}/inc/." "${SDK}/include/fmodstudio/"
cp -a "${CORE}/lib/x86_64"/libfmod*.so* "${SDK}/lib/"
cp -a "${STUDIO}/lib/x86_64"/libfmodstudio*.so* "${SDK}/lib/"
cp "${ROOT}/doc/LICENSE.TXT" "${SDK}/LICENSE.TXT"

# Current build's packages directory is also symlinked from the optimized
# AVX2/LTO build. Existing OpenAL will remain installed as a fallback.
STAGING="${REPO}/build-linux-x86_64/packages/lib/release"
mkdir -p "${STAGING}"
cp -a "${SDK}/lib"/libfmod.so* "${STAGING}/"
cp -a "${SDK}/lib"/libfmodstudio.so* "${STAGING}/"
# The dynamic linker requires SONAME libfmod.so.14, not just an unversioned
# libfmod.so. Stage the complete symlink chain for both local build profiles.
# Do not commit any of these proprietary files to the source repository.
for build in build-linux-x86_64 build-linux-x86_64-avx2-lto; do
  SHARED="${REPO}/${build}/sharedlibs/lib"
  if [[ -d "${REPO}/${build}" ]]; then
    mkdir -p "${SHARED}"
    cp -a "${SDK}/lib"/libfmod*.so* "${SHARED}/"
  fi
done
test -s "${STAGING}/libfmod.so"
test -s "${SDK}/include/fmodstudio/fmod.hpp"

echo "FMOD SDK installed privately at: ${SDK}"
echo "CMake options:"
printf '  -DUSE_FMODSTUDIO:BOOL=ON\n  -DFMODSTUDIO_INCLUDE_DIR:PATH=%s/include\n  -DFMODSTUDIO_LIBRARY:FILEPATH=%s/lib/libfmod.so\n' "${SDK}" "${SDK}"
echo 'FMOD binaries are local only: check redistribution rights before publishing them.'
