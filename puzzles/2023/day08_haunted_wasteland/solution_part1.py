import re
from collections import namedtuple

Node = namedtuple("Node", ["name", "left", "right"])


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
                graph[name] = Node(name, left, right)

        curr = "AAA"
        dir_idx = 0
        steps = 0
        while curr != "ZZZ":
            d = directions[dir_idx]
            n = graph[curr]
            curr = n.left if d == "L" else n.right
            dir_idx = (dir_idx + 1) % len(directions)  # Proceed to next direction, or rap around once we reach the end
            steps += 1
        print(steps)


if __name__ == '__main__':
    main()
