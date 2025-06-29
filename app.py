import streamlit as st
import random
import time

# Setup halaman
st.set_page_config(page_title="Gates of Olympus Mini", layout="centered")
st.markdown("<h1 style='text-align:center;'>🎰 Gates of Olympus Mini</h1>", unsafe_allow_html=True)

# Simbol & warna
symbols = ["⚡", "💎", "🔥", "💰", "👑", "🌀", "🔱"]
colors = {"⚡": "gold", "💎": "cyan", "🔥": "red", "💰": "orange", "👑": "purple", "🌀": "blue", "🔱": "green"}

# Inisialisasi state
if 'saldo' not in st.session_state:
    st.session_state.saldo = 10000
if 'freespins' not in st.session_state:
    st.session_state.freespins = 0
if 'last_win' not in st.session_state:
    st.session_state.last_win = 0
if 'bet' not in st.session_state:
    st.session_state.bet = 100

# Sidebar kontrol taruhan
st.sidebar.header("🎚️ Kontrol Taruhan")
bet_input = st.sidebar.slider("Pilih jumlah taruhan (BET)", min_value=50, max_value=1000, step=50, value=st.session_state.bet)
st.session_state.bet = bet_input

# Tampilkan saldo & info
st.markdown(f"""
<b>💰 Saldo:</b> {st.session_state.saldo}  
<b>🎯 Taruhan:</b> {st.session_state.bet}  
<b>🎁 Free Spins:</b> {st.session_state.freespins}  
<b>🏆 Menang Terakhir:</b> {st.session_state.last_win}  
""", unsafe_allow_html=True)

# Fungsi untuk membuat grid slot
def spin_grid():
    return [[random.choice(symbols) for _ in range(6)] for _ in range(5)]

# Fungsi cek kombinasi menang
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
                        matches += [(r, cc) for cc in range(c - count, c)]
                    count = 0
            if count >= 3:
                matches += [(r, cc) for cc in range(6 - count, 6)]
    return matches

# Tampilkan animasi koin
def show_coin_animation():
    st.markdown("""
    <div style="text-align:center;">
      <img src="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif" width="200"/>
    </div>
    """, unsafe_allow_html=True)

# Tampilkan grid dengan efek menang
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

# Fungsi jatuhkan simbol (tumble)
def tumble(grid, matches):
    cols = {}
    for r, c in matches:
        cols.setdefault(c, []).append(r)
    for c, rows in cols.items():
        rows.sort()
        for r in rows:
            for i in range(r, 0, -1):
                grid[i][c] = grid[i - 1][c]
            grid[0][c] = random.choice(symbols)
    return grid

# Fungsi utama spin
def play_spin():
    st.session_state.saldo -= st.session_state.bet
    grid = spin_grid()
    total_win = 0
    had_match = False

    while True:
        matches = check_matches(grid)
        display_and_animate(grid, matches)
        if not matches:
            break
        had_match = True
        win_piece = len(matches) * (st.session_state.bet // 10)
        total_win += win_piece
        st.write(f"⚡ Matched {len(matches)} simbol → +{win_piece}")
        grid = tumble(grid, matches)

    # Multiplier 30% saat menang
    if had_match and random.random() < 0.3:
        mul = random.choice([2, 3, 5, 10, 25])
        total_win *= mul
        st.markdown(f"<h3 style='color:gold;'>🔥 Multiplier x{mul}! Total Menang: +{total_win}</h3>", unsafe_allow_html=True)
    elif had_match:
        st.markdown(f"<h4 style='color:lime;'>Total Menang: +{total_win}</h4>", unsafe_allow_html=True)

    # Scatter Free Spin
    if random.random() < 0.1:
        fs = random.randint(1, 3)
        st.session_state.freespins += fs
        st.balloons()
        st.success(f"🎉 Scatter! +{fs} Free Spins")

    st.session_state.last_win = total_win
    return total_win

# Tombol spin
if st.session_state.freespins > 0:
    if st.button("🔁 Free Spin"):
        st.session_state.freespins -= 1
        win = play_spin()
        st.session_state.saldo += win
else:
    if st.button("▶️ Spin"):
        if st.session_state.saldo >= st.session_state.bet:
            win = play_spin()
            st.session_state.saldo += win
        else:
            st.warning("Saldo tidak cukup untuk taruhan.")

if st.button("🔄 Reset Game"):
    st.session_state.saldo = 10000
    st.session_state.freespins = 0
    st.session_state.last_win = 0
    st.success("Game telah di-reset.")
