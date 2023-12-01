import re


def main():
    with open("input.txt") as input:
        total = 0
        for line in input.readlines():
            first = None
            last = None
            for val in line:
                if re.match('[0-9]', val):
                    if not first:
                        first = val
                    last = val
            total += int(first + last)
        print(total)


if __name__ == '__main__':
    main()
