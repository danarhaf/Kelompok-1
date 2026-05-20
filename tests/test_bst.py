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


