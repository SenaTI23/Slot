import os
import zipfile
import tempfile
from PIL import Image
import fitz
import subprocess

def compress_pdf(input_path, output_path):
    pdf = fitz.open(input_path)
    pdf.save(output_path, garbage=4, deflate=True)
    return os.path.getsize(output_path)

def compress_image(input_path, output_path, quality, resize_ratio=1.0):
    img = Image.open(input_path)
    img = img.convert("RGB")
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

    original_size = os.path.getsize(input_path) / 1024 / 1024  # in MB
    target_ratio = target_mb / original_size

    print(f"📥 Original: {original_size:.2f} MB | 🎯 Target: {target_mb:.2f} MB")

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

    final_size = os.path.getsize(output_path) / 1024 / 1024
    print(f"✅ Hasil akhir: {final_size:.2f} MB")
    print(f"📁 Lokasi: {output_path}")
    return output_path

# ======== Contoh penggunaan ========
# Ganti path ke file kamu
file_path = "/content/video_200mb.mp4"
target_size_mb = 20  # Target hasil kompresi

compress_with_target(file_path, target_size_mb)
