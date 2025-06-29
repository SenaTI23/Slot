import streamlit as st
import random
import time

# Simbol & Warna
symbol_colors = {
    "⚡": "yellow",
    "💎": "cyan",
    "🔥": "red",
    "💰": "orange",
    "👑": "gold",
    "🌀": "purple",
    "🔱": "green"
}
symbols = list(symbol_colors.keys())

# Konfigurasi Streamlit
st.set_page_config(page_title="⚡ Olympus Slot", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 SLOT OLYMPUS</h1>", unsafe_allow_html=True)

# Inisialisasi saldo
if "saldo" not in st.session_state:
    st.session_state.saldo = 1000

bet = 100
st.markdown(
    f"<div style='text-align:center;font-size:18px;'>💰 <b>Saldo:</b> {st.session_state.saldo} &nbsp;&nbsp; | &nbsp;&nbsp; 🎯 <b>Taruhan:</b> {bet}</div><br>",
    unsafe_allow_html=True
)

# Spin Reels
def spin_reels():
    return [[random.choice(symbols) for _ in range(5)] for _ in range(3)]

# Cek kemenangan: jika semua simbol dalam 1 baris sama
def check_win(grid):
    winning_rows = []
    for idx, row in enumerate(grid):
        if len(set(row)) == 1:
            winning_rows.append(idx)
    return winning_rows

# Tampilkan grid dengan highlight kemenangan
def display_grid(grid, win_rows):
    for i, row in enumerate(grid):
        line = ""
        for sym in row:
            color = symbol_colors[sym]
            if i in win_rows:
                line += f"<span style='color:{color};font-size:28px;'><b>{sym}</b></span> "
            else:
                line += f"<span style='color:gray;font-size:24px;'>{sym}</span> "
        st.markdown(f"<div style='text-align:center;'>{line}</div>", unsafe_allow_html=True)

# Tombol SPIN
if st.button("🔁 SPIN!"):
    if st.session_state.saldo < bet:
        st.error("💸 Saldo tidak cukup!")
    else:
        st.session_state.saldo -= bet
        hasil = spin_reels()
        win_rows = check_win(hasil)

        st.markdown("### 🎰 Hasil:")
        display_grid(hasil, win_rows)

        if win_rows:
            menang = bet * 5 * len(win_rows)
            st.success(f"🎉 Kemenangan di {len(win_rows)} baris! +{menang}")
            st.session_state.saldo += menang
            st.balloons()
        else:
            st.warning("😢 Belum beruntung.")

# Tombol Reset
if st.button("🔄 Reset Game"):
    st.session_state.saldo = 1000
    st.info("🔁 Game di-reset! Saldo kembali ke 1000.")
