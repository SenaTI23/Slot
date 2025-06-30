import streamlit as st
import random
import time
import numpy as np
from PIL import Image
import requests
from io import BytesIO

# Konfigurasi Streamlit
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# CSS Custom untuk animasi
st.markdown("""
<style>
    @keyframes spin {
        0% { transform: translateY(0); }
        100% { transform: translateY(-1000px); }
    }
    .slot-reel {
        height: 200px;
        overflow: hidden;
        position: relative;
        display: inline-block;
        width: 30%;
    }
    .slot-symbols {
        animation: spin 0.1s linear infinite;
    }
    .slot-symbol {
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .win-animation {
        position: absolute;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(255,215,0,0.8) 0%, rgba(255,255,255,0) 70%);
        animation: pulse 0.5s ease-in-out infinite alternate;
    }
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.7; }
        100% { transform: scale(1.1); opacity: 0.9; }
    }
</style>
""", unsafe_allow_html=True)

# Slot Symbols Data dengan gambar yang lebih menarik (placeholder)
symbols = [
    {"name": "Zeus", "image": "https://placehold.co/150x150/gold/black?text=⚡ZEUS", "multiplier": 7},
    {"name": "Hades", "image": "https://placehold.co/150x150/purple/white?text=☠HADES", "multiplier": 5},
    {"name": "Poseidon", "image": "https://placehold.co/150x150/blue/white?text=🌊POSEIDON", "multiplier": 5},
    {"name": "Athena", "image": "https://placehold.co/150x150/silver/black?text=🦉ATHENA", "multiplier": 3},
]

# Inisialisasi state
if 'spinning' not in st.session_state:
    st.session_state.spinning = False
if 'result' not in st.session_state:
    st.session_state.result = [random.choice(symbols) for _ in range(3)]
if 'balance' not in st.session_state:
    st.session_state.balance = 1000
if 'bet' not in st.session_state:
    st.session_state.bet = 10

def spin():
    st.session_state.spinning = True
    st.session_state.balance -= st.session_state.bet
    
    # Animasi putaran
    for _ in range(30):
        for i in range(3):
            st.session_state.result[i] = random.choice(symbols)
        time.sleep(0.05)
    
    # Result akhir
    st.session_state.result = [random.choice(symbols) for _ in range(3)]
    check_win()
    st.session_state.spinning = False

def check_win():
    # Logika kemenangan sederhana
    if len(set(s['name'] for s in st.session_state.result)) == 1:  # Jackpot semua sama
        st.session_state.balance += st.session_state.bet * 10
    elif len(set(s['name'] for s in st.session_state.result)) == 2:  # Dua sama
        st.session_state.balance += st.session_state.bet * 2

# Tampilan Slot Machine
st.title("Olympus Slot Machine")
st.markdown(f"**Balance:** {st.session_state.balance} coins")

st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
for i, symbol in enumerate(st.session_state.result):
    container = st.empty()
    with container:
        if st.session_state.spinning:
            st.markdown(f"""
            <div class="slot-reel">
                <div class="slot-symbols">
                    {''.join(f'<div class="slot-symbol"><img src="{random.choice(symbols)["image"]}" width="100"></div>' for _ in range(5))}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.image(symbol["image"], width=150)
st.markdown("</div>", unsafe_allow_html=True)

# Controls
st.slider("Bet Amount", 10, 100, st.session_state.bet, key='bet', disabled=st.session_state.spinning)
if st.button("SPIN", disabled=st.session_state.spinning or st.session_state.balance < st.session_state.bet):
    spin()

if st.session_state.balance <= 0:
    st.error("Game Over! Refresh browser to restart.")
