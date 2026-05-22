# ============================================================
# test_bst.py
# Unit test untuk BSTKatalog (bst.py)
# Jalankan dari ROOT project: pytest tests/test_bst.py -v
# ============================================================

import sys
import os
import math
import random

# tambahkan src/ ke sys.path agar semua import dari dalam src/ bisa ditemukan
_SRC = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, _SRC)

from data_structures.bst import BSTKatalog
from data_model import Buku, STATUS


# ── helper ────────────────────────────────────────────────────
def buku(isbn, judul='', kategori='Teknik', status=0):
    """Buat objek Buku asli dari data_model untuk keperluan test."""
    return Buku(
        isbn=isbn,
        judul=judul if judul else f'Judul-{isbn}',
        pengarang='Penulis-Test',
        kategori=kategori,
        status=status,
    )


def bst_dengan(*isbn_list):
    """Buat BST dan sisipkan Buku berdasarkan daftar ISBN."""
    pohon = BSTKatalog()
    for isbn in isbn_list:
        pohon.insert(buku(isbn))
    return pohon


# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — kondisi awal
# ══════════════════════════════════════════════════════════════

def test_bst_baru_kosong():
    pohon = BSTKatalog()
    assert len(pohon) == 0
    assert pohon.search('ISBN-0001') is None
    assert pohon.inorder() == []


# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — insert
# ══════════════════════════════════════════════════════════════

def test_insert_satu_buku():
    pohon = BSTKatalog()
    pohon.insert(buku('ISBN-0001', judul='Algoritma Dasar'))
    assert len(pohon) == 1
    assert pohon.search('ISBN-0001') is not None


def test_insert_banyak_buku_size_benar():
    pohon = bst_dengan('ISBN-0005', 'ISBN-0002', 'ISBN-0008', 'ISBN-0001', 'ISBN-0003')
    assert len(pohon) == 5


def test_insert_isbn_duplikat_update_bukan_tambah():
    # ISBN sama tidak boleh menambah node baru, hanya update data
    pohon = BSTKatalog()
    pohon.insert(buku('ISBN-0010', judul='Versi Lama'))
    pohon.insert(buku('ISBN-0010', judul='Versi Baru'))
    assert len(pohon) == 1                              # tetap satu node
    assert pohon.search('ISBN-0010').judul == 'Versi Baru'   # data terupdate


# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — search
# ══════════════════════════════════════════════════════════════

def test_search_isbn_yang_ada():
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0015')
    hasil = pohon.search('ISBN-0005')
    assert hasil is not None
    assert hasil.isbn == 'ISBN-0005'


def test_search_isbn_tidak_ada_kembalikan_none():
    pohon = bst_dengan('ISBN-0010', 'ISBN-0020')
    assert pohon.search('ISBN-0099') is None


def test_search_di_bst_kosong():
    assert BSTKatalog().search('ISBN-0001') is None


def test_search_root_langsung():
    pohon = bst_dengan('ISBN-0040')
    assert pohon.search('ISBN-0040').isbn == 'ISBN-0040'


# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — inorder
# ══════════════════════════════════════════════════════════════

def test_inorder_menghasilkan_urutan_isbn_menaik():
    pohon = bst_dengan('ISBN-0030', 'ISBN-0010', 'ISBN-0050', 'ISBN-0020', 'ISBN-0040')
    isbn_urut = [b.isbn for b in pohon.inorder()]
    assert isbn_urut == sorted(isbn_urut)


def test_inorder_jumlah_elemen_sama_dengan_len():
    pohon = bst_dengan('ISBN-0001', 'ISBN-0002', 'ISBN-0003')
    assert len(pohon.inorder()) == len(pohon)


def test_inorder_bst_satu_node():
    pohon = bst_dengan('ISBN-0007')
    hasil = pohon.inorder()
    assert len(hasil) == 1
    assert hasil[0].isbn == 'ISBN-0007'


def test_inorder_bst_kosong_kembalikan_list_kosong():
    assert BSTKatalog().inorder() == []


# ══════════════════════════════════════════════════════════════
# KELOMPOK 5 — update_status (pakai konstanta STATUS dari data_model)
# ══════════════════════════════════════════════════════════════

def test_update_status_tersedia_ke_dipinjam():
    pohon = bst_dengan('ISBN-0001')
    berhasil = pohon.update_status('ISBN-0001', STATUS['DIPINJAM'])
    assert berhasil is True
    assert pohon.search('ISBN-0001').status == STATUS['DIPINJAM']


def test_update_status_dipinjam_ke_tersedia():
    pohon = BSTKatalog()
    pohon.insert(buku('ISBN-0002', status=STATUS['DIPINJAM']))
    pohon.update_status('ISBN-0002', STATUS['TERSEDIA'])
    assert pohon.search('ISBN-0002').status == STATUS['TERSEDIA']


def test_update_status_isbn_tidak_ada_kembalikan_false():
    pohon = bst_dengan('ISBN-0010')
    assert pohon.update_status('ISBN-9999', STATUS['DIPINJAM']) is False


