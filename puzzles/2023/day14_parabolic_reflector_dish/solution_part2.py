import time
from pprint import pprint
from typing import List


def main():
    platform = []
    with open("input.txt") as f:
        for line in f.readlines():
            platform.append(list(line.strip()))

    snapshots = []
    snapshots.append(deep_copy(platform))
    snapshot_idx = 0
    is_in_cycle = False
    start = time.time()
    i = 0
    for i in range(1_000_000_000):
        has_movement = run_cycle(platform)
        iteration = is_same_as_a_snapshot(snapshots, platform)
        if iteration:
            platform_load = calc_load(platform)
            print(f"Iteration {i} has same snapshot as iteration {iteration}, "
                  f"total snapshot len is {len(snapshots)}, "
                  f"load is {platform_load}")
            platform_loads = {i: calc_load(snapshots[i]) for i in range(len(snapshots))}
            pprint(platform_loads)
            cycle_len = i - iteration
            offset = ((1_000_000_000 - i) % cycle_len) - 1
            iteration_offset = iteration + offset
            print(f"{iteration_offset} - {calc_load(snapshots[iteration_offset])}")
            snapshot_idx = iteration
            break
        else:
            snapshots.append(deep_copy(platform))
            snapshot_idx = len(snapshots) - 1
        # if i % 100_000 == 0:
        #     print(f"Finished cycle {i} after {time.time() - start} seconds ({has_movement})")

    cycle_start_idx = snapshot_idx
    cycle_snapshots = snapshots[cycle_start_idx:]
    pprint({i: calc_load(cycle_snapshots[i]) for i in range(len(cycle_snapshots))})
    cycle_length = len(snapshots) - cycle_start_idx
    i_ = (1_000_000_000 - 1 - i)
    cycle_idx = i_ % cycle_length
    final_snapshot = cycle_snapshots[cycle_idx]

    print(f"{cycle_idx} - {calc_load(final_snapshot)}")
    # for s in snapshots:
    #     print(calc_load(s))



def is_same_as_a_snapshot(snapshots, platform):
    for i in range(len(snapshots)):
        if platform == snapshots[i]:
            return i
    return None


def deep_copy(platform):
    copy_of_platform = []
    for row in platform:
        copy_of_platform.append(list(row))
    return copy_of_platform


def run_cycle(platform):
    while move(platform, "N"):
        pass
    while move(platform, "W"):
        pass
    while move(platform, "S"):
        pass
    while move(platform, "E"):
        pass


def calc_load(platform: List[List[str]]) -> int:
    load = 0
    load_factor = len(platform)
    for r in range(len(platform)):
        for c in range(len(platform[r])):
            if platform[r][c] == "O":
                load += load_factor
        load_factor -= 1
    return load


def move(platform: List[List[str]], direction: str) -> bool:
    has_movement = False
    for r in range(len(platform)):
        for c in range(len(platform[r])):
            if platform[r][c] in {".", "#"}:
                continue

            if direction == "N":
                if r > 0 and platform[r - 1][c] == ".":
                    platform[r - 1][c] = "O"
                    platform[r][c] = "."
                    has_movement = True
            elif direction == "W":
                if c > 0 and platform[r][c - 1] == ".":
                    platform[r][c - 1] = "O"
                    platform[r][c] = "."
                    has_movement = True
            elif direction == "S":
                if r < len(platform) - 1 and platform[r + 1][c] == ".":
                    platform[r + 1][c] = "O"
                    platform[r][c] = "."
                    has_movement = True
            elif direction == "E":
                if c < len(platform[r]) - 1 and platform[r][c + 1] == ".":
                    platform[r][c + 1] = "O"
                    platform[r][c] = "."
                    has_movement = True
    return has_movement


def print_platform(platform: List[List[str]]) -> None:
    for row in platform:
        line = "".join(row)
        print(line)


if __name__ == '__main__':
    main()
