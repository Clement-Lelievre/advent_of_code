example = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


def p1(inp: str) -> int:
    (
        ranges,
        ingredients,
    ) = inp.split("\n\n")

    ranges_int = []
    for range_ in ranges.split():
        start, end = range_.strip().split("-")
        ranges_int.append(range(int(start), int(end) + 1))

    ans = sum(
        any(ingredient in range_int for range_int in ranges_int)
        for ingredient in map(int, ingredients.split())
    )
    print(ans)
    return ans


def merge_ranges(range1: range, range2: range) -> range:
    return range(min(range1.start, range2.start), max(range1.stop, range2.stop))


def ranges_overlap(range1: range, range2: range) -> bool:
    oldest = min(range1, range2, key=lambda x: x.start)
    youngest = max(range1, range2, key=lambda x: x.start)
    return oldest.stop >= youngest.start


def p2(inp: str) -> int:
    ranges, _ = inp.split("\n\n")
    ans = 0
    # create the ranges from the input
    ranges_ = []
    for range_ in ranges.split():
        start, end = range_.strip().split("-")
        ranges_.append(range(int(start), int(end) + 1))

    ranges_ = sorted(
        ranges_, key=lambda x: x.start
    )  # I'll sort and then move towards the right
    disjoint_ranges = []
    for ind, range_ in enumerate(ranges_):
        if any(ranges_overlap(range_, dr) for dr in disjoint_ranges):
            continue
        current_range = range_
        for other_range in ranges_[ind + 1 :]:
            if not ranges_overlap(current_range, other_range):
                disjoint_ranges.append(current_range)
                break
            current_range = merge_ranges(current_range, other_range)
        else:  # when merged with everythg to the right
            disjoint_ranges.append(current_range)

    # sum the nbs of elements in each range
    ans = sum(len(range_) for range_ in disjoint_ranges)
    print(ans)
    return ans


if __name__ == "__main__":
    assert p1(example) == 3
    p1(open("data/day5.txt", "r").read())
    assert p2(example) == 14
    p2(open("data/day5.txt", "r").read())
