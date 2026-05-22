# linked_list.py
# Node dasar untuk Queue dan Stack
# Kompleksitas Ruang dan Waktu Keseluruhan O(1)

class LLNode:
    
    def __init__(self, data=None):
        self.data = data
        self.next = None