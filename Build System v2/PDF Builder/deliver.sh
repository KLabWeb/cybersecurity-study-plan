#!/usr/bin/env bash
# Delivers the plan: the Final PDF copied into its dated folder in Study Plan/Study Plan PDFs.
# Refuses to deliver while any code check of the Build System fails. Run the build first.
# Usage, from any folder: bash "Build System v2/PDF Builder/deliver.sh" YYYY-MM-DD
set -u

BUILDER="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$BUILDER")"
CHECKS="$ROOT/Linters/check_all.sh"

if [ "$#" -ne 1 ]; then
    echo "Usage: bash deliver.sh YYYY-MM-DD"
    exit 1
fi
if ! bash "$CHECKS" > /dev/null; then
    echo "The code checks fail: run bash \"$CHECKS\" to see them. No delivery."
    exit 1
fi
cd "$BUILDER" || exit 1
exec "$ROOT/.venv/bin/python" -m pdf_builder.interface.delivery_cli "$1"
