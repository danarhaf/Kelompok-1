# ============================================================
# test_stack.py
# Unit test untuk Stack berbasis Linked List (stack.py)
# Jalankan: pytest tests/test_stack.py -v
# ============================================================

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_structures.stack import Stack


# ── helper ────────────────────────────────────────────────────
def buat_stack(*items):
    """Buat Stack dan langsung isi dengan items (item terakhir = paling atas)."""
    s = Stack()
    for item in items:
        s.push(item)
    return s


# ══════════════════════════════════════════════════════════════
# KELOMPOK 1 — kondisi awal / state kosong
# ══════════════════════════════════════════════════════════════

def test_stack_baru_pasti_kosong():
    s = Stack()
    assert s.is_empty() is True
    assert len(s) == 0


def test_pop_dari_stack_kosong_kembalikan_none():
    # pop stack kosong tidak boleh error, cukup kembalikan None
    s = Stack()
    assert s.pop() is None


def test_peek_stack_kosong_kembalikan_none():
    s = Stack()
    assert s.peek() is None