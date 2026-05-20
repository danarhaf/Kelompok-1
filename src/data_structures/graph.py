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
        # ----------------------------------------------------------
    # rekomendasikan — BFS dari isbn sumber hingga max_hop lompatan
    # Kembalikan list tuple (isbn, bobot_total, hop) terurut bobot turun
    # Big-O Waktu : O(V + E) — BFS mengunjungi setiap node dan edge sekali
    # Big-O Ruang : O(V) — visited set + antrian BFS
    # ----------------------------------------------------------
    def rekomendasikan(self, isbn_sumber, max_hop=2, min_bobot=1):
        """
        BFS terbatas kedalaman untuk menemukan buku yang sering
        dipinjam bersama isbn_sumber dalam jarak <= max_hop.

        Parameter min_bobot digunakan untuk menyaring rekomendasi:
        hanya edge dengan frekuensi >= min_bobot yang diikuti.
        Dampak Big-O: mengurangi E efektif -> BFS lebih cepat,
        tapi bisa kehilangan rekomendasi dengan bobot rendah.
        """
        if isbn_sumber not in self._adj:
            return []   # buku belum pernah dipinjam atau tidak di graf

        # antrian BFS berisi tuple (isbn, hop_ke, akumulasi_bobot)
        # pakai Queue Linked List sendiri, bukan deque bawaan
        antrian = Queue()
        antrian.enqueue((isbn_sumber, 0, 0))

        # visited mencegah node dikunjungi lebih dari satu kali
        dikunjungi = {isbn_sumber}

        hasil = []   # list (isbn, bobot_total, hop)

        while not antrian.is_empty():
            isbn_kini, hop_kini, bobot_kumulatif = antrian.dequeue()
            
            # jelajahi semua tetangga node saat ini
            for isbn_tetangga, bobot_edge in self._adj.get(isbn_kini, []):

                if isbn_tetangga in dikunjungi:
                    continue   # sudah dikunjungi, lewati

                # filter berdasarkan min_bobot
                if bobot_edge < min_bobot:
                    continue

                dikunjungi.add(isbn_tetangga)
                hop_baru = hop_kini + 1
                bobot_baru = bobot_kumulatif + bobot_edge

                # catat sebagai rekomendasi (bukan sumber sendiri)
                hasil.append((isbn_tetangga, bobot_baru, hop_baru))
                      # lanjut BFS ke level berikutnya jika belum maks hop
                if hop_baru < max_hop:
                    antrian.enqueue((isbn_tetangga, hop_baru, bobot_baru))

        # urutkan berdasarkan bobot total turun (yang paling sering ko-pinjam duluan)
        # menggunakan insertion sort manual agar tidak pakai sorted() bawaan
        hasil = self._insertion_sort_turun(hasil)
        return hasil

    def _insertion_sort_turun(self, data):
        """
        Insertion sort pada list of tuple berdasarkan elemen index-1 (bobot) secara menurun.
        Big-O Waktu : O(k^2) — k = jumlah kandidat rekomendasi (biasanya kecil)
        Dipilih karena k relatif kecil dibanding n buku total.
        """
        for i in range(1, len(data)):
            kunci = data[i]
            j = i - 1
            # geser elemen dengan bobot lebih kecil ke kanan
            while j >= 0 and data[j][1] < kunci[1]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = kunci
        return data