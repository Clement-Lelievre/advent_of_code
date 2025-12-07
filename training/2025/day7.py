import numpy as np

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


if __name__ == "__main__":
    assert p1(example) == 21
    p1(open("data/day7.txt", "r").read())
