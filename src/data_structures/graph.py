# ============================================================
# graph.py
# Implementasi Graf Tak-Berarah Berbobot berbasis adjacency list
# Edge (A, B, w): buku A dan B pernah dipinjam bersama sebanyak w kali
# BFS menggunakan Queue dari queue_ll.py (bukan deque bawaan Python)
# Kompleksitas Ruang Keseluruhan: O(V + E)
# ============================================================

from data_structures.queue_ll import Queue


class GraphRekBuku:
    """
    Graf rekomendasi ko-pinjam antar buku.
    Representasi: adjacency list -> dict { isbn: [(isbn_tetangga, bobot)] }

    Operasi utama:
      add_copinjam      -> O(deg) — perlu cek apakah edge sudah ada
      rekomendasikan    -> O(V + E) — BFS terbatas hop
      tambah_vertex     -> O(1)
    """

    def __init__(self):
        # adj: kunci = isbn, nilai = list of tuple (isbn_tetangga, frekuensi)
        self._adj = {}

    # ----------------------------------------------------------
    # tambah_vertex — daftarkan isbn ke graf jika belum ada
    # Big-O Waktu : O(1)
    # Big-O Ruang : O(1)
    # ----------------------------------------------------------
    def tambah_vertex(self, isbn):
        if isbn not in self._adj:
            self._adj[isbn] = []