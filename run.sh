#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: virtual environment not found. Run ./install_dependencies.sh first." >&2
    exit 1
fi

exec "$VENV_PYTHON" "$SCRIPT_DIR/app.py" "$@"
