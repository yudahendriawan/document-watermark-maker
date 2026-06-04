# KTP Shield - Secure Local Watermarker

Aplikasi Python sederhana, aman, dan 100% lokal untuk memberikan watermark pada scan/foto KTP (Kartu Tanda Penduduk) guna melindungi data pribadi Anda dari penyalahgunaan. Semua proses dilakukan di komputer Anda tanpa mengunggah file ke internet.

## Fitur Utama

- **100% Lokal**: File KTP Anda tidak pernah dikirim ke internet, diproses sepenuhnya menggunakan pustaka Pillow Python.
- **Pola Grid (Tiling)**: Memberikan watermark berulang agar tidak mudah diedit atau dihapus oleh pihak tidak bertanggung jawab.
- **Pengaturan Lengkap**: Ubah teks kustom, opasitas (transparansi), ukuran font dinamis, rotasi sudut, warna hex, dan kerapatan watermark.
- **Preset Verifikasi Cepat**: Pilihan template watermark umum (seperti untuk Shopee, bank, dll.) dengan tanggal otomatis.
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
3. Drag & drop foto KTP Anda (atau gunakan file `dummy_ktp.png` yang sudah disediakan untuk uji coba).
4. Sesuaikan teks, transparansi, ukuran, warna, dan sudut.
5. Klik **Unduh Gambar KTP** untuk menyimpan hasilnya.

### 2. Command Line Interface (CLI)

Untuk memproses cepat melalui terminal:

```bash
# Menambahkan watermark default ke dummy KTP
python watermarker.py -i dummy_ktp.png -o KTP_Watermarked.png

# Menambahkan watermark kustom dengan opasitas 30% dan rotasi 45 derajat
python watermarker.py -i dummy_ktp.png -o KTP_Watermarked.png -t "HANYA UNTUK VERIFIKASI SEBAYA\nPADA 04-06-2026" -op 30 -a 45
```

#### Opsi Parameter CLI:
- `-i`, `--input`: Path gambar KTP asal (Wajib)
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
Kami menyediakan skrip untuk membuat gambar KTP dummy kosong (tanpa data sensitif asli Anda) agar Anda bisa langsung mencoba fitur aplikasi:
```bash
python generate_dummy.py
```
Perintah di atas akan menghasilkan berkas `dummy_ktp.png`.
