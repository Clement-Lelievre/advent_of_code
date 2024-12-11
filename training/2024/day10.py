import numpy as np
from collections import deque

small = """
0123
1234
8765
9876
"""

other = """...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9"""

yet_other = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""

o = """10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01"""

m = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

actual_input = """967801543219877892110120432456765487321234545
854914678900166743026501501329870398100987656
763023498101255654137432672014981287231892187
012109567692341015048976789023569346542763096
101238747887654320157985989121478965456754345
387345656901298743269834870130327101329805210
296096543214386654978723763243210234910418721
145187762105675667871011054358700195894329652
034219853098734789876012343969656786765012347
124309344565623210985985432878545987787601478
565678234674310301234576501701230834594576569
876569132183087456789632101689321127623987654
985432045092196565410547012678101098210891203
876301896700123478326698763543201543109890312
101216789810156389887789654410892672108701021
560125654327667210796612345329763489807632120
456981011498558976545003459458654308716543031
347876320123443089232117868567761218923784787
210945451056782190101656977657890034874695698
987890102349891001212343980342101125665546788
816543211001230417654322821233211056750036569
105565439814376528740011987344780149821123478
219870126765089439951010476035691231034032107
327892345670129310892312362121003412385221016
456781036789438901765403453438912505496102345
012301095490567812989889854567434676787243212
903432787321054923476798763479823987654356601
876563456434143898565210012189714303498987787
569874894321032387654302100001605212567345698
984965765410101234563218761232556721986432183
673454899006565123870109454343457890673212012
542165678187443012989547823254598012364301501
034078543298332132103456910167652345455677652
125609434701245045892321009878541076210588943
010712549889456756701034569969037889821099812
899823456776321893212103278450126985432178901
701209870125410984345232182321125676589067887
654312565034587654456941091101034389678450996
521023454123898343457850190872765210789321045
438985576540123232567569287963898001679877832
307656987239854101098478016554587123456756921
412587610108763003451289123423696564012345670
653496541067654012760345689510789456703430189
743237832378903009801236776421012329898521278
892106901265012108980109865430101012987630167
"""

p2_example = """.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9...."""

thirteen = """..90..9
...1.98
...2..7
6543456
765.987
876....
987...."""

two_two_seven = """012345
123456
234567
345678
4.6789
56789."""


def solve_p1(inp: str) -> int:
    lines = [list(line) for line in inp.splitlines() if line.strip()]
    grid = np.array(lines, dtype=int)
    curr_score = 0
    x, y = grid.shape
    for row in range(x):
        for col in range(y):
            if grid[row, col] == 0:
                curr_score += compute_nb_trails(grid, (row, col))
    print(curr_score)
    return curr_score


def compute_nb_trails(grid: np.ndarray, start_pos: tuple[int, int]) -> int:
    queue = deque([])
    curr_pos = start_pos
    assert grid[curr_pos] == 0
    curr_trail = []
    queue.append((curr_pos, curr_trail))
    seen_destinations = set()
    nb_trails = 0
    while queue:
        pos, trail = queue.popleft()
        if len(trail) == 10 and trail[-1] not in seen_destinations:
            seen_destinations.add(trail[-1])
            nb_trails += 1
            continue
        if len(trail) and grid[pos] != grid[trail[-1]] + 1:
            continue
        for neigh in get_neighbors(pos, grid):
            queue.append((neigh, trail + [pos]))
    return nb_trails


def get_neighbors(pos: tuple[int, int], grid: np.ndarray):
    x, y = pos
    if x - 1 >= 0:
        yield (x - 1, y)
    if y - 1 >= 0:
        yield (x, y - 1)
    if x + 1 < grid.shape[0]:
        yield (x + 1, y)
    if y + 1 < grid.shape[1]:
        yield (x, y + 1)


# part 2
def solve_p2(inp: str) -> int:
    lines = [
        ["-3" if elem == "." else elem for elem in line]
        for line in inp.splitlines()
        if line.strip()
    ]  # -3 is arbitrary, just to avoid dots while making invalid paths
    grid = np.array(lines, dtype=int)
    curr_score = 0
    x, y = grid.shape
    for row in range(x):
        for col in range(y):
            if grid[row, col] == 0:
                curr_score += compute_nb_trails_p2(grid, (row, col))
    print(curr_score)
    return curr_score


def compute_nb_trails_p2(grid: np.ndarray, start_pos: tuple[int, int]) -> int:
    queue = deque([])
    curr_pos = start_pos
    assert grid[curr_pos] == 0
    curr_trail = []
    queue.append((curr_pos, curr_trail))
    seen_trails = set()
    nb_trails = 0
    while queue:
        pos, trail = queue.popleft()
        if len(trail) == 10 and tuple(trail) not in seen_trails:
            seen_trails.add(tuple(trail))
            nb_trails += 1
            continue
        if len(trail) and grid[pos] != grid[trail[-1]] + 1:
            continue
        for neigh in get_neighbors(pos, grid):
            queue.append((neigh, trail + [pos]))
    return nb_trails


if __name__ == "__main__":
    assert (r := solve_p1(small)) == 1, f"found {r}"
    # assert solve_p1(other) == 2
    # assert solve_p1(yet_other) == 4
    # assert solve_p1(o) == 3
    assert solve_p1(m) == 36
    solve_p1(actual_input)
    assert solve_p2(p2_example) == 3
    assert solve_p2(thirteen) == 13
    assert solve_p2(two_two_seven) == 227
    assert solve_p2(m) == 81
    solve_p2(actual_input)
