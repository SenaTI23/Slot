import streamlit as st
import random

st.set_page_config(page_title="⚡ Gates of Olympus Mini", layout="wide")
st.markdown("<h1 style='text-align:center;'>⚡ GATES OF OLYMPUS MINI</h1>", unsafe_allow_html=True)

# Simbol Olympus-style
symbols = ["⚡", "💎", "🔥", "💰", "👑", "🌀", "🔱"]
colors = {
    "⚡": "yellow",
    "💎": "cyan",
    "🔥": "red",
    "💰": "orange",
    "👑": "gold",
    "🌀": "purple",
    "🔱": "green"
}

# Init saldo
if 'saldo' not in st.session_state:
    st.session_state.saldo = 2000

bet = 100
multiplier = random.choice([1, 2, 3, 5, 10, 15, 25, 50])

st.markdown(f"""
<div style='text-align:center;'>
    💰 <b>Saldo:</b> {st.session_state.saldo} &nbsp;&nbsp; | 
    🎯 <b>Taruhan:</b> {bet} &nbsp;&nbsp; | 
    ✨ <b>Multiplier Acak:</b> x{multiplier}
</div><br>
""", unsafe_allow_html=True)

# SPIN
def spin_grid():
    return [[random.choice(symbols) for _ in range(6)] for _ in range(5)]

# Cek kemenangan sederhana (baris penuh simbol sama)
def check_win(grid):
    win_coords = []
    for r in range(5):
        row = grid[r]
        for sym in set(row):
            if row.count(sym) >= 3:
                win_coords.append((r, sym))
    return win_coords

# Tampilkan grid
def display_grid(grid, wins):
    for r, row in enumerate(grid):
        line = ""
        for sym in row:
            color = colors[sym]
            if any(r == win_r and sym == win_sym for win_r, win_sym in wins):
                line += f"<span style='color:{color};font-size:30px;'><b>{sym}</b></span> "
            else:
                line += f"<span style='color:gray;font-size:26px;'>{sym}</span> "
        st.markdown(f"<div style='text-align:center;'>{line}</div>", unsafe_allow_html=True)

if st.button("🎰 SPIN SEKARANG"):
    if st.session_state.saldo < bet:
        st.error("Saldo tidak cukup!")
    else:
        st.session_state.saldo -= bet
        grid = spin_grid()
        wins = check_win(grid)
        display_grid(grid, wins)

        if wins:
            total_win = bet * len(wins) * multiplier
            st.success(f"🎉 MENANG x{multiplier}! Total: +{total_win}")
            st.session_state.saldo += total_win
            st.balloons()
        else:
            st.warning("😢 Belum menang!")

if st.button("🔄 Reset Game"):
    st.session_state.saldo = 2000
    st.info("Game di-reset. Saldo kembali ke 2000.")
