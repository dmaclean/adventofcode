from typing import List


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


def process_group(bags_for_group: List[str]) -> int:
    """
    Evaluate a group of three bags to determine the badge type.

    We're going to do this by converting each bag (string) into a set, and then taking the intersection
    of all three.  This should yield a set with a single item that we can then evalute the priority for.

    :param bags_for_group:  A group of three bags.
    :return:                The priority value of the badge for this group
    """

    if len(bags_for_group) != 3:
        raise Exception(f"Group has {len(bags_for_group)} bags!  Should be 3!")

    bag_one = set(list(bags_for_group[0]))
    bag_two = set(list(bags_for_group[1]))
    bag_three = set(list(bags_for_group[2]))

    badge_item = bag_one.intersection(bag_two.intersection(bag_three)).pop()
    return priority(badge_item)


with open('input.txt') as f:
    group = []
    total_priorities = 0
    for line in f.readlines():
        group.append(line.strip())
        if len(group) == 3:
            total_priorities += process_group(group)
            group = []

    print(total_priorities)
