#!/usr/bin/env bash
set -euo pipefail

APP_NAME="SecurePass"
DIST_ROOT="/src/dist/windows"
DIST_DIR="$DIST_ROOT/$APP_NAME"
WORK_DIR="/tmp/securepass-pyinstaller"
PYTHON='C:\users\root\AppData\Local\Programs\Python\Python311\python.exe'

cd /src

rm -rf "$DIST_DIR" "$WORK_DIR"
mkdir -p "$DIST_ROOT"

xvfb-run -a wine "$PYTHON" -m pip install -r requirements.txt
xvfb-run -a wine "$PYTHON" -m PyInstaller \
    --noconfirm \
    --clean \
    --windowed \
    --name "$APP_NAME" \
    --distpath "$(winepath -w "$DIST_ROOT")" \
    --workpath "$(winepath -w "$WORK_DIR")" \
    --specpath "$(winepath -w "$WORK_DIR")" \
    --add-data "$(winepath -w /src/assets);assets" \
    --add-data "$(winepath -w /src/locales);locales" \
    app.py

rm -rf "$DIST_DIR/database"
mkdir -p "$DIST_DIR/database"

cd "$DIST_ROOT"
rm -f "$APP_NAME-windows-portable.zip"
zip -qr "$APP_NAME-windows-portable.zip" "$APP_NAME"

if [[ -n "${HOST_UID:-}" && -n "${HOST_GID:-}" ]]; then
    chown -R "$HOST_UID:$HOST_GID" "$(dirname "$DIST_ROOT")"
fi

echo "Built $DIST_ROOT/$APP_NAME-windows-portable.zip"
