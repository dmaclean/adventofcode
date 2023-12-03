import re


def main():
    with (open("input.txt") as input):
        sum_of_games = 0
        for line in input.readlines():
            parts = line.split(":")
            game_num = re.match("Game (\d+)", parts[0]).group(1)
            cube_rounds = parts[1].split(";")
            is_game_possible = True
            for cube_round in cube_rounds:
                if not is_game_possible:
                    continue
                for cube in cube_round.split(","):
                    if not is_game_possible:
                        continue
                    p = cube.strip().split(" ")
                    num = int(p[0])
                    cube_type = p[1]
                    if (cube_type == "red" and num > 12) or \
                            (cube_type == "green" and num > 13) or \
                            (cube_type == "blue" and num > 14):
                        is_game_possible = False
            if is_game_possible:
                sum_of_games += int(game_num)
        print(sum_of_games)


if __name__ == '__main__':
    main()
