# ============================================================
# modul_1.py
# Modul Queue Antrian Pemesanan Buku
# Setiap ISBN punya satu Queue sendiri (1 queue per buku).
# Ketika buku sedang dipinjam dan anggota lain memesan,
# NIM anggota masuk ke queue buku tersebut.
# Saat buku dikembalikan, anggota di head queue diprioritaskan.
#
# Struktur data : Queue berbasis Linked List (queue_ll.py)
# Big-O enqueue : O(1)
# Big-O dequeue : O(1)
# ============================================================

import time

from data_structures.queue_ll import Queue
from data_model import STATUS


class ManajerAntrian:
    """
    Mengelola satu dict berisi Queue per ISBN.
    Dipanggil oleh CLI (modul_6) dan modul_2 (untuk undo pesan).

    Struktur internal:
      _antrian : { isbn -> Queue of nim }
    """

    def __init__(self):
        # dict: isbn -> Queue
        # diisi saat sistem pertama kali load koleksi
        self._antrian: dict[str, Queue] = {}