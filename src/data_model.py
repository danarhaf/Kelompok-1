import numpy as np          
import time                 
import random               
from dataclasses import dataclass, field   
from typing import Optional, List, Dict, Tuple  

np.random.seed(13)   
random.seed(13)      

KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']
STATUS   = {'TERSEDIA': 0, 'DIPINJAM': 1, 'DIPESAN': 2}

@dataclass
class Buku:
    isbn      : str   
    judul     : str
    pengarang : str
    kategori  : str
    status    : int = 0   

@dataclass
class Peminjaman:
    transaksi_id : int
    anggota_id   : str          
    isbn         : str
    tgl_pinjam   : float = field(default_factory=time.time)  
    durasi_hari  : int   = 14   