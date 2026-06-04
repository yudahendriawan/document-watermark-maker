#!/usr/bin/env python3
import os
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def get_system_font(font_size=32):
    """
    Mencari font sistem yang tersedia untuk digunakan.
    Mendukung macOS, Windows, dan Linux.
    """
    paths = [
        # macOS
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Verdana.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        # Windows
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, font_size)
            except Exception:
                continue
    # Jika tidak ada font TTF yang ditemukan, gunakan default Pillow font
    return ImageFont.load_default()

def parse_hex_color(hex_str):
    """
    Mengubah format hex color (misal: #ffffff atau ffffff) menjadi tuple RGB.
    """
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join(c*2 for c in hex_str)
    if len(hex_str) != 6:
        return (255, 255, 255) # Fallback ke putih
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def add_watermark(
    image_path,
    text,
    output_path=None,
    opacity=30,      # Persentase 0 - 100
    angle=30,        # Derajat rotasi
    scale=0.035,     # Skala ukuran font relatif terhadap lebar gambar
    grid=True,       # Pola grid berulang
    spacing=150,     # Jarak antar grid (dalam piksel)
    font_path=None,  # Path font kustom
    color_hex="#ffffff" # Warna teks (Hex)
):
    """
    Menambahkan watermark teks ke gambar dokumen konfidensial secara lokal.
    """
    # Membuka gambar dasar
    if isinstance(image_path, str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
        base_image = Image.open(image_path)
    else:
        # Jika berupa file-like object atau PIL Image
        try:
            base_image = Image.open(image_path)
        except Exception:
            base_image = image_path
    # Konversi ke RGBA untuk proses blending transparansi
    original_mode = base_image.mode
    base_rgba = base_image.convert("RGBA")
    
    w_base, h_base = base_rgba.size
    
    # Hitung ukuran font secara dinamis berdasarkan lebar gambar
    font_size = max(12, int(w_base * scale))
    
    # Memuat font
    if font_path and os.path.exists(font_path):
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception as e:
            print(f"Gagal memuat font kustom ({e}), mencari font sistem...")
            font = get_system_font(font_size)
    else:
        font = get_system_font(font_size)
        
    # Ambil warna RGB dari hex
    color_rgb = parse_hex_color(color_hex)
    
    # Konversi opacity dari persentase (0-100) ke skala (0-255)
    alpha = int(max(0, min(100, opacity)) * 2.55)
    
    # Buat dummy image untuk menghitung ukuran teks multiline
    dummy_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    dummy_draw = ImageDraw.Draw(dummy_img)
    
    try:
        # Menggunakan multiline_textbbox jika didukung (Pillow >= 8.0.0)
        bbox = dummy_draw.multiline_textbbox((0, 0), text, font=font, align="center")
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
    except AttributeError:
        # Fallback untuk versi Pillow lama (jarang terjadi di env baru)
        # Mencoba membagi baris secara manual
        lines = text.split('\n')
        text_w = 0
        text_h = 0
        for line in lines:
            line_bbox = dummy_draw.textbbox((0, 0), line, font=font)
            text_w = max(text_w, line_bbox[2] - line_bbox[0])
            text_h += (line_bbox[3] - line_bbox[1]) + 5
            
    # Beri padding agar teks tidak terpotong saat diputar
    pad = int(font_size * 0.5)
    text_w = int(text_w + pad * 2)
    text_h = int(text_h + pad * 2)
    
    # Buat kanvas kecil untuk menggambar teks watermark sebelum dirotasi
    text_img = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    
    # Warna teks dengan alpha penuh terlebih dahulu
    full_color = color_rgb + (255,)
    
    # Gambar teks di tengah kanvas kecil
    # Offset koordinat untuk memposisikan dengan pas di dalam padding
    try:
        draw_x = pad - bbox[0] if 'bbox' in locals() else pad
        draw_y = pad - bbox[1] if 'bbox' in locals() else pad
    except Exception:
        draw_x, draw_y = pad, pad

    text_draw.multiline_text(
        (draw_x, draw_y),
        text,
        fill=full_color,
        font=font,
        align="center",
        spacing=4
    )
    
    # Rotasi teks sesuai sudut yang ditentukan
    # expand=True agar ukuran kanvas bertambah lebar menyesuaikan hasil putaran
    rotated_text = text_img.rotate(angle, expand=True, resample=Image.BICUBIC)
    
    # Terapkan transparansi/opacity pada teks yang sudah diputar
    r, g, b, a = rotated_text.split()
    a = a.point(lambda p: int(p * (alpha / 255.0)))
    rotated_text = Image.merge("RGBA", (r, g, b, a))
    
    w_rot, h_rot = rotated_text.size
    
    # Layer transparan baru seukuran gambar KTP untuk meletakkan watermark
    watermark_layer = Image.new("RGBA", base_rgba.size, (0, 0, 0, 0))
    
    if grid:
        # Pola Grid Berulang (Tile Pattern)
        # Menghitung jarak langkah perulangan
        # Jarak disesuaikan dengan ukuran teks ditambah spacing tambahan
        x_step = w_rot + spacing
        y_step = h_rot + spacing
        
        # Mulai perulangan dari koordinat negatif agar area tepi juga tertutup rapi
        for y in range(-h_rot, h_base + h_rot, y_step):
            # Baris selang-seling digeser sedikit agar pola grid lebih dinamis dan aman
            row_index = y // y_step
            x_offset = (x_step // 2) if (row_index % 2 == 1) else 0
            
            for x in range(-w_rot + x_offset, w_base + w_rot, x_step):
                watermark_layer.paste(rotated_text, (x, y), mask=rotated_text)
    else:
        # Hanya Satu Watermark di Tengah Gambar KTP
        x = (w_base - w_rot) // 2
        y = (h_base - h_rot) // 2
        watermark_layer.paste(rotated_text, (x, y), mask=rotated_text)
        
    # Gabungkan gambar dasar KTP dengan layer watermark
    watermarked_rgba = Image.alpha_composite(base_rgba, watermark_layer)
    
    # Kembalikan ke format mode asal (RGB jika JPG, RGBA jika PNG transparan)
    if original_mode == "RGB":
        result_img = watermarked_rgba.convert("RGB")
    else:
        result_img = watermarked_rgba
        
    if output_path:
        # Menentukan format penyimpanan berdasarkan ekstensi file output
        ext = os.path.splitext(output_path)[1].lower()
        if ext in ['.jpg', '.jpeg']:
            result_img.save(output_path, "JPEG", quality=95)
        elif ext == '.png':
            result_img.save(output_path, "PNG")
        else:
            result_img.save(output_path)
        return output_path
        
    return result_img

if __name__ == "__main__":
    today_str = datetime.today().strftime("%d-%m-%Y")
    default_text = f"DOKUMEN UNTUK VERIFIKASI\n[NAMA LAYANAN]\nPADA {today_str}"
    
    parser = argparse.ArgumentParser(description="Program Python Watermark Dokumen Secara Lokal & Aman")
    parser.add_argument("-i", "--input", required=True, help="Path file gambar dokumen input")
    parser.add_argument("-o", "--output", required=True, help="Path file gambar dokumen hasil output")
    parser.add_argument("-t", "--text", default=default_text, help="Teks watermark (gunakan '\\n' untuk baris baru)")
    parser.add_argument("-op", "--opacity", type=int, default=30, help="Opasitas watermark (0-100, default: 30)")
    parser.add_argument("-a", "--angle", type=int, default=30, help="Sudut rotasi watermark (derajat, default: 30)")
    parser.add_argument("-s", "--scale", type=float, default=0.035, help="Skala font relatif terhadap lebar gambar (default: 0.035)")
    parser.add_argument("-sp", "--spacing", type=int, default=150, help="Jarak antar watermark dalam mode grid (piksel, default: 150)")
    parser.add_argument("-c", "--color", default="#ffffff", help="Kode hex warna teks watermark (default: #ffffff)")
    parser.add_argument("--no-grid", action="store_true", help="Gunakan mode watermark satu di tengah saja (non-grid)")
    
    args = parser.parse_args()
    
    # Mengolah input teks dengan memproses escape karakter newline '\n'
    processed_text = args.text.replace("\\n", "\n")
    
    try:
        print(f"Sedang memproses watermark pada: {args.input}...")
        add_watermark(
            image_path=args.input,
            text=processed_text,
            output_path=args.output,
            opacity=args.opacity,
            angle=args.angle,
            scale=args.scale,
            grid=not args.no_grid,
            spacing=args.spacing,
            color_hex=args.color
        )
        print(f"Selesai! Hasil disimpan di: {args.output}")
    except Exception as e:
        print(f"Error: {e}")
