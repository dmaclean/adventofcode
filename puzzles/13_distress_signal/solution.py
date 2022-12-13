import dataclasses
import re
from typing import List, Union, Tuple, Optional


@dataclasses.dataclass
class DistressList:
    """
    A list of values coming from the handheld device
    """

    values: List[Union["DistressList", int]]

    def append(self, item: Union["DistressList", int]) -> None:
        self.values.append(item)

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, item):
        return self.values[item]

    @classmethod
    def construct(cls, input: str) -> Tuple["DistressList", str]:

        packet_list = DistressList([])
        val = ''
        idx = 0
        while input:
            token = input[:1]
            input = input[1:]
            if re.match('\\d', token):
                val += token
            elif token == ',':
                cls.finish_val(packet_list, val)
                val = ''
            elif token == '[':
                dl, remaining = DistressList.construct(input)
                packet_list.append(dl)
                input = remaining
            elif token == ']':
                cls.finish_val(packet_list, val)
                return packet_list, input
            idx += 1
        cls.finish_val(packet_list, val)
        return packet_list, input

    @classmethod
    def finish_val(cls, packet_list, val):
        if val:
            packet_list.append(int(val))


def compare(left: DistressList, right: DistressList) -> Optional[bool]:
    """
    Compare two DistressList values.

    If both values are integers, the lower integer should come first. If the left integer is lower than the right
    integer, the inputs are in the right order. If the left integer is higher than the right integer, the inputs are
    not in the right order. Otherwise, the inputs are the same integer; continue checking the next part of the input.

    If both values are lists, compare the first value of each list, then the second value, and so on. If the left
    list runs out of items first, the inputs are in the right order. If the right list runs out of items first, the
    inputs are not in the right order. If the lists are the same length and no comparison makes a decision about
    the order, continue checking the next part of the input.

    If exactly one value is an integer, convert the integer to a list which contains that integer as its only value,
    then retry the comparison. For example, if comparing [0,0,0] and 2, convert the right value to [2]
    (a list containing 2); the result is then found by instead comparing [0,0,0] and [2].

    :param left: The first packet of the pair
    :param right: The second packet of the pair
    :return: True, if packets are in order.  False, otherwise
    """
    left_len = len(left)
    right_len = len(right)

    for i in range(0, min(left_len, right_len)):
        left_val = left[i]
        right_val = right[i]

        if isinstance(left_val, int) and isinstance(right_val, int):
            ######################
            # Integer comparison
            ######################
            if left_val < right_val:
                return True
            elif right_val < left_val:
                # Right-hand side should be larger number
                return False
        elif isinstance(left_val, DistressList) and isinstance(right_val, DistressList):
            ###################
            # List comparison
            ###################
            result = compare(left_val, right_val)
            if result is not None:
                return result
        elif isinstance(left_val, int) and isinstance(right_val, DistressList):
            ###############
            # int vs List
            ###############
            result = compare(DistressList([left_val]), right_val)
            if result is not None:
                return result
        elif isinstance(left_val, DistressList) and isinstance(right_val, int):
            ###############
            # List vs int
            ###############
            result = compare(left_val, DistressList([right_val]))
            if result is not None:
                return result

    if left_len > right_len:
        # Right-hand side ran out of items, which means it is out of order
        return False
    elif left_len < right_len:
        return True

    return None


pairs = []
curr_pair = []
with open('input.txt') as f:
    for line in f.readlines():
        if line == '\n':
            pairs.append(curr_pair)
            curr_pair = []
            continue
        trimmed = line.strip()[1:-1]
        dl, _ = DistressList.construct(trimmed)
        curr_pair.append(dl)
    pairs.append(curr_pair)

idx = 1
sum_of_indexes = 0
for pair in pairs:
    if compare(pair[0], pair[1]) is True:
        sum_of_indexes += idx
        print(f'Pair {idx} is in the correct order!')
    idx += 1

print(sum_of_indexes)