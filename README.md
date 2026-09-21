# Kumpulan Surat & Arsip Administrasi Terpadu

Repositori resmi untuk pengelolaan, penomoran, klasifikasi, dan pengarsipan surat dinas, memo internal (IOM), perjanjian kerja (SPK), perizinan, dan naskah administrasi lainnya di bawah naungan **Yanproland Group, PT Kenzo Anatha Bumi, PT Siliwangi Anatha Bumi, Nugi AI Studio, dan Mora Republic**.

---

## 📂 Struktur Direktori Produk & Arsip

| Direktori | Entitas Pengampu | Kode | Ruang Lingkup Dokumen |
| :--- | :--- | :--- | :--- |
| [`00_STANDAR_DAN_REGULASI/`](./00_STANDAR_DAN_REGULASI/) | Seluruh Entitas | `-` | Standar penomoran resmi, template kop, pedoman margin & font, dan register master CSV |
| [`01_GREN_PROPERTYKOST/`](./01_GREN_PROPERTYKOST/) | PT Kenzo Anatha Bumi (KAB) | `GREN` / `EJ` | Kost mahasiswa eksklusif 3 lantai Jatinangor (IOM promo, open table, SKUP, kwitansi) |
| [`02_HUNIAN_ASRI_JATIHANDAP/`](./02_HUNIAN_ASRI_JATIHANDAP/) | PT Siliwangi Anatha Bumi (SAB) | `HJA` | Perumahan tapak & kavling siap bangun Cimenyan Bandung |
| [`03_EMERALDA_KERTAJATI/`](./03_EMERALDA_KERTAJATI/) | Yanproland / PT SAB | `EK` | Aset tanah aerocity 1,4 Ha (20 AJB) dekat Bandara BIJB Kertajati |
| [`04_THE_EMERALDA_RESORT_KINGSTON_PARK/`](./04_THE_EMERALDA_RESORT_KINGSTON_PARK/) | Yanproland / PT SAB | `TER` / `KGP` | Kawasan resort hillside & klaster Kingston Park Padalarang Bandung Barat |
| [`05_FREELANCE_NUGI_AI_STUDIO/`](./05_FREELANCE_NUGI_AI_STUDIO/) | Nugi AI Studio | `FNA` / `NAI` | Rekayasa software AI, bot, serverless RAG, SPK kontrak kerja, NDA, & invoice B2B |
| [`06_MORA_REPUBLIC_WIFI_USWAH/`](./06_MORA_REPUBLIC_WIFI_USWAH/) | Mora Republic & Uswah Cell | `WIFI` / `MR` | Penyedia internet RT/RW net, voucher wifi, izin tarik kabel, formulir langganan |
| [`07_CORPORATE_YANPROLAND_HOLDING/`](./07_CORPORATE_YANPROLAND_HOLDING/) | Yanproland Holding | `CORP` / `YPL` | SK Direksi, surat tugas/kuasa, pengajuan budget lintas divisi, legalitas holding |
| [`tools/`](./tools/) | Sistem Otomasi AI | `-` | Script AI Assistant untuk klasifikasi otomatis via Embedding & penomoran anti-duplikat |

---

## 🔢 Format Baku Nomor Surat

```
[Nomor Urut 3 Digit] / [Kode Divisi] / [Kode Entitas] / [Kode Produk] / [Bulan Romawi] / [Tahun 4 Digit]
```
Contoh Dokumen Aktif:
- `003/MKT/KAB/EJ/III/2026` : Internal Office Memo Promo Survey Serentak Elit Jatinangor.
- `001/MKT/KAB/GREN/VII/2026` : Surat Permohonan Izin Open Table di Jatinangor Golf.
- `001/ENG/NAI/FNA/IX/2026` : SPK Pembuatan AI Automation Engine.

Pedoman lengkap kodefikasi divisi, entitas, dan produk dapat dibaca di:  
👉 [`00_STANDAR_DAN_REGULASI/STANDAR_PENOMORAN_DAN_KODE_SURAT.md`](./00_STANDAR_DAN_REGULASI/STANDAR_PENOMORAN_DAN_KODE_SURAT.md)

---

## 🤖 Penggunaan Asisten AI (Embedding & Penomoran Otomatis)

Repositori ini dilengkapi dengan tool AI berbasis semantic embedding (`http://127.0.0.1:1234/v1/embeddings`) dan reranker (`http://127.0.0.1:8080/v1/rerank`):

### 1. Klasifikasi Surat Otomatis
Menganalisis isi atau perihal surat dan langsung menentukan folder tujuan serta rekomendasinya:
```bash
python tools/letter_manager.py classify "Surat izin penarikan kabel internet fiber optik ke ketua RT 05"
```
*Output: Otomatis mendeteksi produk `06_MORA_REPUBLIC_WIFI_USWAH/01_Surat_Keluar`.*

### 2. Menerbitkan Nomor Surat Baru (Anti-Duplikasi)
Menerbitkan nomor urut berikutnya, mengunci nomor, dan mencatat langsung ke CSV register:
```bash
python tools/letter_manager.py issue --product GREN --div MKT --title "Permohonan Kerjasama Tenant Kampus" --recipient "Rektorat Unpad"
```

### 3. Melihat Daftar Surat Terdaftar
```bash
python tools/letter_manager.py list
```

---
*Dikelola secara terstandar untuk efisiensi kearsipan dan integritas legalitas korporasi.*
