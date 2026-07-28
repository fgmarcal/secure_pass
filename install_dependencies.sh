#!/usr/bin/env bash
set -euo pipefail

APP_NAME="Secure Pass"
APP_COMMAND="secure-pass"
ARCHIVE_URL="${SECURE_PASS_ARCHIVE_URL:-https://github.com/fgmarcal/secure_pass/archive/refs/heads/main.tar.gz}"
INSTALL_DIR="${SECURE_PASS_INSTALL_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/secure-pass}"
BIN_DIR="${SECURE_PASS_BIN_DIR:-$HOME/.local/bin}"
TMP_DIR=""

mkdir -p "$INSTALL_DIR"
INSTALL_DIR="$(cd "$INSTALL_DIR" && pwd)"
mkdir -p "$BIN_DIR"
BIN_DIR="$(cd "$BIN_DIR" && pwd)"
LAUNCHER_PATH="$BIN_DIR/$APP_COMMAND"
VENV_DIR="$INSTALL_DIR/venv"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
    if [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
        rm -rf "$TMP_DIR"
    fi
}
trap cleanup EXIT

echo "$APP_NAME - Linux installer"
echo "-----------------------------"
echo "Install directory: $INSTALL_DIR"
echo "Launcher: $LAUNCHER_PATH"
echo ""

if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is not installed or not in PATH." >&2
    exit 1
fi

if ! command -v curl &>/dev/null; then
    echo "Error: curl is required to download $APP_NAME." >&2
    exit 1
fi

if ! command -v tar &>/dev/null; then
    echo "Error: tar is required to extract $APP_NAME." >&2
    exit 1
fi

if ! python3 -c "import tkinter" &>/dev/null; then
    echo "Error: tkinter is not available for python3." >&2
    echo "Install it with your package manager, for example:" >&2
    echo "  Debian/Ubuntu: sudo apt install python3-tk" >&2
    echo "  Fedora:        sudo dnf install python3-tkinter" >&2
    echo "  Arch:          sudo pacman -S tk" >&2
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Using Python $PYTHON_VERSION"

install_project() {
    local extracted_dir

    if [ -f "$SCRIPT_DIR/app.py" ] && [ -f "$SCRIPT_DIR/requirements.txt" ] && [ "$SCRIPT_DIR" = "$INSTALL_DIR" ]; then
        echo "Running from the installed project directory."
        return
    fi

    if [ -e "$INSTALL_DIR" ] && [ ! -f "$INSTALL_DIR/app.py" ] && [ -n "$(find "$INSTALL_DIR" -mindepth 1 -maxdepth 1 -print -quit)" ]; then
        echo "Error: $INSTALL_DIR already exists and is not a $APP_NAME installation." >&2
        echo "Set SECURE_PASS_INSTALL_DIR to use another directory." >&2
        exit 1
    fi

    echo "Downloading/updating $APP_NAME..."
    TMP_DIR="$(mktemp -d)"
    curl -fsSL "$ARCHIVE_URL" -o "$TMP_DIR/secure-pass.tar.gz"
    tar -xzf "$TMP_DIR/secure-pass.tar.gz" -C "$TMP_DIR"
    extracted_dir="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d -print -quit)"

    if [ -z "$extracted_dir" ]; then
        echo "Error: could not extract $APP_NAME archive." >&2
        exit 1
    fi

    mkdir -p "$INSTALL_DIR"
    cp -R "$extracted_dir/." "$INSTALL_DIR"
}

create_launcher() {
    mkdir -p "$BIN_DIR"

    cat > "$LAUNCHER_PATH" <<LAUNCHER
#!/usr/bin/env bash
set -e
cd "$INSTALL_DIR"
exec ./run.sh "\$@"
LAUNCHER

    chmod +x "$LAUNCHER_PATH"
}

shell_rc_file() {
    case "$(basename "${SHELL:-}")" in
        zsh)
            echo "$HOME/.zshrc"
            ;;
        bash)
            echo "$HOME/.bashrc"
            ;;
        *)
            echo "$HOME/.profile"
            ;;
    esac
}

create_alias() {
    local rc_file
    local marker_start
    local marker_end
    local alias_line
    local temp_file

    rc_file="$(shell_rc_file)"
    marker_start="# >>> secure-pass alias >>>"
    marker_end="# <<< secure-pass alias <<<"
    alias_line="alias $APP_COMMAND=\"$LAUNCHER_PATH\""

    touch "$rc_file"

    if grep -Fq "$marker_start" "$rc_file"; then
        temp_file="$(mktemp)"
        awk -v start="$marker_start" -v end="$marker_end" '
            $0 == start { skip = 1; next }
            $0 == end { skip = 0; next }
            skip != 1 { print }
        ' "$rc_file" > "$temp_file"
        mv "$temp_file" "$rc_file"
    fi

    {
        echo ""
        echo "$marker_start"
        echo "$alias_line"
        echo "$marker_end"
    } >> "$rc_file"

    echo "Alias created in $rc_file: $APP_COMMAND"
}

install_project

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists, skipping creation."
fi

echo "Installing dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip --quiet
"$VENV_DIR/bin/pip" install -r "$INSTALL_DIR/requirements.txt"

chmod +x "$INSTALL_DIR/run.sh"
create_launcher
create_alias

echo ""
echo "Installation complete."
echo "Open a new terminal or run 'source $(shell_rc_file)' to use: $APP_COMMAND"
echo ""
echo "Starting $APP_NAME..."
"$LAUNCHER_PATH"
