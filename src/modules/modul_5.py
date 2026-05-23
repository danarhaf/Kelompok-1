# ============================================================
# modul_5.py
# Modul Sorting Laporan Bulanan
# Menggunakan Shell Sort dan Merge Sort dari data_structures/sorting.py
# Linked List node dari data_structures/linked_list.py
#
# Shell Sort  : ~O(n^1.5) — sorting durasi peminjaman descending
# Merge Sort  : O(n log n) — sorting frekuensi per ISBN descending
# ============================================================

import time

from data_structures.linked_list import LLNode
from data_structures.sorting     import shell_sort_durasi, merge_sort_frekuensi


class LinkedListLaporan:
    """
    Linked List khusus untuk menyimpan record laporan bulanan.
    Menggunakan Node dari linked_list.py (bukan definisi ulang).
    Dipakai sebagai wadah sebelum dan sesudah sorting.
    """

    def __init__(self):
        self.head = None
        self._size = 0

    # ----------------------------------------------------------
    # tambah_belakang — tambah record di akhir list
    # Big-O Waktu : O(n) — tidak ada pointer tail di kelas ini
    # (ukuran data laporan kecil, sehingga ini cukup)
    # ----------------------------------------------------------
    def tambah_belakang(self, data: dict):
        baru = LLNode(data)   # pakai Node dari linked_list.py
        if self.head is None:
            self.head = baru
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = baru
        self._size += 1

    # ----------------------------------------------------------
    # ke_list — konversi ke list Python untuk ditampilkan CLI
    # Big-O Waktu : O(n)
    # ----------------------------------------------------------
    def ke_list(self) -> list:
        hasil, cur = [], self.head
        while cur:
            hasil.append(cur.data)
            cur = cur.next
        return hasil

    def __len__(self):
        return self._size


class ManajerLaporan:
    """
    Mengambil riwayat dari ManajerRiwayat (modul_2),
    menghitung frekuensi per ISBN, lalu menjalankan sorting.
    Fungsi sorting diimport dari data_structures/sorting.py.
    """

    # ----------------------------------------------------------
    # buat_laporan_durasi — Shell Sort berdasarkan durasi
    # Big-O Waktu : ~O(n^1.5) — didelegasikan ke sorting.py
    # ----------------------------------------------------------
    def buat_laporan_durasi(self, riwayat: list) -> list:
        """
        Urutkan riwayat peminjaman berdasarkan durasi descending
        menggunakan Shell Sort dari sorting.py pada Linked List.
        Hanya transaksi PINJAM yang diproses.
        """
        ll = LinkedListLaporan()
        for tx in riwayat:
            if tx.get('aksi') == 'PINJAM':
                ll.tambah_belakang(tx)   # O(n) total

        if ll._size == 0:
            return []

        # delegasikan sorting ke sorting.py — ~O(n^1.5)
        shell_sort_durasi(ll.head)
        return ll.ke_list()   # O(n)

    # ----------------------------------------------------------
    # buat_laporan_frekuensi — Merge Sort berdasarkan frekuensi
    # Big-O Waktu : O(n log n) — didelegasikan ke sorting.py
    # ----------------------------------------------------------
    def buat_laporan_frekuensi(self, riwayat: list) -> list:
        """
        Hitung frekuensi peminjaman per ISBN, lalu urutkan
        menggunakan Merge Sort dari sorting.py pada Linked List.
        """
        # hitung frekuensi per ISBN — O(n)
        freq: dict = {}
        for tx in riwayat:
            if tx.get('aksi') == 'PINJAM':
                isbn = tx.get('isbn', '')
                freq[isbn] = freq.get(isbn, 0) + 1

        if not freq:
            return []

        # bangun Linked List dari dict frekuensi — O(m)
        ll = LinkedListLaporan()
        for isbn, jumlah in freq.items():
            ll.tambah_belakang({'isbn': isbn, 'frekuensi': jumlah})

        # delegasikan ke sorting.py — O(m log m)
        ll.head = merge_sort_frekuensi(ll.head)
        return ll.ke_list()   # O(m)

    # ----------------------------------------------------------
    # benchmark_sorting — eksperimen runtime 3 ukuran data
    # Big-O: Shell ~O(n^1.5), Merge O(n log n)
    # Sesuai syarat dosen: tabel runtime minimal 3 ukuran data
    # ----------------------------------------------------------
    def benchmark_sorting(self, riwayat: list,
                        ukuran_list: list = None) -> list:
        """
        Jalankan Shell Sort dan Merge Sort untuk 3 ukuran data.
        Kembalikan tabel runtime untuk laporan eksperimen.
        """
        if ukuran_list is None:
            ukuran_list = [20, 80, min(300, len(riwayat))]

        hasil = []
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
            shell_sort_durasi(ll_shell.head)   # dari sorting.py
            t_shell = time.perf_counter() - t0

            # ── Merge Sort ─────────────────────────────────
            freq: dict = {}
            for tx in sampel:
                isbn = tx.get('isbn', '')
                freq[isbn] = freq.get(isbn, 0) + 1

            ll_merge = LinkedListLaporan()
            for isbn, jumlah in freq.items():
                ll_merge.tambah_belakang({'isbn': isbn, 'frekuensi': jumlah})

            t0 = time.perf_counter()
            ll_merge.head = merge_sort_frekuensi(ll_merge.head)   # dari sorting.py
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
    def format_tabel_runtime(benchmark: list) -> str:
        baris = [
            '\n[LAPORAN] Tabel Runtime Sorting',
            f"{'N':>6} | {'Shell Sort (s)':>14} | {'Merge Sort (s)':>14}",
            '-' * 42,
        ]
        for row in benchmark:
            baris.append(
                f"{row['n']:>6} | {row['shell_sort_s']:>14.6f} | {row['merge_sort_s']:>14.6f}"
            )
        baris.append("Big-O Shell: ~O(n^1.5) | Big-O Merge: O(n log n)")
        return '\n'.join(baris)