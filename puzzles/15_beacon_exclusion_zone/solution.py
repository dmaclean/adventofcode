import re
from typing import List, Tuple

p = re.compile('Sensor at x=(\\d+), y=(\\d+): closest beacon is at x=([-\\d]+), y=(\\d+)')


def print_map(map: List[List[str]]) -> None:
    for row in map:
        print(''.join(row))


def create_map(sensors: List[Tuple[int, int]], beacons: List[Tuple[int, int]]) -> List[List[str]]:
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0

    for sensor in sensors:
        if sensor[0] < min_x:
            min_x = sensor[0]
        if sensor[0] > max_x:
            max_x = sensor[0]
        if sensor[1] < min_y:
            min_y = sensor[1]
        if sensor[1] > max_y:
            max_y = sensor[1]
    for beacon in beacons:
        if beacon[0] < min_x:
            min_x = beacon[0]
        if beacon[0] > max_x:
            max_x = beacon[0]
        if beacon[1] < min_y:
            min_y = beacon[1]
        if beacon[1] > max_y:
            max_y = beacon[1]

    map = []
    adjust_x = 0
    adjust_y = 0
    if min_x < 0:
        adjust_x = abs(min_x)
    if min_y < 0:
        adjust_y = abs(min_y)
    for y in range(min_y + adjust_y, max_y + adjust_y + 1):
        map.append(list('.' for _ in range(max_x + adjust_x + 1)))

    for sensor in sensors:
        sensor_y = sensor[1] + adjust_y
        sensor_x = sensor[0] + adjust_x
        map[sensor_y][sensor_x] = 'S'
    for beacon in beacons:
        map[beacon[1] + adjust_y][beacon[0] + adjust_x] = 'B'

    return map


sensors = []
beacons = []
with open('sample_input.txt') as f:
    for line in f.readlines():
        m = p.match(line.strip())
        sensor_x = int(m.group(1))
        sensor_y = int(m.group(2))
        beacon_x = int(m.group(3))
        beacon_y = int(m.group(4))
        sensors.append((sensor_x, sensor_y))
        beacons.append((beacon_x, beacon_y))

map = create_map(sensors, beacons)
print_map(map)
