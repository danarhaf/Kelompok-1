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
    def test_add_copinjam_menambah_dua_vertex():
    g = GraphRekBuku()
    g.add_copinjam('ISBN-0001', 'ISBN-0002')
    assert g.info_graf()['vertex'] == 2
    assert g.info_graf()['edge'] == 1


def test_add_copinjam_graf_tidak_berarah():
    # edge (A,B) harus muncul di tetangga A dan di tetangga B
    g = GraphRekBuku()
    g.add_copinjam('ISBN-0001', 'ISBN-0002')
    tetangga_1 = [isbn for isbn, _ in g.tetangga('ISBN-0001')]
    tetangga_2 = [isbn for isbn, _ in g.tetangga('ISBN-0002')]
    assert 'ISBN-0002' in tetangga_1
    assert 'ISBN-0001' in tetangga_2


def test_bobot_naik_saat_dipinjam_bersama_lagi():
    # setiap kali add_copinjam dipanggil untuk pasangan yang sama,
    # bobot edge harus naik 1, bukan menambah edge baru
    g = GraphRekBuku()
    g.add_copinjam('ISBN-0001', 'ISBN-0002')
    g.add_copinjam('ISBN-0001', 'ISBN-0002')
    g.add_copinjam('ISBN-0001', 'ISBN-0002')

    # harus tetap 1 edge, bukan 3
    assert g.info_graf()['edge'] == 1

    # bobot harus 3
    bobot = next(b for isbn, b in g.tetangga('ISBN-0001') if isbn == 'ISBN-0002')
    assert bobot == 3


def test_self_loop_diabaikan():
    # add_copinjam dengan isbn yang sama tidak boleh membuat edge
    g = GraphRekBuku()
    g.add_copinjam('ISBN-0001', 'ISBN-0001')
    assert g.info_graf()['edge'] == 0

# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — rekomendasikan (BFS)
# ══════════════════════════════════════════════════════════════

def test_rekomendasi_hop1_langsung():
    """
    ISBN-0001 terhubung langsung ke ISBN-0002 dan ISBN-0003.
    Dengan max_hop=1 hanya tetangga langsung yang muncul.
    """
     g = buat_graf_sederhana()
    hasil = g.rekomendasikan('ISBN-0001', max_hop=1)
    isbn_hasil = [r[0] for r in hasil]
    assert 'ISBN-0002' in isbn_hasil
    assert 'ISBN-0003' in isbn_hasil
    # ISBN-0004 hanya bisa dicapai lewat ISBN-0002 (hop 2), tidak boleh muncul
    assert 'ISBN-0004' not in isbn_hasil


def test_rekomendasi_hop2_mencakup_tetangga_tetangga():
    """
    Dengan max_hop=2, ISBN-0004 harus muncul karena:
      ISBN-0001 -> ISBN-0002 -> ISBN-0004
    """
    g = buat_graf_sederhana()
    hasil = g.rekomendasikan('ISBN-0001', max_hop=2)
    isbn_hasil = [r[0] for r in hasil]
    assert 'ISBN-0004' in isbn_hasil


def test_rekomendasi_tidak_menyertakan_sumber():
    # ISBN sumber tidak boleh muncul di hasil rekomendasi
    g = buat_graf_sederhana()
    hasil = g.rekomendasikan('ISBN-0001', max_hop=2)
    isbn_hasil = [r[0] for r in hasil]
    assert 'ISBN-0001' not in isbn_hasil


def test_rekomendasi_tidak_ada_duplikat():
    # Setiap ISBN hanya boleh muncul sekali di hasil
    g = buat_graf_sederhana()
    hasil = g.rekomendasikan('ISBN-0001', max_hop=2)
    isbn_hasil = [r[0] for r in hasil]
    assert len(isbn_hasil) == len(set(isbn_hasil))


def test_rekomendasi_terurut_bobot_turun():
    """
    Hasil harus diurutkan berdasarkan bobot kumulatif (sering ko-pinjam duluan).
    Dari graf sederhana, ISBN-0002 (bobot 2) harus di atas ISBN-0003 (bobot 1).
    """
    g = buat_graf_sederhana()
    hasil = g.rekomendasikan('ISBN-0001', max_hop=1)
    bobot_list = [r[1] for r in hasil]
    assert bobot_list == sorted(bobot_list, reverse=True)


def test_rekomendasi_isbn_terisolasi_kembalikan_kosong():
    # Buku yang tidak punya tetangga tidak bisa direkomendasikan
    g = GraphRekBuku()
    g.tambah_vertex('ISBN-0099')   # vertex ada tapi tidak ada edge
    assert g.rekomendasikan('ISBN-0099') == []
   
def test_rekomendasi_min_bobot_memfilter_edge_lemah():
    """
    Dengan min_bobot=2, edge berbobot 1 (ISBN-0001 <-> ISBN-0003) harus disaring.
    Hanya ISBN-0002 (bobot 2) yang lolos.
    Relevan untuk Pertanyaan Analisis no. 3.
    """
    g = buat_graf_sederhana()
    hasil = g.rekomendasikan('ISBN-0001', max_hop=1, min_bobot=2)
    isbn_hasil = [r[0] for r in hasil]
    assert 'ISBN-0003' not in isbn_hasil   # disaring karena bobot=1
    assert 'ISBN-0002' in isbn_hasil       # lolos karena bobot=2