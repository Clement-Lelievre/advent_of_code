from itertools import combinations
from typing import Literal

example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

# I think there's no point in pressing a button more than once, I'll use that
# also, the order in which we press the buttons does not matter
# I'll iterate through combinations of buttons, from the lowest to the highest nb of buttons
Machine = list[Literal[0, 1]]


def press(machine: Machine, button: tuple[int]) -> Machine:
    return [1 - bit if ind in button else bit for ind, bit in enumerate(machine)]


def fewest(target, buttons: list[tuple]) -> int:
    for k in range(1, len(buttons) + 1):
        for comb in combinations(buttons, k):
            arr = [0] * len(target)
            for button in comb:
                arr = press(arr, button)
            if arr == target:
                return len(comb)
    raise


def p1(inp: str) -> int:
    ans = 0
    for line in inp.splitlines():
        line = line.strip()
        if not line:
            continue
        line = line[: line.index(" {")]
        target = line[line.index("[") + 1 : line.index("]")]
        target = [1 if char == "#" else 0 for char in target]
        b = line[line.index("(") :]
        buttons = [
            tuple(int(elem) for elem in tup[1:-1].split(",")) for tup in b.split()
        ]

        ans += fewest(target, buttons)

    print(ans)
    return ans


if __name__ == "__main__":
    assert p1(example) == 7
    p1(open("data/day10.txt", "r").read())
