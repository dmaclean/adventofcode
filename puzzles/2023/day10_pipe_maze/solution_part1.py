import dataclasses
from typing import List, Tuple


@dataclasses.dataclass
class Path:
    curr: Tuple[int, int]
    last: Tuple[int, int]
    steps: int


def main():
    maze = []
    with open("input.txt") as f:
        for line in f.readlines():
            maze.append(list(line.strip()))

    paths = []
    start_coords = find_start(maze)
    sr = start_coords[0]
    sc = start_coords[1]

    # Find two sides of start
    if sr - 1 >= 0 and maze[sr - 1][sc] in {"|", "7", "F"}:
        # Pipe is coming from above
        paths.append(Path((sr - 1, sc), start_coords, 1))
    if sr + 1 < len(maze) and maze[sr + 1][sc] in {"|", "L", "J"}:
        # Pipe is coming from below
        paths.append(Path((sr + 1, sc), start_coords, 1))
    if sc - 1 >= 0 and maze[sr][sc - 1] in {"-", "F", "L"}:
        # Pipe is coming from left side
        paths.append(Path((sr, sc - 1), start_coords, 1))
    if sc + 1 < len(maze[sr]) and maze[sr][sc + 1] in {"-", "J", "7"}:
        # Pipe is coming from right side
        paths.append(Path((sr, sc + 1), start_coords, 1))

    while not paths_at_same_coords(paths):
        for p in paths:
            advance_path(p, maze)
    print(max([p.steps for p in paths]))


def can_move(source, dest, direction) -> bool:
    return (source in {"|", "L", "J"} and dest in {"|", "7", "F"} and direction == "N") or \
        (source in {"|", "7", "F"} and dest in {"|", "L", "J"} and direction == "S") or \
        (source in {"-", "L", "F"} and dest in {"7", "J", "-"} and direction == "E") or \
        (source in {"-", "7", "J"} and dest in {"L", "F", "-"} and direction == "W")


def advance_path(path, maze) -> None:
    r = path.curr[0]
    c = path.curr[1]
    last_r = path.last[0]
    last_c = path.last[1]
    source = maze[r][c]
    if r - 1 >= 0 and last_r != r - 1 and can_move(source, maze[r - 1][c], "N"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r - 1, c)
    elif r + 1 < len(maze) and last_r != r + 1 and can_move(source, maze[r + 1][c], "S"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r + 1, c)
    elif c - 1 >= 0 and last_c != c - 1 and can_move(source, maze[r][c - 1], "W"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r, c - 1)
    elif c + 1 < len(maze[r]) and last_c != c + 1 and can_move(source, maze[r][c + 1], "E"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r, c + 1)
    else:
        print(f"We are stuck")


def paths_at_same_coords(paths: List[Path]) -> bool:
    return len(set([p.curr for p in paths])) == 1 or paths[0].last == paths[1].curr


def find_start(maze: List[List[str]]) -> Tuple[int, int]:
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "S":
                return r, c


if __name__ == '__main__':
    main()
