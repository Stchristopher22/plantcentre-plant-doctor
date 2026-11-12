# Green Guard AI 🌿
### Created by NextGen Innovators

English-language plant identification and AI-assisted plant-health guide. Upload a plant or leaf photo to receive an initial plant identification, visible symptom observations, possible causes, and practical care suggestions.

## App overview
- **App name:** Green Guard AI
- **Brand:** NextGen Innovators
- **Web app:** Streamlit
- **Android app:** WebView wrapper that opens the hosted web app
- **Language:** English

## Interface
The Green Guard AI interface uses a botanical green theme with:
- A welcome banner with gently floating leaf decorations.
- Soft green backgrounds and rounded glass-style report cards.
- Separate report sections for plant identification, health status, possible disease or pests, visible symptoms, possible causes, recovery/treatment, prevention, watering, sunlight, and soil/drainage guidance.
- A responsive layout for mobile and desktop screens.

## Project layout
- `web/`: Streamlit application for plant photo uploads and AI-assisted health checks.
- `android-app/`: Android WebView wrapper that opens the hosted web app.
- `.github/workflows/build-android-apk.yml`: GitHub Actions workflow for building the Android APK online.

## Run the web app locally
Requires Python 3.10+.

```bash
cd web
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501.

## Gemini API key
Create an API key at https://aistudio.google.com/apikey.

For local testing, enter the key in the app when prompted. For Streamlit Community Cloud, open the app's **Settings → Secrets** and add:

```toml
GEMINI_API_KEY = "YOUR_ACTUAL_KEY"
```

Never commit API keys or secrets files to GitHub. Do not share the key in screenshots or chat messages.

## Deploy the web app
1. Sign in at https://share.streamlit.io/.
2. Connect this GitHub repository.
3. Set the main file path to `web/app.py`.
4. Add `GEMINI_API_KEY` in Streamlit Secrets.
5. Deploy the app and confirm that the HTTPS URL opens.
6. The Android wrapper is configured to open the hosted Green Guard AI web app.

Hosted app: https://greenguardai-plant-doctor-5u5wthgerynsptchjeqmuv.streamlit.app/

## Build the Android APK online (no Android Studio required)
The repository includes a GitHub Actions workflow.

1. Open the repository's **Actions** tab.
2. Select **Build NextGen Innovators Android APK**.
3. Open the latest workflow run. A push to the Android app or workflow files also triggers a build.
4. Wait for the workflow to complete successfully.
5. Open the completed run and find **Artifacts**.
6. Download **Green-Guard-AI-APK** and extract the ZIP file.
7. The APK file inside is named `Green-Guard-AI.apk`.
8. Transfer it to an Android phone and install it. Android may ask you to allow installation from that source.

The workflow currently creates a debug APK for testing. A signed release APK is needed before publishing or distributing the app broadly. Test installation and photo upload on a real phone first.

## How the app works
1. The user selects a JPG, JPEG, PNG, or WEBP plant photo.
2. The app sends the photo and an analysis prompt to the Gemini API.
3. Gemini returns a structured plant-care report.
4. Green Guard AI displays the report in separate visual cards.
5. The user reviews the suggested care steps and, where necessary, checks with a horticulture professional.

## Features
- Plant name and scientific name suggestions.
- Identification confidence.
- Visible leaf and plant symptom observations.
- Health status and risk level.
- Possible disease, pest, or environmental causes.
- Recovery and treatment suggestions.
- Watering, sunlight, soil, and drainage guidance.
- Prevention tips and advice on when to seek expert help.

## Limitations and responsible use
This is an AI-assisted prototype, not a validated diagnostic tool. A photo alone cannot reliably confirm every disease or pest, and similar symptoms can have different causes. Treat the report as an initial guide, inspect the plant and growing conditions, and verify high-impact treatments with a qualified horticulture professional. Gemini usage is subject to Google's quotas and pricing.

The Android app is a WebView wrapper, not an offline plant-diagnosis model. It needs an internet connection and the hosted web app must be available. Plant photos are sent to Google Gemini when the user requests an analysis.

## Future improvements
Possible next versions could include saved plant reports, progress-photo comparisons, Tamil language support, plant-care reminders, and a plant reference library.

---
**Green Guard AI · by NextGen Innovators**
