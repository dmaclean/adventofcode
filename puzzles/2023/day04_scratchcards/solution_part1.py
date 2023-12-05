import re
import functools


def main():
    with open("input.txt") as f:
        total_points = 0
        for line in f.readlines():
            numbers = line.split(":")[1].strip()
            parts = numbers.split("|")
            winning = {int(n.strip()) for n in re.split("\\s+", parts[0].strip())}
            mine = {int(n.strip()) for n in re.split("\\s+", parts[1].strip())}
            my_winning = winning.intersection(mine)
            points = functools.reduce(lambda cum, val: 1 if cum == 0 else cum * 2, my_winning, 0)
            total_points += points
        print(total_points)


if __name__ == '__main__':
    main()
