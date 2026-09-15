#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIRECTORY="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIRECTORY/.." && pwd)"
PROJECT_VENV="$PROJECT_ROOT/.venv"

cd "$PROJECT_ROOT"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 could not be found." >&2
    exit 1
fi

if [[ ! -x "$PROJECT_VENV/bin/python" ]]; then
    echo "Creating Python virtual environment..."
    python3 -m venv "$PROJECT_VENV"
else
    echo "Using existing Python virtual environment."
fi

echo "Upgrading pip..."
"$PROJECT_VENV/bin/python" -m pip install --upgrade pip

echo "Installing CloudOps and development dependencies..."
"$PROJECT_VENV/bin/python" -m pip install --editable ".[dev]"

echo "Verifying the CloudOps CLI..."
"$PROJECT_VENV/bin/cloudops" version

echo "Development environment is ready."
echo "Activate it with: source .venv/bin/activate"