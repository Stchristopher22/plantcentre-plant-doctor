import streamlit as st
import requests
import json
import base64

st.set_page_config(page_title="PlantCentre Plant Doctor", page_icon="🌿", layout="centered")
st.markdown("""
<style>
.block-container {max-width:880px;padding-top:1.6rem;padding-bottom:3rem}
.pc-hero {background:linear-gradient(135deg,#e8f5e9,#f4f8ed);padding:24px;border-radius:18px;border:1px solid #d7e8d5}
.pc-hero h1 {color:#1b5e20;margin:0;font-size:2rem}
.pc-hero p {color:#45624a;margin:.35rem 0 0}
div.stButton>button {background:#236b35;color:white;border:0;border-radius:12px;min-height:46px}
</style>
""", unsafe_allow_html=True)

def get_secret_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""

st.markdown('<div class="pc-hero"><h1>🌿 PlantCentre Plant Doctor</h1><p>Identify your plant. Check visible symptoms. Learn how to care for it.</p></div>', unsafe_allow_html=True)
st.write("Upload a clear photo of a plant or leaf. Use natural light, focus on the affected area, and include the whole plant when possible.")
st.caption("English • PlantCentre project prototype")

api_key = get_secret_key()
if not api_key:
    api_key = st.text_input("Gemini API key", type="password", help="For local testing. For hosted deployment, set GEMINI_API_KEY in Streamlit Secrets.")

photo = st.file_uploader("Choose a plant or leaf photo", type=["jpg", "jpeg", "png", "webp"])
if photo:
    st.image(photo, caption="Uploaded plant photo", use_container_width=True)
    if st.button("Check plant health", use_container_width=True):
        if not api_key:
            st.error("Add a Gemini API key to enable image analysis.")
        else:
            prompt = """Act as a cautious horticulture assistant for home gardeners in Chennai, India. Analyse this image and return ONLY valid JSON with these keys:
plant_name, scientific_name, identification_confidence, health_status, visible_symptoms, possible_causes, likely_disease_or_pest, risk_level, recovery_plan, watering, sunlight, soil_and_drainage, prevention, expert_help, uncertainty.
Use plain English. Arrays for visible_symptoms, possible_causes, recovery_plan, prevention. Distinguish visible observations from possible explanations. If unclear, say so. Do not claim a definite disease from a photo alone. Consider overwatering, underwatering, heat/sun scorch, nutrient issues, pests and fungal/bacterial diseases. Give safe practical steps. Avoid chemical pesticides unless necessary; if mentioned, advise following product label and local rules. Tailor general advice to warm, humid Chennai conditions where relevant."""
            try:
                with st.spinner("PlantCentre Plant Doctor is analysing your photo..."):
                    body = {
                        "contents": [{"parts": [
                            {"text": prompt},
                            {"inline_data": {
                                "mime_type": photo.type or "image/jpeg",
                                "data": base64.b64encode(photo.getvalue()).decode("ascii")
                            }}
                        ]}],
                        "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
                    }
                    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
                    response = requests.post(endpoint, params={"key": api_key}, json=body, timeout=90)
                    response.raise_for_status()
                    result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    st.session_state["plant_report"] = json.loads(result_text)
            except requests.HTTPError as exc:
                st.error(f"AI service returned HTTP {exc.response.status_code}. Check your API key, quota and model access.")
            except Exception as exc:
                st.error(f"Analysis could not be completed: {exc}")

report = st.session_state.get("plant_report")
if report:
    st.divider()
    st.header("Your plant health report")
    st.subheader("🌱 Plant identification")
    st.write(f"**Plant:** {report.get('plant_name', 'Not identified')}")
    if report.get("scientific_name"):
        st.write(f"**Scientific name:** {report['scientific_name']}")
    st.caption(f"Identification confidence: {report.get('identification_confidence', 'Unclear')}")
    st.subheader("🩺 Health assessment")
    st.write(f"**Status:** {report.get('health_status', 'Unclear')}")
    st.write(f"**Risk level:** {report.get('risk_level', 'Unclear')}")
    st.write(f"**Possible disease or pest:** {report.get('likely_disease_or_pest', 'Cannot determine')}")
    for heading, key in [
        ("Visible symptoms", "visible_symptoms"),
        ("Possible causes", "possible_causes"),
        ("Recovery plan", "recovery_plan"),
        ("Prevention", "prevention")
    ]:
        st.subheader(heading)
        values = report.get(key, [])
        if isinstance(values, list):
            for index, value in enumerate(values, 1):
                st.write(f"{index}. {value}")
        else:
            st.write(values or "No information available.")
    for heading, key in [
        ("Watering", "watering"), ("Sunlight", "sunlight"),
        ("Soil and drainage", "soil_and_drainage"),
        ("When to contact a plant expert", "expert_help")
    ]:
        st.markdown(f"**{heading}:** {report.get(key, 'Not specified')}")
    if report.get("uncertainty"):
        st.info(report["uncertainty"])
    st.warning("AI photo analysis is an initial guide, not a confirmed diagnosis. Similar problems can look alike. Check leaf undersides, stems, soil moisture and recent care changes. Consult a horticulture professional for valuable or rapidly declining plants.")

st.divider()
st.markdown("**PlantCentre** · Plant care made simpler")
st.caption("Photo analysis is sent to Google Gemini when you request a check. Do not upload personal or sensitive images. API usage may be subject to Google's quotas and pricing.")
