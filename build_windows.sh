#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="securepass-windows-builder"

docker build -f "$SCRIPT_DIR/build/windows/Dockerfile" -t "$IMAGE_NAME" "$SCRIPT_DIR"
docker run --rm \
    -e HOST_UID="$(id -u)" \
    -e HOST_GID="$(id -g)" \
    -v "$SCRIPT_DIR:/src" \
    "$IMAGE_NAME"
