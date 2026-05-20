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
        """
    Graf kecil untuk sebagian besar tes:
      ISBN-0001 <-> ISBN-0002 (bobot 2)
      ISBN-0001 <-> ISBN-0003 (bobot 1)
      ISBN-0002 <-> ISBN-0004 (bobot 3)
    """
    g = GraphRekBuku()
    g.add_copinjam('ISBN-0001', 'ISBN-0002')
    g.add_copinjam('ISBN-0001', 'ISBN-0002')   # frekuensi naik jadi 2
    g.add_copinjam('ISBN-0001', 'ISBN-0003')
    g.add_copinjam('ISBN-0002', 'ISBN-0004')
    g.add_copinjam('ISBN-0002', 'ISBN-0004')
    g.add_copinjam('ISBN-0002', 'ISBN-0004')   # bobot ISBN-0002 <-> ISBN-0004 = 3
    return g


# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — kondisi awal
# ══════════════════════════════════════════════════════════════

def test_graf_baru_tidak_punya_vertex():
    g = GraphRekBuku()
    info = g.info_graf()
    assert info['vertex'] == 0
    assert info['edge'] == 0


def test_rekomendasi_isbn_tidak_ada_kembalikan_kosong():
    g = GraphRekBuku()
    assert g.rekomendasikan('ISBN-9999') == []


# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — tambah_vertex & add_copinjam
# ══════════════════════════════════════════════════════════════

def test_tambah_vertex_manual():
    g = GraphRekBuku()
    g.tambah_vertex('ISBN-0001')
    info = g.info_graf()
    assert info['vertex'] == 1
    assert info['edge'] == 0


def test_tambah_vertex_duplikat_tidak_dobel():
    g = GraphRekBuku()
    g.tambah_vertex('ISBN-0001')
    g.tambah_vertex('ISBN-0001')   # panggil dua kali
    assert g.info_graf()['vertex'] == 1