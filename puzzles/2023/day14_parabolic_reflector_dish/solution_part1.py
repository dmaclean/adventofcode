from typing import List


def main():
    platform = []
    with open("input.txt") as f:
        for line in f.readlines():
            platform.append(list(line.strip()))

    has_movement = move_north(platform)
    print_platform(platform)
    print()
    while has_movement:
        has_movement = move_north(platform)
        print_platform(platform)
        print()

    print(calc_load(platform))


def calc_load(platform: List[List[str]]) -> int:
    load = 0
    load_factor = len(platform)
    for r in range(len(platform)):
        for c in range(len(platform[r])):
            if platform[r][c] == "O":
                load += load_factor
        load_factor -= 1
    return load


def move_north(platform: List[List[str]]) -> bool:
    has_movement = False
    for r in range(len(platform)):
        for c in range(len(platform[r])):
            if platform[r][c] in {".", "#"}:
                continue

            # We have a round rock.  Try to move it up
            if r > 0 and platform[r - 1][c] == ".":
                platform[r - 1][c] = "O"
                platform[r][c] = "."
                has_movement = True
    return has_movement


def print_platform(platform: List[List[str]]) -> None:
    for row in platform:
        line = "".join(row)
        print(line)


if __name__ == '__main__':
    main()
