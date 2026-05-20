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
    
    # ----------------------------------------------------------
    # inisialisasi_antrian
    # Daftarkan semua ISBN ke dict antrian saat startup.
    # Big-O Waktu : O(n) — satu iterasi per buku
    # Big-O Ruang : O(n) — satu Queue kosong per buku
    # ----------------------------------------------------------
    def inisialisasi_antrian(self, daftar_isbn: list[str]):
        """
        Dipanggil sekali di main() setelah generate_koleksi.
        Pastikan setiap ISBN punya slot Queue meski belum ada pemesan.
        """
        for isbn in daftar_isbn:
            if isbn not in self._antrian:
                self._antrian[isbn] = Queue()

    # ----------------------------------------------------------
    # pesan
    # Anggota (nim) memesan buku (isbn) yang sedang dipinjam.
    # Big-O Waktu : O(1) — enqueue ke tail Queue
    # Big-O Ruang : O(1) — satu node baru
    # ----------------------------------------------------------
    def pesan(self, isbn: str, nim: str) -> dict:
        """
        Masukkan nim ke antrian buku isbn.
        Kembalikan dict hasil operasi untuk ditampilkan CLI.
        """
        # pastikan slot ada meski isbn belum terdaftar
        if isbn not in self._antrian:
            self._antrian[isbn] = Queue()