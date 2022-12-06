import re

with open('input.txt') as f:
    processed_crates = False
    stacks = None
    for line in f.readlines():
        stripped = line.strip()
        if stripped.find('1   2') > -1:
            processed_crates = True
            for s in stacks:
                s.reverse()
            continue
        if stripped == '':
            continue

        if processed_crates:
            result = re.search('move (\d+) from (\d+) to (\d+)', stripped)
            amount = int(result.group(1))
            from_stack = int(result.group(2)) - 1
            to_stack = int(result.group(3)) - 1

            temp = []
            for i in range(0, amount):
                temp.append(stacks[from_stack].pop())
            while temp:
                stacks[to_stack].append(temp.pop())
        else:
            crates = stripped \
                .replace('    ', ' [-]') \
                .split(' ')

            # Initialize our stacks now that we know how many crates there are
            if not stacks:
                stacks = [[] for _ in crates]

            idx = 0
            for crate in crates:
                letter = crate[1:2]
                if letter == '-':
                    idx += 1
                    continue
                stacks[idx].append(letter)
                idx += 1

    answer = ''
    for stack in stacks:
        answer += stack[-1]
    print(answer)
