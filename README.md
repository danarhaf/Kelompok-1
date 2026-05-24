# Smart Library Management & Recommendation System

> **ELT60213 Algoritma dan Struktur Data — Team Based Project**
> Program Studi S1 Teknik Elektro, Universitas Negeri Yogyakarta
> Semester 2 | TA 2025/2026 | Topik 6

---

## Data Anggota Kelompok

|         Anggota             |     NIM     |                    Modul                     |
|-----------------------------|-------------|----------------------------------------------|
| FAUZI FAJAR WIJAYA          | 25051030095 | Modul 1  - Queue Antrian Pemesanan           |
| MUHAMMAD DAFFA ADHIRAJASA   | 25051030086 | Modul 2  - Stack Riwayat & Undo              |
| ITQON EL FIKRY FAUSTA       | 25051030083 | Modul 3  - BST Katalog Buku                  |
| DANAR HAFIDZ A'ISY          | 25051030112 | Modul 4  - Graph Rekomendasi Ko-pinjam       |
| ANARGYA KEANO ARIZONA MARICI| 25051030096 | Modul 5  - Sorting Laporan Bulanan + CLI     |

**Dosen:** Dr.Eng. Ir. Aji Ery Burhandenny, ST., M.AIT.
**Link GitHub:** `https://github.com/danarhaf/tbp-asd--Library--kel-1-`

---

## Deskripsi Proyek

Sistem perpustakaan digital terpadu berbasis CLI yang mengintegrasikan **5 struktur data** dari nol (tanpa library bawaan Python):

- **Linked List**                  - fondasi Queue dan Stack
- **Queue** (berbasis Linked List) - antrian pemesanan buku per ISBN
- **Stack** (berbasis Linked List) - riwayat transaksi global + fitur UNDO
- **BST**                          - katalog buku dengan kunci ISBN
- **Graph** (tak-berarah berbobot) - rekomendasi ko-pinjam via BFS

Sistem mendukung **300+ event CLI** campuran secara interaktif dengan analisis Big-O di setiap operasi.

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────┐
│                    CLI (modul_6)                    │
│  CARI_BUKU | PINJAM | KEMBALIKAN | PESAN | UNDO ... │
└────┬──────────┬──────────┬──────────┬──────────┬────┘
     │          │          │          │          │
     ▼          ▼          ▼          ▼          ▼
 Modul 3    Modul 1    Modul 2    Modul 4    Modul 5
 BST        Queue      Stack      Graph      Sorting
 Katalog    Antrian    Riwayat    Rekomend.  Laporan
     │          │          │          │          │
     └──────────┴──────────┴──────────┴──────────┘
                          │
              data_structures/ (implementasi murni)
        linked_list | queue_ll | stack | bst | graph | sorting
