import streamlit as st
import random
import time

# Streamlit setup
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

bet = 100
mult = random.choice([2,3,5,10,20,50,100,200,500])

# Header info
st.markdown(f"""
**Saldo:** {st.session_state.saldo} &nbsp; | &nbsp;
**Bet:** {bet} &nbsp; | &nbsp;
**Multiplier:** x{mult} &nbsp; | &nbsp;
**Free Spins:** {st.session_state.freespins}
""")

# Fungsi spin & tumble
def spin_grid():
    return [[random.choice(symbols) for _ in range(6)] for _ in range(5)]

def check_matches(grid):
    matches = []
    for r in range(5):
        for sym in symbols:
            cnt = grid[r].count(sym)
            if cnt >= 3:
                for c in range(6):
                    if grid[r][c]==sym:
                        matches.append((r,c))
    return matches

def tumble(grid, matches):
    # Hapus matches: replace with random above
    for r,c in sorted(matches):
        for rr in range(r,0,-1):
            grid[rr][c]=grid[rr-1][c]
        grid[0][c]=random.choice(symbols)
    return grid

def display(grid, matches):
    for r in range(5):
        line = ""
        for c in range(6):
            sym = grid[r][c]
            col = colors[sym]
            if (r,c) in matches:
                line += f"<span style='color:{col};font-size:32px;'><b>{sym}</b></span> "
            else:
                line += f"<span style='color:gray;font-size:24px;'>{sym}</span> "
        st.markdown(f"<div style='text-align:center'>{line}</div>", unsafe_allow_html=True)

# Spin atau FreeSpin
def play_spin():
    st.session_state.saldo -= bet
    total_mult = mult
    win = 0
    grid = spin_grid()
    step = 1
    
    while True:
        matches = check_matches(grid)
        display(grid, matches)
        if not matches:
            break
        step_win = len(matches)*bet*total_mult
        win += step_win
        st.write(f"Step {step}: matched {len(matches)} symbols → +{step_win}")
        grid = tumble(grid, matches)
        step += 1
        time.sleep(0.3)

    # Scatter FreeSpin random: 10% chance
    if random.random()<0.1:
        fs = random.randint(1,3)
        st.balloons()
        st.write(f"🎉 Scatter! Kamu dapat {fs} Free Spins!")
        st.session_state.freespins += fs

    return win

# Tombol play
if st.session_state.freespins>0:
    if st.button("🔁 Free Spin"):
        st.session_state.freespins -= 1
        win = play_spin()
        st.success(f"Free Spin Win: +{win}")
        st.session_state.saldo += win
else:
    if st.button("🔁 Spin"):
        win = play_spin()
        st.success(f"Win: +{win}")
        st.session_state.saldo += win

if st.button("🔄 Reset Game"):
    st.session_state.saldo=10000
    st.session_state.freespins=0
    st.success("Game Reset")
