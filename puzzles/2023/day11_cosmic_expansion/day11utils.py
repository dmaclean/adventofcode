from typing import Dict, Tuple, List
from functools import reduce


def find_galaxies(space) -> Dict[int, Tuple[int, int]]:
    galaxies = {}
    count = 1
    for r in range(len(space)):
        for c in range(len(space[r])):
            if space[r][c] == "#":
                galaxies[count] = (r, c)
                count += 1

    return galaxies


def expand_space(space: List[List[str]]) -> None:
    # Expand rows
    indexes = []
    for r in range(len(space)):
        row = space[r]
        empty = reduce(lambda x, y: x and y, [c == "." for c in row])
        if empty:
            indexes.append(r)

    for i in sorted(indexes, reverse=True):
        space.insert(i, ["." for _ in range(len(space[0]))])

    # Expand columns
    indexes = []
    for c in range(len(space[0])):
        empty = reduce(lambda x, y: x and y, [v == "." for v in [space[idx][c] for idx in range(len(space))]])
        if empty:
            indexes.append(c)

    for i in sorted(indexes, reverse=True):
        for r in range(len(space)):
            space[r].insert(i, ".")
