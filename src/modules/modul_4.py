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