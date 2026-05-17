class BSTNode:
    def _init_(self, buku):
        self.buku = buku
        self.left = None
        self.right = None
        
class BSTKatalog:
    def _init_(self):
        self.root = None
        
    def insert(self, buku):
        def _insert(node, buku):
            if not node:
                return BSTNode(buku)
            if buku.isbn < node.buku.isbn:
                node.left = _insert(node.left, buku)
            else:
                node.right = _insert(node.right, buku)
            return node
        self.root = _insert(self.root, buku)

    def search(self, isbn):
        node = self.root
        while node:
            if isbn == node.buku.isbn:
                return node.buku
            elif isbn < node.buku.isbn:
                node = node.left
            else:
                node = node.right
        return None

    def update_status(self, isbn, status):
        buku = self.search(isbn)
        if buku:
            buku.status = status

    def inorder(self):
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.buku)
                _inorder(node.right)
        _inorder(self.root)
        return result