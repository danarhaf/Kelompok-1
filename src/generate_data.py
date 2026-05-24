# ============================================================
# generate_data.py
# Generator koleksi buku dummy untuk sistem perpustakaan
# Seed = 13 (JANGAN diubah agar hasil reprodusibel)
# ============================================================

import random

# import Buku langsung dari data_model (tanpa prefix src.)
# karena file ini dijalankan dari dalam src/ atau sys.path sudah include src/
from data_model import Buku

# konstanta kategori sama seperti di data_model
KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']

# seed diset di sini agar generate_koleksi selalu menghasilkan data yang sama
random.seed(13)


def generate_koleksi(n: int = 80) -> list:
    """
    Hasilkan n objek Buku dengan judul dan pengarang acak.
    Karena random.seed(13) sudah diset, hasilnya selalu sama
    setiap kali program dijalankan (reprodusibel).

    Kata-kata untuk judul diambil acak dari daftar 'kata'.
    Pengarang : 'Penulis-X' dengan X acak 1-20.
    Kategori  : acak dari KATEGORI global.

    Big-O Waktu : O(n)
    Big-O Ruang : O(n) — list n objek Buku
    """
    kata = ['Algoritma', 'Jaringan', 'Python', 'Data', 'Digital',
            'Sistem', 'Kontrol', 'Sinyal', 'Elektronika', 'Fisika']

    return [
        Buku(
            isbn      = f'ISBN-{i:04d}',
            judul     = f'{random.choice(kata)} Vol.{i}',
            pengarang = f'Penulis-{random.randint(1, 20)}',
            kategori  = random.choice(KATEGORI),
        )
        for i in range(1, n + 1)
    ]