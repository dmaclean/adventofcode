import re
from collections import namedtuple

Valve = namedtuple('Valve', ['name', 'flow', 'tunnels'])
p = re.compile('Valve ([A-Z]+) has flow rate=(\\d+); tunnels? leads? to valves? (.+)')

if __name__ == '__main__':
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
            valves[name] = valve

    g = set()
    for v in valves.values():
        for t in v.tunnels:
            tunnel_valve = valves[t]
            g.add(f'{v.name}_{v.flow} -> {tunnel_valve.name}_{tunnel_valve.flow};')
            g.add(f'{tunnel_valve.name}_{tunnel_valve.flow} -> {v.name}_{v.flow};')

    for e in g:
        print(e)