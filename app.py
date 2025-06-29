import streamlit as st
import random
import time

# Setup halaman
st.set_page_config(page_title="Gates of Olympus Mini", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Gates of Olympus Mini</h1>", unsafe_allow_html=True)

# Simbol & warna
symbols = ["⚡","💎","🔥","💰","👑","🌀","🔱"]
colors = {"⚡":"gold","💎":"cyan","🔥":"red","💰":"orange","👑":"purple","🌀":"blue","🔱":"green"}

# State initial
if 'saldo' not in st.session_state:
    st.session_state.saldo = 10000
if 'freespins' not in st.session_state:
    st.session_state.freespins = 0

bet = 100

# Header info
st.markdown(f"**Saldo:** {st.session_state.saldo} &nbsp; | &nbsp;**Bet:** {bet} &nbsp; | &nbsp;**Free Spins:** {st.session_state.freespins}")

# Fungsi grid
def spin_grid():
    return [[random.choice(symbols) for _ in range(6)] for _ in range(5)]

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
                        matches += [(r, cc) for cc in range(c-count, c)]
                    count = 0
            if count >= 3:
                matches += [(r, cc) for cc in range(6-count, 6)]
    return matches

# Animasi koin jatuh sebagai GIF
def show_coin_animation():
    st.markdown("""
    <div style="text-align:center;">
      <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" width="200"/>
    </div>
    """, unsafe_allow_html=True)

# Tampilkan grid dengan ledakan 💥 lalu animasi koin
def display_and_animate(grid, matches):
    for r in range(5):
        line = ""
        for c in range(6):
            sym = grid[r][c]
            col = colors[sym]
            if (r, c) in matches:
                line += f"<span style='color:{col};font-size:40px;'>💥</span> "
            else:
                line += f"<span style='color:{col};font-size:30px;'>{sym}</span> "
        st.markdown(f"<div style='text-align:center'>{line}</div>", unsafe_allow_html=True)
    time.sleep(0.3)
    if matches:
        show_coin_animation()
        time.sleep(0.5)

# Tumble logic jatuhkan simbol
def tumble(grid, matches):
    cols = {}
    for r, c in matches:
        cols.setdefault(c, []).append(r)
    for c, rows in cols.items():
        rows.sort()
        for r in rows:
            for i in range(r, 0, -1):
                grid[i][c] = grid[i-1][c]
            grid[0][c] = random.choice(symbols)
    return grid

# Main spin + tumble + animasi
def play_spin():
    st.session_state.saldo -= bet
    grid = spin_grid()
    total_win = 0
    had_match = False

    while True:
        matches = check_matches(grid)
        display_and_animate(grid, matches)
        if not matches:
            break
        had_match = True
        win_piece = len(matches) * bet
        total_win += win_piece
        st.write(f"⚡ Matched {len(matches)} simbol → +{win_piece}")
        grid = tumble(grid, matches)

    # Multiplier 30% saat menang
    if had_match and random.random() < 0.3:
        mul = random.choice([2, 3, 5, 10, 25, 50, 100, 250, 500])
        total_win *= mul
        st.markdown(f"<h3 style='color:gold;'>🔥 Multiplier x{mul}! Total Menang: +{total_win}</h3>", unsafe_allow_html=True)
    elif had_match:
        st.markdown(f"<h4 style='color:lime;'>Total Menang: +{total_win}</h4>", unsafe_allow_html=True)

    # Scatter Free Spin 10%
    if random.random() < 0.1:
        fs = random.randint(1, 3)
        st.session_state.freespins += fs
        st.balloons()
        st.success(f"🎉 Scatter! +{fs} Free Spins")

    return total_win

# Tombol kontrol
if st.session_state.freespins > 0:
    if st.button("🔁 Free Spin"):
        st.session_state.freespins -= 1
        win = play_spin()
        st.session_state.saldo += win
else:
    if st.button("▶️ Spin"):
        win = play_spin()
        st.session_state.saldo += win

if st.button("🔄 Reset Game"):
    st.session_state.saldo = 10000
    st.session_state.freespins = 0
    st.success("Game sudah di-reset.")
