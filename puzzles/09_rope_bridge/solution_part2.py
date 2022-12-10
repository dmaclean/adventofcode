from typing import List

head = [0, 0]
tails = [
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
    [0, 0],
]
coord_count = {}
for i in range(0, 9):
    coord_count[i] = {'0-0'}


def adjust_tail(head: List[int], tail: List[int], tail_idx: int) -> None:
    """
    Adjust the provided tail based on the position of the provided head.  These are passed as parameters
    because, for part 2, any tail acts as the head of the tail behind it.

    :param head: The head node
    :param tail: The tail node
    :param tail_idx: Index of the tail node for updating coordinate counts
    """

    change = True
    #########################
    # Two-over, two up/down
    #########################
    if head[0] == tail[0] + 2 and head[1] == tail[1] + 2:
        # - - H
        # - - -
        # T - -
        tail[0] += 1
        tail[1] += 1
    elif head[0] == tail[0] - 2 and head[1] == tail[1] + 2:
        # H - -
        # - - -
        # - - T
        tail[0] -= 1
        tail[1] += 1
    elif head[0] == tail[0] + 2 and head[1] == tail[1] - 2:
        # T - -
        # - - -
        # - - H
        tail[0] += 1
        tail[1] -= 1
    elif head[0] == tail[0] - 2 and head[1] == tail[1] - 2:
        # - - T
        # - - -
        # H - -
        tail[0] -= 1
        tail[1] -= 1

    #########################
    # Two-over, one up/down
    #########################
    elif head[0] == tail[0] + 2 and head[1] == tail[1] + 1:
        # - - H
        # T - -
        tail[0] += 1
        tail[1] += 1
    elif head[0] == tail[0] + 2 and head[1] == tail[1] - 1:
        # T - -
        # - - H
        tail[0] += 1
        tail[1] -= 1
    elif head[0] == tail[0] - 2 and head[1] == tail[1] + 1:
        # H - -
        # - - T
        tail[0] -= 1
        tail[1] += 1
    elif head[0] == tail[0] - 2 and head[1] == tail[1] - 1:
        # - - T
        # H - -
        tail[0] -= 1
        tail[1] -= 1
    ########################
    # Two up/down, one over
    ########################
    elif head[0] == tail[0] + 1 and head[1] == tail[1] + 2:
        # - H
        # - -
        # T -
        tail[0] += 1
        tail[1] += 1
    elif head[0] == tail[0] - 1 and head[1] == tail[1] + 2:
        # H -
        # - -
        # - T
        tail[0] -= 1
        tail[1] += 1
    elif head[0] == tail[0] + 1 and head[1] == tail[1] - 2:
        # T -
        # - -
        # - H
        tail[0] += 1
        tail[1] -= 1
    elif head[0] == tail[0] - 1 and head[1] == tail[1] - 2:
        # - T
        # - -
        # H -
        tail[0] -= 1
        tail[1] -= 1

    ################
    # Non-diagonals
    ################
    elif head[0] == tail[0] and head[1] == tail[1] + 2:
        # - - -
        # - H -
        # - - -
        # - T -
        # - - -
        tail[1] += 1
    elif head[0] == tail[0] and head[1] == tail[1] - 2:
        # - - -
        # - T -
        # - - -
        # - H -
        # - - -
        tail[1] -= 1
    elif head[1] == tail[1] and head[0] == tail[0] + 2:
        # - - - - -
        # - T - H -
        # - - - - -
        tail[0] += 1
    elif head[1] == tail[1] and head[0] == tail[0] - 2:
        # - - - - -
        # - H - T -
        # - - - - -
        tail[0] -= 1
    else:
        change = False

    if change:
        key = f'{tail[0]}-{tail[1]}'
        coord_count[tail_idx].add(key)


with open('input.txt') as f:
    for line in f.readlines():
        trimmed = line.strip()
        parts = trimmed.split(' ')
        direction = parts[0]
        steps = int(parts[1])

        for i in range(0, steps):
            if direction == 'L':
                head[0] -= 1
            elif direction == 'R':
                head[0] += 1
            elif direction == 'U':
                head[1] += 1
            else:
                head[1] -= 1

            for idx in range(0, 9):
                if idx == 0:
                    adjust_tail(head, tails[idx], idx)
                else:
                    adjust_tail(tails[idx - 1], tails[idx], idx)

print(len(coord_count[8]))
