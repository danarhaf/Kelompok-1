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