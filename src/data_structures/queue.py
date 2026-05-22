# ============================================================
# queue_ll.py
# Implementasi Queue berbasis Linked List dari nol
# Digunakan untuk antrian pemesanan buku per-ISBN
#
# Node diimport dari linked_list.py (tidak didefinisikan ulang)
#
# Kompleksitas Ruang Keseluruhan: O(n) — n node = n elemen
# ============================================================

from data_structures.linked_list import Node   # import Node dari linked_list.py


class Queue:
    """
    FIFO Queue berbasis Linked List.
    - enqueue: tambah di tail  -> O(1)
    - dequeue: ambil dari head -> O(1)
    Pointer tail dipertahankan agar enqueue tetap O(1)
    tanpa perlu traversal ke akhir list.
    """

    def __init__(self):
        # head: ujung depan antrian (yang duluan keluar)
        # tail: ujung belakang antrian (tempat masuk baru)
        self._head = None
        self._tail = None
        self._size = 0

    # ----------------------------------------------------------
    # enqueue — tambah elemen baru di belakang antrian
    # Big-O Waktu : O(1) — langsung tempel ke tail
    # Big-O Ruang : O(1) — satu node baru per panggilan
    # ----------------------------------------------------------
    def enqueue(self, data):
        baru = Node(data)   # pakai Node dari linked_list.py
        if self._tail is None:
            # antrian kosong: head dan tail menunjuk node yang sama
            self._head = baru
            self._tail = baru
        else:
            # sambung node baru setelah tail, lalu geser tail
            self._tail.next = baru
            self._tail = baru
        self._size += 1

    # ----------------------------------------------------------
    # dequeue — ambil dan hapus elemen paling depan
    # Big-O Waktu : O(1) — langsung cabut head
    # Big-O Ruang : O(1) — tidak alokasi memori baru
    # Mengembalikan data elemen yang diambil, atau None jika kosong
    # ----------------------------------------------------------
    def dequeue(self):
        if self._head is None:
            return None

        data_keluar = self._head.data
        self._head = self._head.next   # geser head ke node berikutnya

        # jika setelah dequeue antrian jadi kosong, reset tail juga
        if self._head is None:
            self._tail = None

        self._size -= 1
        return data_keluar

    # ----------------------------------------------------------
    # peek — lihat elemen terdepan tanpa menghapusnya
    # Big-O Waktu : O(1)
    # Big-O Ruang : O(1)
    # ----------------------------------------------------------
    def peek(self):
        if self._head is None:
            return None
        return self._head.data

    # ----------------------------------------------------------
    # is_empty — cek apakah antrian kosong
    # Big-O Waktu : O(1)
    # ----------------------------------------------------------
    def is_empty(self):
        return self._size == 0

    # ----------------------------------------------------------
    # tampilkan_antrian — kembalikan list semua elemen
    # Big-O Waktu : O(n) — traversal satu kali head ke tail
    # Big-O Ruang : O(n) — salinan semua data ke dalam list
    # ----------------------------------------------------------
    def tampilkan_antrian(self):
        hasil = []
        current = self._head
        while current is not None:
            hasil.append(current.data)
            current = current.next
        return hasil

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"Queue({self.tampilkan_antrian()})"
