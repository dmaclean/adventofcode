import dataclasses
import heapq
import logging
import sys
import time
from typing import List, Tuple, Dict


@dataclasses.dataclass
class HeapItem:
    q_val: str
    dist: int
    removed: bool

    def __lt__(self, other):
        return self.dist < other.dist


def djikstra(grid: List[List[int]]) -> int:
    start = (0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)
    q, prio_q, dist, prev = init_structs(grid, start)

    while q:
        if len(q) % 100 == 0:
            print(f"Queue size: {len(q)}")
        v, direction_from_prev, steps_in_dir = find_vertex_to_explore(q, prio_q, dist)
        if v == end:
            return find_lowest_val(dist[v])  # dist[v]  # Fix the return value once we're settled on this
        remove_from_q(q, v, direction_from_prev, steps_in_dir)

        # Explore all neighbors
        r = v[0]
        c = v[1]

        curr_cost = dist[v][direction_from_prev][steps_in_dir]

        for dest_and_dir in [((r, c + 1), "R"), ((r - 1, c), "U"), ((r + 1, c), "D"), ((r, c - 1), "L")]:
            dest = dest_and_dir[0]
            dir_of_dest = dest_and_dir[1]
            steps_for_dest = steps_in_dir + 1 if dir_of_dest == direction_from_prev else 1
            q_entry = f"{dest[0]}-{dest[1]}-{dir_of_dest}-{steps_for_dest}"
            if q_entry in q and can_move(grid, v, dir_of_dest, direction_from_prev, steps_in_dir):
                curr_dest_cost = dist[dest][dir_of_dest][steps_for_dest]
                dest_cost = find_cost(grid, dest)
                if curr_cost + dest_cost < curr_dest_cost:
                    dist[dest][dir_of_dest][steps_for_dest] = curr_cost + dest_cost
                    prev[dest][dir_of_dest][steps_for_dest] = (v, direction_from_prev, steps_in_dir)


def find_cost(grid, v):
    return grid[v[0]][v[1]]


def can_move(grid: List[List[int]],
             curr: Tuple[int, int],
             dir_of_dest: str,
             direction_from_prev: str,
             steps_in_dir: int) -> bool:
    if direction_from_prev == dir_of_dest and steps_in_dir == 3:
        return False
    if (dir_of_dest == "U" and direction_from_prev == "D") or \
            (dir_of_dest == "L" and direction_from_prev == "R") or \
            (dir_of_dest == "D" and direction_from_prev == "U") or \
            (dir_of_dest == "R" and direction_from_prev == "L"):
        logging.debug(f"Cannot move: Going to move off map at {curr}.")
        return False
    if (dir_of_dest == "U" and curr[0] == 0) or \
            (dir_of_dest == "L" and curr[1] == 0) or \
            (dir_of_dest == "D" and curr[0] == len(grid) - 1) or \
            (dir_of_dest == "R" and curr[1] == len(grid[0]) - 1):
        logging.debug(f"Cannot move: Going to move off map at {curr}.")
        return False
    return True


def remove_from_q(q, v, direction, steps):
    q.remove(f"{v[0]}-{v[1]}-{direction}-{steps}")


def find_lowest_val(dist_entry):
    min_val = sys.maxsize
    for d, steps in dist_entry.items():
        v = min(steps.values())
        if v < min_val:
            min_val = v
    return min_val


def find_vertex_to_explore(q: List[str],
                           prio_q,
                           dist: Dict[Tuple[int, int], Dict[str, Dict[int, int]]]) -> Tuple[Tuple[int, int], str, int]:
    # heap_item: HeapItem = heapq.heappop(prio_q)
    # r, c, d, s = heap_item.q_val.split("-")
    # return (int(r), int(c)), d, int(s)

    min_val = sys.maxsize
    next_vertex = None
    next_direction = None
    next_steps = None
    for entry in q:
        r, c, d, s = entry.split("-")
        r = int(r)
        c = int(c)
        s = int(s)
        v = (r, c)

        # if dist[v] < min_val:
        dist_val = dist[v][d][s]
        if dist_val < min_val:
            min_val = dist_val
            next_vertex = v
            next_direction = d
            next_steps = s
    return next_vertex, next_direction, next_steps


def init_structs(grid, start):
    q = []
    prio_q = []
    heapq.heapify(prio_q)
    dist = {}
    prev = {}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            v = (r, c)
            start_val = 0 if v == (0, 0) else sys.maxsize
            q_items = [
                f"{r}-{c}-U-0", f"{r}-{c}-U-1", f"{r}-{c}-U-2", f"{r}-{c}-U-3",
                f"{r}-{c}-D-0", f"{r}-{c}-D-1", f"{r}-{c}-D-2", f"{r}-{c}-D-3",
                f"{r}-{c}-L-0", f"{r}-{c}-L-1", f"{r}-{c}-L-2", f"{r}-{c}-L-3",
                f"{r}-{c}-R-0", f"{r}-{c}-R-1", f"{r}-{c}-R-2", f"{r}-{c}-R-3",
            ]
            q.extend(q_items)

            for q_item in q_items:
                heapq.heappush(prio_q, HeapItem(q_item, start_val, False))
            dist[v] = {
                "U": {0: start_val, 1: start_val, 2: start_val, 3: start_val},
                "D": {0: start_val, 1: start_val, 2: start_val, 3: start_val},
                "L": {0: start_val, 1: start_val, 2: start_val, 3: start_val},
                "R": {0: start_val, 1: start_val, 2: start_val, 3: start_val}
            }
            prev[v] = {
                "U": {0: None, 1: None, 2: None, 3: None},
                "D": {0: None, 1: None, 2: None, 3: None},
                "L": {0: None, 1: None, 2: None, 3: None},
                "R": {0: None, 1: None, 2: None, 3: None}
            }
    return q, prio_q, dist, prev


def main():
    start = time.time()
    grid = []
    with open("sample_input.txt") as f:
        for line in f.readlines():
            if not line:
                continue
            grid.append([int(v) for v in list(line.strip())])
    cost = djikstra(grid)
    print(cost)
    print(f"Solved puzzle in {time.time() - start} seconds")


if __name__ == '__main__':
    main()
