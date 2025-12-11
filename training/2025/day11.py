from functools import cache

example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

example_p2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def p1(inp: str) -> int:
    d = {}
    for line in inp.splitlines():
        if not line.strip():
            continue
        start, end = line.split(":")
        ends = end.strip().split()
        d[start] = ends
    ans = 0

    def recurse(door: str) -> None:
        nonlocal ans
        if door == "out":
            ans += 1
            return
        for dest in d[door]:
            recurse(dest)

    recurse("you")
    print(ans)

    return ans


Path = str


def p2(inp: str) -> int:
    d = {}
    for line in inp.splitlines():
        if not line.strip():
            continue
        start, end = line.split(":")
        ends = end.strip().split()
        d[start] = ends

    @cache
    def nb_paths(
        curr: Path, dest: Path, need_to_visit: frozenset[Path]
    ) -> int:  # frozenset bcs cache needs the args to be hashable
        if curr == dest:
            return (
                1 if not need_to_visit else 0
            )  # we can stop here bcs once in "out" we cannot go further

        return sum(
            nb_paths(next_, dest, need_to_visit - {curr}) for next_ in d[curr]
        )  # if curr is not in need_to_visit, it's ok need_to_visit will be unchanged, else will remain of frozenset type

    ans = nb_paths("svr", "out", frozenset(["fft", "dac"]))
    print(ans)

    return ans


if __name__ == "__main__":
    assert p1(example) == 5
    p1(open("data/day11.txt", "r").read())
    assert p2(example_p2) == 2
    p2(open("data/day11.txt", "r").read())
