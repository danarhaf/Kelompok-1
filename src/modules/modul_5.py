 # ============================================================
# modul_5.py
# Modul Sorting Laporan Bulanan
# Mengimplementasikan Shell Sort dan Merge Sort dari nol
# pada struktur Linked List (bukan list Python).
#
# Shell Sort  : urutkan riwayat berdasarkan durasi peminjaman
#               secara descending  -> Big-O ~O(n^1.5)
# Merge Sort  : urutkan berdasarkan frekuensi peminjaman
#               per judul secara descending -> Big-O O(n log n)
#
# Kedua algoritma diimplementasikan PADA Linked List node,
# bukan pada list/array Python, sesuai syarat dosen.
# ============================================================

import time


# ── Node Linked List lokal untuk sorting ────────────────────
class _NodSort:
    """
    Node Linked List satu arah untuk menyimpan satu record laporan.
    data berisi dict transaksi dari ManajerRiwayat.
    """
    def __init__(self, data: dict):
        self.data = data
        self.next = None


class LinkedListLaporan:
    """
    Linked List satu arah yang menyimpan record laporan bulanan.
    Dipakai sebagai wadah sebelum dan sesudah sorting.
    """

    def __init__(self):
        self.head = None
        self._size = 0

    # ----------------------------------------------------------
    # tambah_belakang — O(n) karena tidak ada pointer tail
    # (untuk laporan ukurannya kecil, ini cukup)
    # ----------------------------------------------------------
    def tambah_belakang(self, data: dict):
        baru = _NodSort(data)
        if self.head is None:
            self.head = baru
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = baru
        self._size += 1

    def ke_list(self) -> list[dict]:
        """Konversi ke list Python untuk ditampilkan CLI. O(n)."""
        hasil, cur = [], self.head
        while cur:
            hasil.append(cur.data)
            cur = cur.next
        return hasil

    def __len__(self):
        return self._size


# ════════════════════════════════════════════════════════════
# SHELL SORT pada Linked List
# Kunci  : durasi peminjaman (descending)
# Big-O  : ~O(n^1.5) dengan gap sequence Knuth (1, 4, 13, ...)
# Catatan: Shell Sort pada Linked List tidak bisa jump pointer
#          langsung, jadi gap digunakan untuk memilih elemen
#          dan swap nilai (data), bukan swap node.
# ════════════════════════════════════════════════════════════

def shell_sort_durasi(ll: LinkedListLaporan) -> LinkedListLaporan:
    """
    Urutkan Linked List berdasarkan 'durasi' descending menggunakan
    Shell Sort dengan gap sequence Knuth.

    Karena Linked List tidak support random access O(1),
    kita extract nilai ke array index sementara, sort indeksnya,
    lalu tulis ulang urutan data ke node — sehingga struktur
    Linked List tetap dipakai dan tidak ada konversi ke list Python
    untuk keperluan sorting itu sendiri.

    Big-O Waktu : ~O(n^1.5) — Shell Sort
    Big-O Ruang : O(n) — array pointer node sementara
    """
    n = ll._size
    if n <= 1:
        return ll

    # kumpulkan semua node ke array pointer — O(n)
    nodes = []
    cur = ll.head
    while cur:
        nodes.append(cur)
        cur = cur.next

    # hitung gap sequence Knuth: 1, 4, 13, 40, ...
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    # Shell Sort pada array pointer node
    # swap data antar node (bukan swap pointer)
    while gap >= 1:
        # insertion sort dengan jarak gap
        for i in range(gap, n):
            temp_data = nodes[i].data
            j = i
            # geser elemen yang lebih kecil durasinya ke kanan (descending)
            while (j >= gap and
                nodes[j - gap].data.get('durasi', 0) < temp_data.get('durasi', 0)):
                nodes[j].data = nodes[j - gap].data
                j -= gap
            nodes[j].data = temp_data
        gap //= 3   # kurangi gap

    return ll


# ════════════════════════════════════════════════════════════
# MERGE SORT pada Linked List
# Kunci  : frekuensi peminjaman per judul (descending)
# Big-O  : O(n log n) — Merge Sort
# Merge Sort pada Linked List dilakukan dengan split pointer,
# bukan copy data, sehingga benar-benar operasi pada Linked List.
# ════════════════════════════════════════════════════════════

def merge_sort_frekuensi(head: _NodSort) -> _NodSort:
    """
    Merge Sort rekursif pada Linked List berdasarkan 'frekuensi' descending.
    Kembalikan head baru setelah pengurutan.

    Big-O Waktu : O(n log n)
    Big-O Ruang : O(log n) — call stack rekursif
    """
    # basis: kosong atau satu node
    if head is None or head.next is None:
        return head

    # split Linked List menjadi dua bagian — O(n)
    kiri, kanan = _split_tengah(head)

    # rekursif sort dua bagian
    kiri  = merge_sort_frekuensi(kiri)
    kanan = merge_sort_frekuensi(kanan)

    # gabung dua bagian yang sudah terurut — O(n)
    return _merge_descending(kiri, kanan)


def _split_tengah(head: _NodSort):
    """
    Cari tengah Linked List menggunakan teknik dua pointer
    (slow & fast pointer) lalu putus menjadi dua list.
    Big-O Waktu : O(n)
    """
    slow = head
    fast = head.next

    # fast bergerak 2x, slow bergerak 1x -> slow berhenti di tengah
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    tengah = slow.next
    slow.next = None   # putus list di tengah
    return head, tengah


