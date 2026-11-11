# Android APK wrapper

1. Deploy the web app first using the root README instructions.
2. Replace `APP_URL` in `app/src/main/java/com/plantcentre/leafcare/MainActivity.java` with your real HTTPS Streamlit URL.
3. Open the `android-app` folder in Android Studio and allow Gradle sync.
4. Select **Build → Build Bundle(s) / APK(s) → Build APK(s)**.
5. Android Studio will show the APK output location.

This is Android Studio source, not a precompiled APK. The hosted HTTPS app is required; localhost on your computer is not reachable from a phone by default. Sign a release build before public distribution.
