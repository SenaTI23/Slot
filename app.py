import streamlit as st
import random
import time

# Setup awal
st.set_page_config(page_title="Gates of Olympus Mini", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Gates of Olympus Mini</h1>", unsafe_allow_html=True)

# Simbol dan warna
symbols = ["⚡","💎","🔥","💰","👑","🌀","🔱"]
colors = {"⚡":"gold","💎":"cyan","🔥":"red","💰":"orange","👑":"purple","🌀":"blue","🔱":"green"}

# Inisialisasi state
if 'saldo' not in st.session_state:
    st.session_state.saldo = 10000
if 'freespins' not in st.session_state:
    st.session_state.freespins = 0

# Konstanta
bet = 100

# Header info
st.markdown(f"""
**Saldo:** {st.session_state.saldo} &nbsp; | &nbsp;
**Bet:** {bet} &nbsp; | &nbsp;
**Free Spins:** {st.session_state.freespins}
""")

# Fungsi grid
def spin_grid():
    return [[random.choice(symbols) for _ in range(6)] for _ in range(5)]

# Cek kemenangan
def check_matches(grid):
    matches = []
    for r in range(5):
        for sym in symbols:
            count = 0
            for c in range(6):
                if grid[r][c] == sym:
                    count += 1
                else:
                    if count >= 3:
                        for i in range(c - count, c):
                            matches.append((r, i))
                    count = 0
            if count >= 3:
                for i in range(6 - count, 6):
                    matches.append((r, i))
    return matches

# Tumble: Geser ke bawah
def tumble(grid, matches):
    for r, c in sorted(matches):
        for rr in range(r, 0, -1):
            grid[rr][c] = grid[rr - 1][c]
        grid[0][c] = random.choice(symbols)
    return grid

# Tampilan grid
def display(grid, matches):
    for r in range(5):
        line = ""
        for c in range(6):
            sym = grid[r][c]
            col = colors[sym]
            if (r, c) in matches:
                line += f"<span style='color:{col};font-size:32px;'><b>{sym}</b></span> "
            else:
                line += f"<span style='color:gray;font-size:24px;'>{sym}</span> "
        st.markdown(f"<div style='text-align:center'>{line}</div>", unsafe_allow_html=True)

# Fungsi Spin
def play_spin():
    st.session_state.saldo -= bet
    grid = spin_grid()
    win = 0
    step = 1
    had_match = False

    while True:
        matches = check_matches(grid)
        display(grid, matches)
        if not matches:
            break
        had_match = True
        step_win = len(matches) * bet
        win += step_win
        st.write(f"Step {step}: matched {len(matches)} symbols → +{step_win}")
        grid = tumble(grid, matches)
        step += 1
        time.sleep(0.3)

    # Multiplier hanya jika menang dan 30% chance
    if had_match and random.random() < 0.3:
        multiplier = random.choice([2, 3, 5, 10, 25, 50, 100, 250, 500])
        win *= multiplier
        st.markdown(f"<h3 style='color:gold;'>🔥 Multiplier x{multiplier} Aktif! Total Menang: +{win}</h3>", unsafe_allow_html=True)
    elif had_match:
        st.markdown(f"<h4 style='color:lime;'>Total Menang (tanpa multiplier): +{win}</h4>", unsafe_allow_html=True)

    # Scatter: peluang 10% dapat Free Spin
    if random.random() < 0.1:
        fs = random.randint(1, 3)
        st.balloons()
        st.success(f"🎉 Scatter! Kamu mendapatkan {fs} Free Spins!")
        st.session_state.freespins += fs

    return win

# Tombol aksi
if st.session_state.freespins > 0:
    if st.button("🔁 Free Spin"):
        st.session_state.freespins -= 1
        win = play_spin()
        st.session_state.saldo += win
else:
    if st.button("🔁 Spin"):
        win = play_spin()
        st.session_state.saldo += win

if st.button("🔄 Reset Game"):
    st.session_state.saldo = 10000
    st.session_state.freespins = 0
    st.success("Game di-reset ke saldo awal.")
