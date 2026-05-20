# ============================================================
# modul_4.py
# Modul Graph Rekomendasi Ko-pinjam
# Setiap kali anggota meminjam buku, sistem mencatat pasangan
# buku yang pernah dipinjam bersama dalam satu sesi (ko-pinjam).
# BFS digunakan untuk merekomendasikan buku dalam radius hop <= 2.
#
# Struktur data : Graf tak-berarah berbobot (graph.py)
# Big-O BFS     : O(V + E)
# Big-O tambah  : O(deg) per edge
# ============================================================

from data_structures.graph import GraphRekBuku


class ManajerRekomendasi:
    """
    Lapisan bisnis di atas GraphRekBuku.
    Mencatat ko-pinjam setiap kali transaksi PINJAM berhasil,
    lalu menyajikan rekomendasi via BFS saat diminta CLI.

    Riwayat pinjam per anggota disimpan di _sesi_aktif:
      { nim -> [isbn, isbn, ...] }
    Setiap kali sesi ditutup (anggota selesai pinjam),
    semua pasangan buku di sesi itu dicatat ke graf.
    """

    def __init__(self):
        self._graf = GraphRekBuku()
        # sesi_aktif: lacak buku yang sedang dipinjam per anggota
        # dipakai untuk generate edge ko-pinjam
        self._sesi_aktif: dict[str, list[str]] = {}
        # ----------------------------------------------------------
    # catat_pinjam — tambahkan isbn ke sesi aktif anggota
    # dan langsung update edge ko-pinjam dengan buku sebelumnya.
    # Big-O Waktu : O(k * deg) — k = buku aktif anggota ini
    # ----------------------------------------------------------
    def catat_pinjam(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali PINJAM berhasil (dari main/modul_3).
        Buku baru langsung dipasangkan dengan semua buku yang
        sedang dipinjam oleh anggota yang sama.
        """
        # pastikan slot sesi ada
        if nim not in self._sesi_aktif:
            self._sesi_aktif[nim] = []

        # buat edge ko-pinjam dengan semua buku aktif anggota ini
        for isbn_lain in self._sesi_aktif[nim]:
            self._graf.add_copinjam(isbn, isbn_lain)   # O(deg)

        self._sesi_aktif[nim].append(isbn)
            # ----------------------------------------------------------
    # catat_kembalikan — hapus isbn dari sesi aktif anggota
    # Big-O Waktu : O(k) — k = buku aktif anggota
    # ----------------------------------------------------------
    def catat_kembalikan(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali KEMBALIKAN berhasil.
        Buku dikembalikan berarti keluar dari sesi aktif anggota.
        """
        if nim in self._sesi_aktif and isbn in self._sesi_aktif[nim]:
            self._sesi_aktif[nim].remove(isbn)   # O(k)
                # ----------------------------------------------------------
    # catat_pinjam — tambahkan isbn ke sesi aktif anggota
    # dan langsung update edge ko-pinjam dengan buku sebelumnya.
    # Big-O Waktu : O(k * deg) — k = buku aktif anggota ini
    # ----------------------------------------------------------
    def catat_pinjam(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali PINJAM berhasil (dari main/modul_3).
        Buku baru langsung dipasangkan dengan semua buku yang
        sedang dipinjam oleh anggota yang sama.
        """
        # pastikan slot sesi ada
        if nim not in self._sesi_aktif:
            self._sesi_aktif[nim] = []

        # buat edge ko-pinjam dengan semua buku aktif anggota ini
        for isbn_lain in self._sesi_aktif[nim]:
            self._graf.add_copinjam(isbn, isbn_lain)   # O(deg)

        self._sesi_aktif[nim].append(isbn)
            # ----------------------------------------------------------
    # catat_kembalikan — hapus isbn dari sesi aktif anggota
    # Big-O Waktu : O(k) — k = buku aktif anggota
    # ----------------------------------------------------------
    def catat_kembalikan(self, nim: str, isbn: str):
        """
        Dipanggil setiap kali KEMBALIKAN berhasil.
        Buku dikembalikan berarti keluar dari sesi aktif anggota.
        """
        if nim in self._sesi_aktif and isbn in self._sesi_aktif[nim]:
            self._sesi_aktif[nim].remove(isbn)   # O(k)
                # ----------------------------------------------------------
    # rekomendasikan — BFS dari isbn, max 2 hop
    # Big-O Waktu : O(V + E)
    # ----------------------------------------------------------
    def rekomendasikan(self, isbn: str,
                       max_hop: int = 2,
                       min_bobot: int = 1,
                       manajer_katalog=None) -> dict:
                """
        Rekomendasikan buku yang sering dipinjam bersama isbn.
        Jika manajer_katalog diberikan, sertakan info judul buku.
        Kembalikan dict berisi list rekomendasi + info Big-O.
        """
        hasil_bfs = self._graf.rekomendasikan(isbn, max_hop, min_bobot)
        # hasil_bfs: list of (isbn_rek, bobot, hop)

        rekomendasi = []
        for isbn_rek, bobot, hop in hasil_bfs:
            item = {
                'isbn'  : isbn_rek,
                'bobot' : bobot,
                'hop'   : hop,
                'judul' : '-',
                'status': '-',
            }
 # tambahkan info judul dari BST jika katalog tersedia
            if manajer_katalog is not None:
                hasil_cari = manajer_katalog.cari_buku(isbn_rek)
                if hasil_cari['berhasil']:
                    item['judul']  = hasil_cari['buku'].judul
                    item['status'] = hasil_cari['status']
            rekomendasi.append(item)

        return {
            'isbn_sumber'  : isbn,
            'rekomendasi'  : rekomendasi,
            'jumlah'       : len(rekomendasi),
            'big_o'        : 'O(V+E) BFS graf ko-pinjam',
        }
    # ----------------------------------------------------------
    # info_graf — statistik graf untuk laporan eksperimen
    # Big-O Waktu : O(V + E)
    # ----------------------------------------------------------
    def info_graf(self) -> dict:
        return self._graf.info_graf()
    # ----------------------------------------------------------
    # format_rekomendasi — ubah hasil rekomendasikan ke string CLI
    # ----------------------------------------------------------
    @staticmethod
    def format_rekomendasi(hasil: dict) -> str:
        """Kembalikan string siap cetak untuk perintah REKOMENDASI."""
        baris = [f"[REKOMENDASI] Buku yang sering dipinjam bersama {hasil['isbn_sumber']}:"]
        if not hasil['rekomendasi']:
            baris.append('  (belum ada data ko-pinjam untuk buku ini)')
        else:
            for i, item in enumerate(hasil['rekomendasi'], 1):
                baris.append(
                    f"  {i}. {item['isbn']} | {item['judul'][:30]:<30} "
                    f"| Bobot: {item['bobot']} | Hop: {item['hop']} "
                    f"| {item['status']}"
                )
        baris.append(f"  Big-O: {hasil['big_o']}")
        return '\n'.join(baris)