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


# ══════════════════════════════════════════════════════════════
# KELOMPOK 3 — peek (tidak merusak tumpukan)
# ══════════════════════════════════════════════════════════════

def test_peek_tidak_menghapus_elemen():
    s = buat_stack('TX-001', 'TX-002')
    hasil = s.peek()
    assert hasil == 'TX-002'      # top = yang terakhir di-push
    assert len(s) == 2            # ukuran tidak boleh berubah


def test_peek_selalu_menunjuk_top():
    s = buat_stack(1, 2, 3)
    assert s.peek() == 3
    s.pop()
    assert s.peek() == 2
    s.pop()
    assert s.peek() == 1


# ══════════════════════════════════════════════════════════════
# KELOMPOK 4 — tampilkan_stack
# ══════════════════════════════════════════════════════════════

def test_tampilkan_stack_urutan_atas_ke_bawah():
    # tampilkan_stack harus mengembalikan dari top ke bottom
    s = buat_stack('A', 'B', 'C')
    assert s.tampilkan_stack() == ['C', 'B', 'A']


def test_tampilkan_stack_kosong_kembalikan_list_kosong():
    s = Stack()
    assert s.tampilkan_stack() == []


def test_tampilkan_stack_tidak_mengubah_isi():
    s = buat_stack(10, 20, 30)
    s.tampilkan_stack()
    # setelah dipanggil, isi stack tidak boleh berubah
    assert len(s) == 3
    assert s.peek() == 30


# ══════════════════════════════════════════════════════════════
# KELOMPOK 5 — skenario undo transaksi perpustakaan
# ══════════════════════════════════════════════════════════════

def test_undo_transaksi_terakhir():
    """
    Simulasi fitur BATALKAN_TERAKHIR di CLI:
    petugas salah input -> pop transaksi terbaru dari stack.
    """
    s = Stack()
    tx1 = {'id': 1, 'aksi': 'PINJAM', 'isbn': 'ISBN-0001', 'nim': 'NIM-001'}
    tx2 = {'id': 2, 'aksi': 'PINJAM', 'isbn': 'ISBN-0002', 'nim': 'NIM-002'}
    s.push(tx1)
    s.push(tx2)

    # batalkan transaksi terakhir
    dibatalkan = s.pop()
    assert dibatalkan['id'] == 2
    assert dibatalkan['aksi'] == 'PINJAM'

    # stack sekarang hanya berisi tx1
    assert len(s) == 1
    assert s.peek()['id'] == 1


def test_push_setelah_sempat_kosong():
    # Stack boleh dipakai lagi setelah dikosongkan
    s = buat_stack('TX-001')
    s.pop()
    s.push('TX-002')
    assert s.peek() == 'TX-002'
    assert len(s) == 1


def test_push_objek_dict_sebagai_transaksi():
    # Data transaksi berbentuk dict harus bisa masuk stack
    s = Stack()
    for i in range(1, 6):
        s.push({'tx_id': i, 'isbn': f'ISBN-{i:04d}'})
    assert len(s) == 5
    assert s.peek()['tx_id'] == 5   # yang terakhir push ada di atas


# ══════════════════════════════════════════════════════════════
# KELOMPOK 6 — pindah_ke_linked_list (archiving)
# ══════════════════════════════════════════════════════════════

def test_archiving_tidak_terjadi_jika_belum_melebihi_batas():
    s = buat_stack(1, 2, 3)
    arsip = s.arsip_transaksi_lama(maks_simpan=10)
    # belum perlu arsip karena size <= maks_simpan
    assert arsip == []
    assert len(s) == 3


def test_archiving_memindah_elemen_lama():
    """
    Stack isi 10 elemen, maks_simpan=5.
    5 elemen terlama (terbawah) harus dipindah ke arsip.
    Stack menyisakan 5 elemen teratas.
    Relevan untuk Pertanyaan Analisis no. 4.
    """
    s = Stack()
    for i in range(1, 11):   # push 1..10, top = 10
        s.push(i)

    arsip = s.arsip_transaksi_lama(maks_simpan=5)

    # stack menyisakan 5 elemen teratas: 10, 9, 8, 7, 6
    assert len(s) == 5
    assert s.peek() == 10

    # arsip berisi 5 elemen terbawah: 5, 4, 3, 2, 1 (urutan atas->bawah)
    assert len(arsip) == 5
    assert arsip[0] == 5   # elemen terlama yang dipindah pertama


def test_archiving_stack_tetap_berfungsi_normal_setelahnya():
    s = Stack()
    for i in range(1, 11):
        s.push(i)
    s.arsip_transaksi_lama(maks_simpan=5)

    # setelah archiving, push/pop harus tetap normal
    s.push(99)
    assert s.peek() == 99
    assert len(s) == 6
    assert s.pop() == 99


# ══════════════════════════════════════════════════════════════
# KELOMPOK 7 — skala besar (500 operasi)
# ══════════════════════════════════════════════════════════════

def test_500_push_lalu_500_pop_urutan_lifo():
    """
    Tes beban 500 operasi.
    Memastikan pointer top tidak rusak pada skala transaksi harian.
    Big-O total: O(n), setiap push/pop adalah O(1).
    """
    s = Stack()
    n = 500
    for i in range(n):
        s.push(i)
    assert len(s) == n

    for i in range(n - 1, -1, -1):
        nilai = s.pop()
        assert nilai == i   # LIFO: yang terakhir push harus keluar duluan

    assert s.is_empty() is True


