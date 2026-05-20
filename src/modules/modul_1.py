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
    
        # cek apakah nim sudah ada di antrian (hindari duplikat)
        # Big-O cek duplikat: O(k) — k = panjang antrian buku ini
        if self._sudah_antri(isbn, nim):
            return {
                'berhasil': False,
                'pesan'   : f'[ANTRIAN] {nim} sudah ada di antrian {isbn}.',
                'big_o'   : 'O(k) cek duplikat, k=panjang antrian',
            }
            
        self._antrian[isbn].enqueue(nim)
        posisi = len(self._antrian[isbn])

        return {
            'berhasil': True,
            'pesan'   : (f'[ANTRIAN] {nim} berhasil masuk antrian {isbn}. '
                         f'Posisi ke-{posisi}.'),
            'big_o'   : 'enqueue O(1)',
        }

    # ----------------------------------------------------------
    # batalkan_pesan
    # Anggota membatalkan pesanan — hapus nim dari antrian.
    # Karena Queue tidak support random delete, kita rebuild.
    # Big-O Waktu : O(k) — traversal seluruh antrian buku ini
    # Big-O Ruang : O(k) — Queue sementara
    # ----------------------------------------------------------
    def batalkan_pesan(self, isbn: str, nim: str) -> dict:
        """
        Hapus nim dari antrian isbn.
        Rebuild queue tanpa nim yang dibatalkan.
        """
        if isbn not in self._antrian or self._antrian[isbn].is_empty():
            return {
                'berhasil': False,
                'pesan'   : f'[ANTRIAN] Tidak ada antrian untuk {isbn}.',
                'big_o'   : 'O(1)',
            }

        # ambil semua anggota antrian ke list sementara
        # Big-O: O(k)
        semua = self._antrian[isbn].tampilkan_antrian()

        if nim not in semua:
            return {
                'berhasil': False,
                'pesan'   : f'[ANTRIAN] {nim} tidak ditemukan di antrian {isbn}.',
                'big_o'   : 'O(k) traversal',
            }

        # rebuild queue tanpa nim yang dibatalkan
        queue_baru = Queue()
        for anggota in semua:
            if anggota != nim:
                queue_baru.enqueue(anggota)   # O(1) per enqueue

        self._antrian[isbn] = queue_baru

        return {
            'berhasil': True,
            'pesan'   : f'[ANTRIAN] Pesanan {nim} untuk {isbn} berhasil dibatalkan.',
            'big_o'   : 'O(k) rebuild antrian',
        }

    # ----------------------------------------------------------
    # proses_pengembalian
    # Saat buku dikembalikan, ambil pemesan pertama di antrian.
    # Big-O Waktu : O(1) — dequeue dari head
    # ----------------------------------------------------------
    def proses_pengembalian(self, isbn: str) -> str | None:
        """
        Dequeue nim terdepan sebagai pemesan prioritas.
        Kembalikan nim jika ada, None jika antrian kosong.
        Dipanggil oleh modul_2 (proses_kembalikan).
        """
        if isbn not in self._antrian or self._antrian[isbn].is_empty():
            return None   # tidak ada yang mengantri
        return self._antrian[isbn].dequeue()   # O(1)  

    # ----------------------------------------------------------
    # lihat_antrian
    # Tampilkan seluruh isi antrian suatu buku (untuk CLI ANTRIAN).
    # Big-O Waktu : O(k) — traversal antrian
    # ----------------------------------------------------------
    def lihat_antrian(self, isbn: str) -> dict:
        """
        Kembalikan list nim dalam antrian isbn beserta info ukuran.
        """
        if isbn not in self._antrian:
            return {
                'isbn'   : isbn,
                'antrian': [],
                'panjang': 0,
                'big_o'  : 'O(1)',
            }

        isi = self._antrian[isbn].tampilkan_antrian()   # O(k)
        return {
            'isbn'   : isbn,
            'antrian': isi,
            'panjang': len(isi),
            'big_o'  : 'O(k) traversal antrian',
        }

    # ----------------------------------------------------------
    # _sudah_antri — cek apakah nim sudah ada di antrian isbn
    # Big-O Waktu : O(k)
    # ----------------------------------------------------------
    def _sudah_antri(self, isbn: str, nim: str) -> bool:
        if isbn not in self._antrian:
            return False
        return nim in self._antrian[isbn].tampilkan_antrian()
    
    