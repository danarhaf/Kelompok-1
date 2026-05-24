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

from data_structures.linked_list import LLNode
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
    head = LLNode({'tx_id': 1, 'aksi': 'PINJAM',
                'isbn': 'ISBN-0001', 'nim': 'NIM-001',
                'durasi': durasi_list[0]})
    cur = head
    for i, d in enumerate(durasi_list[1:], 2):
        baru = LLNode({'tx_id': i, 'aksi': 'PINJAM',
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
    head = LLNode({'isbn': 'ISBN-0001', 'frekuensi': freq_list[0]})
    cur = head
    for i, f in enumerate(freq_list[1:], 2):
        baru = LLNode({'isbn': f'ISBN-{i:04d}', 'frekuensi': f})
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


# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — merge_sort_frekuensi: kondisi dasar
# ══════════════════════════════════════════════════════════════

def test_merge_sort_none_kembalikan_none():
    assert merge_sort_frekuensi(None) is None

def test_merge_sort_satu_node():
    head = buat_ll_frekuensi(5)
    hasil = merge_sort_frekuensi(head)
    assert ambil_frekuensi(hasil) == [5]

def test_merge_sort_dua_node_descending():
    head = buat_ll_frekuensi(3, 7)
    hasil = merge_sort_frekuensi(head)
    assert ambil_frekuensi(hasil) == [7, 3]

def test_merge_sort_sudah_terurut():
    head = buat_ll_frekuensi(10, 7, 5, 3, 1)
    hasil = merge_sort_frekuensi(head)
    assert ambil_frekuensi(hasil) == [10, 7, 5, 3, 1]


# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — merge_sort_frekuensi: pengurutan benar
# ══════════════════════════════════════════════════════════════

def test_merge_sort_urutan_acak():
    freq = [3, 8, 1, 6, 2]
    head = buat_ll_frekuensi(*freq)
    hasil = merge_sort_frekuensi(head)
    assert ambil_frekuensi(hasil) == sorted(freq, reverse=True)

def test_merge_sort_semua_nilai_sama():
    head = buat_ll_frekuensi(5, 5, 5, 5)
    hasil = merge_sort_frekuensi(head)
    assert ambil_frekuensi(hasil) == [5, 5, 5, 5]

def test_merge_sort_jumlah_node_tidak_berubah():
    freq = [1, 2, 3, 4, 5, 6, 7]
    head = buat_ll_frekuensi(*freq)
    hasil = merge_sort_frekuensi(head)
    assert len(ambil_frekuensi(hasil)) == len(freq)

def test_merge_sort_nilai_tidak_hilang():
    freq = [4, 2, 7, 1, 9, 3]
    head = buat_ll_frekuensi(*freq)
    hasil = merge_sort_frekuensi(head)
    assert sorted(ambil_frekuensi(hasil)) == sorted(freq)

def test_merge_sort_descending_benar():
    freq = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    head = buat_ll_frekuensi(*freq)
    hasil = merge_sort_frekuensi(head)
    assert ambil_frekuensi(hasil) == sorted(freq, reverse=True)

# ══════════════════════════════════════════════════════════════
# KELOMPOK 5 — helper internal: _split_tengah
# ══════════════════════════════════════════════════════════════

def test_split_tengah_dua_node():
    head = buat_ll_frekuensi(1, 2)
    kiri, kanan = _split_tengah(head)
    assert kiri is not None
    assert kanan is not None
    assert kiri.next is None   # kiri hanya satu node

def test_split_tengah_tiga_node():
    head = buat_ll_frekuensi(1, 2, 3)
    kiri, kanan = _split_tengah(head)
    # kiri: 2 node, kanan: 1 node
    kiri_list = ambil_frekuensi(kiri)
    kanan_list = ambil_frekuensi(kanan)
    assert len(kiri_list) + len(kanan_list) == 3

def test_split_tengah_tidak_ada_overlap():
    head = buat_ll_frekuensi(1, 2, 3, 4)
    kiri, kanan = _split_tengah(head)
    kiri_list = ambil_frekuensi(kiri)
    kanan_list = ambil_frekuensi(kanan)
    # tidak ada node yang muncul di dua sisi
    assert set(kiri_list).isdisjoint(set(kanan_list)) or \
        len(kiri_list) + len(kanan_list) == 4


# ══════════════════════════════════════════════════════════════
# KELOMPOK 6 — helper internal: _merge_descending
# ══════════════════════════════════════════════════════════════

def test_merge_descending_dua_list_terurut():
    kiri  = buat_ll_frekuensi(8, 4)
    kanan = buat_ll_frekuensi(6, 2)
    hasil = _merge_descending(kiri, kanan)
    assert ambil_frekuensi(hasil) == [8, 6, 4, 2]

def test_merge_descending_salah_satu_kosong():
    kiri  = buat_ll_frekuensi(5, 3)
    hasil = _merge_descending(kiri, None)
    assert ambil_frekuensi(hasil) == [5, 3]

def test_merge_descending_keduanya_satu_node():
    kiri  = buat_ll_frekuensi(7)
    kanan = buat_ll_frekuensi(3)
    hasil = _merge_descending(kiri, kanan)
    assert ambil_frekuensi(hasil) == [7, 3]

# ══════════════════════════════════════════════════════════════
# KELOMPOK 7 — skenario realistis perpustakaan
# ══════════════════════════════════════════════════════════════

def test_shell_sort_data_peminjaman_nyata():
    """
    Simulasi 10 transaksi PINJAM dengan durasi acak (seed=13).
    Hasil Shell Sort harus descending — anggota pinjam terlama
    tampil paling atas di laporan bulanan.
    """
    random.seed(13)
    durasi_list = [random.randint(7, 30) for _ in range(10)]
    head = buat_ll_durasi(*durasi_list)
    shell_sort_durasi(head)
    hasil = ambil_durasi(head)
    assert hasil == sorted(durasi_list, reverse=True)


def test_merge_sort_frekuensi_80_isbn():
    """
    Simulasi frekuensi peminjaman 80 ISBN dengan seed=13.
    Merge Sort harus menghasilkan urutan descending yang benar.
    Sesuai parameter sistem: 80 buku.
    """
    random.seed(13)
    freq_list = [random.randint(1, 20) for _ in range(80)]
    head = buat_ll_frekuensi(*freq_list)
    hasil = merge_sort_frekuensi(head)
    hasil_list = ambil_frekuensi(hasil)

    assert len(hasil_list) == 80
    assert hasil_list == sorted(freq_list, reverse=True)


# ══════════════════════════════════════════════════════════════
# KELOMPOK 8 — skala besar N=300
# ══════════════════════════════════════════════════════════════

def test_shell_sort_skala_besar():
    """
    Shell Sort 300 elemen. Big-O ~O(n^1.5).
    Memastikan tidak ada error pada skala beban tinggi.
    """
    random.seed(13)
    durasi_list = [random.randint(1, 60) for _ in range(300)]
    head = buat_ll_durasi(*durasi_list)
    shell_sort_durasi(head)
    hasil = ambil_durasi(head)
    assert hasil == sorted(durasi_list, reverse=True)


def test_merge_sort_skala_besar():
    """
    Merge Sort 300 elemen. Big-O O(n log n).
    Memastikan rekursif tidak stack overflow dan hasilnya benar.
    """
    random.seed(13)
    freq_list = [random.randint(1, 50) for _ in range(300)]
    head = buat_ll_frekuensi(*freq_list)
    hasil = merge_sort_frekuensi(head)
    hasil_list = ambil_frekuensi(hasil)
    assert hasil_list == sorted(freq_list, reverse=True)
