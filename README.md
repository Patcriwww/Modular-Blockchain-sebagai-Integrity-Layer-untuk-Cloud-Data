# Blockchain Akademik

Project **Blockchain Akademik** merupakan implementasi sistem blockchain
sederhana yang dirancang untuk mensimulasikan pencatatan data akademik
secara terdistribusi, aman, dan tidak dapat dimanipulasi. Sistem ini
bertujuan untuk menunjukkan bagaimana teknologi blockchain dapat
digunakan dalam dunia pendidikan, seperti penyimpanan nilai, sertifikat,
dan riwayat akademik mahasiswa secara transparan dan *immutable*.

Project ini dibuat sebagai bagian dari tugas mata kuliah yang berkaitan
dengan **Blockchain, Keamanan Data, dan Sistem Terdistribusi**.

------------------------------------------------------------------------

## Latar Belakang

Sistem akademik konvensional masih bergantung pada database terpusat
yang memiliki beberapa kelemahan, antara lain:

-   Rentan terhadap manipulasi data\
-   Memiliki *single point of failure*\
-   Kurangnya transparansi dan auditabilitas

Dengan menggunakan konsep blockchain:

-   Setiap data disimpan dalam bentuk blok\
-   Setiap blok saling terhubung melalui hash\
-   Perubahan data dapat terdeteksi\
-   Integritas data lebih terjamin

------------------------------------------------------------------------

## Fitur Utama

### 1. Pembuatan Blok (Block Creation)

Setiap data akademik disimpan dalam bentuk blok yang terdiri dari: -
Index\
- Timestamp\
- Data akademik\
- Hash\
- Previous Hash

### 2. Validasi Blockchain

Sistem dapat memverifikasi apakah rantai blockchain masih valid dan
tidak mengalami modifikasi.

### 3. Immutability

Data yang telah tersimpan dalam blockchain tidak dapat diubah tanpa
mempengaruhi keseluruhan rantai.

### 4. Simulasi Transaksi Akademik

Contoh data yang dapat disimulasikan: - Nilai mahasiswa\
- Riwayat mata kuliah\
- Sertifikat kelulusan

------------------------------------------------------------------------

## Arsitektur Sistem

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

------------------------------------------------------------------------

## Teknologi yang Digunakan

-   Python 3.x\
-   SHA-256 Hashing Algorithm\
-   Object-Oriented Programming (OOP)\
-   JSON / File Storage

------------------------------------------------------------------------

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

------------------------------------------------------------------------

## Cara Menjalankan

1.  Clone repository:

    ``` bash
    git clone https://github.com/username/blockchain-akademik.git
    cd blockchain-akademik
    ```

2.  Install dependency:

    ``` bash
    pip install -r requirements.txt
    ```

3.  Jalankan program:

    ``` bash
    python main.py
    ```

------------------------------------------------------------------------

## Contoh Alur Kerja

1.  User memasukkan data akademik (NIM, Nama, Mata Kuliah, Nilai).\
2.  Data diproses menjadi transaksi.\
3.  Sistem membuat blok baru.\
4.  Hash blok dihitung menggunakan SHA-256.\
5.  Blok ditambahkan ke dalam blockchain.\
6.  Sistem memverifikasi integritas rantai blockchain.

------------------------------------------------------------------------

## Tujuan Pembelajaran

Project ini bertujuan untuk memahami:

-   Konsep dasar Blockchain\
-   Struktur Block dan Hash\
-   Mekanisme penghubung antar Block\
-   Validasi integritas data\
-   Penerapan Blockchain pada sistem akademik

------------------------------------------------------------------------

## Author

**Fachri Reyhan**\
Mahasiswa -- Teknologi Informasi / Informatika\
Tahun: 2026

------------------------------------------------------------------------

## Lisensi

Project ini dibuat untuk keperluan akademik dan pembelajaran.\
Bebas digunakan sebagai referensi dengan mencantumkan sumber.
