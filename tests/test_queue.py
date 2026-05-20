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
