import dataclasses
from typing import Tuple, Set, List


@dataclasses.dataclass
class Path:
    visited_blocks: Set[Tuple[int, int]]
    curr_position: Tuple[int, int]
    direction: str
    consecutive_moves_in_dir: int

    def duplicate(self):
        return Path(
            {b for b in self.visited_blocks},
            self.curr_position,
            self.direction,
            self.consecutive_moves_in_dir
        )

    def can_move(self, grid, dest: Tuple[int, int], direction: str) -> bool:
        if dest in self.visited_blocks:
            return False
        if direction == self.direction and self.consecutive_moves_in_dir == 3:
            return False
        if (direction == "U" and self.curr_position[0] == 0) or \
                (direction == "L" and self.curr_position[1] == 0) or \
                (direction == "D" and self.curr_position[0] >= len(grid) - 1) or \
                (direction == "R" and self.curr_position[1] >= len(grid[0]) - 1):
            return False

        return True

    def determine_heat_loss(self, grid) -> int:
        return sum([grid[v[0]][v[1]] for v in self.visited_blocks])

    def __eq__(self, __o):
        if not isinstance(__o, Path):
            return False
        return self.curr_position == __o.curr_position and \
            self.direction == __o.direction and \
            self.consecutive_moves_in_dir == __o.consecutive_moves_in_dir and \
            self.visited_blocks == __o.visited_blocks


def main():
    grid = []
    smallest_heat_loss = 99999999999
    with open("sample_input.txt") as f:
        for line in f.readlines():
            grid.append([int(v) for v in list(line.strip())])

    start = (0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)
    paths = [
        Path(set(), (0, 0), "R", 0),
        Path(set(), (0, 0), "D", 0)
    ]

    while paths:
        if len(paths) % 1000 == 0:
            print(f"Now have {len(paths)} paths")
        p = paths.pop()
        heat_loss = p.determine_heat_loss(grid)
        if p.curr_position == end:
            if heat_loss < smallest_heat_loss:
                smallest_heat_loss = heat_loss
                print(f"New smallest heat loss of {smallest_heat_loss}")
            continue
        if heat_loss >= smallest_heat_loss:
            continue

        r = p.curr_position[0]
        c = p.curr_position[1]

        # Try to move the crucible in each direction
        if p.can_move(grid, (r - 1, c), "U"):
            # MOVE UP
            add_path(paths, p, (r - 1, c), "U")
        if p.can_move(grid, (r, c - 1), "L"):
            # MOVE LEFT
            add_path(paths, p, (r, c - 1), "L")
        if p.can_move(grid, (r + 1, c), "D"):
            # MOVE DOWN
            add_path(paths, p, (r + 1, c), "D")
        if p.can_move(grid, (r, c + 1), "R"):
            # MOVE RIGHT
            add_path(paths, p, (r, c + 1), "R")


def add_path(paths: List[Path], curr_path: Path, dest_coords: Tuple[int, int], direction: str) -> None:
    new_path = curr_path.duplicate()
    new_path.visited_blocks.add(dest_coords)
    new_path.curr_position = dest_coords
    if new_path.direction == direction:
        new_path.consecutive_moves_in_dir += 1
    else:
        new_path.direction = direction
        new_path.consecutive_moves_in_dir = 1

    if new_path in paths:
        return
    paths.append(new_path)


if __name__ == '__main__':
    main()
