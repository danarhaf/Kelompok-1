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
        
        while queue:
            current, depth = queue.pop(0)
            if depth >= max_hop:
                continue

            for tetangga in self.adj.get(current, {}):
                if tetangga not in visited:
                    visited.add(tetangga)
                    hasil.add(tetangga)
                    queue.append((tetangga, depth+1))

        return list(hasil)