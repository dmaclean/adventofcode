import math
import re
from collections import namedtuple

Node = namedtuple("Node", ["name", "left", "right", "is_start"])


def main():
    with open("input.txt") as f:
        graph = {}
        directions = None
        for line in f.readlines():
            trimmed = line.strip()
            if not directions:
                directions = trimmed
            elif trimmed != "":
                m = re.match("(\\w+) = \\((\\w+), (\\w+)\\)", trimmed)
                name = m.group(1)
                left = m.group(2)
                right = m.group(3)
                graph[name] = Node(name, left, right, name[-1] == "A")

        curr = [n.name for n in graph.values() if n.is_start]
        steps_tracker = [0 for _ in range(len(curr))]
        print(curr)
        for idx in range(6):
            dir_idx = 0
            steps = 0
            is_done = False
            while not is_done:
                c = curr[idx]
                n = graph[c]
                d = directions[dir_idx]
                curr[idx] = n.left if d == "L" else n.right
                dir_idx = (dir_idx + 1) % len(directions)
                is_done = curr[idx][-1] == "Z"
                steps += 1
            print(steps)
            steps_tracker[idx] = steps

        print(math.lcm(*steps_tracker))
        # found = False
        # common_mult = max(steps_tracker) - 1
        # while not found:
        #     common_mult += 1
        #     found = reduce(lambda x, y: x and y, [common_mult % s == 0 for s in steps_tracker])
        #
        # print(common_mult)


        # for c in curr:
        #     for idx in range(len(curr)):
        #         c = curr[idx]
        #         n = graph[c]
        #         curr[idx] = n.left if d == "L" else n.right
        #     dir_idx = (dir_idx + 1) % len(directions)
        #     is_done = reduce(lambda x, y: x and y, [c[-1] == "Z" for c in curr])
        #     steps += 1
        #     # if dir_idx == 0:
        #     print(f"Wrapping around at step {steps}")
        # if reduce(lambda x, y: x or y, [c[-1] == "Z" for c in curr]):
        # print(f"After {steps} steps, {curr}")
        # print(steps)


if __name__ == '__main__':
    main()
