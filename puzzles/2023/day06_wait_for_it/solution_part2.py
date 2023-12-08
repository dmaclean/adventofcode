import functools
import re


def main():
    with open("input.txt") as f:
        for line in f.readlines():
            if line.startswith("Time"):
                time = int(line.split(":")[1].strip().replace(" ", ""))
            elif line.startswith("Distance"):
                dist = int(line.split(":")[1].strip().replace(" ", ""))
        print(time)
        print(dist)

        num_solutions = 0
        for j in range(time):
            dist_for_race = j * (time - j)
            if dist_for_race > dist:
                num_solutions += 1
        print(f"Solutions for race: {num_solutions}")


if __name__ == '__main__':
    main()
