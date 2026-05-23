# ============================================================
# test_sorting.py
# Unit test untuk Shell Sort & Merge Sort (sorting.py)
# Jalankan dari ROOT project: pytest tests/test_sorting.py -v
# ============================================================

import sys
import os
import random

_SRC = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, _SRC)

from data_structures.linked_list import Node
from data_structures.sorting     import (
    shell_sort_durasi,
    merge_sort_frekuensi,
    _split_tengah,
    _merge_descending,
)


# ── helper ────────────────────────────────────────────────────
def buat_ll_durasi(*durasi_list):
    """
    Buat Linked List berisi dict {'durasi': x} dari list durasi.
    Kembalikan head node.
    """
    if not durasi_list:
        return None
    head = Node({'tx_id': 1, 'aksi': 'PINJAM',
                'isbn': 'ISBN-0001', 'nim': 'NIM-001',
                'durasi': durasi_list[0]})
    cur = head
    for i, d in enumerate(durasi_list[1:], 2):
        baru = Node({'tx_id': i, 'aksi': 'PINJAM',
                    'isbn': f'ISBN-{i:04d}', 'nim': f'NIM-{i:03d}',
                    'durasi': d})
        cur.next = baru
        cur = baru
    return head


def buat_ll_frekuensi(*freq_list):
    """
    Buat Linked List berisi dict {'isbn': ..., 'frekuensi': x}.
    Kembalikan head node.
    """
    if not freq_list:
        return None
    head = Node({'isbn': 'ISBN-0001', 'frekuensi': freq_list[0]})
    cur = head
    for i, f in enumerate(freq_list[1:], 2):
        baru = Node({'isbn': f'ISBN-{i:04d}', 'frekuensi': f})
        cur.next = baru
        cur = baru
    return head


def ambil_durasi(head):
    """Ambil list nilai 'durasi' dari Linked List."""
    hasil, cur = [], head
    while cur:
        hasil.append(cur.data.get('durasi'))
        cur = cur.next
    return hasil


def ambil_frekuensi(head):
    """Ambil list nilai 'frekuensi' dari Linked List."""
    hasil, cur = [], head
    while cur:
        hasil.append(cur.data.get('frekuensi'))
        cur = cur.next
    return hasil
