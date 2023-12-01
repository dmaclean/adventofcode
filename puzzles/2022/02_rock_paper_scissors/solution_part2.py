WIN = 'WIN'
DRAW = 'DRAW'
LOSE = 'LOSE'
ROCK = 'ROCK'
PAPER = 'PAPER'
SCISSORS = 'SCISSORS'

LOSS_PTS = 0
DRAW_PTS = 3
WIN_PTS = 6

ROCK_PTS = 1
PAPER_PTS = 2
SCISSORS_PTS = 3

MAPPINGS = {
    'A': ROCK,
    'B': PAPER,
    'C': SCISSORS,
    # 'X': ROCK,
    # 'Y': PAPER,
    # 'Z': SCISSORS
}

WLD_MAPPINGS = {
    'X': LOSE,
    'Y': DRAW,
    'Z': WIN
}


def main():
    with open("input.txt") as f:
        total_points = 0
        for line in f.readlines():
            parts = line.replace('\n', '').split(" ")
            opponent = MAPPINGS[parts[0]]
            outcome = WLD_MAPPINGS[parts[1]]
            you = determine_play(opponent, outcome)
            total_points += play_round(you, opponent)
        print(total_points)


def determine_play(opponent: str, outcome: str) -> str:
    if outcome == WIN:
        if opponent == ROCK:
            return PAPER
        elif opponent == PAPER:
            return SCISSORS
        else:
            return ROCK
    elif outcome == DRAW:
        if opponent == ROCK:
            return ROCK
        elif opponent == PAPER:
            return PAPER
        else:
            return SCISSORS
    else:
        # You need to lose
        if opponent == ROCK:
            return SCISSORS
        elif opponent == PAPER:
            return ROCK
        else:
            return PAPER


def play_round(you: str, opponent: str) -> int:
    """
    Determine the points awarded for a round based on what you and your opponent throw.

    :param you: String representing what you threw - ROCK, PAPER, or SCISSORS
    :param opponent: String representing what your opponent threw - ROCK, PAPER, or SCISSORS
    :return: The point value of the round based on win/loss/draw points + rock/paper/scissors points
    """
    if you == ROCK:
        if opponent == ROCK:
            return DRAW_PTS + ROCK_PTS
        elif opponent == PAPER:
            return LOSS_PTS + ROCK_PTS
        else:
            return WIN_PTS + ROCK_PTS
    elif you == PAPER:
        if opponent == ROCK:
            return WIN_PTS + PAPER_PTS
        elif opponent == PAPER:
            return DRAW_PTS + PAPER_PTS
        else:
            return LOSS_PTS + PAPER_PTS
    else:
        if opponent == ROCK:
            return LOSS_PTS + SCISSORS_PTS
        elif opponent == PAPER:
            return WIN_PTS + SCISSORS_PTS
        else:
            return DRAW_PTS + SCISSORS_PTS


if __name__ == '__main__':
    main()
