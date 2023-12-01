import re
import time
from typing import Tuple

p = re.compile('Sensor at x=(\\d+), y=(\\d+): closest beacon is at x=([-\\d]+), y=(\\d+)')


def __dist_from_sensor(sensor: Tuple[int, int], location: Tuple[int, int]) -> int:
    return abs(sensor[0] - location[0]) + abs(sensor[1] - location[1])


sensors = set()
beacons = set()
closest = {}
with open('input.txt') as f:
    for line in f.readlines():
        m = p.match(line.strip())
        sensor_x = int(m.group(1))
        sensor_y = int(m.group(2))
        beacon_x = int(m.group(3))
        beacon_y = int(m.group(4))
        sensor = (sensor_x, sensor_y)
        beacon = (beacon_x, beacon_y)
        sensors.add(sensor)
        beacons.add(beacon)
        closest[sensor] = beacon

count = 1
row_coords = set()
row_of_interest = 2000000
for sensor in sensors:
    start = time.time()

    closest_beacon = closest[sensor]
    dist_from_beacon = __dist_from_sensor(sensor, closest_beacon)
    print(f'Found closest beacon at {dist_from_beacon} for sensor {sensor}')

    if abs(sensor[1] - row_of_interest) > dist_from_beacon:
        # Row of interest isn't close enough to this sensor to be in its range
        continue

    min_x = sensor[0] - dist_from_beacon
    max_x = sensor[0] + dist_from_beacon + 1
    for x_coord in range(min_x, max_x):
        curr_coords = (x_coord, row_of_interest)
        dist = __dist_from_sensor(sensor, curr_coords)

        if curr_coords in sensors or curr_coords in beacons:
            # There's already a sensor or beacon here - keep going
            continue
        if dist <= dist_from_beacon:
            row_coords.add(curr_coords)

print(len(row_coords))
