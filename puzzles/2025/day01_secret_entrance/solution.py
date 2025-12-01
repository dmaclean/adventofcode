from collections import namedtuple

Instruction = namedtuple('Instruction', ['direction', 'dist'])


def main():
    instructions = []
    with open("input.txt") as f:
        instructions = [__parse_instruction(line) for line in f.readlines()]

    dial = 50
    landed_at_zero = 0
    for instruction in instructions:
        if instruction.direction == 'R':
            dial += instruction.dist
        else:
            dial -= instruction.dist
            if dial < 0:
                dial = 100 - abs(dial)

        dial = dial % 100
        if dial == 0:
            landed_at_zero += 1

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
