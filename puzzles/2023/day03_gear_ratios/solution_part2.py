import re
from collections import namedtuple
from functools import reduce
from typing import List, Tuple, Dict, Set

Adjacency = namedtuple("Adjacency", ["gear_coords", "part_num"])


def adjacent_gears(lines, x, y) -> List[Tuple[int, int]]:
    """
    Determine coordinates of adjacent gears to this number.

    :param lines: The 2D array of lines.
    :param x: X coordinate of current location
    :param y: Y coordinate of current location
    :return: A list of tuples representing coordinates of gears ([y coord], [x coord])
    """
    adjacencies = []
    if y - 1 >= 0:
        # Look at row above
        if x - 1 >= 0 and lines[y - 1][x - 1] == "*":
            adjacencies.append((y - 1, x - 1))
        elif lines[y - 1][x] == "*":
            adjacencies.append((y - 1, x))
        elif x + 1 <= len(lines[y]) - 1 and lines[y - 1][x + 1] == "*":
            adjacencies.append((y - 1, x + 1))
    if y + 1 <= len(lines) - 1:
        # Look at row below
        if x - 1 >= 0 and lines[y + 1][x - 1] == "*":
            adjacencies.append((y + 1, x - 1))
        elif lines[y + 1][x] == "*":
            adjacencies.append((y + 1, x))
        elif x + 1 <= len(lines[y]) - 1 and lines[y + 1][x + 1] == "*":
            adjacencies.append((y + 1, x + 1))

    if x - 1 >= 0 and lines[y][x - 1] == "*":
        # Look to left
        adjacencies.append((y, x - 1))
    if x + 1 <= len(lines[y]) - 1 and lines[y][x + 1] == "*":
        adjacencies.append((y, x + 1))
    return adjacencies


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

        # We are going to attack this one by maintaining and adjacency list for the gears.
        # Our "gear_ratios" dictionary will have key = gear ratio tuple, val = Set of part numbers
        # This time, as we go through the schematic and encounter numbers, we no longer care
        # about "symbols", as we did in part 1.  Instead, we're just looking for gears ("*").
        # The "adjacent_gears" function will find any gears adjacent to the current char being
        # processed, and we will keep them in a list.
        # When we are done processing the current number, we'll add that number to the adjacency
        # list for each gear we encountered.
        gear_ratios: Dict[Tuple[int, int], Set[int]] = {}
        for y in range(len(lines)):
            line = lines[y]
            curr_num = None
            gear_adjacencies = []
            for x in range(len(line)):
                char = line[x]
                if re.match("\d", char):
                    # Current char is a number
                    if not curr_num:
                        curr_num = char
                    else:
                        curr_num += char
                    gear_adjacencies.extend(adjacent_gears(lines, x, y))
                    if x == len(line) - 1 and curr_num:
                        for g in gear_adjacencies:
                            if g in gear_ratios:
                                gear_ratios[g].add(int(curr_num))
                        gear_adjacencies = []
                elif curr_num is not None:
                    # Current char is not a number, but we were previously processing a number
                    # Do some cleanup by adding this number to the adjacency list for any gears
                    # that were encountered
                    if gear_adjacencies:
                        for g in gear_adjacencies:
                            if g in gear_ratios:
                                gear_ratios[g].add(int(curr_num))
                            else:
                                gear_ratios[g] = {int(curr_num)}
                    curr_num = None
                    gear_adjacencies = []

        gear_ratio_sum = 0
        for gear_coords, part_nums in gear_ratios.items():
            if len(part_nums) != 2:
                continue
            gear_ratio_sum += reduce(lambda x, y: x * y, part_nums)
        print(gear_ratio_sum)


if __name__ == '__main__':
    main()
