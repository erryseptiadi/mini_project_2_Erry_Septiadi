# mini_project_2_Erry_Septiadi

# ASRI: Virtual Assistant Sadar Lemari 🌿💬

**ASRI (Asisten Virtual Sadar Lemari)** adalah solusi cerdas edukasi pengelolaan limbah tekstil dan ekonomi sirkular berbasis **RAG (Retrieval-Augmented Generation)**. Sistem ini dirancang untuk menjawab pertanyaan publik seputar layanan, lokasi *drop point*, biaya kelola, dan prosedur penyerahan pakaian bekas secara cepat, akurat, serta terverifikasi menggunakan basis dokumen internal resmi **Sadar Lemari**.

---

## 📋 Daftar Isi
1. [Deskripsi Case, Latar Belakang & Tujuan](#1-deskripsi-case-latar-belakang--tujuan)
2. [Sumber Data](#2-sumber-data)
3. [Model & Arsitektur Sistem](#3-model--arsitektur-sistem)
4. [Cara Instalasi](#4-cara-instalasi)
5. [Cara Menjalankan Chatbot](#5-cara-menjalankan-chatbot)
6. [Evaluasi & Catatan Pengembangan](#7-evaluasi--catatan-pengembangan)

---

## 1. Deskripsi Case, Latar Belakang & Tujuan

### 🛑 Latar Belakang
* **Krisis Penumpukan Pakaian:** Pertumbuhan *fast fashion* memicu lonjakan limbah pakaian massal yang sulit terurai di Tempat Pemrosesan Akhir (TPA).
* **Minim Akses Informasi:** Masyarakat sering kali tidak memahami prosedur, lokasi, maupun kriteria penyaluran/daur ulang pakaian secara efisien.
* **Kebutuhan Layanan 24/7:** Pertanyaan rutin dari masyarakat memerlukan respon yang cepat, ramah, dan akurat tanpa jeda waktu operasional.

### 🎯 Tentang & Tujuan Sadar Lemari
**Sadar Lemari** adalah inisiatif sosial dan lingkungan untuk pengelolaan limbah tekstil secara bertanggung jawab sekaligus mengedukasi publik agar lebih bijak dalam memiliki dan menggunakan pakaian.

**Tujuan ASRI Virtual Assistant:**
1. **Edukasi Interaktif:** Menjawab pertanyaan seputar *circular economy*, dampak limbah tekstil, dan pola hidup berkelanjutan.
2. **Panduan & Layanan:** Memandu prosedur penyerahan pakaian, informasi *Drop Point*, serta rincian biaya kelola layanan Sadar Lemari.
3. **Akurasi Terjamin (Bebas Halusinasi AI):** Mengunci pengetahuan AI pada dokumen internal resmi untuk memastikan tidak ada asumsi atau jawaban palsu yang berisiko merugikan pengguna.

---

## 2. Sumber Data

Seluruh pengetahuan ASRI terbatas pada **Dokumen Internal Resmi Sadar Lemari**:
* **Standard Operating Procedures (SOP):** Prosedur penyerahan pakaian, tata cara *drop-off* atau pengiriman paket.
* **Data Resmi Layanan:** Daftar lokasi *Drop Point*, struktur biaya pengelolaan, dan kriteria limbah tekstil yang dapat diterima.
* **Statistik & Edukasi:** Data statistik limbah tekstil global dan lokal yang terverifikasi.

---

## 3. Model & Arsitektur Sistem

ASRI menggunakan pendekatan **RAG (Retrieval-Augmented Generation)** untuk memastikan setiap jawaban didasarkan pada fakta dokumen.

```
[ PDF / Dokumen Internal ] ──> [ Vector Database (Embedding & Ingestion) ]
                                          │
[ User Prompt ] ───────────> [ Retrieval Engine (Similarity Search) ]
                                          │
                                          ▼
                                 [ LLM Generator ] ──> [ Output Terverifikasi ]
```

* **Vector Database & Embedding:** Mengubah segmen teks dokumen internal menjadi *vector embeddings* untuk disimpan dan dicari secara cepat berdasarkan kedekatan semantik (*similarity search*).
* **Retrieval Engine:** Mencari segmen dokumen paling relevan ketika pengguna memberikan pertanyaan/kueri.
* **LLM Generator:** Merumuskan sintesis jawaban dengan gaya bahasa yang ramah (*natural language*) berdasarkan konteks terambil dari dokumen.

---

## 4. Cara Instalasi

### Prasyarat System
* Python 3.9 atau versi yang lebih baru
* Git

### Langkah Instalasi

1. **Klon Repositori**
   ```bash
   git clone https://github.com/username/asri-sadar-lemari.git
   cd asri-sadar-lemari
   ```

2. **Buat & Aktifkan Virtual Environment**
   * *Linux/macOS:*
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * *Windows:*
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Environment Variables (`.env`)**
   Buat file `.env` di direktori utama dan masukkan API Key yang sesuai (misal: OpenAI / Gemini API Key):
   ```env
   OPENAI_API_KEY=sk-proj-your-api-key-here
   # atau jika menggunakan Gemini / Provider lain:
   # GEMINI_API_KEY=your-gemini-api-key
   ```

---

## 5. Cara Menjalankan Chatbot

Aplikasi antarmuka obrolan (*chat interface*) dibangun menggunakan **Streamlit**.

1. Jalankan perintah Streamlit dari direktori proyek:
   ```bash
   streamlit run app.py --server.port 8504
   ```

2. Buka peramban (browser) Anda dan akses alamat berikut:
   ```text
   http://localhost:8504
   ```

3. **Cara Penggunaan:**
   * Gunakan tombol *prompt* rekomendasi cepat di halaman utama (misal: *"Gimana cara drop-off atau kirim pakaian?"*, *"Drop Point Sadar Lemari ada di mana aja?"*).
   * Atau ketik pertanyaan kustom pada kolom **TANYA ASRI** di bagian bawah.

---


## 6. Evaluasi & Catatan Pengembangan

### 💡 Temuan Evaluasi
* **Penyelarasan Knowledge Base:** Pada beberapa pengujian awal, terdapat pertanyaan umum (seperti kueri mendalam tentang *"Dampak Lingkungan Limbah Tekstil"* secara luas) yang belum terakomodasi sepenuhnya di dokumen internal, sehingga sistem menjawab secara jujur bahwa informasi detail belum tersedia.
* **Konsistensi Respons:** Diperlukan sinkronisasi rutin antara FAQ/prompt rekomendasi dengan ketersediaan teks pada *knowledge base*.

### 🚀 Rencana Peningkatan (*Roadmap*)
1. **Pengembangan Knowledge Base:** Menyusun & memperbarui *Knowledge Base* agar lebih komprehensif, mencakup artikel edukasi dampak lingkungan lanjutan.
2. **Optimasi Chunking & Prompting:** Meningkatkan teknik pemotongan teks (*chunking strategy*) dan instruksi sistem (*system prompt*) untuk menjaga konsistensi jawaban.
3. **Penyempurnaan Antarmuka:** Menambahkan riwayat percakapan (*chat history*) dan tautan langsung ke pendaftaran/form penyerahan pakaian Sadar Lemari.
