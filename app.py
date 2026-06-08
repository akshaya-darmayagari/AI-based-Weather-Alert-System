import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import google.generativeai as genai
import joblib

if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_key" not in st.session_state:
    st.session_state.chat_key = 0

st.set_page_config(page_title="AI Weather Alert System", layout="wide")

WEATHER_API_KEY = "6f52153195a7db5e7301ebacc675093f"
# MY_GEMINI_KEY   = "AIzaSyCJioFh39s7J9Ps4Y69rgIm3otRcB8Z2N8"
MY_GEMINI_KEY   = "AIzaSyCUS-Z_Vuc0wQmbMpjKUTdzK1A9XPNy-Cg"
rf_model = joblib.load("weather_model.pkl")

# Custom SVGs for Chat Avatars (Boxes with Face and Smart Toy)
USER_AVATAR = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' fill='%23ea580c' rx='4'/%3E%3Cpath fill='white' d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8 0-.29.02-.58.05-.86 2.36-1.05 4.23-2.98 5.21-5.37C11.07 8.33 14.05 10 17.42 10c.78 0 1.53-.09 2.25-.26.21.71.33 1.47.33 2.26 0 4.41-3.59 8-8 8zm-3-8.25c-.69 0-1.25.56-1.25 1.25s.56 1.25 1.25 1.25 1.25-.56 1.25-1.25-.56-1.25-1.25-1.25zm6 0c-.69 0-1.25.56-1.25 1.25s.56 1.25 1.25 1.25 1.25-.56 1.25-1.25-.56-1.25-1.25-1.25z'/%3E%3C/svg%3E"
AI_AVATAR = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' fill='%23dc2626' rx='4'/%3E%3Cpath fill='white' d='M20 9V7c0-1.1-.9-2-2-2h-3c0-1.66-1.34-3-3-3S9 3.34 9 5H6c-1.1 0-2 .9-2 2v2c-1.66 0-3 1.34-3 3s1.34 3 3 3v4c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-4c1.66 0 3-1.34 3-3s-1.34-3-3-3zm-2 10H6V7h12v12zm-9-6c-.83 0-1.5-.67-1.5-1.5S8.17 10 9 10s1.5.67 1.5 1.5S9.83 13 9 13zm7.5-1.5c0 .83-.67 1.5-1.5 1.5s-1.5-.67-1.5-1.5.67-1.5 1.5-1.5 1.5.67 1.5 1.5zM8 15h8v2H8v-2z'/%3E%3C/svg%3E"

try:
    genai.configure(api_key=MY_GEMINI_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction="""You are a Weather Lifestyle Assistant.
RULES:
- If the user has NOT asked a specific question, ONLY respond with:
  "How can I assist you today? Do you need suggestions related to clothing, health, or travel?"
- Give weather-based advice ONLY when the user explicitly asks.
- Keep answers short and friendly."""
    )
except Exception as e:
    st.error(f"AI Config Error: {e}")

def weather_chatbot(question, city, temp, humidity, risk, description):
    context = f"Weather for {city}: {temp}°C, {humidity}% humidity, Risk: {risk}, Condition: {description}."
    try:
        response = model.generate_content(f"{context} User: {question}")
        return response.text
    except Exception as e:
        return f"Chatbot Error: {e}"

def predict_risk_rf(temp, humidity, pressure, wind_speed):
    input_df = pd.DataFrame([{"temp": temp, "humidity": humidity, "pressure": pressure, "wind_speed": wind_speed}])
    return rf_model.predict(input_df)[0]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

