FIVE_OF_KIND = 7
FOUR_OF_KIND = 6
FULL_HOUSE = 5
THREE_OF_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

CARD_PRECEDENCE = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

TYPE_TO_NAME = {
    7: "FIVE",
    6: "FOUR",
    5: "FULL HOUSE",
    4: "THREE",
    3: "TWO",
    2: "ONE",
    1: "HIGH CARD"
}


class Hand:
    """
    A single hand of cards and its associated bid.

    The type (i.e. Full house, three-of-a-kind) gets calculated in the constructor based
    on the card string that comes in.  It is important to calculate once and store it because
    it is used in the sort comparison.  Since efficient sorting algorithms are executed
    in n*log(n) time, we'd rather just call type() n times instead of n*log(n) (once per comparison).
    """

    def __init__(self, cards: str, bid: int):
        super().__init__()
        sorted_cards = "".join(sorted(cards, key=lambda item: CARD_PRECEDENCE.index(item)))
        self.cards = cards
        self.sorted_cards = sorted_cards
        self.bid = bid
        self.type = self.type(sorted_cards)
        if "J" in cards:
            print(f"{sorted_cards} ({cards}) got turned into {TYPE_TO_NAME[self.type]}")

    @classmethod
    def type(cls, cards: str) -> int:
        d = {}
        for card in cards:
            if card not in d:
                d[card] = 1
            else:
                d[card] += 1

        if cards == "JJJJJ":
            # If all cards are Jokers then just make them aces.
            d = {"A": 5}

        # Determine the most common card and how many of it there are.
        # This will be the one that any jokers become.
        most_common_card = None
        num_occurrences = 0
        for k, v in d.items():
            if v > num_occurrences:
                most_common_card = k
                num_occurrences = v

        # Determine the best card available that is not a joker.
        # In the event that the most common card is a joker, we want to
        # apply that joker to the best card.
        # This is a weird edge case that we need to code around.
        best_card = None
        best_card_idx = 100
        for c in cards:
            if c == "J":
                continue
            if best_card is None or CARD_PRECEDENCE.index(c) < best_card_idx:
                best_card = c
                best_card_idx = CARD_PRECEDENCE.index(c)
        if most_common_card == "J":
            d[best_card] += num_occurrences
            del d["J"]

        # Turn any Joker into the most common card
        for k, v in d.items():
            if k == "J":
                d[most_common_card] += v
        if "J" in d:
            del d["J"]

        values = list(d.values())
        if len(d) == 1:
            return FIVE_OF_KIND
        elif len(d) == 2 and (values[0] == 1 or values[1] == 1):
            return FOUR_OF_KIND
        elif len(d) == 2 and (values[0] == 2 or values[1] == 2):
            return FULL_HOUSE
        elif len(d) == 3 and (values[0] == 3 or values[1] == 3 or values[2] == 3):
            return THREE_OF_KIND
        elif len(d) == 3 and (
                (values[0] == 2 and values[1] == 2) or
                (values[0] == 2 and values[2] == 2) or
                (values[1] == 2 and values[2] == 2)
        ):
            return TWO_PAIR
        elif len(d) == 4:
            return ONE_PAIR
        elif len(d) == 5:
            return HIGH_CARD

    def __lt__(self, other: "Hand"):
        """
        Determine precedence by type first (Full House, three-of-a-kind, etc).

        If two cards have the same type, go card-by-card to determine the first card to be higher.
        """

        # Implementing less-than so we can use sort() on an iterable containing Hand objects
        if self.type > other.type:
            return True
        elif self.type < other.type:
            return False
        else:
            for i in range(len(self.cards)):
                mine = self.cards[i]
                theirs = other.cards[i]

                mine_index = CARD_PRECEDENCE.index(mine)
                theirs_index = CARD_PRECEDENCE.index(theirs)
                if mine_index < theirs_index:
                    return True
                elif mine_index > theirs_index:
                    return False
        return False


def main():
    with open("input.txt") as f:
        hands = [parse_hand_from_line(line) for line in f.readlines()]
        sorted_hands = sorted(hands)

        cumulative_winnings = 0
        rank = len(sorted_hands)
        for h in sorted_hands:
            w = rank * h.bid
            cumulative_winnings += w
            print(f"{rank} - {h.cards}, {h.bid}, {w}")
            rank -= 1

        print(cumulative_winnings)


def parse_hand_from_line(line):
    parts = line.split(" ")
    hand = Hand(parts[0].strip(), int(parts[1].strip()))
    return hand


if __name__ == '__main__':
    main()
