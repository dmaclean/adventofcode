import re


def fix_line(line: str) -> str:
    return line.replace('one', 'o1one') \
        .replace('two', 't2two') \
        .replace('three', 't3three') \
        .replace('four', 'f4four') \
        .replace('five', 'f5five') \
        .replace('six', 's6six') \
        .replace('seven', 's7seven') \
        .replace('eight', 'e8eight') \
        .replace('nine', 'n9nine') \
        .replace('zero', 'z0zero')


def main():
    with open("input_part2.txt") as input:
        total = 0
        for line in input.readlines():
            adjusted_line = fix_line(line)
            first = None
            last = None
            for val in adjusted_line:
                if re.match('[0-9]', val):
                    if not first:
                        first = val
                    last = val
            total += int(first + last)
        print(total)


if __name__ == '__main__':
    main()
