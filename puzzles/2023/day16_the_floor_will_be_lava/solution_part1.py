import dataclasses
from typing import List, Set, Tuple


@dataclasses.dataclass
class Tile:
    r: int
    c: int
    type: str
    energized: bool

    def __eq__(self, o):
        return self.r == o.r and self.c == o.c

    def __hash__(self):
        return hash(str(self.r) + "_" + str(self.c))

    def __str__(self):
        return f"({self.r},{self.c}) {self.type} ({self.energized})"


@dataclasses.dataclass
class Beam:
    r: int
    c: int
    direction: str
    deleted: bool

    def __str__(self):
        return f"({self.r},{self.c}) {self.direction}"


splitters_used = set()


def main():
    input = []
    with open("input.txt") as f:
        for line in f.readlines():
            input.append(list(line.strip()))

    grid = []
    not_energized = set()
    for r in range(len(input)):
        row = []
        for c in range(len(input[r])):
            t = Tile(r, c, input[r][c], False)
            row.append(t)
            not_energized.add((r, c))
        grid.append(row)

    beam = Beam(0, 0, "R", False)
    beams = [beam]
    stagnant = 0
    while beams:
        before_size = len(not_energized)
        move_beams(grid, beams, not_energized)
        after_size = len(not_energized)
        if before_size == after_size:
            stagnant += 1
        else:
            stagnant = 0
        if stagnant == 3:
            break
        print(f"Non-energized tiles: {len(not_energized)}, beams: {len(beams)}")
        # print_grid(grid)
        # time.sleep(3)

    print(count_energized(grid))


def print_grid(grid: List[List[Tile]]):
    for r in range(len(grid)):
        row = ""
        for c in range(len(grid[r])):
            if grid[r][c].type in {"\\", "/", "-", "|"} or not grid[r][c].energized:
                row += grid[r][c].type
            elif grid[r][c].energized:
                row += "#"
        print(row)
    print("\n\n")


def move_beams(grid: List[List[Tile]], beams: List[Beam], not_energized: Set[Tuple[int, int]]):
    to_delete = []
    for beam in beams:
        move_beam(grid, beams, beam, not_energized)
        if beam.deleted:
            to_delete.append(beam)

    while to_delete:
        beams.remove(to_delete.pop())


def move_beam(grid: List[List[Tile]], beams: List[Beam], beam: Beam, not_energized: Set[Tuple[int, int]]):
    tile = grid[beam.r][beam.c]
    tile.energized = True
    if (beam.r, beam.c) in not_energized:
        not_energized.remove((beam.r, beam.c))

    if tile.type == "|":
        if beam.direction in {"L", "R"}:
            if tile in splitters_used:
                beam.deleted = True
            else:
                beam.direction = "U"
                beams.append(Beam(beam.r, beam.c, "D", False))
                splitters_used.add(tile)
        elif beam.direction == "U":
            if can_move_up(beam):
                beam.r -= 1
            else:
                beam.deleted = True
        elif beam.direction == "D":
            if can_move_down(beam, grid):
                beam.r += 1
            else:
                beam.deleted = True

    elif tile.type == "-":
        if beam.direction in {"U", "D"}:
            if tile in splitters_used:
                beam.deleted = True
            else:
                beam.direction = "L"
                beams.append(Beam(beam.r, beam.c, "R", False))
                splitters_used.add(tile)
        elif beam.direction == "L":
            if can_move_left(beam):
                beam.c -= 1
            else:
                beam.deleted = True
        elif beam.direction == "R":
            if can_move_right(beam, grid):
                beam.c += 1
            else:
                beam.deleted = True
    elif tile.type == "\\":
        if beam.direction == "U":
            if can_move_left(beam):
                beam.c -= 1
                beam.direction = "L"
            else:
                beam.deleted = True
        elif beam.direction == "D":
            if can_move_right(beam, grid):
                beam.c += 1
                beam.direction = "R"
            else:
                beam.deleted = True
        elif beam.direction == "L":
            if can_move_up(beam):
                beam.r -= 1
                beam.direction = "U"
            else:
                beam.deleted = True
        elif beam.direction == "R":
            if can_move_down(beam, grid):
                beam.r += 1
                beam.direction = "D"
            else:
                beam.deleted = True
    elif tile.type == "/":
        if beam.direction == "U":
            if can_move_right(beam, grid):
                beam.c += 1
                beam.direction = "R"
            else:
                beam.deleted = True
        elif beam.direction == "D":
            if can_move_left(beam):
                beam.c -= 1
                beam.direction = "L"
            else:
                beam.deleted = True
        elif beam.direction == "L":
            if can_move_down(beam, grid):
                beam.r += 1
                beam.direction = "D"
            else:
                beam.deleted = True
        elif beam.direction == "R":
            if can_move_up(beam):
                beam.r -= 1
                beam.direction = "U"
            else:
                beam.deleted = True
    else:
        # empty space - try to continue on
        if can_move_up(beam) and beam.direction == "U":
            beam.r -= 1
        elif can_move_down(beam, grid) and beam.direction == "D":
            beam.r += 1
        elif can_move_left(beam) and beam.direction == "L":
            beam.c -= 1
        elif can_move_right(beam, grid) and beam.direction == "R":
            beam.c += 1
        else:
            beam.deleted = True


def can_move_up(beam):
    return beam.r - 1 >= 0


def can_move_down(beam, grid):
    return beam.r + 1 < len(grid)


def can_move_left(beam):
    return beam.c - 1 >= 0


def can_move_right(beam, grid):
    return beam.c + 1 < len(grid[beam.r])


def count_energized(grid):
    energized = 0
    for row in grid:
        energized += sum([1 for t in row if t.energized])
    return energized


if __name__ == '__main__':
    main()
