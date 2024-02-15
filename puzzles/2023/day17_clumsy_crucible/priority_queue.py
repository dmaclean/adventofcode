import dataclasses
from heapq import heappop, heappush, heapify
from typing import List, Dict


class AocPriorityQueue:
    def __init__(self):
        self.q: List[HeapItem] = []
        self.entry_finder: Dict[str, HeapItem] = {}
        heapify(self.q)

    def queue_length(self):
        return len(self.q)

    def add_task(self, task: "HeapItem") -> None:
        cache_entry = self.entry_finder.get(task.q_val)
        if cache_entry:
            cache_entry.removed = True
        heappush(self.q, task)
        self.entry_finder[task.q_val] = task

    def pop_task(self) -> "HeapItem":
        while self.q:
            task = heappop(self.q)
            if not task.removed:
                return task
        raise KeyError('pop from an empty priority queue')


@dataclasses.dataclass
class HeapItem:
    q_val: str
    dist: int
    removed: bool

    def __lt__(self, other):
        return self.dist < other.dist
