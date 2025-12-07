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


def p2(inp: str) -> int:
    nb_paths = 0
    arr = [list(row) for row in inp.splitlines() if row.strip()]
    # create the first beam
    s_ind = arr[0].index("S")
    arr[1][s_ind] = "|"

    def recurse(grid):
        nonlocal nb_paths
        # pprint_arr(grid)
        beam_row = 0
        beam_col = grid[beam_row].index("|")
        j = 1
        while beam_row + j < len(grid) and grid[beam_row + j][beam_col] == ".":
            j += 1
        if beam_row + j == len(grid):
            nb_paths += 1
            # pprint_arr(grid)
            return
        for k in (beam_col + 1, beam_col - 1):
            row = grid[beam_row + j][:k] + ["|"] + grid[beam_row + j][k + 1 :]
            new = [row]
            new.extend(grid[beam_row + j + 1 :])
            recurse(new)

    recurse(arr[1:])
    print(nb_paths)
    return nb_paths


if __name__ == "__main__":
    assert p1(example) == 21
    p1(open("data/day7.txt", "r").read())
    assert (ans := p2(example)) == 40, ans
    p2(open("data/day7.txt", "r").read())
