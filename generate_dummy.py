#!/usr/bin/env python3
from PIL import Image, ImageDraw

def create_dummy_document(output_path="dummy_document.png"):
    # Rasio standard kertas A4: 800 x 1130 piksel
    width, height = 800, 1130
    
    # Buat latar belakang kertas putih/krem
    img = Image.new("RGB", (width, height), "#fafafa")
    draw = ImageDraw.Draw(img)
    
    # Tambahkan margin/border halaman
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline="#e2e8f0", width=2)
    draw.rectangle([(40, 40), (width - 40, height - 40)], outline="#cbd5e1", width=1)
    
    # Header Dokumen
    draw.text((280, 80), "SURAT PERJANJIAN KERJASAMA", fill="#0f172a")
    draw.text((340, 100), "KATEGORI: RAHASIA", fill="#ef4444")
    draw.text((320, 120), "No. SPK: 2026/SEC/004", fill="#64748b")
    
    # Garis pembatas header
    draw.line([(60, 150), (740, 150)], fill="#94a3b8", width=2)
    
    # Paragraph 1
    p1 = (
        "Yang bertanda tangan di bawah ini menerangkan bahwa dokumen ini bersifat rahasia\n"
        "dan hanya dipergunakan untuk keperluan evaluasi internal. Segala bentuk penyalinan,\n"
        "penyebarluasan, atau penyalahgunaan data tanpa persetujuan tertulis merupakan\n"
        "pelanggaran hukum yang serius."
    )
    draw.text((60, 180), p1, fill="#1e293b", spacing=6)
    
    # Subheading
    draw.text((60, 280), "PASAL 1 - KERAHASIAAN INFORMASI", fill="#0f172a")
    
    # Paragraph 2
    p2 = (
        "1. Informasi Rahasia mencakup namun tidak terbatas pada: data pengguna, informasi\n"
        "   keuangan perusahaan, rencana bisnis, kode sumber (source code), dan kekayaan\n"
        "   intelektual lainnya.\n\n"
        "2. Pihak penerima berkewajiban menjaga kerahasiaan dokumen ini dan tidak boleh\n"
        "   membagikannya kepada pihak ketiga tanpa izin resmi."
    )
    draw.text((60, 310), p2, fill="#1e293b", spacing=6)
    
    # Kotak Tanda Tangan
    draw.text((100, 850), "Pihak Pertama,", fill="#1e293b")
    draw.line([(100, 960), (280, 960)], fill="#94a3b8", width=1)
    draw.text((100, 970), "BUDI SANTOSO\nDirektur Utama", fill="#64748b")
    
    draw.text((500, 850), "Pihak Kedua,", fill="#1e293b")
    draw.line([(500, 960), (680, 960)], fill="#94a3b8", width=1)
    draw.text((500, 970), "ANI SETIAWATI\nMitra Bisnis", fill="#64748b")
    
    # Stamp / Cap Mock (merah melingkar di tengah tanda tangan)
    draw.ellipse([(140, 880), (220, 940)], outline="#ef4444", width=2)
    draw.text((155, 905), "CONFIDENTIAL", fill="#ef4444")
    
    img.save(output_path)
    print(f"Dummy Document berhasil dibuat di: {output_path}")

if __name__ == "__main__":
    create_dummy_document()
