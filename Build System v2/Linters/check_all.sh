#!/usr/bin/env bash
# Runs every code check over all code in the Build System, each tool in turn.
# Prints pass or FAIL per tool, then the list of failed tools. Exits 1 when any tool fails.
# Usage, from any folder: bash "Build System v2/Linters/check_all.sh"
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/.venv/bin"
export PYTHONPATH="$ROOT/Linters:$ROOT/PDF Builder"
cd "$ROOT" || exit 1

FAILED=()

run_check() {
    local label="$1"
    shift
    echo "== $label"
    if "$@"; then
        echo "RESULT: pass"
    else
        echo "RESULT: FAIL"
        FAILED+=("$label")
    fi
}

run_check "ruff: PEP 8, naming, docstrings, type hints, bugs, security" "$BIN/ruff" check .
run_check "wemake: readability limits" "$BIN/flake8" .
run_check "complexipy: cognitive complexity" "$BIN/complexipy" .
run_check "vulture: dead code" "$BIN/vulture"
run_check "pylint: class design" "$BIN/pylint" --recursive=y Linters "PDF Builder"
run_check "mypy: strict types" "$BIN/mypy" .
run_check "import-linter: DDD layers" "$BIN/lint-imports"
run_check "code_rules: no load-time code, no mutable globals, stateless classes" \
    "$BIN/python" -m code_rules .
run_check "pytest: tests and coverage" "$BIN/python" -m pytest -q -p no:cacheprovider \
    Linters/tests "PDF Builder/tests" --cov=code_rules --cov=pdf_builder

echo
if [ "${#FAILED[@]}" -eq 0 ]; then
    echo "All checks passed."
    exit 0
fi
echo "Failed: ${#FAILED[@]}"
printf '   %s\n' "${FAILED[@]}"
exit 1
