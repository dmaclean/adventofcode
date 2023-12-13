import dataclasses
from typing import List, Tuple, Set

PIPE_CHARS = {"|", "-", "J", "L", "F", "7"}


@dataclasses.dataclass
class Path:
    curr: Tuple[int, int]
    last: Tuple[int, int]
    trail: Set[Tuple[int, int]]
    steps: int


def main():
    """
    This one was not fun.

    The approach I ended up taking was to:
    1. Find the path
    2. Mark all non-path original tiles as '%'.
    3. Expand the maze horizontally and vertically (see expand_maze()) to deal with the
       annoyance of being able to "squeeze between pipes".  Pipes are extended appropriately
       with either a "-" or "|", and any new blank space created is marked as "*".
    4. Perform a BFS along the outside to identify outer tiles.
    5. Anything that is 1) not a pipe, 2) not an outer tile (via 4), and not marked as "*" is considered
       an original inner tile.

    Phew.
    """
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
        paths.append(Path((sr - 1, sc), start_coords, {(sr, sc), (sr - 1, sc)}, 1))
    if sr + 1 < len(maze) and maze[sr + 1][sc] in {"|", "L", "J"}:
        # Pipe is coming from below
        paths.append(Path((sr + 1, sc), start_coords, {(sr, sc), (sr + 1, sc)}, 1))
    if sc - 1 >= 0 and maze[sr][sc - 1] in {"-", "F", "L"}:
        # Pipe is coming from left side
        paths.append(Path((sr, sc - 1), start_coords, {(sr, sc), (sr, sc - 1)}, 1))
    if sc + 1 < len(maze[sr]) and maze[sr][sc + 1] in {"-", "J", "7"}:
        # Pipe is coming from right side
        paths.append(Path((sr, sc + 1), start_coords, {(sr, sc), (sr, sc + 1)}, 1))

    while not paths_at_same_coords(paths):
        for p in paths:
            advance_path(p, maze)

    path_coords = set()
    for p in paths:
        for t in p.trail:
            path_coords.add(t)
    print_path(maze, path_coords)

    reformat_maze(maze, path_coords)
    expand_maze(maze)
    visited = find_outer_tiles(maze)
    inner = find_inner_tiles(maze, visited)
    print(inner)


def reformat_maze(maze, path_coords: Set[Tuple[int, int]]):
    """
    After finding the path, for simplicity we are going to mark every other tile not in the path
    with a '%' symbol.  This will let us know what the original tiles were.
    :param maze: The maze being processed.
    :param path_coords: Set of coordinates representing the path.
    """
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "S":
                substitute_s(r, c, maze)
            elif (r, c) not in path_coords:
                maze[r][c] = "%"


def substitute_s(r, c, maze) -> None:
    """
    Convert the S tile into the correct pipe symbol given its surroundings.
    :param r: The row coordinate
    :param c: The column coordinate
    :param maze: The maze
    """
    if r - 1 >= 0 and r + 1 < len(maze) and \
            maze[r - 1][c] in {"|", "7", "F"} and \
            maze[r + 1][c] in {"|", "L", "J"}:
        # Vertical connector
        maze[r][c] = "|"
    elif c - 1 >= 0 and c + 1 < len(maze[r]) and \
            maze[r][c - 1] in {"-", "F", "L"} and \
            maze[r][c + 1] in {"-", "7", "J"}:
        # Horizontal connector
        maze[r][c] = "-"
    elif r - 1 >= 0 and c + 1 < len(maze[r]) and \
            maze[r - 1][c] in {"|", "7", "F"} and \
            maze[r][c + 1] in {"-", "7", "J"}:
        # North-east connector
        maze[r][c] = "L"
    elif r - 1 >= 0 and c - 1 >= 0 and maze[r - 1][c] in {"|", "7", "F"} and maze[r][c - 1] in {"-", "F", "L"}:
        # North-west connector
        maze[r][c] = "J"
    elif r + 1 < len(maze) and c - 1 >= 0 and \
            maze[r + 1][c] in {"|", "L", "J"} and \
            maze[r][c - 1] in {"-", "F", "L"}:
        # South-west connector
        maze[r][c] = "7"
    else:
        # South-east connector
        maze[r][c] = "F"


def expand_maze(maze: List[List[str]]):
    # Vertical expansion
    idx = 0
    while idx < len(maze) - 1:
        new_row = []
        for c_idx in range(len(maze[idx])):
            top = maze[idx][c_idx]
            bottom = maze[idx + 1][c_idx]
            if top in {"|", "7", "F"} and bottom in {"|", "L", "J"}:
                new_row.append("|")
            else:
                new_row.append("*")
        maze.insert(idx + 1, new_row)
        idx += 2

    # Horizontal expansion
    for r in range(len(maze)):
        idx = 0
        while idx < len(maze[0]) - 1:
            left = maze[r][idx]
            right = maze[r][idx + 1]
            if left in {"-", "F", "L"} and right in {"-", "J", "7"}:
                maze[r].insert(idx + 1, "-")
            else:
                maze[r].insert(idx + 1, "*")
            idx += 2


