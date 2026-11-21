#!/usr/bin/env python3
# Injects runtime permissions into the generated AndroidManifest.xml and
# swaps in the WebRTC-granting MainActivity. Idempotent — safe to re-run.
# Run from the android-capacitor/ directory AFTER `npx cap add android`.
import re, pathlib, sys

base = pathlib.Path("android/app/src/main")
man = base / "AndroidManifest.xml"
if not man.exists():
    sys.exit("AndroidManifest.xml not found — run `npx cap add android` first.")

perms = """
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.HIGH_SAMPLING_RATE_SENSORS" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.sensor.compass" android:required="false" />
    <uses-feature android:name="android.hardware.sensor.accelerometer" android:required="false" />
    <uses-feature android:name="android.hardware.location.gps" android:required="false" />
"""

text = man.read_text(encoding="utf-8")
if "android.permission.CAMERA" not in text:
    text = re.sub(r"(<manifest[^>]*>)", r"\1" + perms, text, count=1)
    man.write_text(text, encoding="utf-8")
    print("manifest: permissions added")
else:
    print("manifest: permissions already present")

mact = base / "java/tech/strikeback/allalone/MainActivity.java"
snippet = pathlib.Path("MainActivity-webrtc-snippet.java")
if mact.exists() and snippet.exists():
    mact.write_text(snippet.read_text(encoding="utf-8"), encoding="utf-8")
    print("MainActivity: WebRTC grant installed")
else:
    print("MainActivity: left as default (snippet or target missing)")

# ---- launcher icons ----
import shutil
icons = pathlib.Path("icons/res")
res = base / "res"
if icons.exists():
    # remove Capacitor/AGP default .webp launcher icons so our PNGs don't
    # collide (duplicate resource) with them.
    for mp in res.glob("mipmap-*"):
        for n in ("ic_launcher.webp", "ic_launcher_round.webp", "ic_launcher_foreground.webp"):
            f = mp / n
            if f.exists():
                f.unlink()
    for src in icons.rglob("*"):
        if src.is_file():
            dst = res / src.relative_to(icons)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    print("icons: ALLALONE launcher icons installed")
else:
    print("icons: none found (icons/res missing) — default icon kept")
