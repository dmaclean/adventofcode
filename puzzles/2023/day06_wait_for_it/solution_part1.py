import functools
import re


def main():
    with open("input.txt") as f:
        time = []
        dist = []
        for line in f.readlines():
            if line.startswith("Time"):
                time = [int(val) for val in re.split("\\s+", line.split(":")[1].strip())]
            elif line.startswith("Distance"):
                dist = [int(val) for val in re.split("\\s+", line.split(":")[1].strip())]

        all_solutions = []
        for i in range(len(time)):
            t = time[i]
            d = dist[i]

            num_solutions = 0
            for j in range(t):
                dist_for_race = j * (t - j)
                if dist_for_race > d:
                    num_solutions += 1
            print(f"Solutions for race {i}: {num_solutions}")
            all_solutions.append(num_solutions)
        result = functools.reduce(lambda x, y: x * y, all_solutions, 1)
        print(result)


if __name__ == '__main__':
    main()
