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
# 4. BENCHMARK GRAPH (BFS)
# Operasi: add_copinjam O(deg), BFS O(V+E)
# ════════════════════════════════════════════════════════════

def benchmark_graph(ukuran_list: list) -> list:
    print('\n[GRAPH] Memulai benchmark...')
    hasil = []

    for n in ukuran_list:
        isbn_list = [f'ISBN-{i:04d}' for i in range(1, n + 1)]

        # buat pasangan ko-pinjam acak sebanyak n*2 transaksi
        pasangan = []
        for _ in range(n * 2):
            a, b = random.sample(isbn_list, 2)
            pasangan.append((a, b))

        # ── add_copinjam ──────────────────────────────────
        def uji_add(pasangan=pasangan):
            g = GraphRekBuku()
            for a, b in pasangan:
                g.add_copinjam(a, b)

        t_add = ukur_waktu(uji_add)

        # ── BFS rekomendasi ───────────────────────────────
        g_penuh = GraphRekBuku()
        for a, b in pasangan:
            g_penuh.add_copinjam(a, b)

        sumber = isbn_list[0]

        def uji_bfs(g_penuh=g_penuh, sumber=sumber):
            g_penuh.rekomendasikan(sumber, max_hop=2)

        t_bfs = ukur_waktu(uji_bfs, ulang=10)

        info = g_penuh.info_graf()

        hasil.append([
            n,
            info['vertex'],
            info['edge'],
            f'{info["derajat_rata_rata"]:.2f}',
            f'{t_add:.6f}',
            f'{t_bfs:.6f}',
        ])

    cetak_tabel(
        'GRAPH — add_copinjam & BFS rekomendasi (rata-rata 5 ulangan)',
        ['N buku', 'V', 'E', 'deg rata-rata',
         'add_copinjam N*2 (s)', 'BFS O(V+E) (s)'],
        hasil,
    )
    print('  Catatan: BFS O(V+E), makin banyak edge makin lama')
    print('  Relevan untuk Pertanyaan Analisis no. 3')
    return hasil