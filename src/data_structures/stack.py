# ============================================================
# stack.py
# Implementasi Stack berbasis Linked List dari nol
# Digunakan untuk riwayat transaksi global + fitur UNDO
#
# Node diimport dari linked_list.py (tidak didefinisikan ulang)
#
# Kompleksitas Ruang Keseluruhan: O(n) — satu node per transaksi
# ============================================================

from data_structures.linked_list import LLNode  # import Node dari linked_list.py


class Stack:
    """
    LIFO Stack berbasis Linked List.
    - push : tambah di atas tumpukan -> O(1)
    - pop  : ambil dari atas         -> O(1)
    - peek : intip paling atas       -> O(1)

    Top stack = head linked list, sehingga setiap operasi
    push/pop hanya menyentuh node paling depan tanpa traversal.
    """

    def __init__(self):
        self._top = None   # node paling atas tumpukan
        self._size = 0

    # ----------------------------------------------------------
    # push — taruh data baru di paling atas
    # Big-O Waktu : O(1) — cukup ganti pointer top
    # Big-O Ruang : O(1) — satu node baru per panggilan
    # ----------------------------------------------------------
    def push(self, data):
        baru = LLNode(data)       # pakai Node dari linked_list.py
        baru.next = self._top   # node baru menunjuk ke top lama
        self._top = baru        # top sekarang adalah node baru
        self._size += 1

    # ----------------------------------------------------------
    # pop — ambil dan hapus data paling atas
    # Big-O Waktu : O(1) — langsung cabut top tanpa traversal
    # Big-O Ruang : O(1) — tidak alokasi memori baru
    # Mengembalikan data, atau None jika stack kosong
    # ----------------------------------------------------------
    def pop(self):
        if self._top is None:
            return None

        data_keluar = self._top.data
        self._top = self._top.next   # turunkan top ke node di bawahnya
        self._size -= 1
        return data_keluar

    # ----------------------------------------------------------
    # peek — lihat data paling atas tanpa menghapus
    # Big-O Waktu : O(1)
    # Big-O Ruang : O(1)
    # ----------------------------------------------------------
    def peek(self):
        if self._top is None:
            return None
        return self._top.data

    # ----------------------------------------------------------
    # is_empty — cek apakah stack kosong
    # Big-O Waktu : O(1)
    # ----------------------------------------------------------
    def is_empty(self):
        return self._size == 0

    # ----------------------------------------------------------
    # tampilkan_stack — kembalikan list semua elemen (atas ke bawah)
    # Big-O Waktu : O(n) — traversal penuh dari top ke terbawah
    # Big-O Ruang : O(n) — salinan semua data ke dalam list
    # ----------------------------------------------------------
    def tampilkan_stack(self):
        hasil = []
        current = self._top
        while current is not None:
            hasil.append(current.data)
            current = current.next
        return hasil

    # ----------------------------------------------------------
    # pindah_ke_linked_list — strategi archiving
    # Pindah elemen lama ke list arsip agar stack tetap ringkas
    # Big-O Waktu : O(n) — traversal seluruh stack
    # Big-O Ruang : O(n) — list arsip
    # Relevan untuk Pertanyaan Analisis no. 4
    # ----------------------------------------------------------
    def pindah_ke_linked_list(self, maks_simpan=50):
        """
        Jika stack melebihi maks_simpan, elemen lama (terbawah)
        dipindah ke list arsip. Stack hanya menyisakan maks_simpan
        elemen teratas. Berguna agar Stack tidak tumbuh tak terbatas.
        """
        if self._size <= maks_simpan:
            return []   # belum perlu archiving

        # ambil semua elemen (urutan: atas -> bawah)
        semua = self.tampilkan_stack()

        # sisakan maks_simpan elemen paling atas
        tetap = semua[:maks_simpan]
        arsip = semua[maks_simpan:]   # elemen lama yang dipindah

        # bangun ulang stack hanya dari elemen yang tetap
        self._top = None
        self._size = 0
        for item in reversed(tetap):   # reversed agar urutan tetap benar
            self.push(item)

        return arsip   # kembalikan elemen arsip ke pemanggil

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"Stack(top={self.peek()}, size={self._size})"