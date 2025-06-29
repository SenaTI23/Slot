import streamlit as st
import random
import time

# Konfigurasi halaman
st.set_page_config(page_title="⚡ Gates of Olympus Mini", layout="centered")

# Inisialisasi session state
if 'saldo' not in st.session_state:
    st.session_state.saldo = 10000
if 'bet' not in st.session_state:
    st.session_state.bet = 100
if 'freespin' not in st.session_state:
    st.session_state.freespin = 0
if 'total_win' not in st.session_state:
    st.session_state.total_win = 0

# Simbol
basic_symbols = ["⚡", "💎", "🔥", "💰", "👑", "🌀", "🔱"]
scatter_symbol = "🟡"
multiplier_symbols = ["🔵2x", "🔵5x", "🔵10x", "🔵25x", "🔵50x", "🔵100x", "🔵500x"]

def get_symbol_pool(free_mode=False):
    pool = basic_symbols + [scatter_symbol]*2  # scatter agak langka
    if free_mode:
        pool += multiplier_symbols * 2  # multiplier lebih banyak di free spin
    return pool

# UI Atas
st.title("⚡ Gates of Olympus Mini")
st.markdown(f"""
**💰 Saldo:** `{st.session_state.saldo}`  
**🎯 Taruhan:** `{st.session_state.bet}`  
**🔁 Free Spins Tersisa:** `{st.session_state.freespin}`  
**🏆 Menang Terakhir:** `{st.session_state.total_win}`
""")

# Sidebar Bet
st.sidebar.header("🎚️ Pengaturan Taruhan")
st.session_state.bet = st.sidebar.slider("Pilih Taruhan", 50, 1000, st.session_state.bet, 50)

# Fungsi spin
def spin(free_spin=False):
    grid = []
    pool = get_symbol_pool(free_spin)
    for _ in range(5):
        row = [random.choice(pool) for _ in range(6)]
        grid.append(row)
    return grid

# Cek scatter
def count_scatters(grid):
    return sum(sym == scatter_symbol for row in grid for sym in row)

# Cek kombinasi (sederhana: 3 simbol sama di baris)
def get_matches(grid):
    matches = []
    for r in range(5):
        count = 1
        for c in range(1, 6):
            if grid[r][c] == grid[r][c - 1] and grid[r][c] in basic_symbols:
                count += 1
            else:
                if count >= 3:
                    matches.append((grid[r][c - 1], count))
                count = 1
        if count >= 3:
            matches.append((grid[r][5], count))
    return matches

# Dapatkan multiplier total
def get_multiplier(grid):
    total = 1
    for row in grid:
        for sym in row:
            if sym.startswith("🔵"):
                try:
                    x = int(sym[2:-1])
                    total += x
                except:
                    pass
    return total

# Tampilkan grid
def show_grid(grid):
    for row in grid:
        line = " ".join(row)
        st.markdown(f"<div style='text-align:center; font-size:32px'>{line}</div>", unsafe_allow_html=True)

# Main aksi spin
def do_spin():
    if st.session_state.freespin > 0:
        free = True
        st.session_state.freespin -= 1
    else:
        free = False
        if st.session_state.saldo < st.session_state.bet:
            st.warning("Saldo tidak cukup untuk taruhan.")
            return
        st.session_state.saldo -= st.session_state.bet

    grid = spin(free)
    show_grid(grid)

    scatters = count_scatters(grid)
    matches = get_matches(grid)
    multiplier = get_multiplier(grid) if free else 1

    win = sum(count * (st.session_state.bet // 10) for _, count in matches)
    win *= multiplier

    st.session_state.saldo += win
    st.session_state.total_win = win

    if win > 0:
        st.success(f"🎉 Menang {win}! x{multiplier}")
    else:
        st.info("😢 Tidak ada kemenangan.")

    if scatters >= 4 and not free:
        st.success(f"🎁 {scatters} SCATTER! Kamu mendapatkan 15 Free Spins!")
        st.session_state.freespin += 15

# Tombol
col1, col2 = st.columns(2)
with col1:
    if st.button("🎰 SPIN / FREE SPIN"):
        do_spin()
with col2:
    if st.button("🔄 Reset Game"):
        st.session_state.saldo = 10000
        st.session_state.freespin = 0
        st.session_state.total_win = 0
