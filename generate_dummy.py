#!/usr/bin/env python3
from PIL import Image, ImageDraw

def create_dummy_ktp(output_path="dummy_ktp.png"):
    # Rasio standard KTP (CR80): 856 x 540 piksel
    width, height = 856, 540
    
    # Buat latar belakang biru khas KTP Indonesia
    img = Image.new("RGB", (width, height), "#3a6073")
    draw = ImageDraw.Draw(img)
    
    # Tambahkan pola/border luar sederhana
    draw.rectangle([(15, 15), (width - 15, height - 15)], outline="#203a43", width=4)
    
    # Teks header
    draw.text((300, 30), "PROVINSI DKI JAKARTA", fill="#ffffff")
    draw.text((290, 45), "JAKARTA SELATAN", fill="#ffffff")
    
    # NIK
    draw.text((40, 90), "NIK       : 3171234567890001", fill="#ffffff")
    
    # Data Diri Mock
    labels = [
        "Nama      : BUDI SANTOSO",
        "Tgl Lahir : JAKARTA, 01-01-1990",
        "Jenis Klm : LAKI-LAKI",
        "Alamat    : JL. MERDEKA NO. 10",
        "Agama     : ISLAM",
        "Status    : KAWIN",
        "Pekerjaan : KARYAWAN SWASTA",
        "Kewarganegaraan: WNI",
    ]
    
    y = 130
    for label in labels:
        draw.text((40, y), label, fill="#ffffff")
        y += 25
        
    # Kotak untuk area foto (di sebelah kanan)
    draw.rectangle([(620, 130), (800, 370)], outline="#ffffff", width=2, fill="#4e54c8")
    draw.text((660, 240), "MOCK FOTO", fill="#ffffff")
    
    # Kotak tanda tangan
    draw.rectangle([(620, 390), (800, 480)], outline="#ffffff", width=1, fill="#ffffff")
    draw.text((650, 430), "TANDA TANGAN", fill="#000000")
    
    img.save(output_path)
    print(f"Dummy KTP berhasil dibuat di: {output_path}")

if __name__ == "__main__":
    create_dummy_ktp()
