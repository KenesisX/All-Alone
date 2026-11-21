#!/usr/bin/env python3
# Injects a release signingConfig into the generated app build.gradle so
# `./gradlew bundleRelease` / `assembleRelease` produce a SIGNED .aab/.apk.
# Reads credentials from android/key.properties (created by the CI step).
# Idempotent. Run from android-capacitor/ after `npx cap add android`.
import re, pathlib, sys

g = pathlib.Path("android/app/build.gradle")
if not g.exists():
    sys.exit("app build.gradle not found — run `npx cap add android` first.")
t = g.read_text(encoding="utf-8")

load = """def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) { keystoreProperties.load(new FileInputStream(keystorePropertiesFile)) }

"""
if "keystorePropertiesFile" not in t:
    t = re.sub(r"(android\s*\{)", load + r"\1", t, count=1)

sign = """
    signingConfigs {
        release {
            if (rootProject.file("key.properties").exists()) {
                storeFile file(keystoreProperties['storeFile'])
                storePassword keystoreProperties['storePassword']
                keyAlias keystoreProperties['keyAlias']
                keyPassword keystoreProperties['keyPassword']
            }
        }
    }
"""
if "signingConfigs" not in t:
    t = re.sub(r"(android\s*\{)", r"\1\n" + sign, t, count=1)

if "signingConfig signingConfigs.release" not in t:
    t = re.sub(r"(buildTypes\s*\{\s*release\s*\{)",
               r"\1\n            signingConfig signingConfigs.release",
               t, count=1)

g.write_text(t, encoding="utf-8")
print("signing config injected into app/build.gradle")
