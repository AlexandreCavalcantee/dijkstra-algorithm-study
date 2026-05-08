class MinHeap:
    def __init__(self):
        self._heap = []
        self._position = {}

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return len(self._heap) == 0

    def contains(self, item):
        return item in self._position

    def push(self, item, priority):
        if item in self._position:
            self.decrease_key(item, priority)
            return
        self._heap.append((priority, item))
        index = len(self._heap) - 1
        self._position[item] = index
        self._sift_up(index)

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty heap")
        root_priority, root_item = self._heap[0]
        last = self._heap.pop()
        del self._position[root_item]
        if self._heap:
            self._heap[0] = last
            self._position[last[1]] = 0
            self._sift_down(0)
        return root_item, root_priority

    def peek(self):
        if not self._heap:
            raise IndexError("peek from empty heap")
        priority, item = self._heap[0]
        return item, priority

    def decrease_key(self, item, new_priority):
        if item not in self._position:
            raise KeyError(item)
        index = self._position[item]
        current_priority, _ = self._heap[index]
        if new_priority > current_priority:
            return
        self._heap[index] = (new_priority, item)
        self._sift_up(index)

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self._heap[index][0] < self._heap[parent][0]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _sift_down(self, index):
        size = len(self._heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            if left < size and self._heap[left][0] < self._heap[smallest][0]:
                smallest = left
            if right < size and self._heap[right][0] < self._heap[smallest][0]:
                smallest = right
            if smallest == index:
                break
            self._swap(index, smallest)
            index = smallest

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._position[self._heap[i][1]] = i
        self._position[self._heap[j][1]] = j
