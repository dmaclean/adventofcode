import dataclasses
import functools
import re
import time
from collections import namedtuple
from typing import List, Set, Optional

p = re.compile('Valve ([A-Z]+) has flow rate=(\\d+); tunnels? leads? to valves? (.+)')

Valve = namedtuple('Valve', ['name', 'flow', 'tunnels'])


@dataclasses.dataclass
class Node:
    name: str
    flow: int
    minutes: int
    is_open: bool
    was_already_opened: bool
    remaining_flows: List[int]
    prev: Optional["Node"]
    next: List["Node"]

    def is_valve_open(self, name: str) -> bool:
        if self.name == name:
            return self.is_open
        elif not self.prev:
            # We're at the parent and it looks like we didn't find it
            return False
        # return functools.reduce(lambda a, b: a or b, [n.is_valve_open(name) for n in self.next], False)
        return self.prev.is_valve_open(name)

    def calc_max_flow(self) -> int:
        total = self.flow * self.minutes if self.is_open and not self.was_already_opened else 0
        #print(f'{self.name} - {self.flow}, {self.minutes}')
        return total + (max([n.calc_max_flow() for n in self.next]) if self.next else 0)

    def is_in_cycle(self) -> bool:
        if self.prev:
            if self.prev.prev:
                if self.prev.prev.prev:
                    return self.prev.prev.prev.prev and self.prev.prev.prev.prev.name == self.name
        return False

    def clone_remaining_flows(self) -> List[int]:
        return [x for x in self.remaining_flows]


def is_terminal(curr_valve_name: str, valve: Valve) -> bool:
    return len([t for t in valve.tunnels if t != curr_valve_name]) == 0


root = None
valves = {}
flows_by_size = []
with open('sample_input.txt') as f:
    for line in f.readlines():
        m = p.match(line.strip())
        name = m.group(1)
        flow = int(m.group(2))
        flows_by_size.append(flow)
        tunnels = m.group(3).split(', ')
        valve = Valve(name, flow, tunnels)
        if not root:
            root = valve
        valves[name] = valve

flows_by_size.sort(reverse=True)

minutes_remaining = 30
initial_node = Node(root.name, root.flow, minutes_remaining, False, False, flows_by_size, None, [])
paths = [
    [initial_node]
]

enqueued = [initial_node]
next_moves = []
while minutes_remaining > 0:
    minutes_remaining -= 1
    start = time.time()
    while enqueued:
        node = enqueued.pop(0)
        if node.is_in_cycle():
            continue

        if sum(node.remaining_flows) == 0:
            continue

        # One possibility is to open valve if it is closed
        if not node.is_open and node.flow > 0:
            flows = node.clone_remaining_flows()
            flows.remove(node.flow)
            n = Node(node.name, node.flow, minutes_remaining, True, False, flows, node, [])
            node.next.append(n)
            next_moves.append(n)

        if len(valves[node.name].tunnels) == 1 and not node.is_open:
            # Don't leave terminal nodes without opening them
            continue

        if not node.is_open and node.flow == node.remaining_flows[0]:
            # Don't skip this node if it has the current highest flow
            continue

        # Create one possibility for each tunnel that could be visited
        adjacent_tunnels = valves[node.name].tunnels
        for t in adjacent_tunnels:
            valve = valves[t]
            is_already_open = node.is_valve_open(valve.name)
            terminal = is_terminal(node.name, valve)
            if is_already_open and terminal:
                continue

            if len(valves[node.name].tunnels) > 1 and node.prev and node.prev.name == t:
                # Basically, if a node has multiple edges, don't just go right back where you came from
                continue
            flows = node.clone_remaining_flows()

            n = Node(valve.name, valve.flow, minutes_remaining, is_already_open, is_already_open, flows, node, [])
            node.next.append(n)
            next_moves.append(n)
    enqueued = next_moves
    next_moves = []
    print(f'{minutes_remaining} minutes left, '
          f'{len(enqueued)} nodes enqueued, '
          f'processing took {time.time() - start} seconds')

print(initial_node.calc_max_flow())
