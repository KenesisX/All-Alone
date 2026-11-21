# ALLALONE — signed releases & tagging

`.github/workflows/release.yml` runs when you push a **tag** that starts with
`v` (e.g. `v1.0.0`). It builds the Windows `.exe`, builds the Android app,
and creates a **GitHub Release** with all binaries attached + auto-generated
notes.

- If the Android signing secrets are set → it builds a **signed `.aab` + `.apk`**.
- If they're absent → it falls back to an **unsigned debug `.apk`** (so the
  release still succeeds).

## One-time: create a keystore
```bash
keytool -genkey -v -keystore allalone.keystore \
  -alias allalone -keyalg RSA -keysize 2048 -validity 10000
# remember the store password, alias, and key password
base64 -w0 allalone.keystore > allalone.keystore.b64   # (macOS: base64 -i allalone.keystore)
```
Keep `allalone.keystore` safe and OUT of git — losing it means you can't
update a Play listing.

## One-time: add repo secrets
GitHub repo ▸ **Settings ▸ Secrets and variables ▸ Actions ▸ New secret**:

| Secret | Value |
|--------|-------|
| `ANDROID_KEYSTORE_BASE64` | contents of `allalone.keystore.b64` |
| `ANDROID_KEYSTORE_PASSWORD` | your store password |
| `ANDROID_KEY_ALIAS` | `allalone` (or your alias) |
| `ANDROID_KEY_PASSWORD` | your key password |

## Cut a release
```bash
git tag v1.0.0
git push origin v1.0.0
```
Watch **Actions** → when it finishes, the **Releases** page has
`ALLALONE Setup *.exe`, the portable `.exe`, the signed `.aab`, and `.apk`
attached. Upload the `.aab` to Google Play.

(The per-push `windows.yml` / `android.yml` workflows still give you quick
test builds on every commit; `release.yml` is only for tagged releases.)
