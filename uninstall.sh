#!/usr/bin/env bash
#
# Dell G15 Fn+F9 G-Mode Uninstaller
#
set -e

echo "Uninstalling Dell G15 G-Mode Service..."

if systemctl is-active --quiet dell-gmode.service 2>/dev/null; then
    sudo systemctl stop dell-gmode.service || true
fi

if systemctl is-enabled --quiet dell-gmode.service 2>/dev/null; then
    sudo systemctl disable dell-gmode.service || true
fi

sudo rm -f /etc/systemd/system/dell-gmode.service
sudo systemctl daemon-reload

sudo rm -f /usr/local/bin/dell-gmode

echo "Dell G-Mode service has been uninstalled."
