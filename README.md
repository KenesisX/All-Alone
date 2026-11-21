# ALLALONE — multi-platform build kit

One web app (`www/index.html`), three native targets. Each folder is a
self-contained, build-ready project with its own README and exact commands.

| Target | Folder | Output | Build command |
|--------|--------|--------|---------------|
| Windows | `windows-electron/` | `.exe` installer + portable `.exe` | `npm install && npm run dist` |
| Android | `android-capacitor/` | `.apk` / `.aab` | `npm install && npx cap add android && npx cap sync && npx cap open android` |
| Raspberry Pi | `raspberrypi/` | kiosk (or `.img` via pi-gen) | `./install.sh && sudo reboot` |

## Why source, not pre-built binaries
Compiling a **signed** Windows `.exe`, an Android `.aab`, and a flashable
Pi `.img` requires each platform's toolchain (electron-builder, Android
SDK/Gradle, pi-gen) and **your own signing keys/keystore** — those have to
run on your machines, not in a chat sandbox. These projects produce the
exact binaries when you run the one command per platform.

## Single source of truth
All three load the identical `www/index.html`. To ship an update, replace
that one file in each target's `www/` and rebuild. (They're separate copies
here so each folder is self-contained; symlink them if you prefer.)

## Capability notes
- **Camera / mic / motion / magnetometer / GPS / Web Audio** — work on all
  three (served over a secure context: `file`-app on Electron, internal
  `https://` on Capacitor, `localhost` on the Pi).
- **WebUSB (RTL-SDR direct)** — works on Windows (Electron/Chromium) and
  desktop Chrome; **not** in Android WebView. On Android use the WebSocket
  SDR bridge (SOURCE page) or open the app in Chrome.
- **Downloads** (photos/video/finds export) — Electron and the Pi use the
  normal browser download; the Android WebView uses the same and lands in
  Downloads. The claude.ai artifact build uses the platform download API.

## Auto-build in the cloud (GitHub Actions)
Push this repo to GitHub and the binaries build themselves — no local
toolchain required:
- `.github/workflows/windows.yml` → builds the Windows installer + portable
  `.exe` on `windows-latest`, uploaded as the **ALLALONE-windows** artifact.
- `.github/workflows/android.yml` → generates the Android project, patches
  permissions + WebRTC, builds a debug **APK**, uploaded as
  **ALLALONE-android-apk**.

Both run on every push to `main`/`master` and can be run on demand from the
**Actions** tab (Run workflow). Download the built files from the run's
Artifacts section. A signed release `.aab` stays manual (needs your
keystore) — the android workflow has a comment showing where to wire it in.

```bash
git init && git add . && git commit -m "ALLALONE build kit"
git branch -M main
git remote add origin https://github.com/<you>/allalone.git
git push -u origin main
```

Built for Strikebacktech
