import streamlit as st
import pandas as pd
import time
from datetime import datetime, time as d_time, timedelta
st.set_page_config(page_title="Sleep Quality Predictor", layout="centered")
# Screenshot-il ulla padiye exact Light Blue background matrum Inner White Card CSS setup
st.markdown("""
    <style>
    .stApp { background-color: #4a77d4; }
    .main-card { background-color: #cedcf7; padding: 20px; border-radius: 15px; }
    .white-box { background-color: #ffffff; padding: 25px; border-radius: 15px; margin-top: 20px; }
    h2, p, label { color: #1e3a8a !important; font-weight: 500; }
    .res-title { color: #555; font-size: 16px; margin-bottom: 2px; }
    .res-val { color: #b91c1c; font-size: 26px; font-weight: bold; margin-bottom: 15px; }
    div.stButton > button { background-color: #e2ecf7; color: #1e3a8a; border: 1px solid #1e3a8a; border-radius: 8px; font-weight: bold; }
    div.stButton > button:first-child { background-color: #1e40af; color: white; }
    
    /* Custom Plain Text HTML Table Style matching the photo */
    .custom-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    .custom-table th, .custom-table td { text-align: left; padding: 8px; color: #1e3a8a; font-size: 14px; }
    .custom-table th { color: #475569; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)
if 'history' not in st.session_state:
    st.session_state.history = [
        {"Date": "11 Oct 12:07", "Quality": "Poor", "Hours": "4", "Stress": "8"},
        {"Date": "11 Oct 13:05", "Quality": "Good", "Hours": "7", "Stress": "3"}
    ]
if 'predict' not in st.session_state: st.session_state.predict = False
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown("<h2>🌙 Sleep Quality Predictor</h2><p>A smart way to monitor and improve your sleep</p>", unsafe_allow_html=True)
# 3-Columns Grid Forms Input Elements
c1, c2, c3 = st.columns(3)
with c1:
    bedtime = c1.time_input("⏰ Bedtime", value=d_time(23, 0))
    caffeine = c1.selectbox("☕ Caffeine Intake", ["None", "Low", "Moderate", "High"], index=1)
    stress = c1.slider("🧠 Stress Level: 1-10", 1, 10, 8)
with c2:
    wakeup = c2.time_input("⏰ Wake-up Time", value=d_time(6, 30))
    t1, t2 = datetime.combine(datetime.today(), bedtime), datetime.combine(datetime.today(), wakeup)
    dur = round(((t2 - t1).seconds / 3600) if t2 > t1 else (((t2 + timedelta(days=1)) - t1).seconds / 3600), 1)
    st.text_input("📊 Sleep Duration (hours)", value=str(dur), disabled=True)
    mood = c2.selectbox("🎭 Mood Before Sleep", ["Happy", "Neutral", "Sad", "Anxious"], index=2)
with c3:
    exercise = c3.number_input("🏃‍♂️ Exercise (minutes)", value=25, step=5)
    screen = c3.number_input("📱 Screen Time Before Bed (min)", value=40, step=5)
    interrupt = c3.radio("🛌 Sleep Interruptions?", ["Yes", "No"], index=1)

st.markdown("<br>", unsafe_allow_html=True)
# Main Control Buttons Layout
bc1, bc2, bc3 = st.columns(3)
if bc1.button("Predict Sleep Quality", use_container_width=True): st.session_state.predict = True
if bc2.button("Reset Inputs", use_container_width=True):
    st.session_state.predict = False
    st.rerun()
bc3.button("View Past Predictions", use_container_width=True)
# Output Render Box Block (Visible after clicking predict)
if st.session_state.predict:
    status = "Poor" if stress > 6 or dur < 5 or interrupt == "Yes" else "Good"
    
    st.markdown('<div class="white-box">', unsafe_allow_html=True)
    st.markdown(f'<p class="res-title">Predicted Sleep Quality:</p><p class="res-val">{status}</p>', unsafe_allow_html=True)
    
    st.markdown("<h4>Suggestions</h4>", unsafe_allow_html=True)
    st.markdown("""
    * Try reducing screen time by 30 minutes before bed.
    * Cut down caffeine, especially after afternoon.
    * Try meditation or deep breathing to lower stress.
    * Aim for 7-9 hours of sleep every night.
    * Keep your room dark, cool and quiet to avoid waking up.
    """)
    # Injecting real-time entry into local storage list array
    cur_time = time.strftime("%d Oct %H:%M")
    if not any(d['Date'] == cur_time for d in st.session_state.history):
        st.session_state.history.insert(0, {"Date": cur_time, "Quality": status, "Hours": str(dur), "Stress": str(stress)})
    # Pure HTML plain table parsing grid system matching the visual image style
    st.markdown("<br><h4>Past Predictions</h4>", unsafe_allow_html=True)
    table_html = "<table class='custom-table'><tr><th>Date</th><th>Quality</th><th>Hours</th><th>Stress</th></tr>"
    for row in st.session_state.history:
        q_color = "#b91c1c" if row['Quality'] == "Poor" else "#16a34a"
        table_html += f"<tr><td>{row['Date']}</td><td style='color:{q_color}; font-weight:bold;'>{row['Quality']}</td><td>{row['Hours']}</td><td>{row['Stress']}</td></tr>"
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)