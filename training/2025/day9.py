from itertools import combinations
from collections import namedtuple

example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

Point = namedtuple("Point", ["x", "y"])


def p1(inp: str) -> int:
    points = [
        Point(int(elem.split(",")[0]), int(elem.split(",")[1]))
        for elem in inp.splitlines()
        if elem.strip()
    ]
    ans = max(
        abs(a.x - b.x + 1) * abs(a.y - b.y + 1) for (a, b) in combinations(points, 2)
    )
    print(ans)
    return ans


if __name__ == "__main__":
    assert p1(example) == 50
    p1(open("data/day9.txt", "r").read())
