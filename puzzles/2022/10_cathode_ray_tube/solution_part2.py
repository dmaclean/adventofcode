from typing import List


def draw(screen: List[List[str]], cycle: int, x: int) -> None:
    row = (cycle - 1) // 40
    position = (cycle - 1) % 40
    if x - 1 <= position <= x + 1:
        screen[row][position] = '#'
    else:
        screen[row][position] = '.'


x = 1
cycle = 0

screen = []
for i in range(0, 6):
    screen.append([' ' for _ in range(0, 40)])
crt_pointer = 1

with open('input.txt') as f:
    for line in f.readlines():
        if line == '\n':
            continue
        if line.find('noop') > -1:
            cycle += 1
            draw(screen, cycle, x)
            continue
        parts = line.strip().split(' ')
        op = parts[0]
        val = int(parts[1])

        cycle += 1
        draw(screen, cycle, x)

        cycle += 1
        draw(screen, cycle, x)
        x += val

for i in range(0, 6):
    print(''.join(screen[i]))
