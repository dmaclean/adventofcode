head = [0, 0]
tail = [0, 0]
coord_count = {
    '0-0': 0
}


def adjust_tail():
    change = True
    if head[0] == tail[0] + 2 and head[1] == tail[1] + 1:
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
        if key in coord_count:
            coord_count[key] += 1
        else:
            coord_count[key] = 1


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
            adjust_tail()

print(len(coord_count))
