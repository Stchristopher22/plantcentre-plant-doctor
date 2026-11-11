# PlantCentre Plant Doctor 🌿

English-language plant identification and plant-health assistant for PlantCentre.

## Project layout
- `web/`: Streamlit web application for plant photo uploads and AI-assisted health checks.
- `android-app/`: Android Studio WebView wrapper that opens the hosted web app.

## Run web app locally
Requires Python 3.10+.
```bash
cd web
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open http://localhost:8501.

## Gemini API key
Create one at https://aistudio.google.com/apikey. For local testing, paste it into the app. For Streamlit Community Cloud, add this under App settings → Secrets:
```toml
GEMINI_API_KEY = "YOUR_KEY"
```
Never commit API keys or secrets files.

## Deploy web app
1. Sign in at https://share.streamlit.io/.
2. Create an app from this repository.
3. Set the main file path to `web/app.py`.
4. Add `GEMINI_API_KEY` in Streamlit Secrets.
5. Deploy and copy the HTTPS app URL.

## Build Android APK
1. Deploy the web app first.
2. Replace `APP_URL` in `android-app/app/src/main/java/com/plantcentre/leafcare/MainActivity.java` with the deployed HTTPS URL.
3. Open `android-app` in Android Studio and sync Gradle.
4. Select Build → Build Bundle(s) / APK(s) → Build APK(s).

The Android folder is source code, not a precompiled or signed APK. Build a release APK in Android Studio before distributing it.

## Features
Plant identification, visible leaf symptom observations, possible disease/pest or environmental causes, risk level, recovery steps, watering, sunlight, soil and prevention guidance.

## Limitations
This is an AI-assisted prototype, not a validated diagnostic tool. A photo alone cannot reliably confirm every disease or pest. Verify high-impact treatments with a horticulture professional. Gemini usage is subject to Google's quotas and pricing.
