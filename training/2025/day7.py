import numpy as np
from collections import namedtuple, defaultdict

example = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""


def pprint_arr(arr) -> None:
    for row in arr:
        print(*row)
    print("\n")


def p1(inp: str) -> int:
    arr = [list(row) for row in inp.splitlines() if row.strip()]
    # create the first beam
    s_ind = arr[0].index("S")
    arr[1][s_ind] = "|"
    arr = np.array(arr, dtype=str)
    nb_splits = 0
    for ind in range(1, arr.shape[0] - 1):
        # locate beams
        beams_ind = np.where(arr[ind] == "|")[0]
        # propagate them downward
        for (
            beam_ind
        ) in (
            beams_ind
        ):  # conveniently, no need to check for IndexErrors due to the map setup
            if arr[ind + 1][beam_ind] == ".":
                arr[ind + 1][beam_ind] = "|"
            elif arr[ind + 1][beam_ind] == "^":
                nb_splits += 1
                arr[ind + 1][beam_ind + 1] = arr[ind + 1][beam_ind - 1] = "|"

    # pprint_arr(arr)
    print(nb_splits)
    return nb_splits


Point = namedtuple("Point", ["x", "y"])


def p2(inp: str) -> int:
    arr = [list(row) for row in inp.splitlines() if row.strip()]
    s_ind = arr[0].index("S")
    nb_rows = len(arr)
    visited: defaultdict[Point, int] = defaultdict(int)

    def nb_paths_till_bottom(from_: Point) -> int:
        if from_.x == nb_rows:
            return 1
        if from_ in visited:
            return visited[from_]

        i = 1
        while from_.x + i < nb_rows and arr[from_.x + i][from_.y] != "^":
            i += 1
        if from_.x + i == nb_rows:
            return 1

        left = nb_paths_till_bottom(Point(from_.x + i, from_.y - 1))
        right = nb_paths_till_bottom(Point(from_.x + i, from_.y + 1))
        visited[from_] = left + right
        return visited[from_]

    ans = nb_paths_till_bottom(from_=Point(0, s_ind))
    print(ans)
    return ans


if __name__ == "__main__":
    assert p1(example) == 21
    p1(open("data/day7.txt", "r").read())
    assert (example_ans := p2(example)) == 40, example_ans
    p2(open("data/day7.txt", "r").read())
