from bst import BSTKatalog
from queue import Queue
from stack import Stack
from graph import GraphRekBuku
import random

def generate_koleksi(n=80):
    kata = ['Algoritma','Jaringan','Python','Data','Digital',
            'Sistem','Kontrol','Sinyal','Elektronika','Fisika']

    return [
        (f'ISBN-{i:04d}', f'{random.choice(kata)} Vol.{i}')
        for i in range(1, n+1)
    ]

def main():
    bst = BSTKatalog()
    antrian = {}
    stack = Stack()
    graph = GraphRekBuku()

    print("SMART LIBRARY")

    while True:
        cmd = input(">> ").split()

        if cmd[0] == "KELUAR":
            break

        elif cmd[0] == "KATALOG":
            for b in bst.inorder():
                print(b.isbn, b.judul)