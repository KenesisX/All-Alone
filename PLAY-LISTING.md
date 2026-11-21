# ALLALONE — Google Play listing kit

## Ready-made assets (this folder)
| File | Use | Play requirement |
|------|-----|------------------|
| `play-icon-512.png` | App icon | 512×512, 32-bit PNG, no transparency ✔ |
| `feature-graphic-1024x500.png` | Feature graphic | 1024×500 PNG/JPG ✔ |
| `icon-1024.png` | Master (marketing / web) | — |

You still need **2–8 phone screenshots** (min 1080px, 16:9 or 9:16). Easiest:
open ALLALONE on an Android phone and screenshot the Radar, Scope, Compass,
Sky, and SOS pages.

## Listing text (paste into Play Console)

**App name (30 chars max):**
```
ALLALONE Sensor Suite
```

**Short description (80 chars max):**
```
Radar, scope, compass, SDR, sky & backcountry SOS — one sensor command suite.
```

**Full description:**
```
ALLALONE turns your phone into a field sensor command suite.

• RADAR — real camera motion detection, sized from small animal to human, with live tracking
• SCOPE — digital zoom, reticles, filters (thermal, night, multispectral), photo capture + editor, video record
• COMPASS — tilt-perspective dial with live heading and sun position
• SKY — point up for sun, sunrise/sunset, bright stars and geostationary satellites
• SOUND / WATERFALL / SONAR — live audio FFT, spectrogram and acoustic ping
• EMF — real magnetometer field + anomaly detection
• SDR BRIDGE — connect an RTL-SDR / HackRF / Raspberry Pi backend over WebSocket
• FIELD ID — offline feature keys for tracks, rocks, berries, plants and wildlife + GPS finds log
• DETERRENT — wildlife noisemaker with species guidance
• SOS — GPS emergency beacon with map link, all-clear and test modes, radio-code reference

Built for makers, hikers, and field operators. Many features use your device
sensors; others connect to your own radio hardware.

Note on physics: a phone has no thermal or radiation sensor, so "thermal" is a
visual filter and "heat-trail" is motion persistence. RF and CSI features need
your own SDR hardware via the bridge. ALLALONE does not detect lies, diagnose
illness, or measure blood pressure.
```

## Data safety (declare in Console)
- **Camera** — motion detection, scope, capture (on-device; not sent anywhere by the app).
- **Microphone** — audio analysis / recordings (on-device).
- **Location** — weather, sky, finds log, SOS message. Shared only when YOU
  send an SOS/finds message yourself.
- No analytics/ads SDKs are bundled.

## Content rating
Complete the IARC questionnaire. The wildlife deterrent and SOS are utility
features; there is no violence, gambling, or user-to-user content in the app
itself.
