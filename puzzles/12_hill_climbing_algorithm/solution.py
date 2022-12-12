import dataclasses
from typing import List, Tuple

ELEVATIONS = [
    'S',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    'E'
]


@dataclasses.dataclass
class Node:
    letter: str
    col: int
    row: int
    neighbors: List["Node"]
    steps: int

    def coords_as_tuple(self) -> Tuple[int, int]:
        return self.row, self.col

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Node):
            return False
        return self.letter == o.letter and \
            self.col == o.col and \
            self.row == o.row


def find_start(map: List[List[str]]) -> Tuple[int, int]:
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            if map[i][j] == 'S':
                return i, j
    raise Exception('Could not find starting point of map')


def add_to_graph(curr: Node, new_node: Node) -> None:
    curr.neighbors.append(new_node)
    heads.append(new_node)
    as_tuple = new_node.coords_as_tuple()
    nodes_visited.add(as_tuple)
    #print(
    #    f'Visited [{new_node.row},{new_node.col}] ({new_node.letter}) from [{curr.row},{curr.col}] ({curr.letter}) - {new_node.steps} steps')


def process_coord(coords: Tuple[int, int], curr_node: Node) -> bool:
    if coords not in nodes_visited:
        letter = map[coords[0]][coords[1]]
        if curr_node.letter == 'z' and letter == 'E':
            return True
        n = Node(letter, coords[1], coords[0], [], curr_node.steps + 1)
        add_to_graph(curr_node, n)
    return False


map = []
with open('input.txt') as f:
    for line in f.readlines():
        map.append(list(line.strip()))

start = find_start(map)

root = Node('S', start[1], start[0], [], 0)
nodes_visited = {start}
heads = [root]

while heads:
    curr = heads.pop(0)
    reachable_letters = ELEVATIONS[:ELEVATIONS.index(curr.letter) + 2]

    if curr.row - 1 >= 0 and map[curr.row - 1][curr.col] in reachable_letters:
        # Look up
        coords = (curr.row - 1, curr.col)
        found = process_coord(coords, curr)
        if found:
            print(f'Found highest point at {coords[0]}|{coords[1]} from [{curr.row},{curr.col}] in {curr.steps + 1} steps')
            exit(0)
    if curr.row + 1 < len(map) and map[curr.row + 1][curr.col] in reachable_letters:
        # Look down
        coords = (curr.row + 1, curr.col)
        found = process_coord(coords, curr)
        if found:
            print(
                f'Found highest point at {coords[0]}|{coords[1]} from [{curr.row},{curr.col}] in {curr.steps + 1} steps')
            exit(0)
    if curr.col - 1 >= 0 and map[curr.row][curr.col - 1] in reachable_letters:
        # Look left
        coords = (curr.row, curr.col - 1)
        found = process_coord(coords, curr)
        if found:
            print(
                f'Found highest point at {coords[0]}|{coords[1]} from [{curr.row},{curr.col}] in {curr.steps + 1} steps')
            exit(0)
    if curr.col + 1 < len(map[curr.row]) and map[curr.row][curr.col + 1] in reachable_letters:
        # Look right
        coords = (curr.row, curr.col + 1)
        found = process_coord(coords, curr)
        if found:
            print(
                f'Found highest point at {coords[0]}|{coords[1]} from [{curr.row},{curr.col}] in {curr.steps + 1} steps')
            exit(0)
