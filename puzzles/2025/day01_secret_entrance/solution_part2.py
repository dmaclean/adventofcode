from collections import namedtuple

Instruction = namedtuple('Instruction', ['direction', 'dist'])


def main():
    instructions = []
    with open("input.txt") as f:
        instructions = [__parse_instruction(line) for line in f.readlines()]

    dial = 50
    landed_at_zero = 0
    for instruction in instructions:
        # Divide by 100 to figure out how many extra times we go around the dial
        # For example, with 200 dist, we'd go around the dial twice and land exactly
        # where we started, but would have passed 0 twice.
        landed_at_zero += instruction.dist // 100

        # Determine the distance, ignoring extra rotations around
        dist = instruction.dist % 100

        started_on_zero = dial == 0
        if instruction.direction == 'R':
            dial += dist
            # if (dial - dist) <= 100 <= dial:
            if dial >= 100:
                landed_at_zero += 1
        else:
            dial -= dist
            if dial <= 0 and not started_on_zero:
                dial = 100 - abs(dial)
                landed_at_zero += 1

        dial = dial % 100

    print(landed_at_zero)


def __parse_instruction(line: str) -> Instruction:
    """
    Parse the instruction string and return an instruction object.

    :param line: An instruction string of the form '<direction><dist>'.  For example, L50, R2
    """
    direction = line[0]
    dist = int(line[1:])
    return Instruction(direction, dist)


if __name__ == '__main__':
    main()
