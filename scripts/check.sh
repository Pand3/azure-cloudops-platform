#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIRECTORY/.." && pwd)"

if [[ -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
    PYTHON="$PROJECT_ROOT/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
else
    echo "Error: Python 3 could not be found." >&2
    exit 1
fi

cd "$PROJECT_ROOT"

echo "Checking Python formatting..."
"$PYTHON" -m ruff format --check .

echo "Running Python linting..."
"$PYTHON" -m ruff check .

echo "Running automated tests..."
"$PYTHON" -m pytest

echo "All quality checks passed."