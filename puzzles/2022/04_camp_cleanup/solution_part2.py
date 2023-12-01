from typing import Set


def range_as_set(r: str) -> Set[int]:
    """
    Convert a string of the format XX-YY, where XX and YY are numbers, into a set containing all number
    in that range (inclusive)
    :param r: The string representing the range
    :return: A set of integers representing all numbers in the range
    """
    parts = r.split('-')
    start = int(parts[0])
    end = int(parts[1]) + 1
    return {x for x in range(start, end)}


with open('input.txt') as f:
    fully_contained = 0
    for line in f.readlines():
        parts = line.strip().split(',')
        range1 = range_as_set(parts[0])
        range2 = range_as_set(parts[1])
        intersection = range1.intersection(range2)
        if len(intersection) > 0:
            fully_contained += 1

    print(fully_contained)
