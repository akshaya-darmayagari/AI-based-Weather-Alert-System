import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

.stApp { background: linear-gradient(135deg, #87CEEB 0%, #9AE6B4 100%); color: #0f172a; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; }
.stMarkdown p:empty { display:none; }

/* ── HERO TITLE ── */
.hero-title {
    font-size: 2.8rem; font-weight: 900; letter-spacing: -1.6px;
    color: #0f172a; text-align: left; margin: 0 !important; line-height: 1.05; display: block;
}
.hero-caption {
    font-size: 0.88rem; font-weight: 500; color: rgba(15,23,42,0.5);
    margin: 5px 0 0 !important; letter-spacing: 0.01em;
}
.header-divider {
    border: none; height: 2.5px; margin: 12px 0 16px;
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 30%, #06b6d4 65%, transparent 100%);
    border-radius: 2px; opacity: 0.55;
}
.page-sub {
    font-size: 1.15rem; font-weight: 800; color: #1e1b4b; margin-bottom: 18px;
}

/* ── BACK BUTTON ── */
.stButton > button {
    border-radius: 50px !important; font-size: 0.82rem !important;
    font-weight: 700 !important; height: 42px !important; padding: 0 22px !important;
    border: none !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important; box-shadow: 0 4px 16px rgba(99,102,241,0.5) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-2px) scale(1.04) !important; }

/* ── FORM CARD ── */
.form-card {
    background: rgba(255,255,255,0.5); backdrop-filter: blur(20px);
    border-radius: 24px; overflow: hidden;
    border: 1.5px solid rgba(255,255,255,0.9);
    box-shadow: 0 12px 40px rgba(0,0,0,0.09);
}
.form-header {
    background: linear-gradient(90deg, rgba(13,148,136,0.16), rgba(20,184,166,0.07));
    border-bottom: 1.5px solid rgba(13,148,136,0.18);
    padding: 16px 28px 14px;
}
.form-title   { font-size: 1.15rem; font-weight: 800; color: #134e4a; margin: 0 0 2px; }
.form-caption { font-size: 0.78rem; color: rgba(15,23,42,0.48); font-weight: 500; margin: 0; }
.form-body    { padding: 22px 28px 24px; }

/* ── FIELD LABELS ── */
.field-label {
    display: flex; align-items: center; gap: 7px;
    font-size: 0.72rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 6px 12px; border-radius: 8px; margin-bottom: 6px;
    width: fit-content;
}
.fl-email { background: rgba(6,182,212,0.12);  color: #0e7490; }
.fl-loc   { background: rgba(22,163,74,0.12);  color: #14532d; }
.fl-time  { background: rgba(239,68,68,0.1);   color: #991b1b; }

/* ── INPUTS ── */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid rgba(13,148,136,0.22) !important;
    background: rgba(255,255,255,0.95) !important;
    color: #0f172a !important; font-size: 0.9rem !important;
    font-weight: 500 !important; height: 48px !important;
    padding: 0 16px !important; transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #0d9488 !important;
    box-shadow: 0 0 0 4px rgba(13,148,136,0.16) !important;
    background: #fff !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(15,23,42,0.3) !important; }
label { font-size: 0 !important; }

/* ── SUBMIT ── */
.stFormSubmitButton > button {
    width: 100% !important; height: 52px !important; border-radius: 14px !important;
    background: linear-gradient(135deg, #0d9488, #14b8a6) !important;
    color: #fff !important; font-size: 0.95rem !important;
    font-weight: 800 !important; border: none !important;
    box-shadow: 0 6px 20px rgba(13,148,136,0.45) !important;
    transition: all 0.22s ease !important; margin-top: 10px !important;
}
.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(13,148,136,0.55) !important;
}

/* ── TIP BOX ── */
.tip-box {
    background: linear-gradient(135deg, rgba(14,165,233,0.1), rgba(99,102,241,0.07));
    border: 1.5px solid rgba(14,165,233,0.28); border-left: 4px solid #0ea5e9;
    border-radius: 12px; padding: 13px 16px;
    font-size: 0.78rem; color: #0c4a6e; font-weight: 500;
    margin-top: 16px; line-height: 1.65;
}

/* ── ILLUS CARD ── */
.illus-card {
    background: rgba(255,255,255,0.38); backdrop-filter: blur(14px);
    border-radius: 24px; padding: 32px 24px;
    border: 1.5px solid rgba(255,255,255,0.88);
    box-shadow: 0 10px 34px rgba(0,0,0,0.08); text-align: center;
}
.step-row {
    display: flex; align-items: center; gap: 12px;
    background: rgba(255,255,255,0.58); border-radius: 12px;
    padding: 11px 14px; margin-bottom: 10px;
    border: 1.5px solid rgba(255,255,255,0.88);
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
}
.step-num {
    width: 30px; height: 30px; border-radius: 50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    font-size:0.75rem; font-weight:800; color:#fff;
}
.step-text { font-size:0.82rem; font-weight:600; color:#1e293b; }

@keyframes floaty { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-18px)} }
.float-anim { animation: floaty 4.5s ease-in-out infinite; }
.stAlert { border-radius: 14px !important; }
</style>
""", unsafe_allow_html=True)

# HEADER
colh1, colh2 = st.columns([5, 1])
with colh1:
    st.markdown("""
    <span class="hero-title">AI-Based Weather Alert System</span>
    <p class="hero-caption">Real-time forecasts &middot; AI-powered risk detection &middot; Personalised email alerts</p>
    <hr class="header-divider">
    """, unsafe_allow_html=True)
with colh2:
    if st.button("⬅️ Back"):
        st.session_state.page = "home"; st.rerun()

st.markdown('<p class="page-sub">✏️ Update Location &amp; Alert Time</p>', unsafe_allow_html=True)

left, right = st.columns([1.3, 1])

with left:
    st.markdown("""
    <div class="form-card">
        <div class="form-header">
            <p class="form-title">🔄 Update Your Preferences</p>
            <p class="form-caption">Change your city and preferred alert time — updates take effect immediately</p>
        </div>
        <div class="form-body">
    """, unsafe_allow_html=True)

    with st.form("update_form"):
        st.markdown('<div class="field-label fl-email">📧 Registered Email</div>', unsafe_allow_html=True)
        email          = st.text_input("e", placeholder="john@example.com",     label_visibility="collapsed")
        st.markdown('<div class="field-label fl-loc">📍 New Location</div>', unsafe_allow_html=True)
        new_location   = st.text_input("l", placeholder="Mumbai, Delhi...",      label_visibility="collapsed")
        st.markdown('<div class="field-label fl-time">⏰ New Alert Time (IST) — HH:MM</div>', unsafe_allow_html=True)
        new_alert_time = st.text_input("t", placeholder="07:00  or  20:30",     label_visibility="collapsed")
        submitted      = st.form_submit_button("🔄  Update Details")

        if submitted:
            if not all([email.strip(), new_location.strip(), new_alert_time.strip()]):
                st.warning("⚠️ Please fill in all fields.")
            else:
                try:
                    response = supabase.table("users") \
                        .update({"location": new_location.strip(), "alert_time": new_alert_time.strip()}) \
                        .eq("email", email.strip().lower()).execute()
                    if response.data:
                        st.success("✅ Details updated! Alerts now use the new settings.")
                    else:
                        st.error("❌ Email not found. Please register first.")
                except Exception as e:
                    st.error(f"❌ Database Error: {e}")

    st.markdown("""
    <div class="tip-box">
        💡 <strong>Tip:</strong> Use 24-hour format — <code>09:00</code> for 9 AM, <code>21:30</code> for 9:30 PM IST.
        Only location and alert time can be changed here.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="illus-card">
        <img class="float-anim"
             src="https://cdn-icons-png.flaticon.com/512/1828/1828270.png"
             width="180"
             style="filter:drop-shadow(0 14px 24px rgba(13,148,136,0.3));">
        <p style="margin:20px 0 6px;font-size:1.05rem;font-weight:800;color:#134e4a;letter-spacing:-0.3px;">
            Always Stay Updated
        </p>
        <p style="font-size:0.8rem;color:rgba(15,23,42,0.48);font-weight:500;margin:0 0 20px;line-height:1.65;">
            Moving to a new city? Changed your schedule?<br>Update anytime in seconds.
        </p>
        <div style="text-align:left;">
            <div class="step-row">
                <div class="step-num" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);">1</div>
                <span class="step-text">Enter your registered email</span>
            </div>
            <div class="step-row">
                <div class="step-num" style="background:linear-gradient(135deg,#0ea5e9,#06b6d4);">2</div>
                <span class="step-text">Set your new city &amp; alert time</span>
            </div>
            <div class="step-row">
                <div class="step-num" style="background:linear-gradient(135deg,#0d9488,#14b8a6);">3</div>
                <span class="step-text">Done — alerts update instantly!</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