```

### Parameter Sistem

| Parameter                 |                   Nilai                 |
|---------------------------|-----------------------------------------|
| Koleksi buku              | 80 judul (ISBN-0001 s.d. ISBN-0080)     |
| Jumlah anggota            | 60 anggota (format NIM)                 |
| Kategori buku             | 5 (Fiksi, Sains, Teknik, Sejarah, Seni) |
| Durasi peminjaman default | 14 hari                                 |
| Seed acak                 | 13 (TIDAK diubah - reproducible)        |
| Operasi CLI minimum       | 300 event campuran                      |

---

## Struktur Folder

```
tbp-asd-library-kelXX/
├── README.md                  ← dokumen ini
├── requirements.txt           ← daftar library (numpy, pytest)
├── .gitignore
│
├── src/
│   ├── main.py                ← entry point CLI
│   ├── data_model.py          ← dataclass Buku, Peminjaman, STATUS
│   ├── generate_data.py       ← generate_koleksi(80, seed=13)
│   │
│   ├── data_structures/       ← implementasi murni dari nol
│   │   
│   │   ├── linked_list.py     ← LLNode (fondasi Queue & Stack)
│   │   ├── queue_.py          ← Queue FIFO berbasis Linked List
│   │   ├── stack.py           ← Stack LIFO berbasis Linked List
│   │   ├── bst.py             ← Binary Search Tree (kunci ISBN)
│   │   ├── graph.py           ← Graf tak-berarah berbobot + BFS
│   │   └── sorting.py         ← Shell Sort & Merge Sort pada LL
│   │
│   └── modules/               ← modul aplikasi per anggota
│       ├── modul_1.py         ← ManajerAntrian (Queue per ISBN)
│       ├── modul_2.py         ← ManajerRiwayat (Stack + UNDO)
│       ├── modul_3.py         ← ManajerKatalog (BST)
│       ├── modul_4.py         ← ManajerRekomendasi (Graph + BFS)
│       ├── modul_5.py         ← ManajerLaporan (Sorting)
│       └── modul_6.py         ← CLI (dispatch table + handler)
│
├── tests/                     ← unit test per modul
│   ├── test_queue.py
│   ├── test_stack.py
│   ├── test_bst.py
│   ├── test_graph.py
│   └── test_sorting.py
│
├── experiments/
│   └── benchmark.py           ← eksperimen runtime N=20,80,300
│
├── docs/
│   ├── laporan_final.pdf
│   └── slide_presentasi.pdf
│
└── AI_Log/
    ├── Log_prompt.txt
    └── screenshots/
```

---

## Cara Instalasi & Menjalankan

### Prasyarat

- Python 3.11 atau lebih baru
- pip (package installer)

### 1. Clone Repository

```bash
git clone https://github.com/[username]/tbp-asd-library-kelXX.git
cd tbp-asd-library-kelXX
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Isi `requirements.txt`:
```
numpy
pytest
```

### 3. Jalankan Sistem

```bash
# Jalankan dari ROOT project (bukan dari dalam src/)
python src/main.py
```

### 4. Mode Test (CI/CD)

```bash
python src/main.py --test
```

### 5. Jalankan Unit Test

```bash
pytest tests/ -v
```

### 6. Jalankan Benchmark

```bash
python experiments/benchmark.py
```

---

## Panduan CLI - Daftar Perintah

Setelah program berjalan, ketik perintah berikut di prompt `>>`:

|            Perintah           |                 Deskripsi               |   Big-O    |
|-------------------------------|-----------------------------------------|------------|
| `CARI_BUKU <isbn>`            | Cari buku berdasarkan ISBN              | O(log n)   |
| `PINJAM <nim> <isbn>`         | Pinjam buku (status → DIPINJAM)         | O(log n)   |
| `KEMBALIKAN <isbn>`           | Kembalikan buku + proses antrian        | O(log n)   |
| `PESAN <nim> <isbn>`          | Masuk antrian buku yang sedang dipinjam | O(1)       |
| `BATALKAN_PESAN <nim> <isbn>` | Batalkan pesanan dari antrian           | O(k)       |
| `BATALKAN_TERAKHIR`           | Undo transaksi terakhir                 | O(1)       |
| `REKOMENDASI <isbn>`          | Rekomendasi buku via BFS (max 2 hop)    | O(V+E)     |
| `ANTRIAN <isbn>`              | Lihat antrian pemesanan suatu buku      | O(k)       |
| `KATALOG`                     | Tampilkan semua buku terurut ISBN       | O(n)       |
| `LAPORAN_BULAN`               | Laporan + benchmark Shell/Merge Sort    | O(n log n) |
| `BANTUAN`                     | Tampilkan daftar perintah               | O(1)       |
| `KELUAR`                      | Keluar dari program                     |     -      |

### Contoh Sesi CLI

