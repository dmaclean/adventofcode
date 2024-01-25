from typing import Tuple, List

memo = {}
min_paths = {}


def determine_heat_loss(grid, path: List[Tuple[int, int]]) -> int:
    return sum([grid[v[0]][v[1]] for v in path])


def can_move(grid, curr, dest, path, curr_dir, dir_of_dest, curr_steps_in_dir):
    if dest in path:
        return False
    if dir_of_dest == curr_dir and curr_steps_in_dir == 3:
        return False
    if (dir_of_dest == "U" and curr[0] == 0) or \
            (dir_of_dest == "L" and curr[1] == 0) or \
            (dir_of_dest == "D" and curr[0] >= len(grid) - 1) or \
            (dir_of_dest == "R" and curr[1] >= len(grid[0]) - 1):
        return False

    return True


def grid_nav(grid, curr, path, end: Tuple[int, int], curr_steps_in_dir: int, direction: str):
    # print(f"Visited {curr} in direction {direction} with consecutive steps {curr_steps_in_dir}")
    r = curr[0]
    c = curr[1]
    if curr == end:
        # We have reached the end.  Just return the heat loss for the end location.
        print(f"Reached end at {curr}.  Heat loss is {grid[r][c]}")
        return grid[r][c]

    # Try to move the crucible in each direction
    min_cost = 999999
    min_cost_dir = None
    up_cost = left_cost = down_cost = right_cost = None
    dest = (r - 1, c)
    if can_move(grid, curr, dest, path, direction, "U", curr_steps_in_dir):
        # MOVE UP
        memo_key = f"{r}-{c}-{direction}-U-{curr_steps_in_dir}"
        if memo_key in memo:
            # print(f"Found memo for {memo_key}")
            up_cost = memo[memo_key]
            if up_cost and up_cost < min_cost:
                min_cost = up_cost
                min_cost_dir = "U"
        else:
            path.append(dest)
            steps_in_dir = 1 if direction != "U" else curr_steps_in_dir + 1
            up_cost = grid_nav(grid, dest, path, end, steps_in_dir, "U")
            if up_cost and up_cost < min_cost:
                min_cost = up_cost
                min_cost_dir = "U"
            memo[memo_key] = up_cost
            path.pop()
    dest = (r, c - 1)
    if can_move(grid, curr, dest, path, direction, "L", curr_steps_in_dir):
        # MOVE LEFT
        memo_key = f"{r}-{c}-{direction}-L-{curr_steps_in_dir}"
        if memo_key in memo:
            # print(f"Found memo for {memo_key}")
            left_cost = memo[memo_key]
            if left_cost and left_cost < min_cost:
                min_cost = left_cost
                min_cost_dir = "L"
        else:
            path.append(dest)
            steps_in_dir = 1 if direction != "L" else curr_steps_in_dir + 1
            left_cost = grid_nav(grid, dest, path, end, steps_in_dir, "L")
            if left_cost and left_cost < min_cost:
                min_cost = left_cost
                min_cost_dir = "L"
            memo[memo_key] = left_cost
            path.pop()
    dest = (r + 1, c)
    if can_move(grid, curr, dest, path, direction, "D", curr_steps_in_dir):
        # MOVE DOWN
        memo_key = f"{r}-{c}-{direction}-D-{curr_steps_in_dir}"
        if memo_key in memo:
            # print(f"Found memo for {memo_key}")
            down_cost = memo[memo_key]
            if down_cost and down_cost < min_cost:
                min_cost = down_cost
                min_cost_dir = "D"
        else:
            path.append(dest)
            steps_in_dir = 1 if direction != "D" else curr_steps_in_dir + 1
            down_cost = grid_nav(grid, dest, path, end, steps_in_dir, "D")
            if down_cost and down_cost < min_cost:
                min_cost = down_cost
                min_cost_dir = "D"
            memo[memo_key] = down_cost
            path.pop()
    dest = (r, c + 1)
    if can_move(grid, curr, dest, path, direction, "R", curr_steps_in_dir):
        # MOVE RIGHT
        memo_key = f"{r}-{c}-{direction}-R-{curr_steps_in_dir}"
        if memo_key in memo:
            # print(f"Found memo for {memo_key}")
            right_cost = memo[memo_key]
            if right_cost and right_cost < min_cost:
                min_cost = right_cost
                min_cost_dir = "R"
        else:
            path.append(dest)
            steps_in_dir = 1 if direction != "R" else curr_steps_in_dir + 1
            right_cost = grid_nav(grid, dest, path, end, steps_in_dir, "R")
            if right_cost and right_cost < min_cost:
                min_cost = right_cost
                min_cost_dir = "R"
            memo[memo_key] = right_cost
            # print(f"Persisted {memo_key} with {right_cost}")
            path.pop()

    if min_cost < 999999:
        min_paths[curr] = min_cost_dir
        print(f"Min cost from {curr}|{curr_steps_in_dir}|{direction} is {min_cost + grid[r][c]}")
        return min_cost + grid[r][c]
    return None


def print_optimal_path(end: Tuple[int, int]):
    r = 0
    c = 0
    while (r, c) != end:
        d = min_paths[(r, c)]
        print(f"({r}, {c}) - {d}")
        if d == "U":
            r -= 1
        elif d == "D":
            r += 1
        elif d == "L":
            c -= 1
        elif d == "R":
            c += 1


def main():
    grid = []
    path = []
    with open("input.txt") as f:
        for line in f.readlines():
            grid.append([int(v) for v in list(line.strip())])

    start = (0, 0)
    end = (len(grid) - 1, len(grid[0]) - 1)
    cost = grid_nav(grid, start, path, end, 0, "R")
    print(cost - grid[0][0])


if __name__ == '__main__':
    main()
