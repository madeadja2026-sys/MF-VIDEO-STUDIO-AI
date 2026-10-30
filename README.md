# MF VIDEO STUDIO AI

Aplikasi lokal untuk membuat video pendek dari foto. Antarmuka berbahasa Indonesia, penyimpanan lokal, PWA, dan pembungkus desktop Windows.

## Fitur versi awal
- Susun foto menjadi adegan video.
- Gerakan zoom/pan/statis, durasi dan rasio 16:9, 9:16, 1:1.
- Judul, teks pembuka, subtitle dan pengaturan tampilannya.
- Pratinjau narasi dengan Text-to-Speech bawaan perangkat.
- Musik/audio latar dari file lokal.
- Ekspor WebM secara lokal; opsi MP4 memakai FFmpeg WebAssembly yang perlu diunduh pada pemakaian pertama.
- PWA dan penyimpanan lokal.

## Menjalankan PWA
Jalankan server statis pada folder `public` (contoh: `python -m http.server 8080` dari folder `public`) lalu buka `http://localhost:8080`. Untuk publikasi GitHub Pages: unggah repositori ini ke GitHub pada branch `main`, lalu buka Settings → Pages dan pilih GitHub Actions. Workflow `.github/workflows/pages.yml` akan menerbitkan isi folder `public` secara otomatis. Setelah deploy selesai, buka URL Pages dan pilih Install App / Add to Home Screen.

## Membuat installer Windows 10/11 64-bit
Perlu Node.js LTS dan koneksi internet untuk mengunduh Electron/build dependencies.
1. Buka PowerShell di folder proyek.
2. Jalankan `npm install`
3. Jalankan `npm run build:win`
4. Installer muncul di folder `release`.

File installer Windows tidak disertakan dari lingkungan ini karena build NSIS harus dijalankan pada Windows atau runner Windows.

## Catatan penggunaan audio
Browser menyediakan Text-to-Speech untuk mendengarkan narasi sebagai pratinjau. Audio yang dihasilkan oleh sistem TTS browser tidak dapat direkam langsung secara konsisten oleh semua browser. Untuk narasi di hasil akhir, rekam narasi ke file WAV/MP3 lalu masukkan melalui input audio. Audio file tersebut akan ikut direkam ke video.

## Privasi
Foto dan proyek tidak diunggah ke server. Proyek beserta gambar disimpan di IndexedDB pada perangkat/browser. Simpan backup JSON secara berkala. Hindari menghapus data situs sebelum mengekspor cadangan.
