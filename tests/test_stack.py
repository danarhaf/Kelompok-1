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


# ══════════════════════════════════════════════════════════════
# KELOMPOK 2 — operasi dasar push & pop
# ══════════════════════════════════════════════════════════════

def test_satu_push_lalu_pop():
    s = Stack()
    s.push('TX-001')
    assert s.pop() == 'TX-001'


def test_urutan_lifo_terjaga():
    # Yang terakhir masuk harus pertama keluar
    # push: A, B, C  ->  pop harus: C, B, A
    s = buat_stack('A', 'B', 'C')
    assert s.pop() == 'C'
    assert s.pop() == 'B'
    assert s.pop() == 'A'


def test_size_naik_setiap_push():
    s = Stack()
    for i in range(1, 6):
        s.push(i)
        assert len(s) == i


def test_size_turun_setiap_pop():
    s = buat_stack(10, 20, 30)
    for sisa in [2, 1, 0]:
        s.pop()
        assert len(s) == sisa


def test_stack_kosong_setelah_semua_dipop():
    s = buat_stack('x', 'y', 'z')
    s.pop(); s.pop(); s.pop()
    assert s.is_empty() is True
    assert len(s) == 0    