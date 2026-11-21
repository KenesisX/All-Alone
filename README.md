# ALLALONE — Galaxy Watch / Wear OS companion

`watch.html` is a round-screen companion: swipe (tap left/right half) between
**Heading · GPS · SOS · Medical ID**. It's intentionally tiny and offline.

## Fastest: run it on the watch
Modern Galaxy Watches run **Wear OS** with a browser. Host `watch.html`
anywhere the watch can reach (even the ESP32 AP or your phone) and open it,
or wrap it in a minimal Wear OS WebView app (below).

## Wrap as a real Wear OS app (Android Studio)
1. New Project ▸ **Wear OS** ▸ Empty Activity.
2. Add a full-screen `WebView` to the activity layout.
3. In code: `webView.settings.javaScriptEnabled = true` and
   `webView.loadUrl("file:///android_asset/watch.html")`.
4. Put `watch.html` in `app/src/main/assets/`.
5. Add permissions in the manifest: `INTERNET`, `ACCESS_FINE_LOCATION`,
   `BODY_SENSORS`. Build ▸ APK, install to the watch.

## Honest notes
- A native **tile / complication** (the at-a-glance watch-face widget) needs
  the Wear Tiles API in Kotlin — not doable from HTML. The WebView app above
  gives you the full companion screen; tiles are a follow-on.
- The Medical ID screen reads the same `sv_medid` the main app saves, but
  **only if they share a browser/storage** (e.g. both opened on the watch).
  For cross-device sync you'd point both at your bridge. On its own the watch
  companion is standalone — re-enter Medical info on the watch if needed.
