from typing import Dict, Tuple


def find_galaxies(space) -> Dict[int, Tuple[int, int]]:
    galaxies = {}
    count = 1
    for r in range(len(space)):
        for c in range(len(space[r])):
            if space[r][c] == "#":
                galaxies[count] = (r, c)
                count += 1

    return galaxies


def galaxy_dist(g1: Tuple[int, int], g2: Tuple[int, int]) -> int:
    x = abs(g1[1] - g2[1])
    y = abs(g1[0] - g2[0])
    return x + y
