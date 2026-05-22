# ============================================================
# linked_list.py
# Implementasi dasar Singly Linked List dari nol
# Dipakai sebagai fondasi oleh:
#   - queue_ll.py  (Queue berbasis LL)
#   - stack.py     (Stack berbasis LL)
#   - modul_5.py   (Sorting pada LL)
#
# Kompleksitas Ruang: O(n) — satu node per elemen
# ============================================================


class Node:
    """
    Node dasar Singly Linked List.
    Menyimpan satu data dan pointer ke node berikutnya.
    Digunakan oleh Queue, Stack, dan struktur data lain
    yang membutuhkan node linked list.
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None   # pointer ke node selanjutnya

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    """
    Singly Linked List generik dari nol.
    Mendukung operasi dasar yang dibutuhkan sistem perpustakaan.

    Operasi utama:
    tambah_depan  -> O(1)
    tambah_belakang -> O(n) tanpa tail, O(1) dengan tail
    hapus_depan   -> O(1)
    cari          -> O(n)
    ke_list       -> O(n)
    """

    def __init__(self):
        self.head = None
        self._tail = None   # pointer tail agar tambah_belakang O(1)
        self._size = 0

    # ----------------------------------------------------------
    # tambah_depan — sisipkan node baru di awal list
    # Big-O Waktu : O(1)
    # Big-O Ruang : O(1)
    # ----------------------------------------------------------
    def tambah_depan(self, data):
        baru = Node(data)
        baru.next = self.head
        self.head = baru
        if self._tail is None:
            self._tail = baru   # list tadinya kosong
        self._size += 1

    # ----------------------------------------------------------
    # tambah_belakang — sisipkan node baru di akhir list
    # Big-O Waktu : O(1) — berkat pointer tail
    # Big-O Ruang : O(1)
    # ----------------------------------------------------------
    def tambah_belakang(self, data):
        baru = Node(data)
        if self.head is None:
            self.head = baru
            self._tail = baru
        else:
            self._tail.next = baru
            self._tail = baru
        self._size += 1

    # ----------------------------------------------------------
    # hapus_depan — hapus dan kembalikan data dari node pertama
    # Big-O Waktu : O(1)
    # Big-O Ruang : O(1)
    # ----------------------------------------------------------
    def hapus_depan(self):
        if self.head is None:
            return None
        data_keluar = self.head.data
        self.head = self.head.next
        if self.head is None:
            self._tail = None   # list jadi kosong, reset tail
        self._size -= 1
        return data_keluar

    # ----------------------------------------------------------
    # cari — temukan node dengan data tertentu
    # Big-O Waktu : O(n) — traversal linear
    # Big-O Ruang : O(1)
    # Kembalikan node jika ditemukan, None jika tidak ada
    # ----------------------------------------------------------
    def cari(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                return current
            current = current.next
        return None

    # ----------------------------------------------------------
    # hapus_nilai — hapus node pertama dengan data tertentu
    # Big-O Waktu : O(n) — perlu cari posisi dulu
    # Big-O Ruang : O(1)
    # Kembalikan True jika berhasil, False jika tidak ditemukan
    # ----------------------------------------------------------
    def hapus_nilai(self, data):
        if self.head is None:
            return False

        # kasus: node yang dihapus adalah head
        if self.head.data == data:
            self.head = self.head.next
            if self.head is None:
                self._tail = None
            self._size -= 1
            return True

        # kasus: node ada di tengah atau ekor
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                if current.next == self._tail:
                    self._tail = current   # update tail jika ekor yang dihapus
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False