import os
import tempfile
import zipfile
import streamlit as st
from PIL import Image
import fitz  # PyMuPDF
import subprocess

def compress_pdf(input_path, output_path):
    pdf = fitz.open(input_path)
    pdf.save(output_path, garbage=4, deflate=True)
    return os.path.getsize(output_path)

def compress_image(input_path, output_path, quality, resize_ratio=1.0):
    img = Image.open(input_path).convert("RGB")
    if resize_ratio < 1.0:
        img = img.resize((int(img.width * resize_ratio), int(img.height * resize_ratio)))
    img.save(output_path, optimize=True, quality=quality)
    return os.path.getsize(output_path)

def compress_video(input_path, output_path, crf):
    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-vcodec', 'libx264', '-crf', str(crf),
        '-preset', 'veryslow', output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.getsize(output_path)

def compress_audio(input_path, output_path, bitrate):
    subprocess.run([
        'ffmpeg', '-y', '-i', input_path,
        '-b:a', bitrate, output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.getsize(output_path)

def zip_file(input_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(input_path, os.path.basename(input_path))
    return os.path.getsize(output_path)

def compress_with_target(input_path, target_mb):
    input_ext = os.path.splitext(input_path)[1].lower()
    base = os.path.basename(input_path)
    out_dir = tempfile.gettempdir()
    output_path = os.path.join(out_dir, "compressed_" + base)

    original_size = os.path.getsize(input_path) / 1024 / 1024
    target_ratio = target_mb / original_size

    if input_ext in ['.pdf']:
        compress_pdf(input_path, output_path)

    elif input_ext in ['.jpg', '.jpeg', '.png', '.webp']:
        if target_ratio > 0.8:
            quality, resize = 85, 1.0
        elif target_ratio > 0.5:
            quality, resize = 60, 0.9
        elif target_ratio > 0.2:
            quality, resize = 40, 0.8
        else:
            quality, resize = 25, 0.6
        compress_image(input_path, output_path, quality, resize)

    elif input_ext in ['.mp4', '.mov', '.avi', '.mkv']:
        if target_ratio > 0.8:
            crf = 22
        elif target_ratio > 0.5:
            crf = 28
        elif target_ratio > 0.2:
            crf = 35
        else:
            crf = 40
        output_path = output_path.replace(input_ext, ".mp4")
        compress_video(input_path, output_path, crf)

    elif input_ext in ['.mp3', '.wav', '.ogg', '.aac']:
        if target_ratio > 0.8:
            bitrate = "192k"
        elif target_ratio > 0.5:
            bitrate = "128k"
        elif target_ratio > 0.2:
            bitrate = "64k"
        else:
            bitrate = "32k"
        output_path = output_path.replace(input_ext, ".mp3")
        compress_audio(input_path, output_path, bitrate)

    else:
        output_path += ".zip"
        zip_file(input_path, output_path)

    return output_path, original_size

# ================= STREAMLIT UI =================

st.title("📦 File Compressor with Target Size")
st.write("Upload file besar dan masukkan ukuran target (MB). Kami akan kompres otomatis!")

uploaded = st.file_uploader("📁 Upload File", type=None)
target_size = st.number_input("🎯 Target Ukuran File (MB)", min_value=1.0, step=1.0)

if uploaded and target_size:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    with st.spinner("🔄 Mengompres file..."):
        output_path, original_size = compress_with_target(tmp_path, target_size)
        final_size = os.path.getsize(output_path) / 1024 / 1024

    st.success(f"✅ Selesai! Ukuran awal: {original_size:.2f} MB → hasil: {final_size:.2f} MB")
    with open(output_path, "rb") as f:
        st.download_button("⬇️ Download File Terkompres", f, file_name=os.path.basename(output_path))
