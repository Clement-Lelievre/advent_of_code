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
    """Naive O(n^2) search, but oh well that scaled.
    If it hadn't, then I'd have tried creating a grid to rule out some pairs
    """
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

def p2(inp:str)->int:
    # for each row in the grid, determine which ranges of columns make up the area
    
    # for each pair of tiles, check if all four corners of the rectangle the pair creates are in the area
    # if yes, then update the max area
    ans =0
    print(ans)
    return ans
    

if __name__ == "__main__":
    assert p1(example) == 50
    p1(open("data/day9.txt", "r").read())
    assert p2(example)==24
    p2(open("data/day9.txt", "r").read())
