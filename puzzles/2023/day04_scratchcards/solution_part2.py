import re
from collections import namedtuple
from typing import List, Dict

Card = namedtuple("Card", ["num", "winning", "mine", "my_winning"])


def create_cards(f) -> List[Card]:
    """
    Read input in and create a list of Card objects
    :param f: The file handle for the input
    :return: A List of Card objects
    """
    cards = []
    for line in f.readlines():
        split = line.split(":")
        card_num = int(re.match("Card\\s+(\\d+)", split[0].strip()).group(1))
        numbers = split[1].strip()
        parts = numbers.split("|")
        winning = {int(n.strip()) for n in re.split("\\s+", parts[0].strip())}
        mine = {int(n.strip()) for n in re.split("\\s+", parts[1].strip())}
        my_winning = winning.intersection(mine)
        cards.append(Card(card_num, winning, mine, my_winning))
    return cards


def process_card(card: Card, cards_by_num: Dict[int, List[Card]]) -> int:
    """
    Recursive function to process a card and all of the resulting copies won.

    This will call process_card on the _n_ cards after this card based on the
    number of winning numbers for the card.

    :param card: The Card being processed.
    :param cards_by_num: Dictionary of cards, keyed by their numbers
    :return: The total number of cards processed, including the card passed in.
    """
    total_cards = 1
    if len(card.my_winning) == 0:
        return total_cards
    for card_num in range(card.num + 1, card.num + len(card.my_winning) + 1):
        c = cards_by_num[card_num]
        total_cards += process_card(c, cards_by_num)
    return total_cards


def main():
    with open("sample_input.txt") as f:
        cards_by_num = {c.num: c for c in create_cards(f)}
        total_cards = 0
        for v in cards_by_num.values():
            total_cards += process_card(v, cards_by_num)
        print(total_cards)


if __name__ == '__main__':
    main()
