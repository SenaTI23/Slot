import streamlit as st
import random

# Atur halaman
st.set_page_config(page_title="⚡ Olympus Mini", layout="centered")

# Simbol-simbol
basic_symbols = ["⚡", "💎", "🔥", "💰", "👑", "🌀", "🔱"]
scatter_symbol = "🟡"
multiplier_symbols = ["🔵2x", "🔵5x", "🔵10x", "🔵25x", "🔵50x", "🔵100x", "🔵500x"]

# Streamlit states
if "saldo" not in st.session_state:
    st.session_state.saldo = 10000
if "bet" not in st.session_state:
    st.session_state.bet = 100
if "freespin" not in st.session_state:
    st.session_state.freespin = 0
if "total_win" not in st.session_state:
    st.session_state.total_win = 0
if "spin_count" not in st.session_state:
    st.session_state.spin_count = 0

# Sidebar pengaturan
st.sidebar.title("🎚️ Pengaturan Taruhan")
st.session_state.bet = st.sidebar.slider("BET", 50, 1000, st.session_state.bet, 50)

# Header UI
st.title("⚡ Olympus Mini Slot")
st.markdown(f"""
**💰 Saldo:** `{st.session_state.saldo}`  
**🎯 Taruhan:** `{st.session_state.bet}`  
**🔁 Free Spin:** `{st.session_state.freespin}`  
**🏆 Menang Terakhir:** `{st.session_state.total_win}`
""")

# Fungsi spin grid
def spin(free_spin=False):
    grid = []
    for _ in range(5):  # baris
        row = []
        for _ in range(6):  # kolom
            if free_spin:
                sym = random.choice(basic_symbols)
                row.append(sym)
            else:
                sym = random.choices(
                    basic_symbols + [scatter_symbol],
                    weights=[12]*len(basic_symbols) + [1]
                )[0]
                row.append(sym)
        grid.append(row)
    # Tambah multiplier acak jika free spin
    if free_spin:
        for _ in range(random.randint(1, 4)):
            r = random.randint(0, 4)
            c = random.randint(0, 5)
            row_symbol = random.choice(multiplier_symbols)
            grid[r][c] = row_symbol
    return grid

# Hitung scatter
def count_scatters(grid):
    return sum(sym == scatter_symbol for row in grid for sym in row)

# Cek kemenangan dengan win_boost dinamis
def get_matches(grid, win_boost=1.0):
    matches = []
    for r in range(5):
        count = 1
        for c in range(1, 6):
            if grid[r][c] == grid[r][c - 1] and grid[r][c] in basic_symbols:
                count += 1
            else:
                if count >= 3 and random.random() < win_boost:
                    matches.append((grid[r][c - 1], count))
                count = 1
        if count >= 3 and random.random() < win_boost:
            matches.append((grid[r][5], count))
    return matches

# Hitung total multiplier
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
        st.markdown(f"<div style='text-align:center; font-size:30px'>{' '.join(row)}</div>", unsafe_allow_html=True)

# Proses SPIN
def do_spin():
    st.session_state.spin_count += 1

    if st.session_state.spin_count <= 10:
        win_boost = 1.0  # awal: gampang menang
    elif st.session_state.spin_count <= 30:
        win_boost = 0.7
    else:
        win_boost = 0.3  # makin susah

    if st.session_state.freespin > 0:
        free = True
        st.session_state.freespin -= 1
        win_boost = 0.8
    else:
        free = False
        if st.session_state.saldo < st.session_state.bet:
            st.warning("💸 Saldo tidak cukup untuk spin.")
            return
        st.session_state.saldo -= st.session_state.bet

    grid = spin(free)
    show_grid(grid)

    scatters = count_scatters(grid)
    matches = get_matches(grid, win_boost)
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
        st.success(f"🟡 {scatters} SCATTER! Dapat 15 Free Spins!")
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
        st.session_state.spin_count = 0
