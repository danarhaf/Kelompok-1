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
        

    # ----------------------------------------------------------
    # jalankan — loop utama CLI
    # ----------------------------------------------------------
    def jalankan(self):
        print(BANNER)
        while True:
            try:
                masukan = input('>> ').strip()
            except (EOFError, KeyboardInterrupt):
                print('\n[SISTEM] Sesi berakhir.')
                break

            if not masukan:
                continue

            token = masukan.split()
            perintah = token[0].upper()

            if perintah == 'KELUAR':
                print('[SISTEM] Terima kasih. Program selesai.')
                break

            handler = self._handler.get(perintah)
            if handler is None:
                print(f'[ERROR] Perintah tidak dikenal: {perintah}. '
                    f'Ketik BANTUAN untuk daftar perintah.')
                continue

            # jalankan handler, tangkap error agar loop tidak berhenti
            try:
                handler(token)
            except Exception as e:
                print(f'[ERROR] {e}')

    # ── handler per perintah ──────────────────────────────────

    def _handle_bantuan(self, token):
        print(BANTUAN)

    # ----------------------------------------------------------
    # CARI_BUKU <isbn>
    # Big-O: O(log n) BST search
    # ----------------------------------------------------------
    def _handle_cari_buku(self, token):
        if len(token) < 2:
            print('[ERROR] Penggunaan: CARI_BUKU <isbn>')
            return
        isbn = token[1].upper()
        hasil = self._katalog.cari_buku(isbn)
        print(hasil['pesan'])
        print(f'  Big-O: {hasil["big_o"]}')
        

    # ----------------------------------------------------------
    # PINJAM <nim> <isbn>
    # Big-O: O(log n) BST search + update, O(1) stack push
    # ----------------------------------------------------------
    def _handle_pinjam(self, token):
        if len(token) < 3:
            print('[ERROR] Penggunaan: PINJAM <nim> <isbn>')
            return
        nim  = token[1].upper()
        isbn = token[2].upper()

        hasil = self._katalog.pinjam(isbn, nim, self._riwayat)
        print(hasil['pesan'])
        print(f'  Big-O: {hasil["big_o"]}')

        # catat ke graf rekomendasi jika berhasil
        if hasil['berhasil']:
            self._rekomendasi.catat_pinjam(nim, isbn)
