# ============================================================
# modul_4.py
# Modul Graph Rekomendasi Ko-pinjam
# Setiap kali anggota meminjam buku, sistem mencatat pasangan
# buku yang pernah dipinjam bersama dalam satu sesi (ko-pinjam).
# BFS digunakan untuk merekomendasikan buku dalam radius hop <= 2.
#
# Struktur data : Graf tak-berarah berbobot (graph.py)
# Big-O BFS     : O(V + E)
# Big-O tambah  : O(deg) per edge
# ============================================================

from data_structures.graph import GraphRekBuku


class ManajerRekomendasi:
    """
    Lapisan bisnis di atas GraphRekBuku.
    Mencatat ko-pinjam setiap kali transaksi PINJAM berhasil,
    lalu menyajikan rekomendasi via BFS saat diminta CLI.

    Riwayat pinjam per anggota disimpan di _sesi_aktif:
      { nim -> [isbn, isbn, ...] }
    Setiap kali sesi ditutup (anggota selesai pinjam),
    semua pasangan buku di sesi itu dicatat ke graf.
    """

    def __init__(self):
        self._graf = GraphRekBuku()
        # sesi_aktif: lacak buku yang sedang dipinjam per anggota
        # dipakai untuk generate edge ko-pinjam
        self._sesi_aktif: dict[str, list[str]] = {}
        # ----------------------------------------------------------
    # catat_pinjam — tambahkan isbn ke sesi aktif anggota
    # dan langsung update edge ko-pinjam dengan buku sebelumnya.
    # Big-O Waktu : O(k * deg) — k = buku aktif anggota ini
    # ----------------------------------------------------------
    def catat_pinjam(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali PINJAM berhasil (dari main/modul_3).
        Buku baru langsung dipasangkan dengan semua buku yang
        sedang dipinjam oleh anggota yang sama.
        """
        # pastikan slot sesi ada
        if nim not in self._sesi_aktif:
            self._sesi_aktif[nim] = []

        # buat edge ko-pinjam dengan semua buku aktif anggota ini
        for isbn_lain in self._sesi_aktif[nim]:
            self._graf.add_copinjam(isbn, isbn_lain)   # O(deg)

        self._sesi_aktif[nim].append(isbn)
            # ----------------------------------------------------------
    # catat_kembalikan — hapus isbn dari sesi aktif anggota
    # Big-O Waktu : O(k) — k = buku aktif anggota
    # ----------------------------------------------------------
    def catat_kembalikan(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali KEMBALIKAN berhasil.
        Buku dikembalikan berarti keluar dari sesi aktif anggota.
        """
        if nim in self._sesi_aktif and isbn in self._sesi_aktif[nim]:
            self._sesi_aktif[nim].remove(isbn)   # O(k)
                # ----------------------------------------------------------
    # catat_pinjam — tambahkan isbn ke sesi aktif anggota
    # dan langsung update edge ko-pinjam dengan buku sebelumnya.
    # Big-O Waktu : O(k * deg) — k = buku aktif anggota ini
    # ----------------------------------------------------------
    def catat_pinjam(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali PINJAM berhasil (dari main/modul_3).
        Buku baru langsung dipasangkan dengan semua buku yang
        sedang dipinjam oleh anggota yang sama.
        """
        # pastikan slot sesi ada
        if nim not in self._sesi_aktif:
            self._sesi_aktif[nim] = []

        # buat edge ko-pinjam dengan semua buku aktif anggota ini
        for isbn_lain in self._sesi_aktif[nim]:
            self._graf.add_copinjam(isbn, isbn_lain)   # O(deg)

        self._sesi_aktif[nim].append(isbn)
            # ----------------------------------------------------------
    # catat_kembalikan — hapus isbn dari sesi aktif anggota
    # Big-O Waktu : O(k) — k = buku aktif anggota
    # ----------------------------------------------------------
    def catat_kembalikan(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali KEMBALIKAN berhasil.
        Buku dikembalikan berarti keluar dari sesi aktif anggota.
        """
        if nim in self._sesi_aktif and isbn in self._sesi_aktif[nim]:
            self._sesi_aktif[nim].remove(isbn)   # O(k)
