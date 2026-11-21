#!/usr/bin/env bash
# ALLALONE — build a SIGNED Google Play .aab locally.
#
# Requires on your machine:
#   - Node.js 18+ and npm
#   - JDK 17
#   - Android SDK (Android Studio installed, or ANDROID_SDK_ROOT set)
#   - your signing keystore
#
# Usage:
#   KEYSTORE=~/allalone.keystore KS_PASS=... KEY_ALIAS=allalone KEY_PASS=... ./build-aab.sh
set -e
cd "$(dirname "$0")"

: "${KEYSTORE:?set KEYSTORE=/path/to/allalone.keystore}"
: "${KS_PASS:?set KS_PASS=store password}"
: "${KEY_ALIAS:?set KEY_ALIAS=key alias}"
: "${KEY_PASS:?set KEY_PASS=key password}"

echo "[ALLALONE] installing deps…"
npm install

[ -d android ] || npx cap add android
python3 scripts/patch-android.py           # permissions + WebRTC + icons

echo "[ALLALONE] configuring signing…"
cp "$KEYSTORE" android/app/allalone.keystore
cat > android/key.properties <<EOF
storeFile=allalone.keystore
storePassword=$KS_PASS
keyAlias=$KEY_ALIAS
keyPassword=$KEY_PASS
EOF
python3 scripts/patch-signing.py

npx cap sync android

echo "[ALLALONE] building release bundle…"
cd android
chmod +x gradlew
./gradlew bundleRelease

echo
echo "✅ Signed AAB ready:"
echo "   android-capacitor/android/app/build/outputs/bundle/release/app-release.aab"
echo "Upload that file to Google Play Console."
