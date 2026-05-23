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

from modules.modul_1 import ManajerAntrian
from modules.modul_2 import ManajerRiwayat
from modules.modul_3 import ManajerKatalog
from modules.modul_3 import LABEL_STATUS
from modules.modul_4 import ManajerRekomendasi
from modules.modul_5 import ManajerLaporan


# ── banner & bantuan ─────────────────────────────────────────
BANNER = """
╔══════════════════════════════════════════════════════════╗
║       Smart Library Management & Recommendation System   ║
║       ELT60213 Algoritma dan Struktur Data               ║
║       Ketik BANTUAN untuk daftar perintah                ║
╚══════════════════════════════════════════════════════════╝
"""

BANTUAN = """
┌────────────────────────────────┐────────────────────────────┐
│  DAFTAR PERINTAH               │           Big-O            │
├────────────────────────────────│────────────────────────────┤
│  CARI_BUKU <isbn>              │           O(log n)         │
│  PINJAM <nim> <isbn>           │           O(log n)         │
│  KEMBALIKAN <isbn>             │           O(log n)         │
│  PESAN <nim> <isbn>            │           O(1) enqueue     │
│  BATALKAN_PESAN <nim> <isbn>   │           O(k) rebuild     │
│  BATALKAN_TERAKHIR             │           O(1) pop         │
│  REKOMENDASI <isbn>            │           O(V+E) BFS       │
│  ANTRIAN <isbn>                │           O(k) traversal   │
│  KATALOG                       │           O(n) inorder     │
│  LAPORAN_BULAN                 │           O(n^1.5)/O(nlogn)│
│  BANTUAN                       │           O(1)             │
│  KELUAR                        │           -                │
└────────────────────────────────└────────────────────────────┘
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


    # ----------------------------------------------------------
    # KEMBALIKAN <isbn>
    # Big-O: O(log n) BST, O(1) dequeue antrian
    # ----------------------------------------------------------
    def _handle_kembalikan(self, token):
        if len(token) < 2:
            print('[ERROR] Penggunaan: KEMBALIKAN <isbn>')
            return
        isbn = token[1].upper()

        # cari siapa yang meminjam (dari riwayat stack)
        nim_peminjam = self._cari_peminjam_aktif(isbn)

        hasil = self._katalog.kembalikan(isbn, self._riwayat, self._antrian)
        print(hasil['pesan'])
        print(f'  Big-O: {hasil["big_o"]}')

        # update sesi rekomendasi jika berhasil
        if hasil['berhasil'] and nim_peminjam:
            self._rekomendasi.catat_kembalikan(nim_peminjam, isbn)


    # ----------------------------------------------------------
    # PESAN <nim> <isbn>
    # Big-O: O(1) enqueue (+ O(k) cek duplikat)
    # ----------------------------------------------------------
    def _handle_pesan(self, token):
        if len(token) < 3:
            print('[ERROR] Penggunaan: PESAN <nim> <isbn>')
            return
        nim  = token[1].upper()
        isbn = token[2].upper()

        # pastikan buku memang sedang dipinjam
        cari = self._katalog.cari_buku(isbn)
        if not cari['berhasil']:
            print(cari['pesan'])
            return
        if cari['status'] == 'TERSEDIA':
            print(f'[PESAN] Buku {isbn} sedang TERSEDIA. Langsung gunakan PINJAM.')
            return

        hasil = self._antrian.pesan(isbn, nim)
        print(hasil['pesan'])
        print(f'  Big-O: {hasil["big_o"]}')

        # catat ke stack riwayat
        if hasil['berhasil']:
            self._riwayat.catat('PESAN', nim, isbn)

    # ----------------------------------------------------------
    # BATALKAN_PESAN <nim> <isbn>
    # Big-O: O(k) rebuild antrian
    # ----------------------------------------------------------
    def _handle_batalkan_pesan(self, token):
        if len(token) < 3:
            print('[ERROR] Penggunaan: BATALKAN_PESAN <nim> <isbn>')
            return
        nim  = token[1].upper()
        isbn = token[2].upper()

        hasil = self._antrian.batalkan_pesan(isbn, nim)
        print(hasil['pesan'])
        print(f'  Big-O: {hasil["big_o"]}')

        if hasil['berhasil']:
            self._riwayat.catat('BATAL_PESAN', nim, isbn)

    # ----------------------------------------------------------
    # BATALKAN_TERAKHIR
    # Big-O: O(1) stack pop + O(log n) BST update status
    # ----------------------------------------------------------
    def _handle_batalkan_terakhir(self, token):
        tx = self._riwayat.batalkan_terakhir()   # O(1)

        if tx is None:
            print('[UNDO] Tidak ada transaksi yang bisa dibatalkan.')
            return

        aksi = tx.get('aksi', '')
        isbn = tx.get('isbn', '')
        nim  = tx.get('nim', '')

        print(f'[UNDO] Membatalkan: {ManajerRiwayat.format_tampil(tx)}')

        # balik efek berdasarkan jenis aksi
        if aksi == 'PINJAM':
            # buku kembali ke TERSEDIA
            ok = self._katalog.undo_pinjam(isbn)
            if ok:
                self._rekomendasi.catat_kembalikan(nim, isbn)
                print(f'[UNDO] Status {isbn} dikembalikan ke TERSEDIA.')

        elif aksi == 'KEMBALIKAN':
            # buku kembali ke DIPINJAM
            ok = self._katalog.undo_kembalikan(isbn)
            if ok:
                print(f'[UNDO] Status {isbn} dikembalikan ke DIPINJAM.')

        elif aksi == 'PESAN':
            # hapus nim dari antrian isbn
            self._antrian.batalkan_pesan(isbn, nim)
            print(f'[UNDO] Pesanan {nim} untuk {isbn} dihapus dari antrian.')

        print(f'  Big-O: O(1) stack pop + O(log n) BST update')


    # ----------------------------------------------------------
    # REKOMENDASI <isbn>
    # Big-O: O(V+E) BFS
    # ----------------------------------------------------------
    def _handle_rekomendasi(self, token):
        if len(token) < 2:
            print('[ERROR] Penggunaan: REKOMENDASI <isbn>')
            return
        isbn = token[1].upper()

        hasil = self._rekomendasi.rekomendasikan(
            isbn, max_hop=2, min_bobot=1,
            manajer_katalog=self._katalog
        )
        print(ManajerRekomendasi.format_rekomendasi(hasil))

    # ----------------------------------------------------------
    # ANTRIAN <isbn>
    # Big-O: O(k) traversal antrian
    # ----------------------------------------------------------
    def _handle_antrian(self, token):
        if len(token) < 2:
            print('[ERROR] Penggunaan: ANTRIAN <isbn>')
            return
        isbn = token[1].upper()
        info = self._antrian.lihat_antrian(isbn)

        print(f'[ANTRIAN] {isbn} — {info["panjang"]} anggota mengantri:')
        if not info['antrian']:
            print('  (kosong)')
        else:
            for i, nim in enumerate(info['antrian'], 1):
                print(f'  {i}. {nim}')
        print(f'  Big-O: {info["big_o"]}')


    # ----------------------------------------------------------
    # KATALOG
    # Big-O: O(n) inorder BST
    # ----------------------------------------------------------
    def _handle_katalog(self, token):
        daftar = self._katalog.katalog_semua()   # O(n)
        print(f'\n[KATALOG] Total {len(daftar)} buku (urutan ISBN):')
        print(f"{'No':>4} {'ISBN':<12} {'Judul':<30} {'Pengarang':<18} "
            f"{'Kategori':<10} {'Status'}")
        print('-' * 85)
        for i, b in enumerate(daftar, 1):
            label = LABEL_STATUS.get(b.status, '?')
            print(f"{i:>4} {b.isbn:<12} {b.judul[:28]:<30} "
                f"{b.pengarang:<18} {b.kategori:<10} {label}")
        print(f'\n  Big-O: O(n) inorder BST traversal')

    # ----------------------------------------------------------
    # LAPORAN_BULAN
    # Big-O: Shell Sort ~O(n^1.5), Merge Sort O(n log n)
    # ----------------------------------------------------------
    def _handle_laporan_bulan(self, token):
        riwayat = self._riwayat.riwayat_semua()   # O(n)

        # Shell Sort — durasi descending
        laporan_durasi = self._laporan.buat_laporan_durasi(riwayat)
        print('\n[LAPORAN] Peminjaman Berdasarkan Durasi (Shell Sort, descending):')
        print(f"{'No':>4} {'TX-ID':<8} {'NIM':<12} {'ISBN':<12} {'Durasi (hari)'}")
        print('-' * 55)
        for i, tx in enumerate(laporan_durasi[:10], 1):   # tampil 10 teratas
            print(f"{i:>4} TX-{tx['tx_id']:04d}   {tx['nim']:<12} "
                f"{tx['isbn']:<12} {tx['durasi']}")
        print(f'  Big-O Shell Sort: ~O(n^1.5)')

        # Merge Sort — frekuensi descending
        laporan_freq = self._laporan.buat_laporan_frekuensi(riwayat)
        print('\n[LAPORAN] Frekuensi Peminjaman per Judul (Merge Sort, descending):')
        print(f"{'No':>4} {'ISBN':<12} {'Frekuensi'}")
        print('-' * 30)
        for i, item in enumerate(laporan_freq[:10], 1):
            print(f"{i:>4} {item['isbn']:<12} {item['frekuensi']}")
        print(f'  Big-O Merge Sort: O(n log n)')

        # tabel benchmark runtime
        bench = self._laporan.benchmark_sorting(riwayat)
        print(ManajerLaporan.format_tabel_runtime(bench))

    # ── helper internal ───────────────────────────────────────

    def _cari_peminjam_aktif(self, isbn: str) -> str | None:
        """
        Cari NIM peminjam aktif suatu ISBN dari riwayat stack.
        Ambil transaksi PINJAM terbaru untuk isbn yang belum di-undo.
        Big-O: O(n) traversal riwayat
        """
        for tx in self._riwayat.riwayat_semua():
            if tx.get('isbn') == isbn and tx.get('aksi') == 'PINJAM':
                return tx.get('nim')
        return None
