import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time
import random
import pandas as pd
from backend import NorthPoleEngine, generate_pdf

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NorthPoleOS Command", layout="wide", page_icon="🎅")

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200: return None
        return r.json()
    except:
        return None

# Animations
lottie_santa = load_lottieurl("https://lottie.host/575a7bc1-4439-4d64-9f26-0e1948842609/jC5K7wT2dE.json")
lottie_radar = load_lottieurl("https://lottie.host/9320e8b2-5743-41c6-b796-03f6f9479b18/2b4B8y8n5M.json")

# --- 2. CYBERPUNK STYLING ---
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000000 100%);
    }
    [data-testid="stSidebar"] {
        background-color: #0a0a10;
        border-right: 1px solid #333;
    }
    .tech-card {
        background: rgba(20, 20, 30, 0.7);
        border: 1px solid #333;
        border-left: 3px solid #ff4b1f;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    h1, h2, h3 { font-family: 'Consolas', monospace; color: #fff !important; }
    p, small, li { color: #aaa !important; font-family: 'Verdana', sans-serif; }
    div[data-testid="stMetric"] {
        background-color: #111;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 📡 SIGNAL INPUT")
    input_type = st.selectbox("Data Source", ["Intercepted Letter", "Neural Link (Beta)"])
    
    user_input = ""
    if input_type == "Intercepted Letter":
        user_input = st.text_area("Payload", height=150, placeholder="Awaiting Input...")
    else:
        if st.button("🧠 ACTIVATE SCAN"):
            with st.status("Establishing Neural Handshake...", expanded=True) as status:
                time.sleep(1)
                st.write("Target: Timmy (Age 7)")
                time.sleep(0.5)
                st.write("Decoding...")
                user_input = "I want a rocket ship that goes to Mars."
                status.update(label="Scan Complete", state="complete", expanded=False)
            st.success(f"Decoded: '{user_input}'")

    process_btn = st.button("EXECUTE PROTOCOL", type="primary", use_container_width=True)
    st.divider()
    st.markdown("### 🎅 STATUS")
    st.metric("Sleigh Integrity", "98.4%", "Stable")
    st.metric("Spirit Level", "8,432 TWh", "+12%")

# --- 4. MAIN DASHBOARD ---
col_h1, col_h2, col_h3 = st.columns([1, 6, 2])
with col_h1:
    if lottie_santa: st_lottie(lottie_santa, height=80, key="head")
with col_h2:
    st.title("NORTHPOLE_OS // COMMAND")
with col_h3:
    if lottie_radar: st_lottie(lottie_radar, height=80, key="radar")

if process_btn and user_input:
    engine = NorthPoleEngine()
    
    # Loading Sequence
    prog_bar = st.progress(0, text="Initializing...")
    for i in range(100):
        time.sleep(0.005)
        prog_bar.progress(i + 1, text="Allocating Elf Resources...")
    prog_bar.empty()

    try:
        prd = engine.process_text_request(user_input)
        
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Elf Squads", f"{random.randint(3, 12)} Units")
        m2.metric("Cookie Cost", f"{random.randint(50, 500)} kcal")
        m3.metric("Complexity", "High-Tech")
        m4.metric("Naughty/Nice", f"{random.randint(80, 99)}/100")
        
        # Split View
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.markdown(f"""
            <div class="tech-card">
                <h3 style="color:#ff4b1f">📂 {prd.project_name.upper()}</h3>
                <p><b>PRIORITY:</b> {prd.priority_level.upper()} | <b>OWNER:</b> R&D DEPT</p>
                <hr style="border-color:#333">
                <p>{prd.executive_summary}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("🔧 ENGINEERING TICKETS")
            for story in prd.user_stories:
                st.markdown(f"""
                <div class="tech-card" style="border-left: 3px solid #4CAF50;">
                    <h4 style="margin:0">🎫 {story.id}</h4>
                    <p style="color:#fff">"{story.desire}"</p>
                    <small><b>CRITERIA:</b> {', '.join(story.acceptance_criteria)}</small>
                </div>
                """, unsafe_allow_html=True)

        with c2:
            st.subheader("📊 ALLOCATION")
            df = pd.DataFrame([random.randint(20, 90) for _ in range(3)], index=["Plastic", "Magic", "Metal"], columns=["%"])
            st.bar_chart(df, color="#ff4b1f")
            
            st.subheader("📅 TIMELINE")
            st.markdown("- [x] Interception\n- [x] Spec Gen\n- [ ] Assembly\n- [ ] QC Check")
            
            st.divider()
            pdf_file = generate_pdf(prd)
            with open(pdf_file, "rb") as f:
                st.download_button("💾 EXPORT BLUEPRINT", f, file_name="CONFIDENTIAL_PRD.pdf", use_container_width=True)

    except Exception as e:
        st.error(f"SYSTEM FAILURE: {e}")

else:
    st.info("AWAITING INPUT STREAM... SELECT SOURCE IN SIDEBAR")