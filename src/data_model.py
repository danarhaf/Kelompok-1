import numpy as np          
import time                 
import random               
from dataclasses import dataclass, field   
from typing import Optional, List, Dict, Tuple  

np.random.seed(13)   
random.seed(13)      

KATEGORI = ['Fiksi', 'Sains', 'Teknik', 'Sejarah', 'Seni']
STATUS   = {'TERSEDIA': 0, 'DIPINJAM': 1, 'DIPESAN': 2}