def test_update_status_ke_dipesan():
    pohon = bst_dengan('ISBN-0015')
    pohon.update_status('ISBN-0015', STATUS['DIPESAN'])
    assert pohon.search('ISBN-0015').status == STATUS['DIPESAN']


# ══════════════════════════════════════════════════════════════
# KELOMPOK 6 — delete
# ══════════════════════════════════════════════════════════════

def test_delete_node_daun():
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0015')
    assert pohon.delete('ISBN-0005') is True
    assert pohon.search('ISBN-0005') is None
    assert len(pohon) == 2


def test_delete_node_satu_anak_kiri():
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0003')
    pohon.delete('ISBN-0005')
    assert pohon.search('ISBN-0005') is None
    assert pohon.search('ISBN-0003') is not None
    assert len(pohon) == 2


def test_delete_node_satu_anak_kanan():
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0007')
    pohon.delete('ISBN-0005')
    assert pohon.search('ISBN-0005') is None
    assert pohon.search('ISBN-0007') is not None
    assert len(pohon) == 2


def test_delete_node_dua_anak():
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0015', 'ISBN-0012', 'ISBN-0020')
    assert pohon.delete('ISBN-0015') is True
    assert pohon.search('ISBN-0015') is None
    isbn_urut = [b.isbn for b in pohon.inorder()]
    assert isbn_urut == sorted(isbn_urut)
    assert len(pohon) == 4


def test_delete_root():
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0015')
    pohon.delete('ISBN-0010')
    assert pohon.search('ISBN-0010') is None
    assert len(pohon) == 2
    isbn_urut = [b.isbn for b in pohon.inorder()]
    assert isbn_urut == sorted(isbn_urut)


def test_delete_isbn_tidak_ada_kembalikan_false():
    pohon = bst_dengan('ISBN-0010')
    assert pohon.delete('ISBN-9999') is False
    assert len(pohon) == 1


def test_delete_semua_node_satu_per_satu():
    isbn_list = ['ISBN-0010', 'ISBN-0005', 'ISBN-0015', 'ISBN-0001', 'ISBN-0007']
    pohon = bst_dengan(*isbn_list)
    for isbn in isbn_list:
        pohon.delete(isbn)
    assert len(pohon) == 0
    assert pohon.inorder() == []


# ══════════════════════════════════════════════════════════════
# KELOMPOK 7 — hitung_tinggi
# ══════════════════════════════════════════════════════════════

def test_tinggi_bst_kosong_adalah_nol():
    assert BSTKatalog().hitung_tinggi() == 0


def test_tinggi_satu_node_adalah_satu():
    assert bst_dengan('ISBN-0010').hitung_tinggi() == 1


def test_tinggi_pohon_miring_worst_case():
    """
    Insert urutan leksikografis naik -> pohon miring ke kanan.
    Tinggi = n (worst-case O(n)).
    Relevan untuk Pertanyaan Analisis no. 1.
    """
    pohon = BSTKatalog()
    n = 10
    for i in range(1, n + 1):
        pohon.insert(buku(f'ISBN-{i:04d}'))
    assert pohon.hitung_tinggi() == n


def test_tinggi_pohon_seimbang_sekitar_log_n():
    """
    Insert tidak terurut -> pohon lebih seimbang, tinggi mendekati log2(n).
    """
    urutan_acak = ['ISBN-0040', 'ISBN-0020', 'ISBN-0060',
                'ISBN-0010', 'ISBN-0030', 'ISBN-0050', 'ISBN-0070']
    pohon = bst_dengan(*urutan_acak)
    batas = math.ceil(math.log2(len(urutan_acak) + 1))
    assert pohon.hitung_tinggi() <= batas + 1


# ══════════════════════════════════════════════════════════════
# KELOMPOK 8 — integrasi generate_koleksi (80 buku sistem penuh)
# ══════════════════════════════════════════════════════════════

def test_insert_80_buku_dari_generate_koleksi():
    """
    Pakai generate_koleksi() asli (seed=13) agar mencerminkan
    kondisi sistem nyata saat dijalankan.
    """
    # generate_data.py ada di src/ yang sudah masuk sys.path di atas
    from generate_data import generate_koleksi

    pohon = BSTKatalog()
    koleksi = generate_koleksi(80)

    for b in koleksi:
        pohon.insert(b)

    assert len(pohon) == 80

    for b in koleksi:
        assert pohon.search(b.isbn) is not None

    isbn_urut = [b.isbn for b in pohon.inorder()]
    assert isbn_urut == sorted(isbn_urut)


def test_update_status_setelah_generate_koleksi():
    """
    Setelah insert dari generate_koleksi, update_status harus
    bisa mengubah status buku menggunakan konstanta STATUS asli.
    """
    from generate_data import generate_koleksi

    pohon = BSTKatalog()
    for b in generate_koleksi(80):
        pohon.insert(b)

    ok = pohon.update_status('ISBN-0001', STATUS['DIPINJAM'])
    assert ok is True
    assert pohon.search('ISBN-0001').status == STATUS['DIPINJAM']

    pohon.update_status('ISBN-0001', STATUS['TERSEDIA'])
    assert pohon.search('ISBN-0001').status == STATUS['TERSEDIA']