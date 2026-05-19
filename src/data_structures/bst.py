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
        else:
            self._insert_rekursif(self._root, buku)
        self._jumlah += 1

    def _insert_rekursif(self, node, buku):
        # ISBN lebih kecil -> masuk ke cabang kiri
        if buku.isbn < node.buku.isbn:
            if node.kiri is None:
                node.kiri = BSTNode(buku)
            else:
                self._insert_rekursif(node.kiri, buku)
        # ISBN lebih besar -> masuk ke cabang kanan
        elif buku.isbn > node.buku.isbn:
            if node.kanan is None:
                node.kanan = BSTNode(buku)
            else:
                self._insert_rekursif(node.kanan, buku)
        # ISBN sama -> update data buku yang sudah ada (tidak duplikat)
        else:
            node.buku = buku