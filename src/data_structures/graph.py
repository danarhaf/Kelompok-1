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
    # ----------------------------------------------------------
    # add_copinjam — tambah atau naikkan bobot edge (isbn_a, isbn_b)
    # Dipanggil setiap kali dua buku dipinjam dalam satu sesi anggota
    # Big-O Waktu : O(deg) — perlu scan tetangga untuk cek duplikat
    # Big-O Ruang : O(1) per panggilan
    # ----------------------------------------------------------
    def add_copinjam(self, isbn_a, isbn_b):
        if isbn_a == isbn_b:
            return   # tidak perlu self-loop

        self.tambah_vertex(isbn_a)
        self.tambah_vertex(isbn_b)  
        # cek apakah edge sudah ada, jika ya naikkan bobotnya
        # graf tidak berarah: update kedua sisi
        self._adj[isbn_a] = self._update_bobot(self._adj[isbn_a], isbn_b)
        self._adj[isbn_b] = self._update_bobot(self._adj[isbn_b], isbn_a)
            def _update_bobot(self, daftar_tetangga, isbn_target):
        """
        Cari isbn_target di daftar_tetangga dan naikkan bobotnya +1.
        Jika belum ada, tambahkan entry baru dengan bobot 1.
        Big-O: O(deg) — linear terhadap jumlah tetangga node ini
        """
        for i, (tetangga, bobot) in enumerate(daftar_tetangga):
            if tetangga == isbn_target:
                # sudah ada — naikkan frekuensi
                daftar_tetangga[i] = (tetangga, bobot + 1)
                return daftar_tetangga
        # belum ada — tambahkan edge baru
        daftar_tetangga.append((isbn_target, 1))
        return daftar_tetangga