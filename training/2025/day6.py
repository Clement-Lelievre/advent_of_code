import numpy as np


example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """


def homework(inp: str) -> int:
    lines = [row.strip() for row in inp.splitlines()]
    nbs, symbols = [l.split() for l in lines[:-1]], lines[-1].split()
    ans = 0
    for col in range(len(nbs[0])):
        op = symbols[col].join([line[col] for line in nbs])
        ans += eval(op)

    print(ans)
    return ans


def homework_p2(inp: str) -> int:
    lines = [list(row) for row in inp.splitlines()[:-1]]
    symbols = inp.splitlines()[-1].split()
    grid = np.array(lines, dtype=str)
    grid = np.rot90(grid).tolist()
    grid = [[nb for nb in line if nb.strip()] for line in grid]
    grid = [["".join(line)] if line else "sep" for line in grid]
    #   print(grid)
    ops = []
    nbs = []
    for elem in grid:
        if elem == "sep":
            ops.append(nbs)
            nbs = []
            continue
        nbs.extend(elem)
    ops.append(nbs)  # don't forget the last one!
    ans = 0
    for symbol, line in zip(
        symbols[::-1], ops
    ):  # don't forget to reverse the symbol since we rotated the grid!
        op = symbol.join(line)
        ans += eval(op)

    print(ans)
    return ans


if __name__ == "__main__":
    assert homework(example) == 4277556
    homework(open("data/day6.txt").read())
    assert homework_p2(example) == 3263827
    homework_p2(open("data/day6.txt").read())
