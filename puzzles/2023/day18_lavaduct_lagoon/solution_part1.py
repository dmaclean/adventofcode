import re
from collections import namedtuple

DigPlan = namedtuple("DigPlan", ["direction", "steps", "rgb"])


def main():
    dig_plans = []
    with open("sample_input.txt") as f:
        for line in f.readlines():
            m = re.match("(\\w) (\\d+) \\(#([0-9a-z]+)\\)", line.strip())
            d = m.group(1)
            s = m.group(2)
            rgb = m.group(3)
            dig_plans.append(DigPlan(d, int(s), rgb))

    print(dig_plans)


if __name__ == '__main__':
    main()
