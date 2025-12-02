example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

# looking for any ID which is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.


def solve(inp: str) -> int:
    # naive, early morning solution
    ans = 0
    for r in inp.split(","):
        start, end = r.split("-")
        for nb in range(int(start), int(end) + 1):
            nb_str = str(nb)
            if len(nb_str) % 2:
                continue
            if nb_str[: len(nb_str) // 2] == nb_str[len(nb_str) // 2 :]:
                ans += nb
    print(ans)
    return ans


if __name__ == "__main__":
    assert solve(example) == 1227775554
    with open("data/day2.txt", "r") as f:
        solve(f.read())