```
>> CARI_BUKU ISBN-0001
  ISBN     : ISBN-0001
  Judul    : Algoritma Vol.1
  Pengarang: Penulis-7
  Kategori : Teknik
  Status   : TERSEDIA
  Big-O: O(log n) BST search

>> PINJAM NIM-001 ISBN-0001
[PINJAM] Berhasil. NIM-001 meminjam ISBN-0001 selama 14 hari. TX-0001
  Big-O: O(log n) BST search + update

>> PESAN NIM-002 ISBN-0001
[ANTRIAN] NIM-002 berhasil masuk antrian ISBN-0001. Posisi ke-1.
  Big-O: enqueue O(1)

>> REKOMENDASI ISBN-0001
[REKOMENDASI] Buku yang sering dipinjam bersama ISBN-0001:
  1. ISBN-0015 | Sistem Vol.15              | Bobot: 3 | Hop: 1 | TERSEDIA
  2. ISBN-0032 | Data Vol.32                | Bobot: 2 | Hop: 1 | TERSEDIA
  Big-O: O(V+E) BFS graf ko-pinjam

>> KEMBALIKAN ISBN-0001
[KEMBALIKAN] ISBN-0001 dikembalikan. Langsung dipesan oleh NIM-002. TX-0002
  Big-O: O(log n) BST search + update, O(1) dequeue antrian

>> BATALKAN_TERAKHIR
[UNDO] Membatalkan: [TX-0002] KEMBALIKAN   | NIM: - | ISBN: ISBN-0001
[UNDO] Status ISBN-0001 dikembalikan ke DIPINJAM.
  Big-O: O(1) stack pop + O(log n) BST update

>> LAPORAN_BULAN
[LAPORAN] Peminjaman Berdasarkan Durasi (Shell Sort, descending):
  ...
[LAPORAN] Tabel Runtime Sorting
     N | Shell Sort (s) | Merge Sort (s)
----------------------------------------
    20 |       0.000021 |       0.000018
    80 |       0.000142 |       0.000098
   300 |       0.001876 |       0.000934
Big-O Shell: ~O(n^1.5) | Big-O Merge: O(n log n)
```

---

##  Analisis Big-O Ringkasan

### Struktur Data

|    Struktur Data    |         Operasi          |      Big-O Waktu    | Big-O Ruang |
|---------------------|--------------------------|---------------------|-------------|
| **Linked List**     | add_front / add_back     | O(1) / O(1)         | O(n)        |
| **Queue**           | enqueue / dequeue        | O(1) / O(1)         | O(n)        |
| **Stack**           | push / pop / peek        | O(1) / O(1) / O(1)  | O(n)        |
| **BST** (rata-rata) | insert / search / delete | O(log n)            | O(n)        |
| **BST** (worst-case)| insert / search / delete | O(n)                | O(n)        |
| **Graph BFS**       | traversal penuh          | O(V+E)              | O(V)        | 
| **Shell Sort**      | urut n elemen            | ~O(n^1.5)           | O(n)        |
| **Merge Sort**      | urut n elemen            | O(n log n)          | O(log n)    |

### Ringkasan Per Modul

|       Modul        |          Fungsi Utama           |         Big-O          |
|--------------------|---------------------------------|------------------------|
| ManajerAntrian     | pesan / batalkan_pesan          | O(1) / O(k)            |
| ManajerRiwayat     | catat / batalkan_terakhir       | O(1) / O(1)            |
| ManajerKatalog     | cari_buku / pinjam / kembalikan | O(log n)               |
| ManajerRekomendasi | rekomendasikan (BFS)            | O(V+E)                 |
| ManajerLaporan     | buat_laporan_durasi / frekuensi | ~O(n^1.5) / O(n log n) |

---

## Hasil Eksperimen Runtime

Dijalankan dengan `python experiments/benchmark.py` | Seed = 13 | Rata-rata 5 ulangan

### Queue & Stack (per n operasi)

|  N  | Queue enqueue (s) | Queue dequeue (s) | Stack push (s) | Stack pop (s) |
|-----|-------------------|-------------------|----------------|---------------|
| 20  |      0.000012     |     0.000011      |    0.000010    |    0.000009   |
| 80  |      0.000045     |     0.000043      |    0.000038    |    0.000036   |
| 300 |      0.000178     |     0.000171      |    0.000145    |    0.000139   |

> Rasio ~4x untuk 4x lipat N → konfirmasi O(1) per operasi ✅

### BST — Insert Acak vs Terurut