def print_path(maze, path_coords):
    for r in range(len(maze)):
        row_str = ""
        for c in range(len(maze[r])):
            if (r, c) in path_coords:
                row_str += "#"
            else:
                row_str += maze[r][c]
        print(row_str)


def is_adjacent(p1, p2) -> bool:
    return (p1[0] == p2[0] and abs(p1[1] - p2[0]) == 1) or \
        (abs(p1[0] - p2[0]) == 1 and p1[1] == p2[0])


def find_inner_tiles(maze, outer_tiles: Set[Tuple[int, int]]):
    """

    :param maze:
    :param outer_tiles:
    :return:
    """
    inner = 0
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if (r, c) in outer_tiles or maze[r][c] in PIPE_CHARS or maze[r][c] == "*":
                continue
            inner += 1
    return inner


def find_outer_tiles(maze) -> Set[Tuple[int, int]]:
    """
    Perform a breadth-first-search of the maze to determine the outer tiles.

    We are going to walk along the outside of the maze and queue up any tile that is not a pipe
    as a starting point.  This is because it is not possible for an outer tile to be part of
    the inside of the loop, and if the loop runs along the outer edge then if we only start
    at a single point, we'd be closed off from some outer section (which would then be counted
    as inner tiles).
    :param maze: The maze being processed
    :return: A set of tuples representing coordinates for outer tiles.
    """
    visited = set()
    queue = []
    for r in range(len(maze)):
        if maze[r][0] not in PIPE_CHARS:
            queue.append((r, 0))
        if maze[r][len(maze[0]) - 1] not in PIPE_CHARS:
            queue.append((r, len(maze[0]) - 1))
    for c in range(len(maze[0])):
        if maze[0][c] not in PIPE_CHARS:
            queue.append((0, c))
        if maze[len(maze) - 1][c] not in PIPE_CHARS:
            queue.append((len(maze) - 1, c))

    while queue:
        location = queue.pop()
        r = location[0]
        c = location[1]
        north = (r - 1, c)
        south = (r + 1, c)
        east = (r, c + 1)
        west = (r, c - 1)
        if r - 1 >= 0 and maze[north[0]][north[1]] not in PIPE_CHARS and north not in visited:
            visited.add(north)
            queue.append(north)
        if r + 1 < len(maze) and maze[south[0]][south[1]] not in PIPE_CHARS and south not in visited:
            visited.add(south)
            queue.append(south)
        if c - 1 >= 0 and maze[west[0]][west[1]] not in PIPE_CHARS and west not in visited:
            visited.add(west)
            queue.append(west)
        if c + 1 < len(maze[r]) and maze[east[0]][east[1]] not in PIPE_CHARS and east not in visited:
            visited.add(east)
            queue.append(east)
    return visited


def can_move(source, dest, direction) -> bool:
    """
    Determine if the pipe in the specified direction is compatible with the pipe we are currently at.
    :param source: The value of the current tile.
    :param dest: The value of the tile we are trying to go to.
    :param direction: The direction we are going.
    :return: True, if the pipe is compatible. False, otherwise.
    """
    return (source in {"|", "L", "J"} and dest in {"|", "7", "F"} and direction == "N") or \
        (source in {"|", "7", "F"} and dest in {"|", "L", "J"} and direction == "S") or \
        (source in {"-", "L", "F"} and dest in {"7", "J", "-"} and direction == "E") or \
        (source in {"-", "7", "J"} and dest in {"L", "F", "-"} and direction == "W")


def advance_path(path: Path, maze: List[List[str]]) -> None:
    """
    Move forward in the path by following the pipe.
    :param path: The current path being evaluated
    :param maze: The maze being processed
    """
    r = path.curr[0]
    c = path.curr[1]
    last_r = path.last[0]
    last_c = path.last[1]
    source = maze[r][c]
    if r - 1 >= 0 and last_r != r - 1 and can_move(source, maze[r - 1][c], "N"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r - 1, c)
        path.trail.add(path.curr)
    elif r + 1 < len(maze) and last_r != r + 1 and can_move(source, maze[r + 1][c], "S"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r + 1, c)
        path.trail.add(path.curr)
    elif c - 1 >= 0 and last_c != c - 1 and can_move(source, maze[r][c - 1], "W"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r, c - 1)
        path.trail.add(path.curr)
    elif c + 1 < len(maze[r]) and last_c != c + 1 and can_move(source, maze[r][c + 1], "E"):
        path.steps += 1
        path.last = path.curr
        path.curr = (r, c + 1)
        path.trail.add(path.curr)
    else:
        print(f"We are stuck")


def paths_at_same_coords(paths: List[Path]) -> bool:
    return len(set([p.curr for p in paths])) == 1 or paths[0].last == paths[1].curr


def find_start(maze: List[List[str]]) -> Tuple[int, int]:
    """
    Finds the tile marked "S".
    :param maze: The maze being processed
    :return: A tuple representing the row and column that S is located at.
    """
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == "S":
                return r, c


if __name__ == '__main__':
    main()
