#!/usr/bin/env bash
#
# Dell G15 Fn+F9 G-Mode Installer (Poetry Package Manager)
#
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "    Dell G15 Fn+F9 G-Mode Performance Service Installer   "
echo "=========================================================="
echo ""

# 1. Check Python and Poetry
echo "[1/5] Checking dependencies..."
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is required."
    exit 1
fi

if ! command -v poetry &>/dev/null; then
    echo "Error: Poetry is required. Please install poetry via: sudo apt install python3-poetry or pipx install poetry."
    exit 1
fi

# 2. Poetry install
echo "[2/5] Setting up Poetry environment and installing package..."
cd "$SCRIPT_DIR"
poetry install

VENV_PATH="$(poetry env info -p)"
if [ -z "$VENV_PATH" ] || [ ! -d "$VENV_PATH" ]; then
    echo "Error: Failed to locate Poetry virtual environment."
    exit 1
fi

# 3. Create global symlink
echo "[3/5] Installing global dell-gmode executable (requires sudo)..."
sudo ln -sf "$VENV_PATH/bin/dell-gmode" /usr/local/bin/dell-gmode
sudo chmod +x /usr/local/bin/dell-gmode

# 4. Ensure acpi_call module is enabled
echo "[4/5] Ensuring acpi_call kernel module is loaded..."
echo "acpi_call" | sudo tee /etc/modules-load.d/acpi_call.conf >/dev/null || true
sudo modprobe acpi_call 2>/dev/null || true

# 5. Install & start systemd service
echo "[5/5] Enabling and starting systemd service..."
sudo cp "$SCRIPT_DIR/systemd/dell-gmode.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now dell-gmode.service

echo ""
echo "=========================================================="
echo "               Installation Complete!                     "
echo "=========================================================="
echo ""
echo "The Fn+F9 key is now active!"
echo "  • Press Fn+F9 anytime to toggle between Balanced & G-Mode"
echo "  • Or run via CLI: dell-gmode toggle"
echo "                    dell-gmode status"
echo "                    dell-gmode performance"
echo "                    dell-gmode balanced"
echo ""
