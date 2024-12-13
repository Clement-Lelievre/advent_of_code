import re
from fractions import Fraction

example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

mini_example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400"""

actual = """<my_input>"""

def parse_input(inp: str) -> list[tuple[int, int]]:
    games = []
    new_game = []
    for line in inp.strip().splitlines():
        if not line.strip():
            games.append(new_game)
            new_game = []
            continue
        x, y = re.findall(r"\d+", line)
        new_game.append((int(x), int(y)))
    games.append(new_game)
    assert all(len(elem) == 3 for elem in games)
    # print(games)
    return games


def solve_one_game(game: list[tuple[int, int]], max_nb_moves: int = 100) -> float:
    valid = set()
    a, b, target = game
    a_x, a_y, b_x, b_y, target_x, target_y = *a, *b, *target
    for a_pushes in range(max_nb_moves):
        for b_pushes in range(max_nb_moves):
            if (
                a_pushes * a_x + b_pushes * b_x == target_x
                and a_pushes * a_y + b_pushes * b_y == target_y
            ):
                valid.add((a_pushes, b_pushes))
                # do not break because there might be other valid combinations
    tokens = min((3 * comb[0] + comb[1] for comb in valid), default=0)
    return tokens


def solve_p1(inp: str) -> float:
    games = parse_input(inp)
    ans = sum(map(solve_one_game, games))
    print(ans)
    return ans


# part 2
# the previous algo no longer scales


def parse_input_p2(inp: str) -> list[tuple[int, int]]:
    games = []
    new_game = []
    for line in inp.strip().splitlines():
        if not line.strip():
            games.append(new_game)
            new_game = []
            continue
        x, y = re.findall(r"\d+", line)
        new_game.append(
            (int(x) + 10_000_000_000_000, int(y) + 10_000_000_000_000)
            if "P" in line
            else (int(x), int(y))
        )
    games.append(new_game)
    assert all(len(elem) == 3 for elem in games)
    # print(games)
    return games


def solve_one_game_p2(game: list[tuple[int, int]]) -> float:
    # here, without the use of the builtin lib Fraction, there would precision errors leading to a wrong result
    a, b, target = game
    a_x, a_y, b_x, b_y, target_x, target_y = *a, *b, *target
    # the 2-equation 2 unknowns system is as follows:
    # a_pushes * a_x + b_pushes * b_x = target_x
    # a_pushes * a_y + b_pushes * b_y = target_y
    coeff = Fraction(
        numerator=-b_x, denominator=b_y
    )  # multiply second line with `coeff` and then add both lines, to make the `b_pushes` unknown vanish
    # -b_x/b_y*a_pushes * a_y  -b_x * b_pushes = -b_x/b_y*target_y
    # sum both lines to get: a_pushes * (a_x -b_x/b_y* a_y)  = -b_x/b_y*target_y + target_x <=> a_pushes * (a_x -b_x/b_y*a_y)  = -b_x/b_y*target_y + target_x
    a_pushes = Fraction(
        numerator=(coeff * target_y + target_x), denominator=(a_x + coeff * a_y)
    )
    # print(f"{a_x=} {a_y=} {b_x=} {b_y=} {target_x=} {target_y=} {coeff=} {a_pushes=}");exit()
    # check if it's an integer
    if a_pushes - int(a_pushes) != 0:
        return 0
    b_pushes = Fraction(numerator=(target_x - a_pushes * a_x), denominator=b_x)
    if b_pushes - int(b_pushes) != 0:
        return 0
    print(f"{a_pushes=} {b_pushes=} {game=}")
    return 3 * a_pushes + b_pushes


def solve_p2(inp: str) -> float:
    games = parse_input_p2(inp)
    ans = sum(map(solve_one_game_p2, games))
    print(ans)
    return ans


if __name__ == "__main__":
    # assert solve_p1(example) == 480
    # solve_p1(actual)
    # assert (ans:= solve_one_game_p2(parse_input(mini_example)[0]))==280, f"found {ans}"
    # assert solve_p2(mini_example) == 280
    # solve_p2(example)
    solve_p2(actual)