|  N  | Insert acak (s) | Insert terurut (s) | Tinggi acak | Tinggi terurut |
|-----|-----------------|--------------------|-------------|----------------|
|  20 |     0.000089    |      0.000095      |      6      |       20       |
|  80 |     0.000412    |      0.000687      |      12     |       80       |
| 300 |     0.001823    |      0.004521      |      18     |       300      |

> Tinggi terurut = n (worst-case linear), tinggi acak ≈ log₂(n) ✅

### Sorting pada Linked List

|   N  | Shell Sort (s) | Merge Sort (s) |
|------|----------------|----------------|
|  20  |    0.000021    |    0.000018    |
|  80  |    0.000142    |    0.000098    |
|  300 |    0.001876    |    0.000934    |

> Merge Sort mulai unggul di N besar - konsisten dengan O(n log n) vs ~O(n^1.5) ✅

---

## Detail Implementasi Per Modul

### Modul 1 - Queue Antrian Pemesanan (`modul_1.py`)
- Satu Queue per ISBN, disimpan dalam dict `{isbn → Queue}`
- Cek duplikat NIM sebelum enqueue: O(k)
- Rebuild Queue untuk batalkan pesanan: O(k)
- Koordinasi dengan BST saat buku dikembalikan

### Modul 2 - Stack Riwayat & Undo (`modul_2.py`)
- Stack global menyimpan semua transaksi sebagai dict
- UNDO: pop transaksi → balik efek di BST dan Queue
- Archiving: `arsip_transaksi_lama(maks_simpan=100)` untuk efisiensi memori

### Modul 3 - BST Katalog (`modul_3.py`)
- Kunci = ISBN string (perbandingan leksikografis)
- Insert rekursif, search rekursif, delete dengan inorder successor
- `inorder()` menghasilkan katalog terurut ISBN secara otomatis

### Modul 4 - Graph Rekomendasi (`modul_4.py`)
- Adjacency list: `{isbn → [(isbn_tetangga, bobot)]}`
- BFS dengan batas `max_hop=2` menggunakan Queue Linked List sendiri
- Filter `min_bobot` untuk rekomendasi lebih relevan
- Hasil diurutkan dengan insertion sort berdasarkan bobot kumulatif

### Modul 5 - Sorting Laporan (`modul_5.py`)
- Shell Sort pada Linked List: kumpulkan pointer ke array temp → sort via swap data
- Merge Sort pada Linked List: split (slow/fast pointer) → rekursif → merge
- Benchmark runtime otomatis untuk N=20, 80, 300

### Modul 6 - CLI (`modul_6.py`)
- Dispatch table: `{perintah → handler}` (tidak ada if-elif panjang)
- Setiap perintah menampilkan Big-O operasinya
- Error handling via try-except agar loop tidak berhenti saat input salah

---

## Catatan Teknis Penting

- **Seed = 13** tidak boleh diubah agar hasil eksperimen reproducible
- Semua struktur data diimplementasi **dari nol** - tidak ada `collections.deque`, `heapq`, atau library serupa
- `sorted()` dan `list.sort()` bawaan Python **tidak digunakan** - sorting diimplementasi manual
- Jalankan selalu dari **ROOT project**, bukan dari dalam `src/`

---

## Penggunaan AI Assistant

Proyek ini menggunakan Claude (claude.ai) sebagai AI assistant selama pengembangan.
Detail lengkap prompt dan respons tersedia di:

```
AI_Log/
├── Log_prompt.txt    ← seluruh log percakapan per anggota
└── screenshots/      ← screenshot sesi AI
```

Seluruh kode yang dihasilkan dengan bantuan AI telah ditinjau, dipahami, dan diverifikasi oleh masing-masing anggota sebelum diintegrasikan ke proyek.

---

## ✅ Checklist Deliverable

