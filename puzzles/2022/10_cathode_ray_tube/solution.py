x = 1
cycle = 1
signal_strengths_for_cycles = {
    1: 1
}
with open('input.txt') as f:
    for line in f.readlines():
        if line.find('noop') > -1:
            cycle += 1
            signal_strengths_for_cycles[cycle] = cycle * x
            continue
        parts = line.strip().split(' ')
        op = parts[0]
        val = int(parts[1])

        cycle += 1
        signal_strengths_for_cycles[cycle] = cycle * x

        x += val

        cycle += 1
        signal_strengths_for_cycles[cycle] = cycle * x

print(sum([
    signal_strengths_for_cycles[20],
    signal_strengths_for_cycles[60],
    signal_strengths_for_cycles[100],
    signal_strengths_for_cycles[140],
    signal_strengths_for_cycles[180],
    signal_strengths_for_cycles[220],
]))

