class LLNode:
    def _init_(self, data=None):
        self.data = data
        self.next = None
        
class Queue:
    def _init_(self):
        self.head = None
        self.tail = None
        self._size = 0