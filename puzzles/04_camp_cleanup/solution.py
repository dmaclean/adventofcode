from typing import Set


def range_as_set(r: str) -> Set[int]:
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
        if range1.issubset(range2) or range2.issubset(range1):
            fully_contained += 1

    print(fully_contained)
