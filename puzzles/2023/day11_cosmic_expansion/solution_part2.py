from typing import Tuple

from day11utils import expand_space, find_galaxies


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


def galaxy_dist(g1: Tuple[int, int], g2: Tuple[int, int]) -> int:
    x = abs(g1[1] - g2[1])
    y = abs(g1[0] - g2[0])
    return x + y


def print_space(space):
    for row in space:
        print(row)


if __name__ == '__main__':
    main()
