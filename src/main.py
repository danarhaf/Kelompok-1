# ============================================================
# main.py
# Entry Point Smart Library Management & Recommendation System
# Jalankan dari ROOT project: python src/main.py
#
# Menginisialisasi semua manajer, memuat koleksi 80 buku,
# lalu menyerahkan kontrol ke CLI (modul_6).
#
# Seed = 13 (JANGAN diubah agar hasil reprodusibel)
# ============================================================

import sys
import os

# tambahkan src/ dan src/modules/ ke path
# agar semua import bisa ditemukan saat dijalankan dari root maupun dari src/
_SRC = os.path.dirname(__file__)                    # .../src/
_MOD = os.path.join(_SRC, 'modules')               # .../src/modules/

sys.path.insert(0, _SRC)
sys.path.insert(0, _MOD)

import random
import numpy as np

# seed wajib diset sebelum import apapun yang pakai random
random.seed(13)
np.random.seed(13)

from data_model    import STATUS
from generate_data import generate_koleksi

from modules.modul_1 import ManajerAntrian
from modules.modul_2 import ManajerRiwayat
from modules.modul_3 import ManajerKatalog
from modules.modul_4 import ManajerRekomendasi
from modules.modul_5 import ManajerLaporan
from modules.modul_6 import CLI


def main():
    """
    Inisialisasi sistem dan jalankan CLI.

    Urutan startup:
    
    1. Generate 80 buku dengan seed=13
    2. Muat koleksi ke BST katalog         -> O(n log n)
    3. Inisialisasi antrian per ISBN        -> O(n)
    4. Serahkan kontrol ke loop CLI

    Big-O startup keseluruhan: O(n log n) didominasi insert BST.
    """

    print('[SISTEM] Memulai Smart Library System...')

    # ── 1. generate koleksi 80 buku ───────────────────────
    # seed sudah diset di atas, hasil selalu sama (reprodusibel)
    koleksi = generate_koleksi(80)   # O(n)
    print(f'[SISTEM] {len(koleksi)} buku berhasil di-generate (seed=13).')

    # ── 2. inisialisasi semua manajer ─────────────────────
    manajer_antrian    = ManajerAntrian()
    manajer_riwayat    = ManajerRiwayat()
    manajer_katalog    = ManajerKatalog()
    manajer_rekomendasi= ManajerRekomendasi()
    manajer_laporan    = ManajerLaporan()

    # ── 3. muat koleksi ke BST katalog ────────────────────
    # Big-O: O(n log n) — n kali insert BST O(log n)
    manajer_katalog.muat_koleksi(koleksi)
    print(f'[SISTEM] Katalog BST siap. {manajer_katalog.info_bst()}')

    # ── 4. inisialisasi antrian per ISBN ──────────────────
    # Big-O: O(n) — satu Queue kosong per buku
    daftar_isbn = [b.isbn for b in koleksi]
    manajer_antrian.inisialisasi_antrian(daftar_isbn)
    print(f'[SISTEM] Antrian per ISBN siap ({len(daftar_isbn)} slot).')

    # ── 5. serahkan ke CLI ────────────────────────────────
    cli = CLI(
        manajer_antrian    = manajer_antrian,
        manajer_riwayat    = manajer_riwayat,
        manajer_katalog    = manajer_katalog,
        manajer_rekomendasi= manajer_rekomendasi,
        manajer_laporan    = manajer_laporan,
    )

    cli.jalankan()

# ── mode --test untuk GitHub Actions CI ───────────────────────
# dipanggil oleh ci.yml: python src/main.py --test
# hanya verifikasi startup tanpa masuk loop CLI interaktif

def test_mode():
    """
    Verifikasi bahwa semua modul bisa diimport dan diinisialisasi
    tanpa error. Digunakan oleh GitHub Actions CI.
    Big-O: O(n log n) — sama dengan startup normal.
    """
    print('[TEST] Menjalankan mode test...')

    koleksi = generate_koleksi(80)
    assert len(koleksi) == 80, 'Jumlah buku harus 80'

    manajer_katalog = ManajerKatalog()
    manajer_katalog.muat_koleksi(koleksi)
    assert len(manajer_katalog.katalog_semua()) == 80, 'BST harus berisi 80 buku'

    # verifikasi inorder terurut
    isbn_list = [b.isbn for b in manajer_katalog.katalog_semua()]
    assert isbn_list == sorted(isbn_list), 'Inorder BST harus terurut'

    # verifikasi update status
    ok = manajer_katalog._bst.update_status('ISBN-0001', STATUS['DIPINJAM'])
    assert ok is True, 'update_status harus berhasil'
    manajer_katalog._bst.update_status('ISBN-0001', STATUS['TERSEDIA'])