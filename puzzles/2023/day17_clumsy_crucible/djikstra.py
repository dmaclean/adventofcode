import dataclasses
import heapq
import logging
import math
import sys
from heapq import heapify
from typing import Tuple, List


@dataclasses.dataclass
class Path:
    nodes: List[Tuple[int, int]]
    direction: str
    steps: int
    heat_loss: int

    def clone(self) -> "Path":
        return Path([n for n in self.nodes], self.direction, self.steps, self.heat_loss)

    def determine_heat_loss(self, grid) -> int:
        return sum([grid[r][c] for r, c in self.nodes])

    def take_step(self, grid, dir_of_dest: str, dest: Tuple[int, int]) -> None:
        if dir_of_dest == self.direction:
            self.steps += 1
        else:
            self.steps = 1
            self.direction = dir_of_dest
        self.nodes.append(dest)
        self.heat_loss += grid[dest[0]][dest[1]]

    def __lt__(self, other):
        if not isinstance(other, Path):
            return -1


@dataclasses.dataclass
class HeapItem:
    p: Path
    dist: float

    def __lt__(self, other):
        return self.dist < other.dist


def can_move(grid: List[List[Tuple[int, int]]],
             path: Path,
             curr: Tuple[int, int],
             dest: Tuple[int, int],
             dir_of_dest: str) -> bool:
    # if dest in path.nodes:
    #     return False
    if dir_of_dest == path.direction and path.steps == 3:
        logging.debug(f"Cannot move: Already moved three steps to {dir_of_dest}.")
        return False
    if (dir_of_dest == "U" and curr[0] == 0) or \
            (dir_of_dest == "L" and curr[1] == 0) or \
            (dir_of_dest == "D" and curr[0] == len(grid) - 1) or \
            (dir_of_dest == "R" and curr[1] == len(grid[0]) - 1):
        logging.debug(f"Cannot move: Going to move off map at {curr}.")
        return False
    return True


def djikstra(grid):
    shortest = {}
    end = (len(grid) - 1, len(grid[0]) - 1)
    q = [HeapItem(Path([], "R", 0, 0), 0)]
    heapify(q)
    best_heat_loss = sys.maxsize
    while q:
        if len(q) % 10000:
            print(f"Queue size: {len(q)}")
        p = heapq.heappop(q).p
        curr = (0, 0) if not p.nodes else p.nodes[-1]
        r = curr[0]
        c = curr[1]

        try_to_move(curr, (r, c + 1), "R", grid, p, q, shortest, end, best_heat_loss)
        try_to_move(curr, (r + 1, c), "D", grid, p, q, shortest, end, best_heat_loss)
        try_to_move(curr, (r - 1, c), "U", grid, p, q, shortest, end, best_heat_loss)
        try_to_move(curr, (r, c - 1), "L", grid, p, q, shortest, end, best_heat_loss)

    return shortest


def try_to_move(curr, dest, dir_of_dest, grid, p, q, shortest, end, best_heat_loss):
    if curr == dest:
        raise Exception("Current location is same as destination!")
    r = dest[0]
    c = dest[1]
    if can_move(grid, p, curr, dest, dir_of_dest):
        # Check if moving here would represent the new shortest path
        heat_loss = p.heat_loss + grid[r][c]
        if heat_loss >= best_heat_loss:
            return

        # q.insert(0, clone)
        if dest not in shortest or shortest[dest] > heat_loss:
            shortest[dest] = heat_loss
            if dest == end and heat_loss < best_heat_loss:
                best_heat_loss = heat_loss
            clone = p.clone()
            clone.take_step(grid, dir_of_dest, dest)
            dist = math.sqrt((r - end[0]) ** 2 + (c - end[1]) ** 2)
            heapq.heappush(q, HeapItem(clone, dist))
            print(f"Found new shortest path ({heat_loss}) to {dest}: {clone.nodes}")


def main():
    grid = []
    with open("sample_input.txt") as f:
        for line in f.readlines():
            if not line:
                continue
            grid.append([int(v) for v in list(line.strip())])

    shortest = djikstra(grid)
    end = (len(grid) - 1, len(grid[0]) - 1)
    print(shortest[end])


if __name__ == '__main__':
    main()
