# ============================================================
# modul_3.py
# Modul BST Katalog Buku
# Menangani operasi bisnis utama: CARI_BUKU, PINJAM, KEMBALIKAN.
# BST dipakai sebagai katalog dengan kunci ISBN.
# Setiap operasi yang mengubah status buku juga mencatat
# transaksi ke ManajerRiwayat (modul_2).
#
# Struktur data : BST berbasis Linked Node (bst.py)
# Big-O search  : O(log n) rata-rata
# Big-O insert  : O(log n) rata-rata
# Big-O delete  : O(log n) rata-rata
# ============================================================

from data_structures.bst import BSTKatalog
from data_model import Buku, STATUS


# label status untuk ditampilkan CLI
LABEL_STATUS = {
    STATUS['TERSEDIA']: 'TERSEDIA',
    STATUS['DIPINJAM']: 'DIPINJAM',
    STATUS['DIPESAN'] : 'DIPESAN',
}


class ManajerKatalog:
    """
    Lapisan bisnis di atas BSTKatalog.
    Menerima panggilan dari CLI (modul_6) dan berkoordinasi
    dengan ManajerRiwayat (modul_2) dan ManajerAntrian (modul_1).
    """

    def __init__(self):
        self._bst = BSTKatalog()

    # ----------------------------------------------------------
    # muat_koleksi — insert semua buku dari generate_koleksi
    # Big-O Waktu : O(n log n) rata-rata — n kali insert O(log n)
    # Big-O Ruang : O(n)
    # ----------------------------------------------------------
    def muat_koleksi(self, daftar_buku: list[Buku]):
        """Dipanggil sekali di main() saat startup."""
        for buku in daftar_buku:
            self._bst.insert(buku)   # O(log n)