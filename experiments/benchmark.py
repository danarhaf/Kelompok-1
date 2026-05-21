# ════════════════════════════════════════════════════════════
# 5. BENCHMARK SORTING (Shell Sort vs Merge Sort)
# Pada Linked List, bukan list Python
# ════════════════════════════════════════════════════════════

def benchmark_sorting(ukuran_list: list) -> list:
    print('\n[SORTING] Memulai benchmark...')
    hasil = []

    for n in ukuran_list:
        tx_list = [
            {'tx_id': i, 'aksi': 'PINJAM',
             'isbn': f'ISBN-{random.randint(1, 80):04d}',
             'nim': f'NIM-{i:03d}',
             'durasi': random.randint(7, 30),
             'waktu': time.time()}
            for i in range(n)
        ]

        # ── Shell Sort pada Linked List ───────────────────
        def uji_shell(tx_list=tx_list):
            ll = LinkedListLaporan()
            for tx in tx_list:
                ll.tambah_belakang(tx)
            shell_sort_durasi(ll)

        t_shell = ukur_waktu(uji_shell)

        # ── Merge Sort pada Linked List ───────────────────
        freq = {}
        for tx in tx_list:
            isbn = tx['isbn']
            freq[isbn] = freq.get(isbn, 0) + 1

        def uji_merge(freq=freq):
            ll = LinkedListLaporan()
            for isbn, jumlah in freq.items():
                ll.tambah_belakang({'isbn': isbn, 'frekuensi': jumlah})
            merge_sort_frekuensi(ll.head)

        t_merge = ukur_waktu(uji_merge)

        hasil.append([
            n,
            f'{t_shell:.6f}',
            f'{t_merge:.6f}',
            '~O(n^1.5)',
            'O(n log n)',
        ])

    cetak_tabel(
        'SORTING — Shell Sort vs Merge Sort pada Linked List (rata-rata 5 ulangan)',
        ['N', 'Shell Sort (s)', 'Merge Sort (s)',
         'Big-O Shell', 'Big-O Merge'],
        hasil,
    )
    print('  Catatan: Merge Sort lebih konsisten O(n log n),')
    print('  Shell Sort lebih cepat untuk data hampir terurut.')
    return hasil