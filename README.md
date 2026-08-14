# QMS ISO 9001 — Streamlit App

Aplikasi hasil migrasi dari modul Odoo `qms` (Quality Management System
ISO 9001) menjadi aplikasi Streamlit mandiri, dengan SQLite sebagai database.

## Struktur Proyek

```
qms_streamlit/
├── app.py              <- MAIN PATH untuk deploy di Streamlit Cloud
├── entities.py          konfigurasi semua ~30 entitas (field, tipe, relasi)
├── db.py                 layer database generik (SQLite, CRUD)
├── crud_ui.py             komponen form & tabel generik
├── requirements.txt
└── pages/                 9 halaman modul (multipage app bawaan Streamlit)
    ├── 1_Konteks_Organisasi.py   (Pihak Berkepentingan, Sumber Daya)
    ├── 2_Perencanaan.py          (Proses, Kebijakan, Sasaran Mutu, Indikator)
    ├── 3_Manajemen_Risiko.py     (Risiko/Hazard)
    ├── 4_Dokumentasi.py          (Dokumen, Prosedur, Instruksi, Formulir, Versi)
    ├── 5_Audit.py                (Audit, Verifikasi, Evaluasi Auditor)
    ├── 6_Temuan.py                (Ketidaksesuaian, Observasi, Keluhan, Peluang)
    ├── 7_Tindak_Lanjut.py         (Aksi, Verifikasi Efektivitas)
    ├── 8_Tinjauan_Manajemen.py    (Tinjauan, Tinjauan oleh Manajemen Puncak)
    └── 9_Master_Data.py           (Tahapan, Asal Temuan, Penyebab, Komponen Kebijakan)
```

## Menjalankan secara lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Database SQLite (`qms_data.db`) akan dibuat otomatis di folder yang sama
saat aplikasi pertama kali dijalankan.

## Deploy ke Streamlit Community Cloud

1. Push folder ini (isi `qms_streamlit/`) ke repository GitHub (root repo
   atau di sub-folder, bebas).
2. Buka https://share.streamlit.io → **New app**.
3. Pilih repo & branch, lalu isi **Main file path** dengan:
   ```
   app.py
   ```
   (atau `qms_streamlit/app.py` kalau proyek ini ditaruh di sub-folder repo).
4. Klik **Deploy**.

> ⚠️ Catatan penting soal data: Streamlit Community Cloud memakai
> penyimpanan sementara (ephemeral) — file `qms_data.db` bisa hilang saat
> container di-restart/redeploy. Untuk pemakaian produksi yang datanya
> harus persisten, sambungkan `db.py` ke database eksternal (mis. Postgres
> via `st.connection`, atau layanan seperti Supabase/Neon) alih-alih SQLite
> lokal. Struktur `db.py` sudah dipisah rapi supaya penggantian ini mudah.

## Catatan migrasi dari Odoo

- Setiap model Odoo (`qms.xxx`) dipetakan 1:1 ke satu entitas di
  `entities.py`, termasuk field, tipe data, relasi many2one, dan
  many2many (disimpan sebagai tabel junction terpisah).
- Beberapa logika otomatis di Odoo (nomor referensi otomatis via
  `ir.sequence`, field computed seperti "tanggal review terakhir", validasi
  seperti "harus isi tanggal verifikasi sebelum menutup efektivitas")
  **belum** direplikasi — form saat ini adalah CRUD generik. Beri tahu jika
  ada logika bisnis spesifik yang perlu ditambahkan.
- Field HTML di Odoo (`fields.Html`) dipetakan menjadi `textarea` teks
  polos (tanpa rich-text editor).
