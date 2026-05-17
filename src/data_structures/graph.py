class GraphRekBuku:
    def _init_(self):
        self.adj = {}
        
    def add_copinjam(self, a, b):
        if a == b:
            return

        self.adj.setdefault(a, {})
        self.adj.setdefault(b, {})

        self.adj[a][b] = self.adj[a].get(b, 0) + 1
        self.adj[b][a] = self.adj[b].get(a, 0) + 1
        
    def rekomendasikan(self, isbn, max_hop=2):
        visited = set([isbn])
        queue = [(isbn, 0)]
        hasil = set()