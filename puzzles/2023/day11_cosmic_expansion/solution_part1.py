from functools import reduce
from typing import List

from day11utils import find_galaxies, galaxy_dist


def main():
    with open("input.txt") as f:
        space = []
        for line in f.readlines():
            space.append(list(line.strip()))

        expand_space(space)
        galaxies = find_galaxies(space)
        idx = 1
        total = 0
        for i in range(len(galaxies) - 1):
            for j in range(i + 1, len(galaxies)):
                dist = galaxy_dist(galaxies[i + 1], galaxies[j + 1])
                total += dist
                print(f"{idx} - ({i + 1}, {j + 1}) - {dist}")
                idx += 1
        print(total)


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


def print_space(space):
    for row in space:
        print(row)


if __name__ == '__main__':
    main()
