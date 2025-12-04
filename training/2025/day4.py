import numpy as np

example = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def remove_rolls(inp: str | np.ndarray) -> tuple[np.ndarray, int]:
    ans = 0
    if isinstance(inp, str):
        grid = np.array(
            [list(line) for line in inp.splitlines() if line.strip()], dtype=str
        )
    else:
        grid = inp
    new = np.empty_like(grid)
    nb_rows, nb_cols = grid.shape
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            curr = grid[row, col]
            if curr != "@":
                new[row, col] = curr
                continue
            around = grid[
                max(0, row - 1) : min(row + 2, nb_rows),
                max(0, col - 1) : min(col + 2, nb_cols),
            ]
            assert around.size in (9, 4, 6)
            nb_rolls_paper = (around == "@").sum() - (1 if curr == "@" else 0)
            if nb_rolls_paper < 4:
                new[row, col] = "x"
                ans += 1
            else:
                new[row, col] = "@"
    print(ans)
    return new, ans


def remove_rolls_until_nomore(inp: str) -> int:
    ans = 0
    new_grid = inp
    while True:
        new_grid, added = remove_rolls(new_grid)
        if not added:
            break
        ans += added
    print(ans)
    return ans


if __name__ == "__main__":
    assert remove_rolls(example)[1] == 13
    remove_rolls(open("data/day4.txt", "r").read())
    assert remove_rolls_until_nomore(example) == 43
    remove_rolls_until_nomore(open("data/day4.txt", "r").read())
