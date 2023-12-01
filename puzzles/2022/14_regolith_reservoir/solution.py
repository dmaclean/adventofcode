from typing import List


def draw_rocks_on_map(map, paths) -> None:
    # Draw rock paths onto map
    for path in paths:
        for i in range(0, len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]

            if p1[0] == p2[0]:
                # X coordinates are the same - we're moving vertically
                p_min = min(p1[1], p2[1])
                p_max = max(p1[1], p2[1])
                for j in range(p_min, p_max + 1):
                    map[j][p1[0]] = '#'
            elif p1[1] == p2[1]:
                # Y coordinates are the same - we're moving horizontally
                p_min = min(p1[0], p2[0])
                p_max = max(p1[0], p2[0])
                for j in range(p_min, p_max + 1):
                    map[p1[1]][j] = '#'
            else:
                raise Exception("Nothing is the same?")


def produce_sand(map) -> bool:
    curr_x = 500
    curr_y = 0

    blocked = False
    while not blocked:
        if curr_y == len(map) - 1:
            # We've reached the abyss
            return True
        elif map[curr_y + 1][curr_x] == '.':
            # Straight down is clear
            curr_y += 1
        elif map[curr_y + 1][curr_x - 1] == '.':
            # Diagonally down/left
            curr_x -= 1
            curr_y += 1
        elif map[curr_y + 1][curr_x + 1] == '.':
            curr_x += 1
            curr_y += 1
        else:
            blocked = True
            map[curr_y][curr_x] = 'o'
            print_map(map)

    return False


def print_map(map: List[List[str]]) -> None:
    for row in map:
        print(''.join(row))


paths = []
largest_x = 0
largest_y = 0

# Read input
with open('input.txt') as f:
    for line in f.readlines():
        trimmed = line.strip()
        if trimmed == '':
            continue

        parts = trimmed.split(' -> ')
        path = []
        for part in parts:
            x_y_pairs = part.split(',')
            x = int(x_y_pairs[0])
            y = int(x_y_pairs[1])

            if x > largest_x:
                largest_x = x
            if y > largest_y:
                largest_y = y

            path.append((x, y))
        paths.append(path)

largest_x += 1


def create_map() -> List[List[str]]:
    # Create map
    map = []
    for i in range(0, largest_y + 1):
        row = list('.' * (largest_x + 1))
        map.append(row)
    # Draw sand source
    map[0][500] = '+'
    draw_rocks_on_map(map, paths)
    return map


map = create_map()

units = 0
reached_abyss = False
while True:
    reached_abyss = produce_sand(map)
    if reached_abyss:
        break
    units += 1

print(f'{units} units of sand produced before falling into abyss')
