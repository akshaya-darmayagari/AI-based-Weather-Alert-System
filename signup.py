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

/* ── KILL GHOST BOXES ── */
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

/* ── FORM CARD HEADER BAND ── */
.form-header {
    background: linear-gradient(90deg, rgba(99,102,241,0.18), rgba(139,92,246,0.08));
    border-bottom: 1.5px solid rgba(99,102,241,0.15);
    padding: 16px 28px 14px;
}
.form-title   { font-size: 1.15rem; font-weight: 800; color: #1e1b4b; margin: 0 0 2px; }
.form-caption { font-size: 0.78rem; color: rgba(15,23,42,0.48); font-weight: 500; margin: 0; }

.form-body { padding: 22px 28px 24px; }

/* ── FIELD GROUPS — coloured label strips ── */
.field-label {
    display: flex; align-items: center; gap: 7px;
    font-size: 0.72rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 6px 12px; border-radius: 8px; margin-bottom: 6px;
    width: fit-content;
}
.fl-name   { background: rgba(99,102,241,0.12);  color: #3730a3; }
.fl-email  { background: rgba(6,182,212,0.12);   color: #0e7490; }
.fl-mobile { background: rgba(245,158,11,0.12);  color: #92400e; }
.fl-loc    { background: rgba(22,163,74,0.12);   color: #14532d; }
.fl-time   { background: rgba(239,68,68,0.1);    color: #991b1b; }

/* ── INPUTS ── */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid rgba(99,102,241,0.2) !important;
    background: rgba(255,255,255,0.95) !important;
    color: #0f172a !important; font-size: 0.9rem !important;
    font-weight: 500 !important; height: 48px !important;
    padding: 0 16px !important; transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.14) !important;
    background: #fff !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(15,23,42,0.3) !important; }
label { font-size: 0 !important; }

/* ── CHECKBOX ── */
.stCheckbox label { font-size: 0.82rem !important; color: #334155 !important; font-weight: 500 !important; }

/* ── SUBMIT ── */
.stFormSubmitButton > button {
    width: 100% !important; height: 52px !important; border-radius: 14px !important;
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important; font-size: 0.95rem !important;
    font-weight: 800 !important; border: none !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.45) !important;
    transition: all 0.22s ease !important; margin-top: 10px !important;
}
.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(99,102,241,0.55) !important;
}

/* ── SECURITY NOTE ── */
.sec-note {
    display: flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, rgba(22,163,74,0.1), rgba(5,150,105,0.07));
    border: 1.5px solid rgba(22,163,74,0.25); border-radius: 10px;
    padding: 10px 14px; font-size: 0.77rem; color: #166534;
    font-weight: 600; margin-top: 14px;
}

/* ── ILLUS CARD ── */
.illus-card {
    background: rgba(255,255,255,0.38); backdrop-filter: blur(14px);
    border-radius: 24px; padding: 36px 24px;
    border: 1.5px solid rgba(255,255,255,0.88);
    box-shadow: 0 10px 34px rgba(0,0,0,0.08); text-align: center;
}
.feature-pill {
    display: inline-block;
    border-radius: 50px; padding: 6px 15px;
    font-size: 0.76rem; font-weight: 700; margin: 4px 3px;
}
.fp-blue   { background: rgba(99,102,241,0.14); color: #3730a3; border: 1.5px solid rgba(99,102,241,0.25); }
.fp-cyan   { background: rgba(6,182,212,0.14);  color: #0e7490; border: 1.5px solid rgba(6,182,212,0.25); }
.fp-green  { background: rgba(22,163,74,0.13);  color: #14532d; border: 1.5px solid rgba(22,163,74,0.25); }
.fp-amber  { background: rgba(245,158,11,0.13); color: #92400e; border: 1.5px solid rgba(245,158,11,0.25); }

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

left, right = st.columns([1.3, 1])

with left:
    st.markdown("""
    <div class="form-card">
        <div class="form-header">
            <p class="form-title">📝 Create Your Account</p>
            <p class="form-caption">Sign up to receive personalised daily weather alerts via email</p>
        </div>
        <div class="form-body">
    """, unsafe_allow_html=True)

    # Coloured field labels are placed just before each input inside the form below

    with st.form("signup_form"):
        st.markdown('<div class="field-label fl-name">👤 Full Name</div>', unsafe_allow_html=True)
        name       = st.text_input("n",  placeholder="John Doe",           label_visibility="collapsed")
        st.markdown('<div class="field-label fl-email">📧 Email Address</div>', unsafe_allow_html=True)
        email      = st.text_input("e",  placeholder="john@example.com",   label_visibility="collapsed")
        st.markdown('<div class="field-label fl-mobile">📱 Mobile Number</div>', unsafe_allow_html=True)
        mobile     = st.text_input("m",  placeholder="9876543210",          label_visibility="collapsed")
        st.markdown('<div class="field-label fl-loc">📍 Location</div>', unsafe_allow_html=True)
        location   = st.text_input("l",  placeholder="Hyderabad",           label_visibility="collapsed")
        st.markdown('<div class="field-label fl-time">⏰ Alert Time (IST) — HH:MM</div>', unsafe_allow_html=True)
        alert_time = st.text_input("t",  placeholder="09:00  or  18:30",   label_visibility="collapsed")
        agree      = st.checkbox("I agree to the Terms & Privacy Policy")
        submitted  = st.form_submit_button("🚀  Register Now")

        if submitted:
            if not all([name.strip(), email.strip(), mobile.strip(), location.strip(), alert_time.strip()]):
                st.warning("⚠️ Please fill in all fields.")
            elif not agree:
                st.warning("⚠️ Please accept the Terms & Privacy Policy.")
            else:
                try:
                    supabase.table("users").insert({
                        "email": email.strip().lower(), "name": name.strip(),
                        "mobile": mobile.strip(), "location": location.strip(),
                        "alert_time": alert_time.strip()
                    }).execute()
                    st.success("✅ Registered! Your weather alerts are now active.")
                except Exception as e:
                    if "duplicate key" in str(e).lower():
                        st.error("❌ Email already registered. Try updating instead.")
                    else:
                        st.error(f"❌ Database Error: {e}")

    st.markdown('<div class="sec-note">🔒 Your data is encrypted and stored securely</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="illus-card">
        <img class="float-anim"
             src="https://cdn-icons-png.flaticon.com/512/1146/1146869.png"
             width="200"
             style="filter:drop-shadow(0 16px 28px rgba(99,102,241,0.3));">
        <p style="margin:22px 0 6px;font-size:1.05rem;font-weight:800;color:#1e1b4b;letter-spacing:-0.3px;">
            Smart Weather Alerts
        </p>
        <p style="font-size:0.8rem;color:rgba(15,23,42,0.48);font-weight:500;margin-bottom:20px;line-height:1.65;">
            Get notified at the exact time you choose,<br>every single day — powered by AI.
        </p>
        <div>
            <span class="feature-pill fp-blue">📡 Real-time Data</span>
            <span class="feature-pill fp-cyan">🤖 AI Powered</span>
            <span class="feature-pill fp-green">📧 Email Alerts</span>
            <span class="feature-pill fp-amber">⏰ Custom Time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
