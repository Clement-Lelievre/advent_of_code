example = """987654321111111
811111111111119
234234234234278
818181911112111"""

line1 = """987654321111111"""
line2 = """811111111111119"""
line3 = "234234234234278"
line4 = "818181911112111"


def p1(inp: str) -> int:
    ans = 0
    for line in inp.splitlines():
        ints = list(map(int, list(line)))
        left = max(ints[:-1])
        left_ind = ints.index(left)
        right = max(ints[left_ind + 1 :])
        ans += 10 * left + right
    print(ans)
    return ans


def p2(inp: str) -> int:
    ans = 0
    for line in inp.splitlines():
        ints = list(map(int, list(line)))
        rightmost_battery_ind = -1
        for nb_batteries in range(12, 0, -1):
            candidates = (
                ints[rightmost_battery_ind + 1 : -nb_batteries + 1]
                if nb_batteries != 1
                else ints[rightmost_battery_ind + 1 :]
            )
            digit = max(candidates)
            rightmost_battery_ind = ints.index(digit, rightmost_battery_ind + 1)
            ans += 10 ** (nb_batteries - 1) * digit
    print(ans)
    return ans


if __name__ == "__main__":
    assert p1(example) == 357
    with open("data/day3.txt", "r") as f:
        p1(f.read())
    assert p2(line1) == 987654321111
    assert p2(line2) == 811111111119
    assert p2(line3) == 434234234278
    assert p2(line4) == 888911112111
    assert p2(example) == 3_121_910_778_619
    with open("data/day3.txt", "r") as f:
        p2(f.read())
