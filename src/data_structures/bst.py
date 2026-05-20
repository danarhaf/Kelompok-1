# ============================================================
# bst.py
# Implementasi Binary Search Tree (BST) untuk katalog buku
# Kunci = ISBN string (perbandingan leksikografis)
# Kompleksitas Ruang Keseluruhan: O(n) — satu node per buku
# ============================================================


class BSTNode:
    """
    Node BST yang menyimpan objek Buku.
    Kunci pencarian = buku.isbn (string).
    Anak kiri: ISBN lebih kecil secara leksikografis
    Anak kanan: ISBN lebih besar
    """
    def __init__(self, buku):
        self.buku = buku
        self.kiri = None
        self.kanan = None


class BSTKatalog:
    """
    Binary Search Tree untuk katalog buku perpustakaan.
    Kasus rata-rata (data acak):
    insert / search / delete / update_status -> O(log n)
    Kasus terburuk (data sudah terurut, pohon menjadi miring):
    semua operasi -> O(n)  [lihat Pertanyaan Analisis no. 1]
    """

    def __init__(self):
        self._root = None
        self._jumlah = 0    # counter manual, tidak pakai len() bawaan

    # ----------------------------------------------------------
    # insert — sisipkan buku baru ke BST
    # Big-O Waktu : O(log n) rata-rata | O(n) worst-case (pohon miring)
    # Big-O Ruang : O(log n) call stack rekursif rata-rata
    # ----------------------------------------------------------
    def insert(self, buku):
        if self._root is None:
            self._root = BSTNode(buku)
            self._jumlah += 1   # node benar-benar baru
        else:
            # _insert_rekursif mengembalikan True jika node baru dibuat,
            # False jika hanya update duplikat — counter hanya naik jika baru
            ditambah = self._insert_rekursif(self._root, buku)
            if ditambah:
                self._jumlah += 1

    def _insert_rekursif(self, node, buku):
        """
        Kembalikan True jika node baru dibuat (bukan duplikat).
        Kembalikan False jika ISBN sudah ada dan hanya di-update.
        """
        # ISBN lebih kecil -> masuk ke cabang kiri
        if buku.isbn < node.buku.isbn:
            if node.kiri is None:
                node.kiri = BSTNode(buku)
                return True    # node baru dibuat
            else:
                return self._insert_rekursif(node.kiri, buku)
        # ISBN lebih besar -> masuk ke cabang kanan
        elif buku.isbn > node.buku.isbn:
            if node.kanan is None:
                node.kanan = BSTNode(buku)
                return True    # node baru dibuat
            else:
                return self._insert_rekursif(node.kanan, buku)
        # ISBN sama -> update data saja, tidak tambah node baru
        else:
            node.buku = buku
            return False       # bukan node baru, hanya update

    # ----------------------------------------------------------
    # search — cari buku berdasarkan ISBN
    # Big-O Waktu : O(log n) rata-rata | O(n) worst-case
    # Big-O Ruang : O(log n) call stack rekursif
    # Mengembalikan objek Buku jika ditemukan, atau None
    # ----------------------------------------------------------
    def search(self, isbn):
        return self._search_rekursif(self._root, isbn)

    def _search_rekursif(self, node, isbn):
        # basis: node kosong berarti tidak ditemukan
        if node is None:
            return None
        # basis: ISBN cocok
        if isbn == node.buku.isbn:
            return node.buku
        # rekursif ke kiri jika ISBN yang dicari lebih kecil
        if isbn < node.buku.isbn:
            return self._search_rekursif(node.kiri, isbn)
        # rekursif ke kanan jika ISBN lebih besar
        return self._search_rekursif(node.kanan, isbn)

    # ----------------------------------------------------------
    # update_status — ubah status buku (TERSEDIA/DIPINJAM/DIPESAN)
    # Big-O Waktu : O(log n) rata-rata — cari dulu baru update
    # Big-O Ruang : O(log n) call stack
    # Mengembalikan True jika berhasil, False jika ISBN tidak ada
    # ----------------------------------------------------------
    def update_status(self, isbn, status_baru):
        buku = self.search(isbn)
        if buku is None:
            return False
        buku.status = status_baru
        return True

    # ----------------------------------------------------------
    # inorder — traversal inorder menghasilkan buku terurut ISBN
    # Big-O Waktu : O(n) — setiap node dikunjungi tepat satu kali
    # Big-O Ruang : O(n) — list hasil + O(log n) call stack
    # ----------------------------------------------------------
    def inorder(self):
        hasil = []
        self._inorder_rekursif(self._root, hasil)
        return hasil   # list Buku terurut menaik berdasarkan ISBN

    def _inorder_rekursif(self, node, hasil):
        if node is None:
            return
        self._inorder_rekursif(node.kiri, hasil)    # kunjungi kiri dulu
        hasil.append(node.buku)                      # catat node saat ini
        self._inorder_rekursif(node.kanan, hasil)   # kunjungi kanan

    # ----------------------------------------------------------
    # delete — hapus buku dari BST (misal buku rusak/hilang)
    # Big-O Waktu : O(log n) rata-rata | O(n) worst-case
    # Big-O Ruang : O(log n) call stack
    # Mengembalikan True jika berhasil, False jika tidak ditemukan
    # ----------------------------------------------------------
    def delete(self, isbn):
        root_baru, berhasil = self._delete_rekursif(self._root, isbn)
        if berhasil:
            self._root = root_baru
            self._jumlah -= 1
        return berhasil

    def _delete_rekursif(self, node, isbn):
        """
        Kembalikan (node_baru, berhasil).
        Tiga kasus penghapusan:
        1. Node adalah daun (tidak punya anak)    -> langsung hapus
        2. Node punya satu anak                   -> ganti dengan anak
        3. Node punya dua anak                    -> ganti dengan successor
            (node terkecil di subtree kanan = inorder successor)
        """
        if node is None:
            return None, False   # ISBN tidak ditemukan

        berhasil = False

        if isbn < node.buku.isbn:
            node.kiri, berhasil = self._delete_rekursif(node.kiri, isbn)
        elif isbn > node.buku.isbn:
            node.kanan, berhasil = self._delete_rekursif(node.kanan, isbn)
        else:
            # node yang akan dihapus ditemukan
            berhasil = True

            # Kasus 1 & 2: tidak punya anak atau hanya satu anak
            if node.kiri is None:
                return node.kanan, berhasil
            if node.kanan is None:
                return node.kiri, berhasil

            # Kasus 3: punya dua anak
            # cari inorder successor (node paling kiri di subtree kanan)
            successor = self._cari_minimum(node.kanan)
            # salin data successor ke node ini
            node.buku = successor.buku
            # hapus successor dari subtree kanan
            node.kanan, _ = self._delete_rekursif(node.kanan, successor.buku.isbn)

        return node, berhasil

    def _cari_minimum(self, node):
        """
        Cari node dengan ISBN terkecil di subtree yang di-root oleh node.
        Big-O Waktu : O(h) — h = tinggi subtree
        """
        while node.kiri is not None:
            node = node.kiri
        return node

    # ----------------------------------------------------------
    # hitung_tinggi — ukur tinggi pohon (untuk analisis Big-O)
    # Big-O Waktu : O(n) — traversal seluruh pohon
    # ----------------------------------------------------------
    def hitung_tinggi(self):
        return self._tinggi_rekursif(self._root)

    def _tinggi_rekursif(self, node):
        if node is None:
            return 0
        tinggi_kiri = self._tinggi_rekursif(node.kiri)
        tinggi_kanan = self._tinggi_rekursif(node.kanan)
        return 1 + max(tinggi_kiri, tinggi_kanan)

    def __len__(self):
        return self._jumlah

    def __repr__(self):
        return f"BSTKatalog(jumlah_buku={self._jumlah}, tinggi={self.hitung_tinggi()})"