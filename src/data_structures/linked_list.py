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