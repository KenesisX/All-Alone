# ALLALONE — Windows (.exe)

Electron wrapper around the ALLALONE web app. Builds an installer (`.exe`)
and a portable `.exe`.

## Prerequisites
- Node.js 18+ and npm (https://nodejs.org)
- Windows 10/11 to build the Windows target (electron-builder can also
  cross-build from macOS/Linux with Wine, but building **on Windows** is
  the least-friction path).

## Build
```bat
cd windows-electron
npm install
npm run dist
```
Output lands in `dist\`:
- `ALLALONE Setup 1.0.0.exe`  (NSIS installer)
- `ALLALONE 1.0.0.exe`        (portable, no install)

## Run without building (dev)
```bat
npm install
npm start
```

## Camera / mic note
`main.js` auto-grants camera, microphone and geolocation to the bundled
app. On first use Windows itself may still ask you to allow **desktop apps**
to use the camera/mic under *Settings → Privacy & security → Camera/Microphone*.

## Icon
Drop a `build\icon.ico` (256×256) to brand the installer and window.
Without one, Electron's default icon is used.

## Updating the app
The entire UI is `www\index.html`. Replace that one file with a newer
export and rebuild — nothing else changes.
