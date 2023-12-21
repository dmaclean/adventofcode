from typing import List, Optional


def main():
    platform = []
    with open("input.txt") as f:
        for line in f.readlines():
            platform.append(list(line.strip()))

    snapshots = [deep_copy(platform)]
    cycle_start_idx = 0
    cycle = 0
    for cycle in range(1_000_000_000):
        run_cycle(platform)
        iteration = detect_cycle(snapshots, platform)
        if iteration:
            print(f"Iteration {cycle} has same snapshot as iteration {iteration}")
            cycle_start_idx = iteration
            break
        else:
            snapshots.append(deep_copy(platform))
            cycle_start_idx = len(snapshots) - 1

    # Now that we know there is a cycle, we don't need to run every single
    # iteration of the 1B to know the state of the platform.
    # Instead, we can just use some modulus math to figure out where we would
    # have landed, and what the platform state looks like.

    # Take a slice of the snapshots to isolate the cycle.
    cycle_snapshots = snapshots[cycle_start_idx:]
    cycle_length = len(cycle_snapshots)
    # Figure out how many "spin cycles" we had left to run.
    # I think this part confused me the most because with the 1 billion
    # I was working with a 1-based number, but the "cycle" value is 0-based
    # so I lost track of where I was and whether I needed to subtract a 1.
    # Anyways, a couple hours later, here we are with a solution.
    i_ = (1_000_000_000 - 1 - cycle)
    cycle_idx = i_ % cycle_length
    final_snapshot = cycle_snapshots[cycle_idx]

    print(f"{cycle_idx} - {calc_load(final_snapshot)}")


def detect_cycle(snapshots, platform) -> Optional[int]:
    """
    Check if the current state of the platform is the same as one of the existing snapshots
    from a previous iteration.

    :param snapshots: Collection of snapshots of previous platform states.
    :param platform: The current state of the platform.
    :return: The snapshot index of a matching snapshot, or None if no match.
    """
    for i in range(len(snapshots)):
        if platform == snapshots[i]:
            return i
    return None


def deep_copy(platform):
    copy_of_platform = []
    for row in platform:
        copy_of_platform.append(list(row))
    return copy_of_platform


def run_cycle(platform) -> None:
    """
    Run through a full N, W, S, E cycle.
    :param platform: The platform to manipulate
    """
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
    """
    Tilt the platform in the specified direction and report whether any movement occurred.

    This function might have been more sensible to write as a while loop, where the loop
    only stops when no movement is detected.  Instead, I moved those while loops up into
    run_cycle().

    :param platform: The platform to manipulate.
    :param direction: The direction to tilt the platform.  One of "N", "W", "S", "E".
    :return: True, if any rocks moved.  False, otherwise.
    """
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
