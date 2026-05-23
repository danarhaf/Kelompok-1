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

# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — shell_sort_durasi: kondisi dasar
# ══════════════════════════════════════════════════════════════

def test_shell_sort_head_none_kembalikan_none():
    assert shell_sort_durasi(None) is None

def test_shell_sort_satu_node_tidak_error():
    head = buat_ll_durasi(14)
    hasil = shell_sort_durasi(head)
    assert ambil_durasi(hasil) == [14]

def test_shell_sort_dua_node_descending():
    head = buat_ll_durasi(7, 21)
    shell_sort_durasi(head)
    assert ambil_durasi(head) == [21, 7]

def test_shell_sort_sudah_terurut_descending():
    head = buat_ll_durasi(30, 21, 14, 7)
    shell_sort_durasi(head)
    assert ambil_durasi(head) == [30, 21, 14, 7]


# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — shell_sort_durasi: pengurutan benar
# ══════════════════════════════════════════════════════════════

def test_shell_sort_urutan_acak():
    durasi = [7, 30, 14, 21, 10]
    head = buat_ll_durasi(*durasi)
    shell_sort_durasi(head)
    assert ambil_durasi(head) == sorted(durasi, reverse=True)

def test_shell_sort_semua_nilai_sama():
    head = buat_ll_durasi(14, 14, 14)
    shell_sort_durasi(head)
    assert ambil_durasi(head) == [14, 14, 14]

def test_shell_sort_jumlah_node_tidak_berubah():
    durasi = [5, 20, 15, 10, 25, 30]
    head = buat_ll_durasi(*durasi)
    shell_sort_durasi(head)
    hasil = ambil_durasi(head)
    assert len(hasil) == len(durasi)

def test_shell_sort_nilai_tidak_hilang():
    durasi = [7, 30, 14, 21, 10]
    head = buat_ll_durasi(*durasi)
    shell_sort_durasi(head)
    assert sorted(ambil_durasi(head)) == sorted(durasi)

def test_shell_sort_descending_benar():
    durasi = [3, 1, 4, 1, 5, 9, 2, 6]
    head = buat_ll_durasi(*durasi)
    shell_sort_durasi(head)
    hasil = ambil_durasi(head)
    assert hasil == sorted(durasi, reverse=True)
