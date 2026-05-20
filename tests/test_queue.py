# ============================================================
# test_queue.py
# Unit test untuk Queue berbasis Linked List (queue_ll.py)
# Jalankan: pytest tests/test_queue.py -v
# ============================================================

import sys
import os

# supaya bisa import dari src/ tanpa install package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_structures.queue_ll import Queue