.stApp { background: linear-gradient(135deg, #87CEEB 0%, #9AE6B4 100%); color: #0f172a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }

/* ── KILL ALL GHOST/EMPTY STREAMLIT WRAPPERS ── */
.stMarkdown:empty,
div[data-testid="stVerticalBlock"] > div:empty,
.element-container:has(> .stMarkdown:empty) { display: none !important; }

/* ══════════════════════════════════════
   HERO HEADER — clean flat professional
   ══════════════════════════════════════ */
.hero-wrap { padding: 8px 0 0; text-align: center; }

.hero-title {
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    letter-spacing: -1.4px;
    line-height: 1.05;
    margin: 0 !important;
    color: #0f172a;
    display: block;
}

.hero-caption {
    font-size: 0.88rem;
    font-weight: 500;
    color: rgba(15,23,42,0.52);
    margin: 6px 0 0 !important;
    letter-spacing: 0.01em;
}

.header-divider {
    border: none; height: 2.5px; margin: 14px 0 18px;
    background: linear-gradient(90deg,
        #6366f1 0%, #8b5cf6 30%, #06b6d4 65%, transparent 100%);
    border-radius: 2px;
    opacity: 0.55;
}

/* ── NAV BUTTONS ── */
.stButton > button {
    border-radius: 12px !important;
    font-size: 0.875rem !important; font-weight: 700 !important;
    height: 44px !important; padding: 0 22px !important;
    border: none !important; width: 100% !important;
    transition: all 0.22s ease !important;
    letter-spacing: 0.02em !important;
    white-space: nowrap !important;
}

/* Sign Up — solid indigo */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton:first-child > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #fff !important;
    box-shadow: 0 4px 18px rgba(99,102,241,0.42) !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton:first-child > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 26px rgba(99,102,241,0.58) !important;
}

/* Update — outlined / ghost */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton:last-child > button {
    background: rgba(255,255,255,0.7) !important;
    color: #4338ca !important;
    border: 2px solid rgba(99,102,241,0.4) !important;
    box-shadow: 0 3px 12px rgba(99,102,241,0.12) !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton:last-child > button:hover {
    background: rgba(99,102,241,0.08) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.22) !important;
}

/* ── BUTTON COLUMN vertical alignment ── */
div[data-testid="stHorizontalBlock"] > div:nth-child(2) {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    gap: 0 !important;
    padding-top: 2px !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) > div {
    margin-bottom: 0 !important;
}
div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton {
    margin-bottom: 10px !important;
}

.header-divider {
    border: none; height: 1.5px; margin: 14px 0 18px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.2), transparent);
}

