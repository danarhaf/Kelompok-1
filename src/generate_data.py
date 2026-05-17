def generate_data(n=80):
    kata = ['Algoritma','Jaringan','Python','Data','Digital',
            'Sistem','Kontrol','Sinyal','Elektronika','Fisika']
    
    return [Buku(f'ISBN-{i:04d}',
                f'{random.choice(kata)} Vol.{i}',
                f'Penulis-{random.randint(1,20)}',
                random.choice(KATEGORI))
            for i in range(1, n+1)]