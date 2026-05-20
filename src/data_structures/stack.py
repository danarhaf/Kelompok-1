# ============================================================
# stack.py
# Implementasi Stack berbasis Linked List dari nol
# Digunakan untuk riwayat transaksi global + fitur UNDO
# Kompleksitas Ruang Keseluruhan: O(n) — satu node per transaksi
# ============================================================


class _Node:
    """
    Node internal Stack.
    Hanya butuh pointer ke node di bawahnya (prev dalam tumpukan).
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None   # menunjuk ke node yang lebih lama (di bawah)


class Stack:
    """
    LIFO Stack berbasis Linked List.
    - push : tambah di atas tumpukan -> O(1)
    - pop  : ambil dari atas         -> O(1)
    - peek : intip paling atas       -> O(1)

    Top stack = head linked list, sehingga setiap operasi
    push/pop hanya menyentuh node paling depan — tidak ada traversal.
    """

    def __init__(self):
        self._top = None   # node paling atas tumpukan
        self._size = 0

    # ----------------------------------------------------------
    # push — taruh data baru di paling atas
    # Big-O Waktu : O(1) — cukup ganti pointer top, tidak perlu cari posisi
    # Big-O Ruang : O(1) — satu node baru per panggilan
    # ----------------------------------------------------------
    def push(self, data):
        baru = _Node(data)
        baru.next = self._top   # node baru menunjuk ke node top lama
        self._top = baru        # top sekarang adalah node baru
        self._size += 1

    # ----------------------------------------------------------
    # pop — ambil dan hapus data paling atas
    # Big-O Waktu : O(1) — langsung cabut top tanpa traversal
    # Big-O Ruang : O(1) — tidak alokasi memori baru
    # Mengembalikan data yang diambil, atau None jika stack kosong
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
    # tampilkan_stack — kembalikan list semua elemen dari atas ke bawah
    # Big-O Waktu : O(n) — traversal penuh dari top ke node terbawah
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
    # pindah_ke_linked_list — strategi archiving: pindah N elemen
    # terbawah (terlama) ke struktur lain agar stack tetap ringkas
    # Big-O Waktu : O(n) — traversal seluruh stack sekali
    # Big-O Ruang : O(n) — membuat linked list baru sebesar isi stack
    # ----------------------------------------------------------
    def pindah_ke_linked_list(self, maks_simpan=50):
        """
        Jika stack melebihi maks_simpan, elemen-elemen lama
        (yang ada di bawah) dipindah dan dikembalikan sebagai list.
        Stack hanya menyisakan maks_simpan elemen teratas.
        Berguna agar Stack tidak tumbuh tak terbatas dalam produksi.
        """
        if self._size <= maks_simpan:
            return []   # belum perlu archiving

        # ambil semua elemen dulu (urutan: atas -> bawah)
        semua = self.tampilkan_stack()

        # sisakan maks_simpan elemen paling atas di stack
        tetap = semua[:maks_simpan]
        arsip = semua[maks_simpan:]   # elemen lama yang dipindah

        # bangun ulang stack hanya dari elemen yang tetap
        # (harus dibalik dulu karena push menambah dari atas)
        self._top = None
        self._size = 0
        for item in reversed(tetap):
            self.push(item)

        return arsip   # kembalikan elemen arsip ke pemanggil

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"Stack(top={self.peek()}, size={self._size})"
