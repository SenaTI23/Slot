import streamlit as st
import os
import tempfile
import shutil
import zipfile
from PIL import Image
import subprocess
import fitz  # PyMuPDF for PDFs

st.set_page_config(page_title="📦 Universal File Compressor", layout="centered")

st.title("📦 Universal File Compressor")
st.markdown("Unggah file besar dan kompres secara otomatis tanpa merusak isi.")

uploaded_file = st.file_uploader("📁 Upload File", type=None)

compression_level = st.selectbox("Pilih level kompresi:", ["Ringan", "Sedang", "Tinggi"])

def compress_pdf(input_path, output_path):
    try:
        pdf = fitz.open(input_path)
        pdf.save(output_path, garbage=4, deflate=True)
        return True
    except Exception as e:
        st.error(f"Gagal kompres PDF: {e}")
        return False

def compress_image(input_path, output_path, quality):
    try:
        img = Image.open(input_path)
        img.save(output_path, optimize=True, quality=quality)
        return True
    except Exception as e:
        st.error(f"Gagal kompres gambar: {e}")
        return False

def compress_video(input_path, output_path, crf):
    try:
        result = subprocess.run([
            "ffmpeg", "-y", "-i", input_path,
            "-vcodec", "libx264", "-crf", str(crf),
            "-preset", "slow", output_path
        ], capture_output=True)
        return result.returncode == 0
    except Exception as e:
        st.error(f"Gagal kompres video: {e}")
        return False

def zip_file(file_path, output_path):
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(file_path, os.path.basename(file_path))
        return True
    except Exception as e:
        st.error(f"Gagal zip file: {e}")
        return False

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_input:
        tmp_input.write(uploaded_file.read())
        input_path = tmp_input.name

    original_size = os.path.getsize(input_path) / 1024 / 1024  # MB
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()

    st.info(f"Ukuran asli: {original_size:.2f} MB")
    compressed_path = input_path + "_compressed" + file_ext

    success = False

    with st.spinner("🔄 Mengompres file..."):

        if file_ext in [".pdf"]:
            success = compress_pdf(input_path, compressed_path)

        elif file_ext in [".jpg", ".jpeg", ".png", ".webp"]:
            q = 85 if compression_level == "Ringan" else 65 if compression_level == "Sedang" else 40
            success = compress_image(input_path, compressed_path, quality=q)

        elif file_ext in [".mp4", ".mov", ".avi", ".mkv"]:
            crf = 23 if compression_level == "Ringan" else 28 if compression_level == "Sedang" else 33
            compressed_path = input_path + "_compressed.mp4"
            success = compress_video(input_path, compressed_path, crf=crf)

        else:
            compressed_path = input_path + ".zip"
            success = zip_file(input_path, compressed_path)

    if success:
        compressed_size = os.path.getsize(compressed_path) / 1024 / 1024
        saved_percent = 100 * (1 - compressed_size / original_size)
        st.success(f"✅ Kompresi selesai! Ukuran baru: {compressed_size:.2f} MB ({saved_percent:.1f}% lebih kecil)")

        with open(compressed_path, "rb") as f:
            st.download_button("⬇️ Download File Terkompres", f, file_name=os.path.basename(compressed_path))
    else:
        st.error("❌ Gagal kompres file.")
