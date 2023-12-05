import functools
import re
from collections import namedtuple
from typing import List

Card = namedtuple("Card", ["num", "winning", "mine", "my_winning"])


def create_cards(f) -> List[Card]:
    cards = []
    for line in f.readlines():
        split = line.split(":")
        card_num = re.match("Card\\s+(\\d+)", split[0].strip()).group(1)
        numbers = split[1].strip()
        parts = numbers.split("|")
        winning = {int(n.strip()) for n in re.split("\\s+", parts[0].strip())}
        mine = {int(n.strip()) for n in re.split("\\s+", parts[1].strip())}
        my_winning = winning.intersection(mine)
        cards.append(Card(card_num, winning, mine, my_winning))
    return cards


def main():
    with open("input.txt") as f:
        cards_by_num = {c.num: c for c in create_cards(f)}


if __name__ == '__main__':
    main()
