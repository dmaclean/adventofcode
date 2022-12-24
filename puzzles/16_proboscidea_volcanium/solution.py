import dataclasses
import re
import time
from collections import namedtuple
from typing import List, Optional

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
        return self.prev.is_valve_open(name)

    def calc_max_flow(self) -> int:
        total = self.flow * self.minutes if self.is_open and not self.was_already_opened else 0
        max_for_children = 0
        if self.next:
            max_for_children = max([n.calc_max_flow() for n in self.next])
        return total + max_for_children

    def is_in_cycle(self) -> bool:
        if self.prev:
            if self.prev.prev:
                if self.prev.prev.prev:
                    return self.prev.prev.prev.prev and self.prev.prev.prev.prev.name == self.name
        return False

    def clone_remaining_flows(self) -> List[int]:
        return [x for x in self.remaining_flows]

    def num_visits(self, valve: str) -> int:
        visits = 0
        if self.name == valve:
            visits += 1
        if self.prev:
            return visits + self.prev.num_visits(valve)
        return visits

    def curr_total_flow(self) -> int:
        f = self.flow * self.minutes if (self.is_open and not self.was_already_opened) else 0
        if not self.prev:
            return f
        tf = f + self.prev.curr_total_flow()
        return tf

    def print_path(self, curr_path, current_total_flow=0):
        ctf = current_total_flow + (self.flow * self.minutes if self.is_open and not self.was_already_opened else 0)
        curr_path.append(f'{self.name} ({"o" if self.is_open else "c"} {self.flow}|{self.minutes})')
        if self.next:
            for n in self.next:
                n.print_path(curr_path, ctf)
        elif ctf > 1200:
            print(' -> '.join(curr_path) + f"   TOTAL = {ctf}")
        curr_path.pop()


# def is_terminal(curr_valve_name: str, valve: Valve) -> bool:
#     return len([t for t in valve.tunnels if t != curr_valve_name]) == 0


def is_terminal(valve: Valve) -> bool:
    return len(valve.tunnels) == 1


def visited_max_times(node: Node, valve: str) -> bool:
    num_visits = node.num_visits(valve)
    return num_visits > len(valves[valve])


def calc_theoretical_highest_flow(n):
    m = minutes_remaining
    rest = 0
    # for f in flows:
    #     rest += f * m
    #     m -= 1
    idx = 0
    while m > 0 and idx < len(n.remaining_flows):
        rest += n.remaining_flows[idx] * m
        m -= 2
        idx += 1
    return n.curr_total_flow() + rest


root = None
valves = {}
flows_by_size = []
with open('input.txt') as f:
    for line in f.readlines():
        m = p.match(line.strip())
        name = m.group(1)
        flow = int(m.group(2))
        flows_by_size.append(flow)
        tunnels = m.group(3).split(', ')
        valve = Valve(name, flow, tunnels)
        if valve.name == 'AA':
            root = valve
        valves[name] = valve

flows_by_size.sort(reverse=True)

minutes_remaining = 30
initial_node = Node(root.name, root.flow, minutes_remaining, False, False, flows_by_size, None, [])
enqueued = [initial_node]
next_moves = []
largest_flow = 0
largest_theo_flow = 0

while minutes_remaining > 0:
    minutes_remaining -= 1
    start = time.time()
    while enqueued:
        node = enqueued.pop(0)
        # if node.is_in_cycle():
        #     continue

        if sum(node.remaining_flows) == 0:
            continue

        # One possibility is to open valve if it is closed
        if not node.is_open and node.flow > 0:
            flows = node.clone_remaining_flows()
            flows.remove(node.flow)
            n = Node(node.name, node.flow, minutes_remaining, True, False, flows, node, [])
            node.next.append(n)
            next_moves.append(n)

            total_flow = n.curr_total_flow()
            total_theo_flow = n.calc_max_flow()
            if total_flow > largest_flow:
                largest_flow = total_flow
            # if total_theo_flow > largest_theo_flow:
            #     largest_theo_flow = total_theo_flow

        # if len(valves[node.name].tunnels) == 1 and not node.is_open:
            # Don't leave terminal nodes without opening them
            # continue

        if not node.is_open and node.flow == node.remaining_flows[0]:
            # Don't skip this node if it has the current highest flow
            continue

        # Create one possibility for each tunnel that could be visited
        adjacent_tunnels = valves[node.name].tunnels
        for t in adjacent_tunnels:
            valve = valves[t]
            is_already_open = node.is_valve_open(valve.name)
            dest_valve_is_terminal = is_terminal(valve)
            if is_already_open and dest_valve_is_terminal:
                continue

            # if not is_terminal2(valves[node.name]) and not terminal and \
            #         node.prev and node.prev.name == node.name and \
            #         node.prev.prev and node.prev.prev.name == t:
            #     # Don't go back where you came from if a node has multiple edges.
            # This condition accounts for when the current node is us opening a valve and
            # the previous one is the same node, just closed.
            #     continue

            if len(valves[node.name].tunnels) > 1 and node.prev and node.prev.name == t:
                # Basically, if a node has multiple edges, don't just go right back where you came from
                continue

            if visited_max_times(node, t):
                continue
            flows = node.clone_remaining_flows()

            n = Node(valve.name, valve.flow, minutes_remaining, is_already_open, is_already_open, flows, node, [])

            theoretical_highest_flow = calc_theoretical_highest_flow(n)
            if theoretical_highest_flow < largest_flow:
                continue
            node.next.append(n)
            next_moves.append(n)
    enqueued = next_moves
    next_moves = []

    print(f'{minutes_remaining} minutes left, '
          f'{len(enqueued)} nodes enqueued, '
          f'largest flow seen so far is {largest_flow}, '
          f'processing took {time.time() - start} seconds')
    # if largest_flow > 1200:
    #     initial_node.print_path([])
    #     print()

print(initial_node.calc_max_flow())
