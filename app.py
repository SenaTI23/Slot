import streamlit as st
import random

# Daftar simbol seperti di game slot Olympus
symbols = ["🔱", "⚡", "💎", "🔥", "💰", "👑", "🌀"]

# Fungsi spin: 3 baris × 5 kolom
def spin_reels():
    return [[random.choice(symbols) for _ in range(5)] for _ in range(3)]

# Cek kemenangan: semua simbol di 1 baris sama
def check_win(grid):
    for row in grid:
        if len(set(row)) == 1:
            return True
    return False

# Set konfigurasi halaman
st.set_page_config(page_title="🎰 Slot Olympus Mini", layout="centered")
st.title("🎰 Slot Olympus Mini")

# Inisialisasi saldo
if 'saldo' not in st.session_state:
    st.session_state.saldo = 1000

bet = 100
st.markdown(
    f"💰 **Saldo kamu: {st.session_state.saldo}**  <br>🎯 Taruhan per spin: {bet}",
    unsafe_allow_html=True
)

# Tombol SPIN
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

# Tombol Reset
if st.button("🔄 Reset Game"):
    st.session_state.saldo = 1000
    st.info("🔁 Game di-reset! Saldo kembali ke 1000.")
