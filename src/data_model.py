import numpy as np          # untuk operasi numerik / array
import time                 # untuk timestamp peminjaman & benchmark
import random               # untuk generate data acak

from dataclasses import dataclass, field   # membuat class data sederhana
from typing import Optional, List, Dict, Tuple  # type hints

# ── random seed sesuai starter code ────────────────────────────
np.random.seed(13)   # seed untuk numpy random
random.seed(13)      # seed untuk random bawaan Python

# ── Konstanta global sesuai starter code ───────────────────────
KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']
STATUS   = {'TERSEDIA': 0, 'DIPINJAM': 1, 'DIPESAN': 2}

# ================================================================
#                        DATACLASS
#  Pakai @dataclass agar tidak perlu nulis __init__ manual
# ================================================================


# ─────────────────── DATA CLASS BUKU ────────────────────────────
@dataclass
class Buku:
    """
    Representasi satu buku dalam koleksi perpustakaan.
    'isbn' adalah kunci utama yang dipakai di BST.
    """
    isbn      : str   # kunci BST, format 'ISBN-XXXX'
    judul     : str
    pengarang : str
    kategori  : str
    status    : int = 0   # default TERSEDIA (0=TERSEDIA, 1=DIPINJAM, 2=DIPESAN)

# ─────────────────── DATA CLASS PEMINJAMAN ────────────────────────
@dataclass
class Peminjaman:
    """
    Merekam satu transaksi peminjaman.
    Disimpan di Stack riwayat untuk mendukung fitur undo.
    """
    transaksi_id : int
    anggota_id   : str          # NIM anggota
    isbn         : str
    tgl_pinjam   : float        # timestamp otomatis
    durasi_hari  : int   = 14   # default 14 hari sesuai starter code