# ============================================================
# benchmark.py
# Eksperimen Runtime Semua Struktur Data
# Jalankan dari ROOT project: python experiments/benchmark.py
#
# Mengukur waktu eksekusi operasi utama untuk 3 ukuran data:
#   N = 20, 80, 300
# Hasil ditampilkan sebagai tabel runtime di terminal.
# Sesuai syarat dosen: minimal 3 ukuran dataset berbeda.
# ============================================================

import sys
import os
import time
import random

# tambahkan src/ dan src/modules/ ke path
# agar semua import bisa ditemukan saat dijalankan dari root project
_ROOT = os.path.join(os.path.dirname(__file__), '..')
_SRC  = os.path.join(_ROOT, 'src')
_MOD  = os.path.join(_ROOT, 'src', 'modules')

sys.path.insert(0, _SRC)   # untuk data_structures, data_model, generate_data
sys.path.insert(0, _MOD)   # untuk modul_1 s.d. modul_6

from data_structures.queue_ll import Queue
from data_structures.stack    import Stack
from data_structures.bst      import BSTKatalog
from data_structures.graph    import GraphRekBuku
from data_model               import Buku, STATUS
from generate_data            import generate_koleksi
from modules.modul_5          import (LinkedListLaporan,
                                    shell_sort_durasi,
                                    merge_sort_frekuensi)

# seed tetap agar hasil reprodusibel
random.seed(13)

# ── utilitas ─────────────────────────────────────────────────

def ukur_waktu(fungsi, *args, ulang: int = 5):
    """
    Jalankan fungsi sebanyak `ulang` kali, kembalikan waktu rata-rata (detik).
    Pengulangan mengurangi noise pengukuran waktu.
    Big-O pengukuran: O(ulang * kompleksitas_fungsi)
    """
    total = 0.0
    for _ in range(ulang):
        t0 = time.perf_counter()
        fungsi(*args)
        total += time.perf_counter() - t0
    return total / ulang


def cetak_tabel(judul: str, header: list, baris: list):
    """Cetak tabel hasil benchmark ke terminal."""
    lebar = [max(len(str(h)), max(len(str(b[i])) for b in baris))
            for i, h in enumerate(header)]
    sep = '-' * (sum(lebar) + len(lebar) * 3 + 1)

    print(f'\n{"=" * len(sep)}')
    print(f'  {judul}')
    print(sep)
    print('  ' + ' | '.join(str(h).ljust(lebar[i]) for i, h in enumerate(header)))
    print(sep)
    for b in baris:
        print('  ' + ' | '.join(str(b[i]).ljust(lebar[i]) for i in range(len(header))))
    print(sep)


def buat_buku(isbn: str) -> Buku:
    """Helper: buat objek Buku dummy untuk benchmark."""
    return Buku(
        isbn=isbn,
        judul=f'Judul-{isbn}',
        pengarang='Penulis-Test',
        kategori='Teknik',
        status=STATUS['TERSEDIA'],
    )

# ════════════════════════════════════════════════════════════
# 3. BENCHMARK BST
# Operasi: insert O(log n), search O(log n), inorder O(n)
# Dua skenario: data acak (rata-rata) & data terurut (worst-case)
# ════════════════════════════════════════════════════════════

def benchmark_bst(ukuran_list: list) -> list:
    print('\n[BST] Memulai benchmark...')
    hasil = []

    for n in ukuran_list:
        isbn_urut = [f'ISBN-{i:04d}' for i in range(1, n + 1)]
        isbn_acak = isbn_urut.copy()
        random.shuffle(isbn_acak)

        # ── insert acak (rata-rata case) ──────────────────
        def uji_insert_acak(isbn_acak=isbn_acak):
            pohon = BSTKatalog()
            for isbn in isbn_acak:
                pohon.insert(buat_buku(isbn))

        t_insert_acak = ukur_waktu(uji_insert_acak)

        # ── insert terurut (worst-case: pohon miring) ─────
        def uji_insert_urut(isbn_urut=isbn_urut):
            pohon = BSTKatalog()
            for isbn in isbn_urut:
                pohon.insert(buat_buku(isbn))

        t_insert_urut = ukur_waktu(uji_insert_urut)

        # ── search pada pohon acak ────────────────────────
        pohon_acak = BSTKatalog()
        for isbn in isbn_acak:
            pohon_acak.insert(buat_buku(isbn))

        isbn_cari = isbn_acak[n // 2]

        def uji_search(pohon_acak=pohon_acak, isbn_cari=isbn_cari):
            pohon_acak.search(isbn_cari)

        t_search = ukur_waktu(uji_search, ulang=20)

        # ── inorder O(n) ──────────────────────────────────
        def uji_inorder(pohon_acak=pohon_acak):
            pohon_acak.inorder()

        t_inorder = ukur_waktu(uji_inorder)

        # tinggi pohon untuk bukti empiris O(log n) vs O(n)
        pohon_urut = BSTKatalog()
        for isbn in isbn_urut:
            pohon_urut.insert(buat_buku(isbn))

        tinggi_acak = pohon_acak.hitung_tinggi()
        tinggi_urut = pohon_urut.hitung_tinggi()

        hasil.append([
            n,
            f'{t_insert_acak:.6f}',
            f'{t_insert_urut:.6f}',
            f'{t_search:.6f}',
            f'{t_inorder:.6f}',
            tinggi_acak,
            tinggi_urut,
        ])

    cetak_tabel(
        'BST — insert / search / inorder (rata-rata 5 ulangan)',
        ['N', 'insert acak (s)', 'insert urut (s)',
        'search (s)', 'inorder (s)', 'tinggi acak', 'tinggi urut'],
        hasil,
    )
    print('  Catatan: tinggi acak ≈ O(log n), tinggi urut = O(n) [worst-case]')
    print('  Relevan untuk Pertanyaan Analisis no. 1')
    return hasil
