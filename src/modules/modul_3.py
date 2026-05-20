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
            
    # ----------------------------------------------------------
    # cari_buku — cari satu buku berdasarkan ISBN
    # Big-O Waktu : O(log n) rata-rata
    # ----------------------------------------------------------
    def cari_buku(self, isbn: str) -> dict:
        """
        Cari buku di BST. Kembalikan dict info buku atau pesan error.
        Dipanggil oleh CLI perintah CARI_BUKU <isbn>.
        """
        buku = self._bst.search(isbn)   # O(log n)
        if buku is None:
            return {
                'berhasil': False,
                'pesan'   : f'[KATALOG] Buku {isbn} tidak ditemukan.',
                'big_o'   : 'O(log n) BST search',
            }
        return {
            'berhasil': True,
            'buku'    : buku,
            'status'  : LABEL_STATUS.get(buku.status, '?'),
            'pesan'   : self._format_buku(buku),
            'big_o'   : 'O(log n) BST search',
        }
    # ----------------------------------------------------------
    # pinjam — proses peminjaman buku oleh anggota
    # Big-O Waktu : O(log n) search + O(log n) update = O(log n)
    # ----------------------------------------------------------
    def pinjam(self, isbn: str, nim: str,
            manajer_riwayat, durasi: int = 14) -> dict:
        """
        Syarat: buku harus berstatus TERSEDIA.
        Jika berhasil, status diubah ke DIPINJAM dan transaksi dicatat.
        Jika sedang DIPINJAM/DIPESAN, sarankan pesan via modul_1.
        """
        buku = self._bst.search(isbn)   # O(log n)

        if buku is None:
            return {
                'berhasil': False,
                'pesan'   : f'[PINJAM] Buku {isbn} tidak ditemukan di katalog.',
                'big_o'   : 'O(log n) BST search',
            }

        if buku.status != STATUS['TERSEDIA']:
            label = LABEL_STATUS.get(buku.status, '?')
            return {
                'berhasil': False,
                'pesan'   : (f'[PINJAM] Buku {isbn} sedang {label}. '
                            f'Gunakan PESAN {nim} {isbn} untuk mengantri.'),
                'big_o'   : 'O(log n) BST search',
            }

        # ubah status ke DIPINJAM
        self._bst.update_status(isbn, STATUS['DIPINJAM'])   # O(log n)

        # catat ke stack riwayat — O(1)
        tx_id = manajer_riwayat.catat('PINJAM', nim, isbn, durasi)

        return {
            'berhasil': True,
            'tx_id'   : tx_id,
            'pesan'   : (f'[PINJAM] Berhasil. {nim} meminjam {isbn} '
                        f'selama {durasi} hari. TX-{tx_id:04d}'),
            'big_o'   : 'O(log n) BST search + update',
        }
