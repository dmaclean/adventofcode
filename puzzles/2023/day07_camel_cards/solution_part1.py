FIVE_OF_KIND = 7
FOUR_OF_KIND = 6
FULL_HOUSE = 5
THREE_OF_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

CARD_PRECEDENCE = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


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
        self.cards = cards
        self.bid = bid
        self.type = self.type(cards)

    @classmethod
    def type(cls, cards: str) -> int:
        dict = {}
        for card in cards:
            if card not in dict:
                dict[card] = 1
            else:
                dict[card] += 1

        values = list(dict.values())
        if len(dict) == 1:
            return FIVE_OF_KIND

        elif len(dict) == 2 and (values[0] == 1 or values[1] == 1):
            return FOUR_OF_KIND
        elif len(dict) == 2 and (values[0] == 2 or values[1] == 2):
            return FULL_HOUSE
        elif len(dict) == 3 and (values[0] == 3 or values[1] == 3 or values[2] == 3):
            return THREE_OF_KIND
        elif len(dict) == 3 and (
                (values[0] == 2 and values[1] == 2) or
                (values[0] == 2 and values[2] == 2) or
                (values[1] == 2 and values[2] == 2)
        ):
            return TWO_PAIR
        elif len(dict) == 4:
            return ONE_PAIR
        elif len(dict) == 5:
            return HIGH_CARD

    def __lt__(self, other: "Hand"):
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

        winnings = 0
        rank = len(sorted_hands)
        for h in sorted_hands:
            winnings += rank * h.bid
            rank -= 1

        print(winnings)


def parse_hand_from_line(line):
    parts = line.split(" ")
    hand = Hand(parts[0].strip(), int(parts[1].strip()))
    return hand


if __name__ == '__main__':
    main()
