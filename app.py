import streamlit as st
import chess
import chess.svg
import base64
import io

# Fungsi untuk menampilkan papan catur
def render_board(board):
    svg = chess.svg.board(board=board)
    return f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg.encode("utf-8")).decode("utf-8")}"/>'

# Inisialisasi session state untuk papan
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

st.title("♟️ Game Catur Sederhana")

# Tampilkan papan catur
st.markdown(render_board(st.session_state.board), unsafe_allow_html=True)

# Form untuk input langkah
with st.form("move_form"):
    col1, col2 = st.columns(2)
    with col1:
        move_input = st.text_input("Masukkan langkah (misal: e2e4)", max_chars=5)
    with col2:
        submit = st.form_submit_button("Jalankan Langkah")

if submit:
    try:
        move = chess.Move.from_uci(move_input)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
        else:
            st.warning("Langkah tidak valid.")
    except:
        st.warning("Format langkah salah. Gunakan format seperti e2e4.")

# Tombol reset
if st.button("🔄 Reset Papan"):
    st.session_state.board = chess.Board()

# Info status permainan
if st.session_state.board.is_checkmate():
    st.success("Skakmat! Permainan selesai.")
elif st.session_state.board.is_stalemate():
    st.info("Stalemate! Seri.")
elif st.session_state.board.is_insufficient_material():
    st.info("Remis karena material tidak cukup.")
elif st.session_state.board.is_check():
    st.warning("Skak!")
