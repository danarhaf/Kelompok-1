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
# 1. BENCHMARK QUEUE
# Operasi: enqueue O(1), dequeue O(1)
# ════════════════════════════════════════════════════════════

def benchmark_queue(ukuran_list: list) -> list:
    print('\n[QUEUE] Memulai benchmark...')
    hasil = []

    for n in ukuran_list:
        nim_list = [f'NIM-{i:03d}' for i in range(n)]

        # ── enqueue N elemen ──────────────────────────────
        def uji_enqueue(nim_list=nim_list):
            q = Queue()
            for nim in nim_list:
                q.enqueue(nim)

        t_enqueue = ukur_waktu(uji_enqueue)

        # ── dequeue N elemen ──────────────────────────────
        def uji_dequeue(nim_list=nim_list):
            q = Queue()
            for nim in nim_list:
                q.enqueue(nim)
            while not q.is_empty():
                q.dequeue()

        t_dequeue = ukur_waktu(uji_dequeue)

        hasil.append([
            n,
            f'{t_enqueue:.6f}',
            f'{t_dequeue:.6f}',
            'O(1) per op',
        ])

    cetak_tabel(
        'QUEUE — enqueue & dequeue (rata-rata 5 ulangan)',
        ['N', 'enqueue N (s)', 'dequeue N (s)', 'Big-O per operasi'],
        hasil,
    )
    return hasil