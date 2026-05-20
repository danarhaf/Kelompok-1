# ============================================================
# test_bst.py
# Unit test untuk BSTKatalog (bst.py)
# Jalankan dari ROOT project: pytest tests/test_bst.py -v
# ============================================================

import sys
import os
import math
import random

# path ke src/ agar bisa import data_structures dan data_model
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_structures.bst import BSTKatalog
from data_model import Buku          # <-- pakai Buku asli dari data_model
from data_model import STATUS        # <-- pakai konstanta STATUS yang sama


# ── helper ────────────────────────────────────────────────────
def buku(isbn, judul='', kategori='Teknik', status=0):
    """
    Buat objek Buku asli (dari data_model) untuk keperluan test.
    Pengarang diisi dummy agar tidak error di dataclass.
    """
    return Buku(
        isbn=isbn,
        judul=judul if judul else f'Judul-{isbn}',
        pengarang='Penulis-Test',
        kategori=kategori,
        status=status,
    )


def bst_dengan(*isbn_list):
    """Buat BST dan sisipkan Buku asli berdasarkan daftar ISBN."""
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
    # ISBN yang sama tidak boleh menambah node baru, hanya update datanya
    pohon = BSTKatalog()
    pohon.insert(buku('ISBN-0010', judul='Versi Lama'))
    pohon.insert(buku('ISBN-0010', judul='Versi Baru'))
    assert len(pohon) == 1             # tetap satu node
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
    pohon = BSTKatalog()
    assert pohon.search('ISBN-0001') is None


def test_search_root_langsung():
    pohon = bst_dengan('ISBN-0040')
    assert pohon.search('ISBN-0040').isbn == 'ISBN-0040'
    
# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — inorder (urutan ISBN)
# ══════════════════════════════════════════════════════════════

def test_inorder_menghasilkan_urutan_isbn_menaik():
    pohon = bst_dengan('ISBN-0030', 'ISBN-0010', 'ISBN-0050', 'ISBN-0020', 'ISBN-0040')
    hasil = pohon.inorder()
    isbn_urut = [b.isbn for b in hasil]
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
    pohon = BSTKatalog()
    assert pohon.inorder() == []

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
    # Kasus 1: hapus node tanpa anak (daun)
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0015')
    assert pohon.delete('ISBN-0005') is True
    assert pohon.search('ISBN-0005') is None
    assert len(pohon) == 2


def test_delete_node_satu_anak_kiri():
    # Kasus 2a: node hanya punya anak kiri
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0003')
    pohon.delete('ISBN-0005')
    assert pohon.search('ISBN-0005') is None
    assert pohon.search('ISBN-0003') is not None   # anak tetap ada
    assert len(pohon) == 2


def test_delete_node_satu_anak_kanan():
    # Kasus 2b: node hanya punya anak kanan
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0007')
    pohon.delete('ISBN-0005')
    assert pohon.search('ISBN-0005') is None
    assert pohon.search('ISBN-0007') is not None
    assert len(pohon) == 2


def test_delete_node_dua_anak():
    # Kasus 3: hapus node dengan dua anak (pakai inorder successor)
    pohon = bst_dengan('ISBN-0010', 'ISBN-0005', 'ISBN-0015', 'ISBN-0012', 'ISBN-0020')
    assert pohon.delete('ISBN-0015') is True
    assert pohon.search('ISBN-0015') is None
    isbn_urut = [b.isbn for b in pohon.inorder()]
    assert isbn_urut == sorted(isbn_urut)   # BST tetap valid setelah delete
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
    
