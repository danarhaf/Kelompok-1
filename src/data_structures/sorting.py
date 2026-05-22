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
