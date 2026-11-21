#!/usr/bin/env bash
# ALLALONE kiosk launcher — serves the app on localhost (a secure context,
# so camera/mic work) and opens Chromium full-screen.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR/www"

# Static server on localhost:8080 (localhost = secure context for getUserMedia)
python3 -m http.server 8080 --bind 127.0.0.1 &
SERVER_PID=$!
trap "kill $SERVER_PID 2>/dev/null" EXIT
sleep 2

# Prefer chromium-browser, fall back to chromium
BROWSER="$(command -v chromium-browser || command -v chromium)"
"$BROWSER" \
  --kiosk \
  --noerrdialogs \
  --disable-infobars \
  --disable-session-crashed-bubble \
  --autoplay-policy=no-user-gesture-required \
  --use-fake-ui-for-media-stream \
  --enable-features=WebBluetooth \
  "http://localhost:8080/index.html"
