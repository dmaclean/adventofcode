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

#max_coord = 20
max_coord = 4_000_000
count = 0
possible_beacon_coords = {}

# The idea here is to walk around the perimeter of each sensor, identifying the coordinates just outside
# of the coverage. For each visited coordinate, we'll record it in a dictionary and insert/increment the
# number of visits to it.  If there is a single coordinate that is undiscovered, it should be the one
# with the most number of visits (any ties would indicate that there is more than one undiscovered one).
#
# This approach also allows us to compute this (relatively) efficiently.  The overall coverage area
# is 4M x 4M, which yields 16 trillion possible coordinates - clearly too many to process brute-force.
# This approach would reduce the number of comparisons by... a lot.
for sensor in sensors:
    start = time.time()

    closest_beacon = closest[sensor]
    dist_from_beacon = __dist_from_sensor(sensor, closest_beacon)

    # Walk the top-right edge of the coverage area
    top_coord = [sensor[0], sensor[1] - dist_from_beacon - 1]
    curr_coord = [sensor[0], sensor[1] - dist_from_beacon - 1]
    while curr_coord[1] <= sensor[1]:
        # keep walking diagonally until we are even with the sensor's y-coordinate
        curr_coord_tuple = (curr_coord[0], curr_coord[1])
        if 0 <= curr_coord[0] <= max_coord and \
                0 <= curr_coord[1] <= max_coord and \
                curr_coord_tuple not in sensors and \
                curr_coord_tuple not in beacons:
            if curr_coord_tuple in possible_beacon_coords:
                possible_beacon_coords[curr_coord_tuple] += 1
            else:
                possible_beacon_coords[curr_coord_tuple] = 1

        curr_coord[0] += 1
        curr_coord[1] += 1

    # Walk the top-left edge of the coverage area
    curr_coord = [sensor[0], sensor[1] - dist_from_beacon - 1]
    while curr_coord[1] <= sensor[1]:
        # keep walking diagonally until we are even with the sensor's y-coordinate
        curr_coord_tuple = (curr_coord[0], curr_coord[1])
        if 0 <= curr_coord[0] <= max_coord and \
                0 <= curr_coord[1] <= max_coord and \
                curr_coord_tuple not in sensors and \
                curr_coord_tuple not in beacons:
            if curr_coord_tuple in possible_beacon_coords:
                possible_beacon_coords[curr_coord_tuple] += 1
            else:
                possible_beacon_coords[curr_coord_tuple] = 1

        curr_coord[0] -= 1
        curr_coord[1] += 1

    # Walk the bottom-left edge of the coverage area
    curr_coord = [sensor[0], sensor[1] + dist_from_beacon + 1]
    while curr_coord[1] >= sensor[1]:
        # keep walking diagonally until we are even with the sensor's y-coordinate
        curr_coord_tuple = (curr_coord[0], curr_coord[1])
        if 0 <= curr_coord[0] <= max_coord and \
                0 <= curr_coord[1] <= max_coord and \
                curr_coord_tuple not in sensors and \
                curr_coord_tuple not in beacons:
            if curr_coord_tuple in possible_beacon_coords:
                possible_beacon_coords[curr_coord_tuple] += 1
            else:
                possible_beacon_coords[curr_coord_tuple] = 1

        curr_coord[0] -= 1
        curr_coord[1] -= 1

    # Walk the bottom-right edge of the coverage area
    curr_coord = [sensor[0], sensor[1] + dist_from_beacon + 1]
    while curr_coord[1] >= sensor[1]:
        # keep walking diagonally until we are even with the sensor's y-coordinate
        curr_coord_tuple = (curr_coord[0], curr_coord[1])
        if 0 <= curr_coord[0] <= max_coord and \
                0 <= curr_coord[1] <= max_coord and \
                curr_coord_tuple not in sensors and \
                curr_coord_tuple not in beacons:
            if curr_coord_tuple in possible_beacon_coords:
                possible_beacon_coords[curr_coord_tuple] += 1
            else:
                possible_beacon_coords[curr_coord_tuple] = 1

        curr_coord[0] += 1
        curr_coord[1] -= 1

    count += 1
    print(f'Processed sensor {count} of {len(sensors)} in {time.time() - start} seconds')

best_count = 0
best = None
for k, v in possible_beacon_coords.items():
    if best is None or v > best_count:
        best = k
        best_count = v

print(f'{best} - {best_count}')
print(f'Tuning frequency is {best[0] * 4_000_000 + best[1]}')
