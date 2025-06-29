
# Membuat file app.py
code = """
import streamlit as st
import random

symbols = ["🔱", "⚡", "💎", "🔥", "💰", "👑", "🌀"]

def spin_reels():
    return [[random.choice(symbols) for _ in range(5)] for _ in range(3)]

def check_win(grid):
    for row in grid:
        if len(set(row)) == 1:
            return True
    return False

st.set_page_config(page_title="🎰 Slot Olympus Mini", layout="centered")
st.title("🎰 Slot Olympus Mini")

if 'saldo' not in st.session_state:
    st.session_state.saldo = 1000

bet = 100
st.markdown(f"💰 **Saldo kamu: {st.session_state.saldo}**  \\n🎯 Taruhan per spin: {bet}")

if st.button("🔁 Spin Sekarang"):
    if st.session_state.saldo < bet:
        st.error("💸 Saldo tidak cukup!")
    else:
        st.session_state.saldo -= bet
        hasil = spin_reels()
        st.markdown("### 🎰 Hasil:")
        for row in hasil:
            st.write(" | ".join(row))
        if check_win(hasil):
            menang = bet * 5
            st.success(f"🎉 Kamu MENANG! +{menang}")
            st.session_state.saldo += menang
        else:
            st.warning("😢 Belum beruntung.")

if st.button("🔄 Reset Game"):
    st.session_state.saldo = 1000
    st.info("🔁 Game di-reset! Saldo kembali ke 1000.")
"""

# Simpan ke file
with open("app.py", "w") as f:
    f.write(code)

# Buat tombol download
from google.colab import files
files.download("app.py")
