# Blockchain Akademik

Project **Blockchain Akademik** merupakan implementasi sistem blockchain sederhana yang dirancang untuk mensimulasikan pencatatan data akademik secara terdistribusi, aman, dan tidak dapat dimanipulasi. Sistem ini bertujuan untuk menunjukkan bagaimana teknologi blockchain dapat digunakan dalam dunia pendidikan, seperti penyimpanan nilai, sertifikat, atau riwayat akademik mahasiswa secara transparan dan immutable.

Project ini dibuat sebagai bagian dari tugas mata kuliah yang berkaitan dengan **Blockchain / Keamanan Data / Sistem Terdistribusi**.

---

## Latar Belakang

Sistem akademik konvensional masih bergantung pada database terpusat yang rentan terhadap:
- Manipulasi data
- Single point of failure
- Kurangnya transparansi

Dengan menggunakan konsep blockchain:
- Setiap data disimpan dalam blok
- Setiap blok saling terhubung melalui hash
- Perubahan data dapat terdeteksi
- Integritas data terjamin

---

## Fitur Utama

### 1. Pembuatan Blok (Block Creation)
Setiap data akademik disimpan dalam bentuk blok yang berisi:
- Index
- Timestamp
- Data akademik
- Hash
- Previous Hash

### 2. Validasi Blockchain
Sistem dapat memverifikasi apakah rantai blockchain masih valid dan tidak dimodifikasi.

### 3. Immutability
Data yang sudah masuk ke dalam blok tidak dapat diubah tanpa merusak seluruh rantai.

### 4. Simulasi Transaksi Akademik
Contoh data:
- Input nilai mahasiswa
- Riwayat mata kuliah
- Sertifikat kelulusan

---

## Arsitektur Sistem

```text
User Input
   ↓
Transaction (Data Akademik)
   ↓
Block Creation
   ↓
Hashing (SHA-256)
   ↓
Blockchain Ledger
   ↓
Validation & Verification

---

## Teknologi yang Digunakan
- Python 3.x
- Hashing Algorithm (SHA-256)
- Object-Oriented Programming
- JSON / File Storage

---

## Struktur Folder

blockchain-akademik/
│
├── main.py
├── block.py
├── blockchain.py
├── transaction.py
├── utils.py
├── data/
│   └── chain.json
│
├── requirements.txt
└── README.md

---

## Cara Menjalankan
- Clone Repository
  **git clone https://github.com/username/blockchain-akademik.git
  cd blockchain-akademik**
- Install Dependency
  **pip install -r requirements.txt**
- Jalankan Program
  **python main.py**

---

## Contoh Alur Kerja
- User memasukkan data akademik (NIM, Nama, Mata Kuliah, Nilai).
- Data diproses menjadi transaksi.
- Sistem membuat blok baru.
- Hash blok dihitung.
- Blok ditambahkan ke blockchain.
- Sistem memverifikasi integritas rantai.  

---

## Tujuan Pembelajaran
**Project ini bertujuan untuk memahami:**
- Konsep dasar Blockchain.
- Struktur Block & Hash.
- Mekanisme Linking antar Block.
- Validasi Integritas Data.
- Penerapan Blockchain di Sistem Akademik. 

---

## Author
**Fachri Reyhan**
Mahasiswa – Teknologi Informasi / Informatika
Tahun: 2026

---

## Lisensi
Project ini dibuat untuk keperluan akademik dan pembelajaran. Bebas digunakan sebagai referensi dengan mencantumkan sumber.


 
