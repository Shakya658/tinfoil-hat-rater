
import streamlit as st
import joblib
import requests
import random

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tinfoil Hat Rater",
    page_icon="🎩",
    layout="centered"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Share+Tech+Mono&display=swap');

    html, body, [class*="css"] {
        background-color: #0a0a0a;
        color: #c8b560;
        font-family: 'Share Tech Mono', monospace;
    }
    .main { background-color: #0a0a0a; }
    h1, h2, h3 { 
        font-family: 'Special Elite', cursive;
        color: #c8b560;
        letter-spacing: 2px;
    }
    .stTextArea textarea {
        background-color: #111;
        color: #c8b560;
        border: 1px solid #c8b560;
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
    }
    .stButton > button {
        background-color: #0a0a0a;
        color: #c8b560;
        border: 1px solid #c8b560;
        font-family: 'Special Elite', cursive;
        letter-spacing: 2px;
        width: 100%;
        padding: 12px;
        font-size: 16px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #c8b560;
        color: #0a0a0a;
    }
    .verdict-box {
        border: 1px solid #c8b560;
        padding: 20px;
        margin: 10px 0;
        text-align: center;
        font-family: 'Special Elite', cursive;
    }
    .classified {
        color: #ff3333;
        font-family: 'Special Elite', cursive;
        font-size: 11px;
        letter-spacing: 4px;
        border: 1px solid #ff3333;
        padding: 2px 8px;
        display: inline-block;
    }
    .headline-btn {
        background-color: #111;
        border: 1px solid #333;
        color: #c8b560;
        padding: 8px;
        margin: 4px 0;
        font-size: 12px;
        cursor: pointer;
        width: 100%;
        text-align: left;
    }
    .stProgress > div > div {
        background-color: #c8b560;
    }
    div[data-testid="stDecoration"] { display: none; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("model/tinfoil_pipeline.pkl")

model = load_model()

# ── Fetch conspiracy headlines ─────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_headlines():
    api_key = st.secrets.get("NEWS_API_KEY", "")
    if not api_key:
        return []
    
    queries  = ["conspiracy", "cover up government", "secret society", 
                "deep state", "they dont want you to know"]
    articles = []
    
    for q in queries:
        try:
            r = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q"        : q,
                    "language" : "en",
                    "pageSize" : 5,
                    "sortBy"   : "publishedAt",
                    "apiKey"   : api_key
                },
                timeout=5
            )
            data = r.json()
            if data.get("status") == "ok":
                for a in data.get("articles", []):
                    if a.get("title") and a["title"] != "[Removed]":
                        articles.append(a["title"])
        except:
            pass
    
    return list(set(articles))[:10]  # dedupe, cap at 10

# ── Verdict config ────────────────────────────────────────────────────────────
def get_verdict(score):
    if score < 25:
        return {
            "level"  : "AGENT OF THE SYSTEM",
            "hats"   : "🎩",
            "color"  : "#4CAF50",
            "msg"    : "Suspiciously reasonable. Are you sure you're not one of THEM?",
            "stamp"  : "CREDIBLE"
        }
    elif score < 50:
        return {
            "level"  : "SUSPICIOUS CITIZEN",
            "hats"   : "🎩🎩",
            "color"  : "#FFC107",
            "msg"    : "You're asking questions. They've noticed.",
            "stamp"  : "QUESTIONABLE"
        }
    elif score < 75:
        return {
            "level"  : "AWAKENING",
            "hats"   : "🎩🎩🎩",
            "color"  : "#FF9800",
            "msg"    : "The Rothschilds would like a word. The lizards are watching.",
            "stamp"  : "SUSPICIOUS"
        }
    else:
        return {
            "level"  : "FULL TINFOIL",
            "hats"   : "🎩🎩🎩🎩🎩",
            "color"  : "#FF3333",
            "msg"    : "NASA, the Moon, the Freemasons and Big Pharma all just got a notification.",
            "stamp"  : "CLASSIFIED"
        }

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<span class='classified'>◆ DECLASSIFIED ◆</span>", unsafe_allow_html=True)
st.title("🎩 TINFOIL HAT RATER")
st.markdown("*Analysing the linguistic fingerprints of misinformation since 2024*")
st.markdown("---")

# ── Main input ────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    claim = st.text_area(
        "ENTER CLAIM FOR ANALYSIS:",
        placeholder="e.g. The moon landing was filmed by Stanley Kubrick in a secret studio funded by the Rothschilds...",
        height=120,
        label_visibility="visible"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyse = st.button("⚡ ANALYSE\nCLAIM")

st.markdown("---")

# ── Score display ─────────────────────────────────────────────────────────────
if analyse and claim.strip():
    score   = round(model.predict_proba([claim])[0][1] * 100, 1)
    verdict = get_verdict(score)

    st.markdown(f"""
    <div class="verdict-box" style="border-color: {verdict['color']};">
        <div style="font-size: 40px; margin-bottom: 10px;">{verdict['hats']}</div>
        <div style="color: {verdict['color']}; font-size: 24px; letter-spacing: 4px;">
            {verdict['level']}
        </div>
        <div style="font-size: 48px; color: {verdict['color']}; margin: 10px 0;">
            {score}%
        </div>
        <div style="color: #888; font-size: 13px; font-style: italic;">
            {verdict['msg']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(int(score))

    with st.expander("⚠ WHAT DOES THIS SCORE MEAN?"):
        st.markdown("""
        This model was trained on the **LIAR dataset** — 12,791 statements rated by 
        PolitiFact fact-checkers. It detects **language patterns** associated with 
        misinformation, not actual facts.

        A well-worded lie can score low. A clumsily worded truth can score high.  
        **This is a style detector, not an oracle.**
        """)

# ── Live headlines ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📡 INTERCEPTED TRANSMISSIONS")
st.markdown("*Live conspiracy-adjacent headlines. Click to rate.*")

headlines = fetch_headlines()

if headlines:
    for headline in headlines:
        if st.button(f"▶  {headline}", key=headline):
            score   = round(model.predict_proba([headline])[0][1] * 100, 1)
            verdict = get_verdict(score)
            st.markdown(f"""
            <div class="verdict-box" style="border-color: {verdict['color']}; padding: 10px;">
                {verdict['hats']} &nbsp;
                <span style="color: {verdict['color']};">{verdict['level']}</span> — 
                <strong style="color: {verdict['color']};">{score}%</strong>
            </div>
            """, unsafe_allow_html=True)
else:
    # Fallback hardcoded claims if API key missing or quota hit
    fallbacks = [
        "The moon landing was staged by Stanley Kubrick.",
        "5G towers are being used to control human behaviour.",
        "The Rothschild family controls all central banks.",
        "Chemtrails are being used to modify the weather.",
        "The Freemasons control every major world government.",
        "Birds are not real — they are government surveillance drones.",
    ]
    for claim_ex in fallbacks:
        if st.button(f"▶  {claim_ex}", key=claim_ex):
            score   = round(model.predict_proba([claim_ex])[0][1] * 100, 1)
            verdict = get_verdict(score)
            st.markdown(f"""
            <div class="verdict-box" style="border-color: {verdict['color']}; padding: 10px;">
                {verdict['hats']} &nbsp;
                <span style="color: {verdict['color']};">{verdict['level']}</span> — 
                <strong style="color: {verdict['color']};">{score}%</strong>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#444; font-size:11px; letter-spacing:2px;'>"
    "◆ THEY ARE WATCHING ◆ ALL CLAIMS MONITORED ◆ STAY VIGILANT ◆"
    "</div>",
    unsafe_allow_html=True
)
