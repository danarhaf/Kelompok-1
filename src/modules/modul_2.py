# ============================================================
# modul_2.py
# Modul Stack Riwayat Transaksi & Undo
# Setiap aksi PINJAM / KEMBALIKAN / PESAN / BATALKAN_PESAN
# dicatat di stack global. Fitur BATALKAN_TERAKHIR (undo)
# akan mem-pop transaksi terbaru dan membalik efeknya.
#
# Struktur data : Stack berbasis Linked List (stack.py)
# Big-O push   : O(1)
# Big-O pop    : O(1)
# ============================================================

import time

from data_structures.stack import Stack
from data_model import Peminjaman, STATUS


class ManajerRiwayat:
    """
    Mengelola stack transaksi global perpustakaan.
    Setiap transaksi disimpan sebagai dict berisi:
    {
        'tx_id'   : int,
        'aksi'    : str,   # 'PINJAM' | 'KEMBALIKAN' | 'PESAN' | 'BATAL_PESAN'
        'nim'     : str,
        'isbn'    : str,
        'waktu'   : float, # time.time()
        'durasi'  : int,   # hanya untuk PINJAM
    }
    Dipanggil oleh modul_3 (BST) dan modul_1 (Queue)
    setelah setiap operasi berhasil.
    """

    def __init__(self):
        self._stack    = Stack()
        self._tx_counter = 0   # counter transaksi, naik terus

    # ----------------------------------------------------------
    # catat
    # Rekam satu transaksi ke atas stack.
    # Big-O Waktu : O(1) — push ke top Stack
    # Big-O Ruang : O(1) — satu node baru
    # ----------------------------------------------------------
    def catat(self, aksi: str, nim: str, isbn: str, durasi: int = 14) -> int:
        """
        Simpan transaksi ke stack dan kembalikan tx_id-nya.
        Dipanggil setelah operasi BST berhasil (modul_3).
        """
        self._tx_counter += 1
        transaksi = {
            'tx_id' : self._tx_counter,
            'aksi'  : aksi,
            'nim'   : nim,
            'isbn'  : isbn,
            'waktu' : time.time(),
            'durasi': durasi,
        }
        self._stack.push(transaksi)   # O(1)
        return self._tx_counter
    
    # ----------------------------------------------------------
    # batalkan_terakhir (UNDO)
    # Pop transaksi teratas dan kembalikan detailnya agar
    # modul_3 dan modul_1 bisa membalik efeknya.
    # Big-O Waktu : O(1) — pop dari top Stack
    # ----------------------------------------------------------
    def batalkan_terakhir(self) -> dict | None:
        """
        Ambil transaksi terakhir dari stack.
        Kembalikan dict transaksi jika ada, None jika stack kosong.
        Pemanggil (main / modul_3) bertanggung jawab membalik efeknya.
        """
        tx = self._stack.pop()   # O(1)
        if tx is None:
            return None
        return tx
    
    # ----------------------------------------------------------
    # intip_terakhir — lihat transaksi teratas tanpa menghapus
    # Big-O Waktu : O(1)
    # ----------------------------------------------------------
    def intip_terakhir(self) -> dict | None:
        return self._stack.peek()   # O(1)
    
    # ----------------------------------------------------------
    # riwayat_semua — kembalikan semua transaksi (atas ke bawah)
    # Dipakai modul_5 untuk sorting laporan bulanan.
    # Big-O Waktu : O(n) — traversal seluruh stack
    # Big-O Ruang : O(n)
    # ----------------------------------------------------------
    def riwayat_semua(self) -> list[dict]:
        """
        Kembalikan list semua transaksi dari terbaru ke terlama.
        Tidak mengubah isi stack.
        """
        return self._stack.tampilkan_stack()   # O(n)
    
    # ----------------------------------------------------------
    # archiving — pindah transaksi lama ke list arsip
    # agar stack tidak tumbuh tak terbatas.
    # Big-O Waktu : O(n) — lihat stack.pindah_ke_linked_list
    # Relevan untuk Pertanyaan Analisis no. 4
    # ----------------------------------------------------------
    def archiving(self, maks_simpan: int = 100) -> list[dict]:
        """
        Jika stack melebihi maks_simpan, elemen lama dipindah
        ke list arsip dan dikembalikan ke pemanggil.
        Stack tetap menyimpan maks_simpan transaksi terbaru.
        """
        return self._stack.arsip_transaksi_lama(maks_simpan)   # O(n)
    
    # ----------------------------------------------------------
    # ukuran — jumlah transaksi di stack saat ini
    # Big-O Waktu : O(1)
    # ----------------------------------------------------------
    def ukuran(self) -> int:
        return len(self._stack)
    
    # ----------------------------------------------------------
    # format_tampil — ubah dict transaksi ke string untuk CLI
    # Big-O Waktu : O(1)
    # ----------------------------------------------------------
    @staticmethod
    def format_tampil(tx: dict) -> str:
        """Kembalikan baris ringkasan satu transaksi untuk ditampilkan CLI."""
        from datetime import datetime
        waktu_str = datetime.fromtimestamp(tx['waktu']).strftime('%Y-%m-%d %H:%M:%S')
        return (f"[TX-{tx['tx_id']:04d}] {tx['aksi']:<12} | "
                f"NIM: {tx['nim']} | ISBN: {tx['isbn']} | {waktu_str}")