- [x] Kode berjalan tanpa error saat demo
- [x] Semua struktur data diimplementasi dari nol (tanpa library)
- [x] CLI interaktif berfungsi end-to-end
- [x] Analisis Big-O ada di setiap fungsi (docstring)
- [x] Tabel runtime ≥ 3 ukuran data tersedia
- [x] 5 pertanyaan analisis wajib dijawab
- [x] Laporan PDF 8-12 hal., semua Bab I-VII ada
- [x] Slide presentasi 10-12 lembar
- [x] Struktur folder sesuai panduan (src/, tests/, docs/, experiments/, AI_Log/)
- [x] README berisi cara menjalankan + contoh input/output
- [x] AI_Log/ tersedia (Log_prompt.txt + screenshots)
- [x] Setiap anggota dapat menjelaskan modulnya
- [x] GitHub: branch feat/* digunakan
- [x] Commit history menunjukkan kontribusi semua anggota
- [x] Seed acak TIDAK diubah (reproducible)
- [x] Eksperimen runtime tersedia di folder experiments/

---

## Referensi

- Panduan TBP ELT60213 TA 2025/2026 - Dr.Eng. Ir. Aji Ery Burhandenny, ST., M.AIT.
- Cormen, T.H. et al. *Introduction to Algorithms*, 4th Ed. MIT Press, 2022.
- Sedgewick, R. & Wayne, K. *Algorithms*, 4th Ed. Addison-Wesley, 2011.

---

*Dibuat untuk memenuhi deliverable Team Based Project ELT60213 Algoritma dan Struktur Data, Semester 2 TA 2025/2026, Program Studi S1 Teknik Elektro UNY.*

---

## Tools AI yang Digunakan

Proyek ini dikerjakan dengan bantuan dua AI assistant:

|       AI Tool      |       Model       |                                  Kegunaan                                    |
|--------------------|-------------------|------------------------------------------------------------------------------|
| Claude (Anthropic) | Claude Sonnet 4.6 | Review kode, analisis Big-O, debugging, penjelasan konsep struktur data      |
| ChatGPT (OpenAI)   | GPT-5.5           | Brainstorming desain sistem, penjelasan algoritma, bantuan penulisan laporan |

Detail lengkap seluruh percakapan tersedia di folder `AI_Log/Log_prompt.txt` beserta screenshot sesi.

> Seluruh output AI telah dibaca, dipahami, dan diverifikasi kebenarannya oleh masing-masing anggota kelompok sebelum digunakan dalam proyek.

---

## Pernyataan Kelompok

Kami, seluruh anggota kelompok, menyatakan bahwa:

1. **Kami memahami seluruh kode** yang terdapat dalam repositori ini. Setiap anggota mampu menjelaskan modul yang menjadi tanggung jawabnya, termasuk alasan pemilihan struktur data, cara kerja algoritma, dan analisis Big-O setiap operasi.

2. **Pembagian tugas dilakukan secara merata.** Setiap anggota mengerjakan minimal satu modul secara mandiri dan berkontribusi nyata sebagaimana tercermin dalam commit history GitHub.

3. **Penggunaan AI bersifat asistensi**, bukan pengganti pemahaman. Kami menggunakan AI untuk mempercepat proses debugging dan memperdalam pemahaman konsep — bukan untuk menyalin kode tanpa memahaminya.

4. **Kode ini merupakan hasil karya kelompok kami sendiri** dan tidak identik dengan kelompok lain. Kami memahami bahwa kode identik antar kelompok berakibat nilai 0 untuk semua pihak.

5. **Kami siap menjelaskan setiap baris kode** saat sesi presentasi dan tanya jawab dengan dosen pada Pertemuan 15.

|           Nama               |     NIM     |  Tanda Tangan  |
|------------------------------|-------------|----------------|
| FAUZI FAJAR WIJAYA           | 25051030095 | .............. |
| MUHAMMAD DAFFA ADHIRAJASA    | 25051030086 | .............. |
| ITQON EL FIKRY FAUSTA        | 25051030083 | .............. |
| DANAR HAFIDZ A'ISY           | 25051030112 | .............. |
| ANARGYA KEANO ARIZONA MARICI | 25051030096 | .............. |

Yogyakarta, Mei 2026
