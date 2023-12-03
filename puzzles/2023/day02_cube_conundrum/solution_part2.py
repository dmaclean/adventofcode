import re


def main():
    with open("input.txt") as input:
        sum_of_games = 0
        for line in input.readlines():
            parts = line.split(":")
            cube_rounds = parts[1].split(";")
            max_red = 0
            max_green = 0
            max_blue = 0
            for cube_round in cube_rounds:
                for cube in cube_round.split(","):
                    p = cube.strip().split(" ")
                    num = int(p[0])
                    cube_type = p[1]
                    if cube_type == "red" and num > max_red:
                        max_red = num
                    elif cube_type == "green" and num > max_green:
                        max_green = num
                    elif cube_type == "blue" and num > max_blue:
                        max_blue = num
            sum_of_games += max_red * max_green * max_blue
        print(sum_of_games)


if __name__ == '__main__':
    main()
