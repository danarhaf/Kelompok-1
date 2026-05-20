# ============================================================
#  GENERATE KOLEKSI BUKU
#  Membuat 80 buku dummy dengan data acak menggunakan seed=13
#  Format ISBN: 'ISBN-XXXX' (4 digit, zero-padded)
# ============================================================

import numpy as np
import random 

from src.data_model import Buku

# ── Konstanta global sesuai starter code (sama seperti di data_model) ───────────────────────
KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']


def generate_koleksi(n=80):
    """
    Hasilkan n objek Buku dengan judul dan pengarang acak.
    Karena random.seed(13) sudah diset di awal, hasilnya
    selalu sama setiap kali program dijalankan (reprodusibel).

    Kata-kata untuk judul diambil acak dari daftar 'kata'.
    Pengarang: 'Penulis-X' dengan X acak 1-20.
    Kategori : acak dari KATEGORI global.
    """
    kata = ['Algoritma', 'Jaringan', 'Python', 'Data', 'Digital',
            'Sistem', 'Kontrol', 'Sinyal', 'Elektronika', 'Fisika']

    return [
        Buku(
            isbn      = f'ISBN-{i:04d}',                      # ISBN-0001 s.d. ISBN-0080
            judul     = f'{random.choice(kata)} Vol.{i}',     # misal: 'Python Vol.7'
            pengarang = f'Penulis-{random.randint(1, 20)}',   # misal: 'Penulis-14'
            kategori  = random.choice(KATEGORI),               # acak dari 5 kategori
        )
        for i in range(1, n + 1)
]