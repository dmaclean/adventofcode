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
        print(f"Starting Nodes: {curr}")
        for idx in range(len(curr)):
            # Iterate through each node separately and count the number of steps it takes to get to a Z node.
            # Thankfully, the way the puzzle is designed, both traversal from start to end, as well as proceeding
            # past the end and back to it yield the same number of steps.
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

        # The answer is just the LCM of all individual paths (this one can't be brute-forced).
        print(math.lcm(*steps_tracker))


if __name__ == '__main__':
    main()
