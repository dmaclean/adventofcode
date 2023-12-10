from typing import List


def main():
    histories = []
    hist_next_vals = []
    with open("input.txt") as f:
        for line in f.readlines():
            histories.append([int(v) for v in line.split(" ")])

        for h in histories:
            diffs = [h]
            while not all_values_zero(diffs[-1]):
                diff = []
                curr = diffs[-1]
                for i in range(0, len(curr) - 1):
                    diff.append(curr[i + 1] - curr[i])
                diffs.append(diff)

            diffs[-1].append(0)
            for i in range(len(diffs) - 2, -1, -1):
                val = diffs[i][-1] + diffs[i + 1][-1]
                diffs[i].append(val)
            hist_next_vals.append(diffs[0][-1])
    print(sum(hist_next_vals))


def all_values_zero(vals: List[int]) -> bool:
    for v in vals:
        if v != 0:
            return False
    return True


if __name__ == '__main__':
    main()
