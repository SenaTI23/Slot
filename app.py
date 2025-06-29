import streamlit as st
import random

# Konfigurasi halaman
st.set_page_config(page_title="⚡ Olympus Slot Mini", layout="centered")

# Simbol & nilainya
basic_symbols = ["⚡", "💎", "🔥", "💰", "👑", "🌀", "🔱"]
scatter_symbol = "🟡"
multiplier_symbols = ["🔵2x", "🔵5x", "🔵10x", "🔵25x", "🔵50x", "🔵100x", "🔵500x"]

symbol_values = {
    "⚡": 1,
    "💎": 2,
    "🔥": 3,
    "💰": 5,
    "👑": 7,
    "🌀": 4,
    "🔱": 10
}

# Inisialisasi session state
for key, val in {
    "saldo": 10000,
    "bet": 100,
    "freespin": 0,
    "total_win": 0,
    "spin_count": 0
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Sidebar pengaturan taruhan
st.sidebar.title("🎚️ Pengaturan Taruhan")
st.session_state.bet = st.sidebar.slider("BET", 50, 1000, st.session_state.bet, 50)

# Tampilkan info utama
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
    # Tambah multiplier jika free spin
    if free_spin:
        for _ in range(random.randint(1, 4)):
            r, c = random.randint(0, 4), random.randint(0, 5)
            grid[r][c] = random.choice(multiplier_symbols)
    return grid

# Hitung scatter
def count_scatters(grid):
    return sum(sym == scatter_symbol for row in grid for sym in row)

# Cek kombinasi menang
def get_matches(grid, win_boost=1.0):
    matches = []
    for r in range(5):
        count = 1
        for c in range(1, 6):
            curr, prev = grid[r][c], grid[r][c - 1]
            if curr == prev and curr in symbol_values:
                count += 1
            else:
                if count >= 3 and random.random() < win_boost:
                    matches.append((prev, count))
                count = 1
        if count >= 3 and random.random() < win_boost:
            matches.append((grid[r][5], count))
    return matches

# Hitung multiplier dari grid
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

# Fungsi spin
def do_spin():
    st.session_state.spin_count += 1

    # Dinamika kemenangan makin sulit
    if st.session_state.spin_count <= 10:
        win_boost = 1.0
    elif st.session_state.spin_count <= 30:
        win_boost = 0.7
    else:
        win_boost = 0.3

    free = False
    if st.session_state.freespin > 0:
        st.session_state.freespin -= 1
        free = True
        win_boost = 0.8
    else:
        if st.session_state.saldo < st.session_state.bet:
            st.warning("💸 Saldo tidak cukup!")
            return
        st.session_state.saldo -= st.session_state.bet

    grid = spin(free)
    show_grid(grid)

    scatters = count_scatters(grid)
    matches = get_matches(grid, win_boost)
    multiplier = get_multiplier(grid) if free else 1

    # Hitung kemenangan
    win = 0
    for sym, count in matches:
        base = symbol_values.get(sym, 1)
        win += base * count * (st.session_state.bet // 10)
    win *= multiplier

    # Tambah proteksi agar tidak kalah terus
    if win == 0 and st.session_state.spin_count > 5 and random.random() < 0.4:
        fake_symbol = random.choice(list(symbol_values.keys()))
        fake_win = symbol_values[fake_symbol] * 3 * (st.session_state.bet // 10)
        st.session_state.saldo += fake_win
        st.session_state.total_win = fake_win
        st.success(f"🎉 Menang {fake_win} (bonus acak)")
        return

    st.session_state.saldo += win
    st.session_state.total_win = win

    if win > 0:
        st.success(f"🎉 Menang {win}! x{multiplier}")
    else:
        st.info("😢 Tidak ada kemenangan.")

    if scatters >= 4 and not free:
        st.success(f"🟡 {scatters} SCATTER! Dapat 15 Free Spins!")
        st.session_state.freespin += 15

# Tombol kontrol
col1, col2 = st.columns(2)
with col1:
    if st.button("🎰 SPIN"):
        do_spin()
with col2:
    if st.button("🔄 Reset Game"):
        for key in ["saldo", "bet", "freespin", "total_win", "spin_count"]:
            st.session_state[key] = 10000 if key == "saldo" else 0
