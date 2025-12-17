# Modular-Blockchain-sebagai-Integrity-Layer-untuk-Cloud-Data
Repo untuk Modular Blockchain sebagai Integrity Layer  untuk Cloud Data

🎓 Academic Credential Micro-Ledger

Anti Pemalsuan Nilai & Sertifikat Akademik (Case 3)

📌 Deskripsi Proyek

Academic Credential Micro-Ledger adalah sistem berbasis blockchain sederhana yang dirancang untuk mencegah pemalsuan nilai dan sertifikat akademik mahasiswa.
Proyek ini mengintegrasikan Flask (backend) dengan Google Sheets (cloud storage) untuk mensimulasikan bagaimana manipulasi data di cloud dapat terdeteksi melalui mekanisme hash blockchain.

Sistem memastikan bahwa data nilai yang telah tercatat di blockchain tidak dapat diubah secara sepihak, meskipun data di Google Sheets dimanipulasi secara manual.

🎯 Tujuan Proyek

Mencegah perubahan nilai mahasiswa tanpa otorisasi

Mendeteksi pemalsuan sertifikat akademik

Menjaga integritas dan konsistensi data akademik

Mensimulasikan kasus manipulasi data pada cloud (Google Sheets)

🧩 Skenario Sistem

Dosen menginput nilai mahasiswa ke sistem

Data disimpan ke dalam blockchain

Data blockchain dikirim dan ditampilkan di Google Sheets

Data di Google Sheets diubah secara manual (simulasi kecurangan)

Sistem tetap menampilkan data asli dari blockchain dan mendeteksi manipulasi

📦 Struktur Data Blockchain (Case 3)
{
  "block_id": 4,
  "student_id": "MHS-2023-001",
  "nama_mahasiswa": "Budi",
  "mata_kuliah": "Kriptografi",
  "nilai": "A",
  "semester": 5,
  "tanggal": "2025-12-08 13:00:00",
  "dosen_pengampu": "Dr. Lina",
  "prev_hash": "ff21ac8812...",
  "current_hash": "99bce712aa..."
}

⛓️ Jumlah Blok Wajib

Sistem wajib memiliki minimal 4 blok, yaitu:

Blok	Fungsi
Blok 1	Input Nilai UTS
Blok 2	Input Nilai UAS
Blok 3	Finalisasi Mata Kuliah
Blok 4	Penerbitan Sertifikat

Empat blok ini diperlukan agar pemalsuan sertifikat dapat diuji dan diverifikasi.

🔗 Endpoint API

Sistem menyediakan endpoint berikut:

Method	Endpoint	Fungsi
POST	/add_data	Menambahkan data nilai ke blockchain
GET	/get_chain	Menampilkan seluruh blockchain
GET	/verify_chain	Verifikasi integritas blockchain
GET	/detect_cloud_tampering	Mendeteksi manipulasi data di Google Sheets
☁️ Integrasi Google Sheets

Alur pengiriman data:

Flask API → Google Apps Script → Google Sheets


Tujuan integrasi:

Menampilkan data blockchain ke cloud

Mensimulasikan manipulasi data

Menguji integritas data antara blockchain dan cloud

🧪 Pengujian Sistem (Postman)
✅ Uji Normal

Jalankan server Flask

Kirim data menggunakan POST /add_data sebanyak 4 kali

Cek blockchain menggunakan GET /get_chain

Verifikasi integritas menggunakan GET /verify_chain

Sistem menampilkan status DATA SAMA

❌ Simulasi Kecurangan

Ubah data langsung di Google Sheets
(contoh: nama mahasiswa atau nilai)

Jalankan GET /verify_chain atau GET /detect_cloud_tampering

Sistem menampilkan status DATA TIDAK SAMA

Sistem menunjukkan blok yang telah dimanipulasi

📊 Hasil Pengujian

Sebelum Tampering
Blockchain dan Google Sheets konsisten → DATA SAMA

Sesudah Tampering
Data di Google Sheets diubah tanpa pembaruan hash → DATA TIDAK SAMA

Sistem berhasil mendeteksi perubahan data akademik secara otomatis.

🛠️ Teknologi yang Digunakan

Python (Flask)

Blockchain (SHA-256 Hash)

Google Apps Script

Google Sheets

Postman (API Testing)

👨‍🎓 Konteks Akademik

Proyek ini dikembangkan sebagai implementasi Case 3 – Academic Credential Micro-Ledger untuk mata kuliah yang membahas:

Blockchain fundamentals

Data integrity

Cloud tampering detection

Sistem anti-pemalsuan data akademik

📌 Catatan

Google Sheets digunakan hanya sebagai simulasi cloud,
sumber kebenaran utama (single source of truth) tetap berada di blockchain.
