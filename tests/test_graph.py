# ============================================================
# test_graph.py
# Unit test untuk GraphRekBuku (graph.py)
# Jalankan: pytest tests/test_graph.py -v
# ============================================================

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_structures.graph import GraphRekBuku


# ── helper ────────────────────────────────────────────────────
def buat_graf_sederhana():