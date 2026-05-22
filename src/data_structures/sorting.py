# ============================================================
# sorting.py
# Implementasi Shell Sort dan Merge Sort dari nol
# khusus untuk Linked List — tanpa library Python
#
# Diimport oleh modul_5.py (ManajerLaporan)
#
# Shell Sort  : ~O(n^1.5) — sorting durasi peminjaman
# Merge Sort  : O(n log n) — sorting frekuensi per ISBN
# ============================================================

from data_structures.linked_list import Node


# ════════════════════════════════════════════════════════════
# SHELL SORT PADA LINKED LIST
# Kunci  : field 'durasi' (descending)
# Big-O  : ~O(n^1.5) dengan gap sequence Knuth
#
# Karena Linked List tidak punya random access O(1),
# kita kumpulkan pointer node ke array sementara,
# sort menggunakan swap DATA (bukan swap pointer),
# lalu urutan di LL otomatis mencerminkan hasil sort.
# Struktur pointer Linked List tidak diubah sama sekali.
# ════════════════════════════════════════════════════════════

def shell_sort_durasi(head_node):
    """
    Shell Sort pada Linked List berdasarkan field 'durasi' descending.
    Menerima head node dari Linked List (Node dari linked_list.py).
    Mengembalikan head yang sama (sort in-place via swap data).

    Langkah:
    1. Kumpulkan semua pointer node ke array sementara  -> O(n)
    2. Hitung gap awal Knuth: 1, 4, 13, 40, ...
    3. Shell Sort pada array pointer dengan swap data    -> ~O(n^1.5)

    Big-O Waktu : ~O(n^1.5) dengan gap Knuth
    Big-O Ruang : O(n) — array pointer sementara
    """
    # kumpulkan semua node ke array — O(n)
    nodes = []
    cur = head_node
    while cur is not None:
        nodes.append(cur)
        cur = cur.next

    n = len(nodes)
    if n <= 1:
        return head_node

    # hitung gap awal Knuth: 1, 4, 13, 40, 121, ...
    # gap dipilih agar Shell Sort mendekati O(n^1.5)
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1

    # Shell Sort: insertion sort dengan jarak gap
    while gap >= 1:
        for i in range(gap, n):
            temp_data = nodes[i].data
            j = i
            # geser elemen yang durasinya lebih kecil ke kanan (descending)
            while (j >= gap and
                nodes[j - gap].data.get('durasi', 0) < temp_data.get('durasi', 0)):
                nodes[j].data = nodes[j - gap].data
                j -= gap
            nodes[j].data = temp_data
        gap //= 3   # kurangi gap untuk iterasi berikutnya

    return head_node   # head tidak berubah, hanya data di dalam node yang bergeser

# ════════════════════════════════════════════════════════════
# MERGE SORT PADA LINKED LIST
# Kunci  : field 'frekuensi' (descending)
# Big-O  : O(n log n) — guaranteed semua kasus
#
# Dilakukan murni dengan pointer manipulation:
#   1. Split : slow/fast pointer temukan tengah LL
#   2. Rekursif sort dua bagian
#   3. Merge  : gabung dua LL terurut dengan sentinel node
# ════════════════════════════════════════════════════════════

def merge_sort_frekuensi(head_node):
    """
    Merge Sort pada Linked List berdasarkan field 'frekuensi' descending.
    Menerima head node. Mengembalikan head baru setelah pengurutan.

    Tidak ada konversi ke array — murni pointer Node.

    Big-O Waktu : O(n log n)
    Big-O Ruang : O(log n) — call stack rekursif
    """
    # basis: kosong atau satu node tidak perlu diurutkan
    if head_node is None or head_node.next is None:
        return head_node

    # split Linked List menjadi dua bagian di tengah — O(n)
    kiri, kanan = _split_tengah(head_node)

    # rekursif sort masing-masing bagian
    kiri  = merge_sort_frekuensi(kiri)
    kanan = merge_sort_frekuensi(kanan)

    # gabung dua bagian yang sudah terurut — O(n)
    return _merge_descending(kiri, kanan)


def _split_tengah(head_node):
    """
    Cari tengah Linked List menggunakan teknik slow/fast pointer.
    Slow bergerak 1 langkah, fast bergerak 2 langkah.
    Saat fast mencapai akhir, slow berada di tengah.
    Putus list menjadi dua bagian dan kembalikan keduanya.

    Big-O Waktu : O(n)
    Big-O Ruang : O(1)
    """
    slow = head_node
    fast = head_node.next

    # fast bergerak dua langkah, slow satu langkah
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    # slow sekarang di tengah — putus list di sini
    tengah = slow.next
    slow.next = None   # putus sambungan antara dua bagian

    return head_node, tengah


def _merge_descending(kiri, kanan):
    """
    Gabungkan dua Linked List yang sudah terurut menjadi satu
    terurut descending berdasarkan field 'frekuensi'.
    Menggunakan sentinel node dummy agar tidak perlu
    penanganan head khusus.

    Big-O Waktu : O(n)
    Big-O Ruang : O(1)
    """
    # sentinel: node dummy sebagai titik awal hasil merge
    # sehingga kita tidak perlu if-else untuk kasus head kosong
    dummy = Node({'frekuensi': 0})
    cur = dummy

    while kiri is not None and kanan is not None:
        freq_kiri  = kiri.data.get('frekuensi', 0)
        freq_kanan = kanan.data.get('frekuensi', 0)

        # ambil yang lebih besar dulu (descending)
        if freq_kiri >= freq_kanan:
            cur.next = kiri
            kiri = kiri.next
        else:
            cur.next = kanan
            kanan = kanan.next
        cur = cur.next

    # sambung sisa node yang belum habis
    cur.next = kiri if kiri is not None else kanan

    return dummy.next   # lewati sentinel, kembalikan head asli