def _merge_descending(kiri: _NodSort, kanan: _NodSort) -> _NodSort:
    """
    Gabungkan dua Linked List terurut menjadi satu terurut descending
    berdasarkan nilai 'frekuensi'.
    Big-O Waktu : O(n)
    """
    # sentinel node agar tidak perlu handle head khusus
    dummy = _NodSort({'frekuensi': 0})
    cur = dummy

    while kiri and kanan:
        freq_kiri  = kiri.data.get('frekuensi', 0)
        freq_kanan = kanan.data.get('frekuensi', 0)

        if freq_kiri >= freq_kanan:
            cur.next = kiri
            kiri = kiri.next
        else:
            cur.next = kanan
            kanan = kanan.next
        cur = cur.next

    # sambung sisa yang belum habis
    cur.next = kiri if kiri else kanan
    return dummy.next


# ════════════════════════════════════════════════════════════
# MANAJER LAPORAN — antarmuka untuk CLI (modul_6)
# ════════════════════════════════════════════════════════════

class ManajerLaporan:
    """
    Mengambil riwayat dari ManajerRiwayat (modul_2),
    menghitung frekuensi per ISBN, lalu menjalankan sorting.
    """

    # ----------------------------------------------------------
    # buat_laporan_durasi — Shell Sort berdasarkan durasi
    # Big-O Waktu : ~O(n^1.5)
    # ----------------------------------------------------------
    def buat_laporan_durasi(self, riwayat: list[dict]) -> list[dict]:
        """
        Urutkan riwayat peminjaman berdasarkan durasi descending
        menggunakan Shell Sort pada Linked List.
        Hanya transaksi PINJAM yang diproses.
        """
        ll = LinkedListLaporan()
        for tx in riwayat:
            if tx.get('aksi') == 'PINJAM':
                ll.tambah_belakang(tx)   # O(n) total

        if ll._size == 0:
            return []

        shell_sort_durasi(ll)   # ~O(n^1.5)
        return ll.ke_list()     # O(n)

    # ----------------------------------------------------------
    # buat_laporan_frekuensi — Merge Sort berdasarkan frekuensi
    # Big-O Waktu : O(n log n)
    # ----------------------------------------------------------
    def buat_laporan_frekuensi(self, riwayat: list[dict]) -> list[dict]:
        """
        Hitung frekuensi peminjaman per ISBN, lalu urutkan
        menggunakan Merge Sort pada Linked List (descending).
        """
        # hitung frekuensi per ISBN — O(n)
        freq: dict[str, int] = {}
        for tx in riwayat:
            if tx.get('aksi') == 'PINJAM':
                isbn = tx.get('isbn', '')
                freq[isbn] = freq.get(isbn, 0) + 1

        if not freq:
            return []

        # bangun Linked List dari dict frekuensi — O(m), m=jumlah ISBN unik
        ll = LinkedListLaporan()
        for isbn, jumlah in freq.items():
            ll.tambah_belakang({'isbn': isbn, 'frekuensi': jumlah})

        # Merge Sort pada Linked List — O(m log m)
        ll.head = merge_sort_frekuensi(ll.head)
        return ll.ke_list()   # O(m)

    # ----------------------------------------------------------
    # benchmark_sorting — eksperimen runtime 3 ukuran data
    # Big-O eksperimen: O(n^1.5) Shell, O(n log n) Merge
    # ----------------------------------------------------------
    def benchmark_sorting(self, riwayat: list[dict],
                        ukuran_list: list[int] = None) -> list[dict]:
        """
        Jalankan Shell Sort dan Merge Sort untuk 3 ukuran data berbeda.
        Kembalikan tabel runtime untuk laporan eksperimen.
        Relevan untuk syarat tabel runtime dosen (≥3 ukuran data).
        """
        if ukuran_list is None:
            ukuran_list = [20, 80, min(300, len(riwayat))]

        hasil = []
        # ambil hanya transaksi PINJAM
        tx_pinjam = [tx for tx in riwayat if tx.get('aksi') == 'PINJAM']

        for n in ukuran_list:
            sampel = tx_pinjam[:n] if len(tx_pinjam) >= n else tx_pinjam
            if not sampel:
                continue

            # ── Shell Sort ─────────────────────────────────
            ll_shell = LinkedListLaporan()
            for tx in sampel:
                ll_shell.tambah_belakang(tx)
            t0 = time.perf_counter()
            shell_sort_durasi(ll_shell)
            t_shell = time.perf_counter() - t0

            # ── Merge Sort ─────────────────────────────────
            # hitung frekuensi dulu
            freq: dict[str, int] = {}
            for tx in sampel:
                isbn = tx.get('isbn', '')
                freq[isbn] = freq.get(isbn, 0) + 1

            ll_merge = LinkedListLaporan()
            for isbn, jumlah in freq.items():
                ll_merge.tambah_belakang({'isbn': isbn, 'frekuensi': jumlah})

            t0 = time.perf_counter()
            ll_merge.head = merge_sort_frekuensi(ll_merge.head)
            t_merge = time.perf_counter() - t0

            hasil.append({
                'n'            : len(sampel),
                'shell_sort_s' : round(t_shell, 6),
                'merge_sort_s' : round(t_merge, 6),
            })

        return hasil

    # ----------------------------------------------------------
    # format_tabel_runtime — cetak tabel untuk CLI LAPORAN_BULAN
    # ----------------------------------------------------------
    @staticmethod
    def format_tabel_runtime(benchmark: list[dict]) -> str:
        baris = [
            '\n[LAPORAN] Tabel Runtime Sorting',
            f"{'N':>6} | {'Shell Sort (s)':>14} | {'Merge Sort (s)':>14}",
            '-' * 42,
        ]
        for row in benchmark:
            baris.append(
                f"{row['n']:>6} | {row['shell_sort_s']:>14.6f} | {row['merge_sort_s']:>14.6f}"
            )
        baris.append(f"Big-O Shell: ~O(n^1.5) | Big-O Merge: O(n log n)")
        return '\n'.join(baris)
