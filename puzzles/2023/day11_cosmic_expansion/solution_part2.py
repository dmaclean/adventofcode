from functools import reduce
from typing import List

from day11utils import find_galaxies, galaxy_dist


def main():
    with open("input.txt") as f:
        space = []
        for line in f.readlines():
            space.append(list(line.strip()))

        galaxies = find_galaxies(space)
        expand_space(space, galaxies, 1_000_000)
        idx = 1
        total = 0
        for i in range(len(galaxies) - 1):
            for j in range(i + 1, len(galaxies)):
                dist = galaxy_dist(galaxies[i + 1], galaxies[j + 1])
                total += dist
                idx += 1
        print(total)


def expand_space(space: List[List[str]], galaxies, size=1_000_000):
    """
    Expand space and recalculate the coordinates of the galaxies.

    Despite the fact that space is expanding, we don't actually need to modify the grid at all.
    Instead, we just need to increase the coordinates for galaxies that would be affected by a
    given row or column pre-expansion.  Since we're only calculating a Manhattan distance, we
    just need to subtract coordinates instead of actually searching grid space via BFS or similar.
    """
    # Expand columns
    indexes = []
    # We are reversing the order of evaluation so galaxies further down aren't affected
    # by expansion at lower-index rows and columns.
    # For example, assume a galaxy is at row=7, col=1, and that there are empty rows at 1, 5, and 8.
    # The galaxy should not be affected by expansion at row 8.  However, if we start processing at row 0
    # then it would push the galaxy to row = 9 (assuming we're only doubling).  Then, by the time we
    # process row 8, it looks like the galaxy should be pushed out more.
    # By starting at the end, we would only move the galaxy twice, with rows 1 and 5.
    for c in sorted(range(len(space[0])), reverse=True):
        empty = reduce(lambda x, y: x and y, [v == "." for v in [space[idx][c] for idx in range(len(space))]])
        if empty:
            indexes.append(c)
            for k, v in galaxies.items():
                if v[1] > c:
                    galaxies[k] = (v[0], v[1] + (size - 1))

    # Expand rows
    indexes = []
    for r in sorted(range(len(space)), reverse=True):
        row = space[r]
        empty = reduce(lambda x, y: x and y, [c == "." for c in row])
        if empty:
            indexes.append(r)
            for k, v in galaxies.items():
                if v[0] > r:
                    galaxies[k] = (v[0] + (size - 1), v[1])


def print_space(space):
    for row in space:
        print(row)


if __name__ == '__main__':
    main()
