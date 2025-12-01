"""https://adventofcode.com/2025/day/1"""

example_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

Cmd = str


def rotate(inp: list[Cmd]) -> int:
    val = 50
    ans = 0
    for cmd in inp:
        d, v = cmd[0], int(cmd[1:])
        val = ((val + v) if d == "R" else (val - v)) % 100
        if val == 0:
            ans += 1
    print(ans)
    return ans


def rotate_p2(inp: list[Cmd]) -> int:
    val = 50
    ans = 0
    # print(f"{ans=} {val=}")
    for cmd in inp:
        d, v = cmd[0], int(cmd[1:])
        ans += nb_times_cross_zero(val, d, v)
        val = ((val + v) if d == "R" else (val - v)) % 100
        if val == 0:
            ans += 1
        # print(f"{ans=} {val=}")
    print(ans)
    return ans


def nb_times_cross_zero(start_val, d, increment) -> int:
    dist_to_0 = 100 - start_val if d == "R" else start_val
    if start_val == 0 and increment < 100:
        return 0
    if increment <= dist_to_0:
        return 0
    v = 1 + (increment - dist_to_0 - 1) // 100
    # print(v)
    return v


if __name__ == "__main__":
    assert rotate(example_input.splitlines()) == 3
    with open("data/day1.txt", "r") as f:
        inp = f.readlines()
    rotate(inp)
    assert nb_times_cross_zero(99, "R", 2) == 1
    assert nb_times_cross_zero(99, "R", 1) == 0
    assert nb_times_cross_zero(85, "R", 14) == 0
    assert nb_times_cross_zero(85, "R", 15) == 0
    assert nb_times_cross_zero(99, "R", 102) == 2
    assert nb_times_cross_zero(99, "R", 101) == 1
    assert nb_times_cross_zero(6, "L", 7) == 1
    assert nb_times_cross_zero(6, "L", 6) == 0
    assert nb_times_cross_zero(6, "L", 107) == 2
    assert nb_times_cross_zero(6, "L", 106) == 1
    assert nb_times_cross_zero(0, "L", 5) == 0
    assert nb_times_cross_zero(50, "R", 1000) == 10
    assert rotate_p2(["R51", "L2", "R301"]) == 6
    assert rotate_p2(["L450"]) == 5
    assert rotate_p2(example_input.splitlines()) == 6
    assert rotate_p2(inp) > 4988
