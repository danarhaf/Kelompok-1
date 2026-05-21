# ════════════════════════════════════════════════════════════
# 2. BENCHMARK STACK
# Operasi: push O(1), pop O(1)
# ════════════════════════════════════════════════════════════

def benchmark_stack(ukuran_list: list) -> list:
    print('\n[STACK] Memulai benchmark...')
    hasil = []

    for n in ukuran_list:
        tx_list = [{'tx_id': i, 'aksi': 'PINJAM', 'isbn': f'ISBN-{i:04d}',
                    'nim': f'NIM-{i:03d}', 'durasi': 14, 'waktu': time.time()}
                   for i in range(n)]

        def uji_push(tx_list=tx_list):
            s = Stack()
            for tx in tx_list:
                s.push(tx)

        t_push = ukur_waktu(uji_push)

        def uji_pop(tx_list=tx_list):
            s = Stack()
            for tx in tx_list:
                s.push(tx)
            while not s.is_empty():
                s.pop()

        t_pop = ukur_waktu(uji_pop)

        hasil.append([
            n,
            f'{t_push:.6f}',
            f'{t_pop:.6f}',
            'O(1) per op',
        ])

    cetak_tabel(
        'STACK — push & pop (rata-rata 5 ulangan)',
        ['N', 'push N (s)', 'pop N (s)', 'Big-O per operasi'],
        hasil,
    )
    return hasil