#!/usr/bin/env bash
# Builds the plan PDF into Study Plan/Study Plan PDFs.
# Refuses to build while any code check of the Build System fails.
# Usage, from any folder: bash "Build System v2/PDF Builder/build.sh"
set -u

BUILDER="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$BUILDER")"
CHECKS="$ROOT/Linters/check_all.sh"

if ! bash "$CHECKS" > /dev/null; then
    echo "The code checks fail: run bash \"$CHECKS\" to see them. No build."
    exit 1
fi
cd "$BUILDER" || exit 1
exec "$ROOT/.venv/bin/python" -m pdf_builder
