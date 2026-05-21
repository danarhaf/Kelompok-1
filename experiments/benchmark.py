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

# ════════════════════════════════════════════════════════════
# 2. BENCHMARK STACK
# Operasi: push O(1), pop O(1)
# ════════════════════════════════════════════════════════════

def benchmark_stack(ukuran_list: list) -> list:
    print('\n[STACK] Memulai benchmark...')
    hasil = []

    for n in ukuran_list:
        tx_list = [{'tx_id': i, 'aksi': 'PINJAM', 'isbn': f'ISBN-{i:04d}',
                    'nim': f'NIM-{i:03d}', 'durasi': 14, 'waktu': time.time()}
                for i in range(n)]

        def uji_push(tx_list=tx_list):
            s = Stack()
            for tx in tx_list:
                s.push(tx)

        t_push = ukur_waktu(uji_push)

        def uji_pop(tx_list=tx_list):
            s = Stack()
            for tx in tx_list:
                s.push(tx)
            while not s.is_empty():
                s.pop()

        t_pop = ukur_waktu(uji_pop)

        hasil.append([
            n,
            f'{t_push:.6f}',
            f'{t_pop:.6f}',
            'O(1) per op',
        ])

    cetak_tabel(
        'STACK — push & pop (rata-rata 5 ulangan)',
        ['N', 'push N (s)', 'pop N (s)', 'Big-O per operasi'],
        hasil,
    )
    return hasil

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

# ════════════════════════════════════════════════════════════
# 5. BENCHMARK SORTING (Shell Sort vs Merge Sort)
# Pada Linked List, bukan list Python
# ════════════════════════════════════════════════════════════

def benchmark_sorting(ukuran_list: list) -> list:
    print('\n[SORTING] Memulai benchmark...')
    hasil = []

    for n in ukuran_list:
        tx_list = [
            {'tx_id': i, 'aksi': 'PINJAM',
            'isbn': f'ISBN-{random.randint(1, 80):04d}',
            'nim': f'NIM-{i:03d}',
            'durasi': random.randint(7, 30),
            'waktu': time.time()}
            for i in range(n)
        ]

        # ── Shell Sort pada Linked List ───────────────────
        def uji_shell(tx_list=tx_list):
            ll = LinkedListLaporan()
            for tx in tx_list:
                ll.tambah_belakang(tx)
            shell_sort_durasi(ll)

        t_shell = ukur_waktu(uji_shell)

        # ── Merge Sort pada Linked List ───────────────────
        freq = {}
        for tx in tx_list:
            isbn = tx['isbn']
            freq[isbn] = freq.get(isbn, 0) + 1

        def uji_merge(freq=freq):
            ll = LinkedListLaporan()
            for isbn, jumlah in freq.items():
                ll.tambah_belakang({'isbn': isbn, 'frekuensi': jumlah})
            merge_sort_frekuensi(ll.head)

        t_merge = ukur_waktu(uji_merge)

        hasil.append([
            n,
            f'{t_shell:.6f}',
            f'{t_merge:.6f}',
            '~O(n^1.5)',
            'O(n log n)',
        ])

    cetak_tabel(
        'SORTING — Shell Sort vs Merge Sort pada Linked List (rata-rata 5 ulangan)',
        ['N', 'Shell Sort (s)', 'Merge Sort (s)',
        'Big-O Shell', 'Big-O Merge'],
        hasil,
    )
    print('  Catatan: Merge Sort lebih konsisten O(n log n),')
    print('  Shell Sort lebih cepat untuk data hampir terurut.')
    return hasil

# ════════════════════════════════════════════════════════════
# 6. BENCHMARK INTEGRASI — simulasi 300 event campuran
# Sesuai parameter sistem: "Operasi CLI minimum 300 event"
# ════════════════════════════════════════════════════════════

def benchmark_integrasi() -> None:
    """
    Simulasi end-to-end 300 event campuran:
    PINJAM, KEMBALIKAN, PESAN, REKOMENDASI.
    Mengukur total waktu pipeline sesuai parameter sistem.
    """
    print('\n[INTEGRASI] Simulasi 300 event campuran...')

    koleksi  = generate_koleksi(80)
    bst      = BSTKatalog()
    antrian  = {b.isbn: Queue() for b in koleksi}
    stack_tx = Stack()
    graf     = GraphRekBuku()

    for b in koleksi:
        bst.insert(b)

    isbn_list = [b.isbn for b in koleksi]
    nim_list  = [f'NIM-{i:03d}' for i in range(1, 61)]
    tx_counter = 0
    sedang_dipinjam = {}

    t_mulai = time.perf_counter()

    for _ in range(300):
        aksi = random.choice(['PINJAM', 'PINJAM', 'KEMBALIKAN', 'PESAN', 'REKOMENDASI'])
        isbn = random.choice(isbn_list)
        nim  = random.choice(nim_list)
        buku = bst.search(isbn)   # O(log n)

        if aksi == 'PINJAM' and buku and buku.status == STATUS['TERSEDIA']:
            bst.update_status(isbn, STATUS['DIPINJAM'])   # O(log n)
            tx_counter += 1
            stack_tx.push({'tx_id': tx_counter, 'aksi': 'PINJAM',
                        'nim': nim, 'isbn': isbn, 'durasi': 14,
                        'waktu': time.time()})           # O(1)
            sedang_dipinjam[isbn] = nim

        elif aksi == 'KEMBALIKAN' and buku and buku.status == STATUS['DIPINJAM']:
            pemesan = antrian[isbn].dequeue()              # O(1)
            status_baru = STATUS['DIPESAN'] if pemesan else STATUS['TERSEDIA']
            bst.update_status(isbn, status_baru)           # O(log n)
            tx_counter += 1
            stack_tx.push({'tx_id': tx_counter, 'aksi': 'KEMBALIKAN',
                        'nim': nim, 'isbn': isbn, 'durasi': 0,
                        'waktu': time.time()})           # O(1)
            sedang_dipinjam.pop(isbn, None)

        elif aksi == 'PESAN' and buku and buku.status == STATUS['DIPINJAM']:
            antrian[isbn].enqueue(nim)                     # O(1)

        elif aksi == 'REKOMENDASI':
            graf.rekomendasikan(isbn, max_hop=2)           # O(V+E)

    total = time.perf_counter() - t_mulai

    print(f'  Total 300 event selesai dalam : {total:.4f} detik')
    print(f'  Transaksi PINJAM/KEMBALIKAN   : {tx_counter}')
    print(f'  Ukuran Stack akhir            : {len(stack_tx)}')
    print(f'  Info Graf                     : {graf.info_graf()}')
    print(f'  Big-O dominan per event       : O(log n) BST + O(1) Stack/Queue')

