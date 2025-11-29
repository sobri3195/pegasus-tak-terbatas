# 🦅 Pegasus Tak Terbatas

**Pegasus Tak Terbatas** adalah asisten AI lokal canggih yang dirancang dan dikembangkan oleh **dr. Sobri**.  
Dibangun khusus untuk **keamanan siber, ethical hacking, dan penelitian bug bounty** — memberdayakan peneliti untuk menganalisis, mengotomatisasi, dan memahami **kerentanan dunia nyata**.

---

## 👨‍⚕️ Tentang Penulis

**Lettu Kes dr. Muhammad Sobri Maulana, S.Kom, CEH, OSCP, OSCE**

Seorang profesional keamanan siber dengan latar belakang medis dan teknologi informasi. Berpengalaman dalam penetration testing, ethical hacking, dan pengembangan tools keamanan.

### 📧 Kontak
- **Email**: muhammadsobrimaulana31@gmail.com
- **GitHub**: [github.com/sobri3195](https://github.com/sobri3195)
- **Website**: [muhammadsobrimaulana.netlify.app](https://muhammadsobrimaulana.netlify.app)
- **Toko Online**: [Pegasus Shop](https://pegasus-shop.netlify.app)

### 🌐 Media Sosial
- **YouTube**: [Muhammad Sobri Maulana](https://www.youtube.com/@muhammadsobrimaulana6013)
- **TikTok**: [@dr.sobri](https://www.tiktok.com/@dr.sobri)
- **Telegram**: [winlin_exploit](https://t.me/winlin_exploit)
- **WhatsApp Group**: [Join Group](https://chat.whatsapp.com/B8nwRZOBMo64GjTwdXV8Bl)

### 💰 Dukung Pengembangan
Jika tools ini bermanfaat, dukung pengembangan lebih lanjut melalui:

- **Lynk**: [lynk.id/muhsobrimaulana](https://lynk.id/muhsobrimaulana)
- **Trakteer**: [trakteer.id/g9mkave5gauns962u07t](https://trakteer.id/g9mkave5gauns962u07t)
- **Gumroad**: [maulanasobri.gumroad.com](https://maulanasobri.gumroad.com/)
- **Karya Karsa**: [karyakarsa.com/muhammadsobrimaulana](https://karyakarsa.com/muhammadsobrimaulana)
- **Nyawer**: [nyawer.co/MuhammadSobriMaulana](https://nyawer.co/MuhammadSobriMaulana)
- **Sevalla**: [muhammad-sobri-maulana-kvr6a.sevalla.page](https://muhammad-sobri-maulana-kvr6a.sevalla.page/)

---

## 🌐 Gambaran Umum

Pegasus Tak Terbatas berjalan sepenuhnya **offline** dan terintegrasi langsung dengan **Ollama** menggunakan model AI lokal kustom.  
Memungkinkan Anda untuk chat, menjalankan perintah, mengunggah file, dan mengatur penelitian — semua dalam lingkungan yang aman dan pribadi.

---

## ⚙️ Persyaratan Sistem

Untuk memastikan performa lancar saat menjalankan Pegasus Tak Terbatas dan model AI lokal Anda, sistem Anda harus memenuhi:

| Kategori | Minimum | Direkomendasikan |
|-----------|----------|-------------|
| **CPU** | Prosesor 8-core | 12-core atau lebih tinggi |
| **RAM** | 16 GB | 32 GB atau lebih tinggi |
| **GPU (opsional)** | GPU NVIDIA dengan ≥ 8 GB VRAM | RTX 3060 Ti / 4070 atau lebih tinggi |
| **Storage** | 15 GB kosong | SSD dengan 30 GB+ kosong |
| **OS** | Linux | Kali Linux |
| **Python** | 3.10+ | Versi stabil 3.x terbaru |

> 💡 Bekerja pada sistem CPU-only (respons lebih lambat). GPU direkomendasikan untuk streaming AI real-time.

---

## 🧩 Panduan Instalasi Lengkap

Ikuti langkah-langkah berikut dengan hati-hati 👇

---

### 1️⃣ Clone atau Persiapkan Folder Proyek

```bash
git clone https://github.com/sobri3195/pegasus-tak-terbatas.git
cd pegasus-tak-terbatas
```

### 2️⃣ Buat Virtual Environment

```bash
python3 -m venv venv

# Aktifkan environment
source venv/bin/activate
```

### 3️⃣ Install Semua Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Ollama

Download dan install Ollama dari website resmi:

[ollama.com/download](https://ollama.com/download)

### 5️⃣ Pull Model Kustom

```bash
ollama run IHA089/drana-infinity-v1
```

Verifikasi bahwa model tersedia:

```bash
ollama list
```

### 6️⃣ Jalankan Backend Ollama

```bash
ollama serve
```

### 7️⃣ Jalankan Server Pegasus Tak Terbatas

```bash
python3 pegasus_tak_terbatas.py
```

Server akan berjalan di `http://127.0.0.1:80`

---

## 🚀 Fitur Utama

- ✅ **AI Chat Lokal** - Chat dengan AI tanpa koneksi internet
- ✅ **Eksekusi Command** - Jalankan command terminal langsung dari interface
- ✅ **Upload File** - Analisis file dan dokumen dengan AI
- ✅ **Project Management** - Organisir penelitian dalam project
- ✅ **Command History** - Simpan dan akses kembali output command
- ✅ **Markdown Support** - Format rich text untuk response AI
- ✅ **Multi-Model Support** - Pilih model AI yang berbeda

---

## 📝 Catatan Penting

- Tools ini dirancang untuk tujuan **educational dan ethical hacking** saja
- Selalu dapatkan izin sebelum melakukan testing pada sistem
- Pengguna bertanggung jawab atas penggunaan tools ini
- Patuhi hukum dan regulasi yang berlaku di wilayah Anda

---

## 🤝 Kontribusi

Kontribusi, issues, dan feature requests sangat diterima!  
Jangan ragu untuk check [issues page](https://github.com/sobri3195/pegasus-tak-terbatas/issues) jika Anda ingin berkontribusi.

---

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Ucapan Terima Kasih

Terima kasih kepada semua kontributor dan komunitas yang telah mendukung pengembangan Pegasus Tak Terbatas!

---

**Made with ❤️ by dr. Sobri**

**#CyberSecurity #EthicalHacking #BugBounty #PegasusTakTerbatas**
