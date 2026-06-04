# DocShield - Secure Local Document Watermarker

![Dashboard Screenshot](dashboard.png)

Aplikasi Python sederhana, aman, dan 100% lokal untuk memberikan watermark pada berkas gambar dokumen sensitif/konfidensial (seperti KTP, kontrak, laporan keuangan, sertifikat, dll.) guna melindungi data pribadi Anda dari penyalahgunaan. Semua proses dilakukan di komputer Anda tanpa mengunggah file ke internet.

## Fitur Utama

- **100% Lokal**: File dokumen Anda tidak pernah dikirim ke internet, diproses sepenuhnya menggunakan pustaka Pillow Python.
- **Pola Grid (Tiling)**: Memberikan watermark berulang agar tidak mudah diedit atau dihapus oleh pihak tidak bertanggung jawab.
- **Pengaturan Lengkap**: Ubah teks kustom, opasitas (transparansi), ukuran font dinamis, rotasi sudut, warna hex, dan kerapatan watermark.
- **Preset Verifikasi Cepat**: Pilihan template watermark umum (seperti verifikasi layanan, keperluan khusus, dll.) dengan tanggal otomatis.
- **Dua Antarmuka**: Tersedia versi **Command Line Interface (CLI)** dan **Aplikasi Web (FastAPI)** yang cantik.

---

## Persiapan Instalasi

1. Pastikan Anda memiliki Python 3.8 ke atas terinstal di komputer.
2. Buka terminal/command prompt di direktori proyek ini.
3. Instal semua dependensi yang diperlukan:
   ```bash
   pip install -r requirements.txt
   ```

---

## Cara Menggunakan

### 1. Aplikasi Web Lokal (Sangat Direkomendasikan)

Aplikasi web menyediakan antarmuka grafis yang ramah pengguna dengan live preview real-time.

1. Jalankan server web lokal:
   ```bash
   python app.py
   ```
2. Buka browser Anda dan akses:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)
3. Drag & drop foto/scan dokumen Anda (atau gunakan file `dummy_document.png` yang disediakan untuk uji coba).
4. Sesuaikan teks, transparansi, ukuran, warna, dan sudut.
5. Klik **Unduh Gambar Dokumen** untuk menyimpan hasilnya.

### 2. Command Line Interface (CLI)

Untuk memproses cepat melalui terminal:

```bash
# Menambahkan watermark default ke dummy document
python watermarker.py -i dummy_document.png -o document_watermarked.png

# Menambahkan watermark kustom dengan opasitas 25% dan rotasi 45 derajat
python watermarker.py -i dummy_document.png -o document_watermarked.png -t "RAHASIA & KONFIDENSIAL\nHANYA UNTUK VERIFIKASI SEBAYA" -op 25 -a 45
```

#### Opsi Parameter CLI:
- `-i`, `--input`: Path gambar dokumen asal (Wajib)
- `-o`, `--output`: Path untuk menyimpan gambar hasil watermark (Wajib)
- `-t`, `--text`: Teks watermark (gunakan `\n` untuk baris baru)
- `-op`, `--opacity`: Transparansi watermark (0 - 100, default: 30)
- `-a`, `--angle`: Sudut rotasi watermark (derajat, default: 30)
- `-s`, `--scale`: Ukuran font relatif terhadap lebar gambar (default: 0.035)
- `-sp`, `--spacing`: Jarak antar grid watermark (default: 150)
- `-c`, `--color`: Kode warna teks hex (default: #ffffff)
- `--no-grid`: Gunakan mode satu watermark di tengah (bukan grid menyebar)

---

## Contoh File untuk Uji Coba
Kami menyediakan skrip untuk membuat gambar dokumen dummy kosong (tanpa data sensitif asli Anda) agar Anda bisa langsung mencoba fitur aplikasi:
```bash
python generate_dummy.py
```
Perintah di atas akan menghasilkan berkas `dummy_document.png`.
