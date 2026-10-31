#!/usr/bin/env bash
set -euo pipefail
bash -n scripts/import_firestorm.sh
bash -n scripts/verify-foundation.sh
python3 -m py_compile scripts/generate_icons.py
grep -q 'TrixieStorm Viewer' README.md ROADMAP.md docs/BRANDING.md
test -s LICENSE
echo "Foundation checks passed (not a compiled viewer test)."
