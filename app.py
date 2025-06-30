import streamlit as st
import random
import time
from PIL import Image
import numpy as np
import requests
from io import BytesIO
import plotly.graph_objects as go
import pandas as pd

# Konfigurasi dasar
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Styling CSS untuk tampilan mobile
st.markdown(
    """
    <style>
    .main {
        padding: 0 !important;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .slot-machine {
        width: 100%;
        padding: 0;
    }
    .slot-reel {
        width: 30%;
        margin: 0 auto;
        overflow: hidden;
    }
    .slot-container {
        display: flex;
        justify-content: center;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .controls {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 20px;
    }
    .bet-controls {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 15px;
    }
    .result-display {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
        color: gold;
    }
    button {
        width: 100%;
        padding: 12px;
        border-radius: 25px;
        font-weight: bold;
    }
    .table-info {
        width: 100%;
        margin-top: 20px;
        color: white;
    }
    .history-item {
        display: flex;
        justify-content: space-between;
        padding: 5px;
        border-bottom: 1px solid #333;
    }
    @media (max-width: 768px) {
        .slot-reel {
            width: 100%;
        }
        button {
            font-size: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Daftar simbol slot (Olympus theme)
symbols = [
    {"name": "Zeus", "image": "https://placehold.co/150x150?text=ZEUS", "multiplier": 7},
    {"name": "Hades", "image": "https://placehold.co/150x150?text=HADES", "multiplier": 5},
    {"name": "Poseidon", "image": "https://placehold.co/150x150?text=POSEIDON", "multiplier": 5},
    {"name": "Athena", "image": "https://placehold.co/150x150?text=ATHENA", "multiplier": 3},
    {"name": "Ares", "image": "https://placehold.co/150x150?text=ARES", "multiplier": 3},
    {"name": "Apollo", "image": "https://placehold.co/150x150?text=APOLLO", "multiplier": 2},
    {"name": "Artemis", "image": "https://placehold.co/150x150?text=ARTEMIS", "multiplier": 2},
    {"name": "Hermes", "image": "https://placehold.co/150x150?text=HERMES", "multiplier": 2},
]

# Variabel state
if "balance" not in st.session_state:
    st.session_state.balance = 1000
if "current_bet" not in st.session_state:
    st.session_state.current_bet = 10
if "spinning" not in st.session_state:
    st.session_state.spinning = False
if "result" not in st.session_state:
    st.session_state.result = ["Zeus", "Hades", "Poseidon"]
if "win_amount" not in st.session_state:
    st.session_state.win_amount = 0
if "history" not in st.session_state:
    st.session_state.history = []

def spin_reels():
    st.session_state.spinning = True
    st.session_state.win_amount = 0
    st.session_state.result = []
    
    # Deduct bet from balance
    st.session_state.balance -= st.session_state.current_bet
    
    # Simulate spinning animation
    for _ in range(15):
        st.session_state.result = [random.choice(symbols)["name"] for _ in range(3)]
        time.sleep(0.1)
        
    # Final result
    st.session_state.result = [random.choice(symbols)["name"] for _ in range(3)]
    check_win()
    st.session_state.spinning = False
    st.session_state.history.insert(0, {
        "time": time.strftime("%H:%M:%S"),
        "result": st.session_state.result.copy(),
        "win": st.session_state.win_amount
    })
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[:10]

def check_win():
    payouts = []
    for symbol in symbols:
        count = st.session_state.result.count(symbol["name"])
        if count >= 2:
            multiplier = symbol["multiplier"] ** (count - 1)
            payout = st.session_state.current_bet * multiplier
            payouts.append(payout)
    
    if payouts:
        st.session_state.win_amount = max(payouts)
        st.session_state.balance += st.session_state.win_amount
    
def adjust_bet(amount):
    st.session_state.current_bet += amount
    st.session_state.current_bet = max(10, min(500, st.session_state.current_bet))

# UI Komponen
def slot_reel(icon, spinning):
    symbol = next((s for s in symbols if s["name"] == icon), symbols[0])
    col1, col2, col3 = st.columns([1,8,1])
    
    with col2:
        container = st.empty()
        with container:
            st.image(symbol["image"], width=150)
        
        if spinning:
            time.sleep(0.1)
            spinning_symbol = random.choice(symbols)
            container.image(spinning_symbol["image"], width=150)
    
    return icon

# Layout utama
# Header dengan logo Olympus
st.image("https://placehold.co/800x200?text=OLYMPUS+SLOTS", use_column_width=True)

# Kontainer utama
col1, col2 = st.columns([7, 3])

with col1:
    # Slot machine visual
    st.markdown("<div class='slot-machine'>", unsafe_allow_html=True)
    
    st.markdown("<div class='slot-container'>", unsafe_allow_html=True)
    for i in range(3):
        with st.empty():
            slot_reel(st.session_state.result[i], st.session_state.spinning)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Kontrol taruhan
    st.markdown("<div class='controls'>", unsafe_allow_html=True)
    
    if st.button("SPIN", disabled=st.session_state.spinning or st.session_state.balance < st.session_state.current_bet, 
                 on_click=spin_reels):
        pass
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display hasil
    if st.session_state.win_amount > 0:
        st.markdown(f"<div class='result-display'>YOU WON {st.session_state.win_amount} COINS!</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-display'> </div>", unsafe_allow_html=True)

with col2:
    # Info pemain
    st.markdown("<div class='table-info'>", unsafe_allow_html=True)
    
    # Balance display
    st.markdown("### SALDO")
    st.progress(st.session_state.balance / 2000)
    st.write(f"**{st.session_state.balance}** coins")
    
    # Bet control
    st.markdown("### TARUHAN")
    st.progress(st.session_state.current_bet / 500)
    st.write(f"**{st.session_state.current_bet}** coins per spin")
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("-10", disabled=st.session_state.current_bet <= 10):
            adjust_bet(-10)
    with btn_col2:
        if st.button("+10", disabled=st.session_state.current_bet >= 500):
            adjust_bet(10)
    
    st.markdown("### PEMBAYARAN")
    payout_df = pd.DataFrame([
        {"Simbol": s["name"], "2 Simbol": f"{s['multiplier']}x", "3 Simbol": f"{s['multiplier']**2}x"}
        for s in sorted(symbols, key=lambda x: -x["multiplier"])
    ])
    st.table(payout_df)
    
    st.markdown("### RIWAYAT")
    for h in st.session_state.history:
        st.markdown(f"<div class='history-item'>"
                    f"<span>{h['time']}</span>"
                    f"<span>{' - '.join(h['result'])}</span>"
                    f"<span>{'+' + str(h['win']) if h['win'] > 0 else ''}</span>"
                    f"</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
