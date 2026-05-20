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
    