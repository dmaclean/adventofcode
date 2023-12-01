def priority(item: str) -> int:
    """
    Determine the priority of an item in the rucksack.

    For this, we will change the item letter to its ASCII integer representation, then normalize
    based on the range (97 - 122 for lowercase a-z, 65 - 90 for uppercase A-Z).

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

    :param item:    The item being evaluated.
    :return:        The integer priority of the item.
    """
    int_val = ord(item)
    if 97 <= int_val <= 122:
        # Lowercase
        return int_val - 96
    elif 65 <= int_val <= 90:
        # Uppercase
        return int_val - 64 + 26


def process_line(line: str) -> int:
    if len(line) == 0:
        return 0
    half = int(len(line) / 2)
    comp_one = set(list(line[:half]))
    comp_two = set(list(line[half:]))
    intersection = comp_one.intersection(comp_two)
    return priority(intersection.pop())


with open('input.txt') as f:
    print(sum([process_line(line.strip()) for line in f.readlines()]))
