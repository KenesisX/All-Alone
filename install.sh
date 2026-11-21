#!/usr/bin/env bash
# ALLALONE — Raspberry Pi kiosk installer.
# Run on Raspberry Pi OS (Bookworm, 64-bit, Desktop) as the `pi` user.
set -e

echo "[ALLALONE] installing dependencies…"
sudo apt-get update
sudo apt-get install -y chromium-browser unclutter python3 || \
  sudo apt-get install -y chromium unclutter python3

APPDIR="$HOME/allalone"
echo "[ALLALONE] installing app to $APPDIR"
mkdir -p "$APPDIR"
cp -r "$(dirname "$0")/www" "$APPDIR/"
cp "$(dirname "$0")/run.sh" "$APPDIR/"
chmod +x "$APPDIR/run.sh"

echo "[ALLALONE] installing kiosk service…"
sudo cp "$(dirname "$0")/allalone-kiosk.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable allalone-kiosk.service

echo
echo "[ALLALONE] done. Reboot to launch the kiosk:  sudo reboot"
echo "Camera/mic need a Pi Camera or USB webcam attached."
