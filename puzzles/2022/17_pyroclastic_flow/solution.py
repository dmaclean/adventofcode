import dataclasses


@dataclasses.dataclass
class Shape:
    height: int
    width: int

    # def


def print_chamber(chamber) -> None:
    for row in chamber:
        print(' '.join(row))


jet = list(open('sample_input.txt').readline().strip())
print(jet)

types = ['hbar', '+', 'rev_l', 'vbar', 'square']

# The tall, vertical chamber is exactly seven units wide.
# Each rock appears so that its left edge is two units away
# from the left wall and its bottom edge is three units above
# the highest rock in the room (or the floor, if there isn't one).

chamber = []
for _ in range(4):
    chamber.append(list('.' * 7))

rock_num = 0
type = types[rock_num % len(types)]

print_chamber(chamber)

# shape = N
# if type == 'hbar':
#
#
# bottom_row = 0
# left_col = 2
touching = False
while not touching:
    if type == 'hbar':
        pass

