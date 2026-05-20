# ============================================================
# modul_6.py
# Modul CLI Perpustakaan
# Menangani input pengguna, mem-parse perintah, dan memanggil
# modul yang tepat. Setiap perintah menampilkan Big-O operasi.
#
# Perintah yang didukung:
#   CARI_BUKU <isbn>
#   PINJAM <nim> <isbn>
#   KEMBALIKAN <isbn>
#   PESAN <nim> <isbn>
#   BATALKAN_PESAN <nim> <isbn>
#   BATALKAN_TERAKHIR
#   REKOMENDASI <isbn>
#   ANTRIAN <isbn>
#   KATALOG
#   LAPORAN_BULAN
#   BANTUAN
#   KELUAR
# ============================================================

from modul_1 import ManajerAntrian
from modul_2 import ManajerRiwayat
from modul_3 import ManajerKatalog
from modul_4 import ManajerRekomendasi
from modul_5 import ManajerLaporan


# ── banner & bantuan ─────────────────────────────────────────
BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Smart Library Management & Recommendation System   ║
║       ELT60213 Algoritma dan Struktur Data               ║
║       Ketik BANTUAN untuk daftar perintah                ║
╚══════════════════════════════════════════════════════════╝
"""

BANTUAN = """
┌─────────────────────────────────────────────────────────┐
│  DAFTAR PERINTAH                          Big-O          │
├─────────────────────────────────────────────────────────┤
│  CARI_BUKU <isbn>                         O(log n)       │
│  PINJAM <nim> <isbn>                      O(log n)       │
│  KEMBALIKAN <isbn>                        O(log n)       │
│  PESAN <nim> <isbn>                       O(1) enqueue   │
│  BATALKAN_PESAN <nim> <isbn>              O(k) rebuild   │
│  BATALKAN_TERAKHIR                        O(1) pop       │
│  REKOMENDASI <isbn>                       O(V+E) BFS     │
│  ANTRIAN <isbn>                           O(k) traversal │
│  KATALOG                                  O(n) inorder   │
│  LAPORAN_BULAN                            O(n^1.5)/O(nlogn)│
│  BANTUAN                                  O(1)           │
│  KELUAR                                   -              │
└─────────────────────────────────────────────────────────┘
"""


class CLI:
    """
    Loop utama CLI perpustakaan.
    Menerima perintah teks, mem-parse token, memanggil modul.
    Semua manajer diinisialisasi dari luar dan disuntikkan
    ke CLI agar mudah diuji secara terpisah.
    """

    def __init__(self,
                manajer_antrian   : ManajerAntrian,
                manajer_riwayat   : ManajerRiwayat,
                manajer_katalog   : ManajerKatalog,
                manajer_rekomendasi: ManajerRekomendasi,
                manajer_laporan   : ManajerLaporan):

        self._antrian    = manajer_antrian
        self._riwayat    = manajer_riwayat
        self._katalog    = manajer_katalog
        self._rekomendasi= manajer_rekomendasi
        self._laporan    = manajer_laporan

        # tabel dispatch: perintah -> method handler
        self._handler = {
            'CARI_BUKU'         : self._handle_cari_buku,
            'PINJAM'            : self._handle_pinjam,
            'KEMBALIKAN'        : self._handle_kembalikan,
            'PESAN'             : self._handle_pesan,
            'BATALKAN_PESAN'    : self._handle_batalkan_pesan,
            'BATALKAN_TERAKHIR' : self._handle_batalkan_terakhir,
            'REKOMENDASI'       : self._handle_rekomendasi,
            'ANTRIAN'           : self._handle_antrian,
            'KATALOG'           : self._handle_katalog,
            'LAPORAN_BULAN'     : self._handle_laporan_bulan,
            'BANTUAN'           : self._handle_bantuan,
        }