/* ── SEARCH CARD ── */
.search-wrap {
    background: rgba(255,255,255,0.5);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 14px 24px 16px;
    border: 1.5px solid rgba(255,255,255,0.88);
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.search-label {
    font-size: 0.72rem; font-weight: 800;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #4338ca; margin-bottom: 8px;
    display: flex; align-items: center; gap: 6px;
}

/* ── INPUTS ── */
.stTextInput > div > div > input {
    border-radius: 14px !important;
    border: 2px solid rgba(99,102,241,0.22) !important;
    background: rgba(255,255,255,0.95) !important;
    color: #0f172a !important; font-size: 0.95rem !important;
    font-weight: 500 !important; height: 50px !important;
    padding: 0 18px !important; transition: all 0.2s !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.07) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important; background: #fff !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(15,23,42,0.32) !important; }
label {
    font-size: 0 !important; /* hide default labels — we use custom sec-header */
}

/* ── SECTION BOX ── */
.section-box {
    background: rgba(255,255,255,0.48);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 0;           /* NO padding top – header provides it */
    border: 1.5px solid rgba(255,255,255,0.85);
    box-shadow: 0 6px 28px rgba(0,0,0,0.07);
    margin-bottom: 18px;
    overflow: hidden;
}

/* ── SECTION HEADER BAND ── */
.sec-header {
    display: flex; align-items: center; gap: 9px;
    padding: 13px 20px 11px;
    font-size: 0.78rem; font-weight: 800;
    letter-spacing: 0.1em; text-transform: uppercase;
    border-bottom: 1.5px solid rgba(255,255,255,0.7);
}
.sec-body { padding: 14px 20px 16px; }

/* Kill the blank top space Streamlit injects between the sec-header markdown
   and the first widget inside a section-box */
.section-box > div[data-testid="stVerticalBlock"] > div:first-child:empty,
.section-box .element-container:first-child:empty { display: none !important; }
.section-box > div[data-testid="stVerticalBlock"] { gap: 0 !important; }
/* Remove top margin from first element-container inside section boxes */
.section-box .element-container:first-child { margin-top: 0 !important; padding-top: 0 !important; }

/* CURRENT CONDITIONS header */
.sh-blue   { background: linear-gradient(90deg,rgba(99,102,241,0.18),rgba(139,92,246,0.08)); color: #3730a3; }
/* FORECAST header */
.sh-cyan   { background: linear-gradient(90deg,rgba(6,182,212,0.18),rgba(14,165,233,0.08)); color: #0e7490; }
/* RISK header */
.sh-risk-n { background: linear-gradient(90deg,rgba(22,163,74,0.16),rgba(16,185,129,0.08)); color: #14532d; }
.sh-risk-r { background: linear-gradient(90deg,rgba(217,119,6,0.16),rgba(245,158,11,0.08)); color: #78350f; }
.sh-risk-w { background: linear-gradient(90deg,rgba(220,38,38,0.16),rgba(239,68,68,0.08));  color: #7f1d1d; }
/* CHATBOT header */
.sh-purple { background: linear-gradient(90deg,rgba(139,92,246,0.18),rgba(168,85,247,0.08)); color: #4c1d95; }

/* ── WEATHER STAT CARDS ── */
/* Negative top margin pulls cards up tight under the header box */
.element-container:has(.w-card) { margin-top: -4px !important; }
.w-card {
    border-radius: 18px; padding: 18px 10px 15px;
    text-align: center; border: 1.5px solid rgba(255,255,255,0.85);
    box-shadow: 0 6px 22px rgba(0,0,0,0.1);
    transition: transform 0.22s, box-shadow 0.22s;
}
.w-card:hover { transform: translateY(-6px); box-shadow: 0 16px 36px rgba(0,0,0,0.16); }
.w-card .icon { font-size: 1.8rem; line-height: 1; margin-bottom: 7px; }
.w-card .lbl  { font-size: 0.66rem; font-weight: 800; letter-spacing: 0.09em; text-transform: uppercase; margin-bottom: 5px; }
.w-card .val  { font-size: 1.8rem; font-weight: 900; line-height: 1.1; }
.w-card .unit { font-size: 0.8rem; font-weight: 600; opacity: 0.6; }

.wc-temp { background: linear-gradient(145deg,#fff7ed,#fed7aa); }
.wc-temp .lbl { color:#c2410c; } .wc-temp .val { color:#ea580c; }
.wc-hum  { background: linear-gradient(145deg,#eff6ff,#bfdbfe); }
.wc-hum  .lbl { color:#1d4ed8; } .wc-hum  .val { color:#2563eb; }
.wc-wind { background: linear-gradient(145deg,#f0fdfa,#99f6e4); }
.wc-wind .lbl { color:#0f766e; } .wc-wind .val { color:#0d9488; }

/* Pull plotly chart tight under its header box */
.element-container:has(.stPlotlyChart) { margin-top: -4px !important; }

/* ── RISK CARD ── */
.risk-inner {
    border-radius: 16px; padding: 18px 18px 14px;
    border: 2px solid; margin: 0 0 12px;
}
.risk-badge {
    display: inline-flex; align-items: center; gap: 6px;
    border-radius: 50px; padding: 5px 16px;
    font-size: 0.74rem; font-weight: 800;
    letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 8px;
}
.risk-val { font-size: 2.5rem; font-weight: 900; line-height: 1; }
.risk-sub { font-size: 0.8rem; font-weight: 500; margin-top: 5px; font-style: italic; }
.risk-legend {
    font-size: 0.72rem; color: rgba(15,23,42,0.44);
    font-weight: 600; text-align: center;
}

/* ── SAMPLE QUESTION PILLS ── */
.sq {
    background: linear-gradient(135deg,rgba(99,102,241,0.1),rgba(139,92,246,0.07));
    border: 1.5px solid rgba(99,102,241,0.22);
    border-left: 4px solid #6366f1;
    padding: 9px 13px; border-radius: 10px;
    margin-bottom: 8px; font-size: 0.82rem;
    font-weight: 600; color: #3730a3;
}

/* ── CHAT ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.55) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.8) !important;
    margin-bottom: 6px !important;
}

/* Make avatars exact boxes instead of circles */
[data-testid="stChatMessageAvatar"], 
[data-testid="stChatMessageAvatar"] img, 
[data-testid="stChatMessageAvatar"] svg {
    border-radius: 6px !important;
}

.stAlert { border-radius: 14px !important; }

/* Remove top padding from st.write("") spacers that cause ghost boxes */
.stMarkdown p:empty { display:none; }
div[data-testid="stVerticalBlockBorderWrapper"]:has(.stMarkdown:only-child:empty) { display:none; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════
#  HOME PAGE
# ═══════════════════════════════════════════
if st.session_state.page == "home":

    colh1, colh2 = st.columns([6, 1])
    with colh1:
        st.markdown("""
        <div class="hero-wrap">
            <span class="hero-title">AI-Based Weather Alert System</span>
            <p class="hero-caption">Real-time forecasts &nbsp;&middot;&nbsp; AI-powered risk detection &nbsp;&middot;&nbsp; Personalised email alerts</p>
        </div>
        <hr class="header-divider">
        """, unsafe_allow_html=True)
    with colh2:
        if st.button("📝  Sign Up"):
            st.session_state.page = "signup"; st.rerun()
        if st.button("✏️  Update"):
            st.session_state.page = "update"; st.rerun()

    # SEARCH
    st.markdown('<div class="search-wrap"><div class="search-label">📍 Enter Your Location</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        city = st.text_input("_", placeholder="🔍  Search city — Hyderabad, Delhi, Mumbai...", label_visibility="collapsed")
    with col2:
        fetch = st.button("Fetch 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

    if city or fetch:
        try:
            res = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            ).json()
            if res.get("cod") != 200:
                st.error("❌ City not found. Check the spelling and try again.")
            else:
                fore = requests.get(
                    f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
                ).json()

                temp        = res["main"]["temp"]
                humidity    = res["main"]["humidity"]
                pressure    = res["main"]["pressure"]
                wind_speed  = res["wind"]["speed"]
                description = res["weather"][0]["description"]
                ml_pred     = predict_risk_rf(temp, humidity, pressure, wind_speed)

                if ml_pred == 2:
                    rs, rl, rc  = 8, "Warning", "#dc2626"
                    rbg, rbd, rbadge, ri, rsh = "linear-gradient(145deg,#fff1f2,#fee2e2)", "#fca5a5", "rgba(220,38,38,0.12)", "🔴", "sh-risk-w"
                elif ml_pred == 1:
                    rs, rl, rc  = 5, "Risky", "#d97706"
                    rbg, rbd, rbadge, ri, rsh = "linear-gradient(145deg,#fffbeb,#fef3c7)", "#fcd34d", "rgba(217,119,6,0.12)", "🟡", "sh-risk-r"
                else:
                    rs, rl, rc  = 2, "Normal", "#16a34a"
                    rbg, rbd, rbadge, ri, rsh = "linear-gradient(145deg,#f0fdf4,#dcfce7)", "#86efac", "rgba(22,163,74,0.12)", "🟢", "sh-risk-n"

                left, right = st.columns([2, 1])

                with left:
                    # CURRENT CONDITIONS
                    st.markdown(f"""
                    <div class="section-box">
                        <div class="sec-header sh-blue">📍 Current Conditions — {city.title()}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown(f"""<div class="w-card wc-temp">
                            <div class="icon">🌡️</div>
                            <div class="lbl">Temperature</div>
                            <div class="val">{round(temp,1)}<span class="unit">°C</span></div>
                        </div>""", unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""<div class="w-card wc-hum">
                            <div class="icon">💧</div>
                            <div class="lbl">Humidity</div>
                            <div class="val">{humidity}<span class="unit">%</span></div>
                        </div>""", unsafe_allow_html=True)
                    with c3:
                        st.markdown(f"""<div class="w-card wc-wind">
                            <div class="icon">🌬️</div>
                            <div class="lbl">Wind</div>
                            <div class="val">{wind_speed}<span class="unit"> km/h</span></div>
                        </div>""", unsafe_allow_html=True)

                    # FORECAST
                    forecast_data = [{"Time": f"{(i+1)*3}h", "Temp": e["main"]["temp"]} for i, e in enumerate(fore["list"][:8])]
                    df = pd.DataFrame(forecast_data)
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df["Time"], y=df["Temp"], mode="lines+markers",
                        line=dict(width=3.5, color="#6366f1", shape="spline"),
                        marker=dict(size=9, color="#fff", line=dict(width=2.5, color="#6366f1")),
                        fill="tozeroy", fillcolor="rgba(99,102,241,0.12)",
                        hovertemplate="<b>%{x}</b><br>%{y:.1f}°C<extra></extra>"
                    ))
                    fig.update_layout(
                        height=230, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(showgrid=False, showline=False, tickfont=dict(size=11, color="#64748b")),
                        yaxis=dict(gridcolor="rgba(99,102,241,0.1)", zeroline=False, tickfont=dict(size=11, color="#64748b")),
                        margin=dict(l=8, r=8, t=8, b=8), showlegend=False
                    )
                    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div class="section-box">
                        <div class="sec-header sh-cyan">📈 24-Hour Temperature Forecast</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.plotly_chart(fig, use_container_width=True, config={"staticPlot": True, "displayModeBar": False})

                with right:
                    # RISK
                    st.markdown(f"""
                    <div class="section-box">
                        <div class="sec-header {rsh}">⚠️ Risk Assessment</div>
                        <div class="sec-body">
                            <div class="risk-inner" style="background:{rbg};border-color:{rbd};">
                                <div class="risk-badge" style="background:{rbadge};color:{rc};">
                                    {ri}&nbsp; {rl}
                                </div>
                                <div class="risk-val" style="color:{rc};">
                                    {rs}<span style="font-size:1rem;font-weight:600;opacity:0.45;"> /10</span>
                                </div>
                                <div class="risk-sub" style="color:{rc}cc;">{description.capitalize()}</div>
                            </div>
                            <div class="risk-legend">🟢 Normal &nbsp;·&nbsp; 🟡 Risky &nbsp;·&nbsp; 🔴 Warning</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # CHATBOT
                    st.markdown("""
                    <div class="section-box">
                        <div class="sec-header sh-purple">🤖 Weather AI Chatbot</div>
                        <div class="sec-body">
                            <div class="sq">☁️ Will it rain today?</div>
                            <div class="sq">🏃 Is it safe to go outside?</div>
                            <div class="sq">👕 What should I wear today?</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Render Chat History with Custom Avatars
                    for msg in st.session_state.messages:
                        avatar_choice = USER_AVATAR if msg["role"] == "user" else AI_AVATAR
                        with st.chat_message(msg["role"], avatar=avatar_choice):
                            st.markdown(msg["content"])

                    user_q = st.text_input("_q", placeholder="Ask about weather...", key=f"chat_input_{st.session_state.chat_key}", label_visibility="collapsed")
                    
                    if st.button("Ask AI 💬"):
                        if user_q.strip():
                            st.session_state.messages.append({"role": "user", "content": user_q.strip()})
                            
                            with st.spinner("Thinking..."):
                                reply = weather_chatbot(user_q.strip(), city, temp, humidity, rl, description)
                                st.session_state.messages.append({"role": "assistant", "content": reply})
                            
                            st.session_state.chat_key += 1
                            st.rerun()

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

if st.session_state.page == "signup":
    with open("signup.py", "r", encoding="utf-8") as f:
        exec(f.read())

if st.session_state.page == "update":
    with open("update_location.py", "r", encoding="utf-8") as f:
        exec(f.read())
