import streamlit as st
import requests
import json
import base64
import html

st.set_page_config(page_title="Green Guard AI", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root { --leaf:#276749; --deep:#153e2d; --mint:#e8f5ec; }
.stApp { background: radial-gradient(circle at 10% 5%,#e7f5e9 0,transparent 30%), linear-gradient(150deg,#f7fbf7,#edf5ef 55%,#f8faf7); }
.block-container {max-width:900px;padding-top:1.5rem;padding-bottom:3rem}
html, body, [class*="css"] {font-family:'DM Sans',sans-serif}
.pc-hero {position:relative;overflow:hidden;padding:30px 28px;border-radius:26px;background:linear-gradient(125deg,rgba(20,75,48,.96),rgba(48,117,75,.88));border:1px solid rgba(255,255,255,.35);box-shadow:0 18px 45px rgba(27,74,49,.18);color:white;margin-bottom:18px}
.pc-hero h1 {font-family:'Playfair Display',serif;color:#fff;margin:0;font-size:2.65rem;letter-spacing:-.7px}
.pc-hero p {color:#e1f3e5;margin:8px 0 0;font-size:1rem}
.pc-kicker {font-size:.72rem;letter-spacing:2px;text-transform:uppercase;color:#c8e6ce;font-weight:700;margin-bottom:9px}
.pc-leaf {position:absolute;font-size:38px;opacity:.82;filter:drop-shadow(0 8px 12px #0b2d1c55);animation:leafFloat 5s ease-in-out infinite}
.leaf-a {right:12%;top:17%;animation-delay:0s}.leaf-b {right:27%;bottom:12%;font-size:25px;animation-delay:1.4s}.leaf-c {right:5%;bottom:18%;font-size:20px;animation-delay:2.1s}
@keyframes leafFloat {0%,100%{transform:translate3d(0,0,0) rotate(-8deg)}50%{transform:translate3d(9px,-15px,0) rotate(13deg)}}
.pc-section {font-weight:800;color:#1d4932;font-size:1.12rem;margin:22px 0 10px}
.pc-glass {background:rgba(255,255,255,.66);border:1px solid rgba(255,255,255,.88);border-radius:20px;padding:17px 19px;margin:10px 0;box-shadow:0 10px 28px rgba(36,74,49,.08);backdrop-filter:blur(14px);transition:transform .25s ease,box-shadow .25s ease;animation:cardIn .55s ease both}
.pc-glass:hover {transform:translateY(-3px);box-shadow:0 15px 34px rgba(36,74,49,.13)}
@keyframes cardIn {from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.pc-label {font-size:.75rem;text-transform:uppercase;letter-spacing:1.2px;color:#64816d;font-weight:700}
.pc-value {font-size:1.2rem;color:#173f2b;font-weight:800;margin-top:4px}
.pc-chip {display:inline-block;background:#e2f3e7;color:#24613b;border-radius:999px;padding:5px 11px;font-size:.8rem;font-weight:700;margin:4px 5px 0 0}
div[data-testid="stVerticalBlockBorderWrapper"] {background:rgba(255,255,255,.62);border:1px solid rgba(255,255,255,.9);border-radius:20px;box-shadow:0 8px 25px rgba(36,74,49,.07);backdrop-filter:blur(12px)}
div.stButton>button {background:linear-gradient(120deg,#276749,#39875b);color:white;border:0;border-radius:14px;min-height:48px;font-weight:700;box-shadow:0 7px 16px rgba(39,103,73,.2);transition:transform .2s ease}
div.stButton>button:hover {background:linear-gradient(120deg,#1e563b,#2f754d);transform:translateY(-2px);color:white}
[data-testid="stFileUploader"] {background:rgba(255,255,255,.58);border:1px dashed #8ab69a;border-radius:18px;padding:10px}
.stAlert {border-radius:16px}
footer {visibility:hidden}
@media(max-width:600px){.pc-hero{padding:24px 20px}.pc-hero h1{font-size:2.1rem}.pc-leaf{font-size:26px}}
</style>
""", unsafe_allow_html=True)

def get_secret_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""

st.markdown("""
<div class="pc-hero">
  <div class="pc-kicker">NextGen Innovators presents</div>
  <h1>Green Guard AI 🌿</h1>
  <p>A little care, a healthier plant. Identify, understand and nurture your green friends.</p>
  <span class="pc-leaf leaf-a">🍃</span><span class="pc-leaf leaf-b">🌿</span><span class="pc-leaf leaf-c">🍃</span>
</div>
""", unsafe_allow_html=True)
st.write("Upload a clear photo of a plant or leaf. Green Guard AI will help identify visible symptoms and suggest practical care steps.")
st.caption("English • Created by NextGen Innovators")

api_key = get_secret_key()
if not api_key:
    api_key = st.text_input("Gemini API key", type="password", help="For local testing. For hosted deployment, set GEMINI_API_KEY in Streamlit Secrets.")

photo = st.file_uploader("Choose a plant or leaf photo", type=["jpg", "jpeg", "png", "webp"])
if photo:
    st.image(photo, caption="Your uploaded plant photo", use_container_width=True)
    if st.button("🌱  Analyse my plant", use_container_width=True):
        if not api_key:
            st.error("Add a Gemini API key to enable image analysis.")
        else:
            prompt = """Act as a cautious horticulture assistant for home gardeners in Chennai, India. Analyse this image and return ONLY valid JSON with these keys:
plant_name, scientific_name, identification_confidence, health_status, visible_symptoms, possible_causes, likely_disease_or_pest, risk_level, recovery_plan, watering, sunlight, soil_and_drainage, prevention, expert_help, uncertainty.
Use plain English. Arrays for visible_symptoms, possible_causes, recovery_plan, prevention. Distinguish visible observations from possible explanations. If unclear, say so. Do not claim a definite disease from a photo alone. Consider overwatering, underwatering, heat/sun scorch, nutrient issues, pests and fungal/bacterial diseases. Give safe practical steps. Avoid chemical pesticides unless necessary; if mentioned, advise following product label and local rules. Tailor general advice to warm, humid Chennai conditions where relevant."""
            try:
                with st.spinner("🍃 Green Guard AI is checking your plant..."):
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
                    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"
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
    st.markdown('<div class="pc-section">🌿 Your plant care report</div>', unsafe_allow_html=True)
    plant_name = html.escape(str(report.get("plant_name", "Not identified")))
    scientific = html.escape(str(report.get("scientific_name", "Not specified")))
    confidence = html.escape(str(report.get("identification_confidence", "Unclear")))
    status = html.escape(str(report.get("health_status", "Unclear")))
    risk = html.escape(str(report.get("risk_level", "Unclear")))
    disease = html.escape(str(report.get("likely_disease_or_pest", "Cannot determine")))
    st.markdown(f'<div class="pc-glass"><div class="pc-label">Plant identification</div><div class="pc-value">{plant_name}</div><i>{scientific}</i><div class="pc-chip">Confidence: {confidence}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pc-glass"><div class="pc-label">Health status</div><div class="pc-value">🩺 {status}</div><div class="pc-chip">Risk: {risk}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pc-glass"><div class="pc-label">Possible disease or pest</div><div class="pc-value">🔎 {disease}</div></div>', unsafe_allow_html=True)

    sections = [
        ("👀", "Visible symptoms", "visible_symptoms"),
        ("🧩", "Possible causes", "possible_causes"),
        ("🛟", "Recovery and treatment", "recovery_plan"),
        ("🛡️", "Prevention", "prevention")
    ]
    for icon, heading, key in sections:
        values = report.get(key, [])
        if not isinstance(values, list):
            values = [str(values)] if values else []
        items = "".join(f"<li>{html.escape(str(value))}</li>" for value in values) or "<li>No information available.</li>"
        st.markdown(f'<div class="pc-glass"><div class="pc-section">{icon} {heading}</div><ul>{items}</ul></div>', unsafe_allow_html=True)

    care_items = [
        ("💧 Watering", "watering"),
        ("☀️ Sunlight", "sunlight"),
        ("🪴 Soil and drainage", "soil_and_drainage"),
        ("🧑‍🌾 When to contact a plant expert", "expert_help")
    ]
    for heading, key in care_items:
        value = html.escape(str(report.get(key, "Not specified")))
        st.markdown(f'<div class="pc-glass"><div class="pc-label">{heading}</div><div style="color:#234a34;margin-top:7px">{value}</div></div>', unsafe_allow_html=True)

    if report.get("uncertainty"):
        st.info(str(report["uncertainty"]))
    st.warning("AI photo analysis is an initial guide, not a confirmed diagnosis. Similar problems can look alike. Check leaf undersides, stems, soil moisture and recent care changes. Consult a horticulture professional for valuable or rapidly declining plants.")

st.divider()
st.markdown("<div style='text-align:center;color:#54725c;font-weight:700'>Green Guard AI · by NextGen Innovators</div>", unsafe_allow_html=True)
st.caption("Photo analysis is sent to Google Gemini when you request a check. Do not upload personal or sensitive images. API usage may be subject to Google's quotas and pricing.")
