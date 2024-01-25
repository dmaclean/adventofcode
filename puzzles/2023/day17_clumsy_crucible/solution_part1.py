import dataclasses
from typing import Tuple, List


@dataclasses.dataclass
class Path:
    visited_blocks: List[Tuple[int, int]]
    curr_position: Tuple[int, int]
    direction: str
    consecutive_moves_in_dir: int

    def duplicate(self):
        return Path(
            [b for b in self.visited_blocks],
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


memo = {}


def grid_nav(grid, r, c, path: Path, end: Tuple[int, int]):
    if r == end[0] and c == end[1]:
        return grid[r][c]

    # Try to move the crucible in each direction
    up_cost = left_cost = down_cost = right_cost = None
    if path.can_move(grid, (r - 1, c), "U"):
        # MOVE UP
        pre_dir = path.direction
        pre_steps = path.consecutive_moves_in_dir
        path.visited_blocks.append((r - 1, c))
        if path.direction == "U":
            path.consecutive_moves_in_dir += 1
        else:
            path.consecutive_moves_in_dir = 1
        up_cost = grid_nav(grid, r - 1, c, path, end) + grid[r][c]
        memo[f"{r}-{c}-U-{path.consecutive_moves_in_dir}"] = up_cost
        path.visited_blocks.pop()
        path.direction = pre_dir
        path.consecutive_moves_in_dir = pre_steps
    if path.can_move(grid, (r, c - 1), "L"):
        # MOVE LEFT
        pre_dir = path.direction
        pre_steps = path.consecutive_moves_in_dir
        path.visited_blocks.append((r, c - 1))
        if path.direction == "L":
            path.consecutive_moves_in_dir += 1
        else:
            path.consecutive_moves_in_dir = 1
        left_cost = grid_nav(grid, r, c - 1, path, end) + grid[r][c]
        memo[f"{r}-{c}-L-{path.consecutive_moves_in_dir}"] = left_cost
        path.visited_blocks.pop()
        path.direction = pre_dir
        path.consecutive_moves_in_dir = pre_steps
    if path.can_move(grid, (r + 1, c), "D"):
        # MOVE DOWN
        pre_dir = path.direction
        pre_steps = path.consecutive_moves_in_dir
        path.visited_blocks.append((r + 1, c))
        if path.direction == "D":
            path.consecutive_moves_in_dir += 1
        else:
            path.consecutive_moves_in_dir = 1
        down_cost = grid_nav(grid, r + 1, c, path, end) + grid[r][c]
        memo[f"{r}-{c}-D-{path.consecutive_moves_in_dir}"] = down_cost
        path.visited_blocks.pop()
        path.direction = pre_dir
        path.consecutive_moves_in_dir = pre_steps
    if path.can_move(grid, (r, c + 1), "R"):
        # MOVE RIGHT
        pre_dir = path.direction
        pre_steps = path.consecutive_moves_in_dir
        path.visited_blocks.append((r, c + 1))
        if path.direction == "R":
            path.consecutive_moves_in_dir += 1
        else:
            path.consecutive_moves_in_dir = 1
        right_cost = grid_nav(grid, r, c + 1, path, end) + grid[r][c]
        memo[f"{r}-{c}-R-{path.consecutive_moves_in_dir}"] = right_cost
        path.visited_blocks.pop()
        path.direction = pre_dir
        path.consecutive_moves_in_dir = pre_steps

    return min([v for v in [up_cost, down_cost, left_cost, right_cost] if v is not None])


def main():
    grid = []
    smallest_heat_loss = 99999999999
    with open("sample_input.txt") as f:
        for line in f.readlines():
            grid.append([int(v) for v in list(line.strip())])

    start = (0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)
    path = Path([], (0, 0), "R", 0)
    cost = grid_nav(grid, 0, 0, path, end)


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
