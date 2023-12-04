import re

SYMBOL_REGEX = "[^\w\d\s\.]"


def has_adjacent_symbol(lines, x, y) -> bool:
    if y - 1 >= 0:
        # Look at row above
        if x - 1 >= 0 and re.match(SYMBOL_REGEX, lines[y - 1][x - 1]):
            return True
        elif re.match(SYMBOL_REGEX, lines[y - 1][x]):
            return True
        elif x + 1 <= len(lines[y]) - 1 and re.match(SYMBOL_REGEX, lines[y - 1][x + 1]):
            return True
    if y + 1 <= len(lines) - 1:
        # Look at row below
        if x - 1 >= 0 and re.match(SYMBOL_REGEX, lines[y + 1][x - 1]):
            return True
        elif re.match(SYMBOL_REGEX, lines[y + 1][x]):
            return True
        elif x + 1 <= len(lines[y]) - 1 and re.match(SYMBOL_REGEX, lines[y + 1][x + 1]):
            return True

    if x - 1 >= 0 and re.match(SYMBOL_REGEX, lines[y][x - 1]):
        # Look to left
        return True
    if x + 1 <= len(lines[y]) - 1 and re.match(SYMBOL_REGEX, lines[y][x + 1]):
        return True
    return False


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
        part_numbers = []
        for y in range(len(lines)):
            line = lines[y]
            curr_num = None
            curr_has_adjacent_symbol = False
            for x in range(len(line)):
                char = line[x]
                if re.match("\d", char):
                    if not curr_num:
                        curr_num = char
                    else:
                        curr_num += char
                    curr_has_adjacent_symbol |= has_adjacent_symbol(lines, x, y)
                    if x == len(line) - 1 and curr_has_adjacent_symbol:
                        part_numbers.append(int(curr_num))
                        print(f"Added {curr_num} from line {y + 1}.")
                elif curr_num is not None:
                    if curr_has_adjacent_symbol:
                        part_numbers.append(int(curr_num))
                        print(f"Added {curr_num} from line {y + 1}.")
                    curr_num = None
                    curr_has_adjacent_symbol = False
        print(sum(part_numbers))


if __name__ == '__main__':
    main()
