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
    
