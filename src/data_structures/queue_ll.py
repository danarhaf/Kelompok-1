class LLNode:
    def _init_(self, data=None):
        self.data = data
        self.next = None
        
class Queue:
    def _init_(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, data):
        node = LLNode(data)
        if not self.tail:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def dequeue(self):
        if not self.head:
            return None
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self._size -= 1
        return data
    
    def is_empty(self):
        return self._size == 0

    def _len_(self):
        return self._size