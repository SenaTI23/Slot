import streamlit as st
import random
import time

st.set_page_config(page_title="Gates of Olympus Mini", layout="centered")
st.markdown("<h1 style='text-align:center;'>⚡ Gates of Olympus Mini ⚡</h1>", unsafe_allow_html=True)

symbols = ["⚡", "💎", "🔥", "💰", "👑", "🌀", "🔱"]
colors = {"⚡": "gold", "💎": "cyan", "🔥": "red", "💰": "orange", "👑": "purple", "🌀": "blue", "🔱": "green"}

# Inisialisasi session
if 'saldo' not in st.session_state:
    st.session_state.saldo = 10000
if 'freespins' not in st.session_state:
    st.session_state.freespins = 0
if 'last_win' not in st.session_state:
    st.session_state.last_win = 0
if 'bet' not in st.session_state:
    st.session_state.bet = 100

# Sidebar pengaturan
st.sidebar.header("🎚️ Taruhan & Mode")
st.session_state.bet = st.sidebar.slider("Taruhan (BET)", 50, 1000, 100, step=50)

# Tampilan Info
st.markdown(f"""
**💰 Saldo:** {st.session_state.saldo}  
**🎁 Free Spins:** {st.session_state.freespins}  
**🏆 Menang Terakhir:** {st.session_state.last_win}
""")

# Fungsi spin
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

# Tampilkan grid
def show_grid(grid, matches):
    for r in range(5):
        row_html = ""
        for c in range(6):
            sym = grid[r][c]
            color = colors[sym]
            if (r, c) in matches:
                row_html += f"<span style='color:{color};font-size:38px;'>💥</span> "
            else:
                row_html += f"<span style='color:{color};font-size:30px;'>{sym}</span> "
        st.markdown(f"<div style='text-align:center'>{row_html}</div>", unsafe_allow_html=True)
        time.sleep(0.1)

# Spin
def spin():
    grid = spin_grid()
    matches = check_matches(grid)
    show_grid(grid, matches)

    if matches:
        base_win = len(matches) * (st.session_state.bet // 10)
        multiplier = random.choice([1, 2, 3, 5, 10]) if random.random() < 0.3 else 1
        total_win = base_win * multiplier
        st.session_state.saldo += total_win
        st.session_state.last_win = total_win

        st.success(f"🎉 Menang {base_win} x{multiplier} = {total_win}!")
        st.audio("assets/win.mp3")
        if multiplier > 1:
            st.image("assets/zeus.gif", width=200)
    else:
        st.session_state.last_win = 0
        st.info("😢 Belum Beruntung.")
    return matches

# Tombol aksi
if st.session_state.freespins > 0:
    if st.button("🔁 Free Spin"):
        st.session_state.freespins -= 1
        spin()
else:
    if st.button("▶️ SPIN"):
        if st.session_state.saldo >= st.session_state.bet:
            st.session_state.saldo -= st.session_state.bet
            spin()
        else:
            st.error("Saldo tidak cukup!")

# Reset
if st.button("🔄 Reset Game"):
    st.session_state.saldo = 10000
    st.session_state.freespins = 0
    st.session_state.last_win = 0
