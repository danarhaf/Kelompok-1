# ============================================================
# test_queue.py
# Unit test untuk Queue berbasis Linked List (queue_ll.py)
# Jalankan: pytest tests/test_queue.py -v
# ============================================================

import sys
import os

# supaya bisa import dari src/ tanpa install package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_structures.queue_ll import Queue


# ── helper ────────────────────────────────────────────────────
def buat_queue(*items):
    """Buat Queue dan langsung isi dengan items yang diberikan."""
    q = Queue()
    for item in items:
        q.enqueue(item)
    return q


# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — kondisi awal / state kosong
# ══════════════════════════════════════════════════════════════

def test_queue_baru_pasti_kosong():
    # Queue yang baru dibuat harus langsung kosong
    q = Queue()
    assert q.is_empty() is True
    assert len(q) == 0


def test_dequeue_dari_queue_kosong_kembalikan_none():
    # Dequeue dari queue kosong tidak boleh error, cukup kembalikan None
    q = Queue()
    assert q.dequeue() is None


def test_peek_queue_kosong_kembalikan_none():
    q = Queue()
    assert q.peek() is None



# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — operasi dasar enqueue & dequeue
# ══════════════════════════════════════════════════════════════

def test_satu_enqueue_lalu_dequeue():
    # enqueue satu elemen, dequeue harus mengembalikan elemen itu
    q = Queue()
    q.enqueue('NIM-001')
    assert q.dequeue() == 'NIM-001'


def test_urutan_fifo_terjaga():
    # Yang pertama masuk harus pertama keluar
    # enqueue: A, B, C  ->  dequeue harus: A, B, C
    q = buat_queue('A', 'B', 'C')
    assert q.dequeue() == 'A'
    assert q.dequeue() == 'B'
    assert q.dequeue() == 'C'

def test_size_bertambah_setiap_enqueue():
    q = Queue()
    for i in range(5):
        q.enqueue(i)
        assert len(q) == i + 1   # ukuran harus naik tepat 1 setiap kali


def test_size_berkurang_setiap_dequeue():
    q = buat_queue(10, 20, 30)
    for sisa in [2, 1, 0]:
        q.dequeue()
        assert len(q) == sisa


def test_queue_kosong_setelah_semua_didequeue():
    q = buat_queue('x', 'y')
    q.dequeue()
    q.dequeue()
    assert q.is_empty() is True
    assert len(q) == 0

# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — peek (tidak merusak antrian)
# ══════════════════════════════════════════════════════════════

def test_peek_tidak_menghapus_elemen():
    q = buat_queue('NIM-010', 'NIM-011')
    hasil_peek = q.peek()
    assert hasil_peek == 'NIM-010'
    # setelah peek, ukuran tidak boleh berubah
    assert len(q) == 2


def test_peek_menunjuk_head_bukan_tail():
    q = buat_queue(1, 2, 3)
    # peek harus selalu mengembalikan elemen paling depan
    assert q.peek() == 1
    q.dequeue()
    assert q.peek() == 2

# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — tampilkan_antrian
# ══════════════════════════════════════════════════════════════

def test_tampilkan_antrian_urutan_benar():
    q = buat_queue('A', 'B', 'C', 'D')
    assert q.tampilkan_antrian() == ['A', 'B', 'C', 'D']


def test_tampilkan_antrian_kosong_kembalikan_list_kosong():
    q = Queue()
    assert q.tampilkan_antrian() == []