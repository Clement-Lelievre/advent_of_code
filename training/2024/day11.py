from collections import Counter

example_input = "0 1 10 99 999"
example_input_2 = "125 17"
actual_input = "773 79858 0 71 213357 2937 1 3998391"


def solve_p1(input_str: str, nb_blinks: int, *, debug: bool = False) -> int:
    nbs = list(map(int, input_str.split()))
    print(f"input {nbs}")
    for _ in range(nb_blinks):
        nbs = blink(nbs)
        if debug:
            print(nbs)
    ans = len(nbs)
    print(f"Answer: {ans}")
    return ans


def blink(nbs: list[int]) -> list[int]:
    new = []
    for nb in nbs:
        if nb == 0:
            new.append(1)
        elif (str_len := len((as_str := str(nb)))) % 2 == 0:
            new.append(int(as_str[str_len // 2 :]))
            new.append(int(as_str[: str_len // 2]))
        else:
            new.append(nb * 2024)
    # del nbs
    return new


# part 2
# this time, storing all ints will lead to an OOM due to the combinatorial explosion
# let us store only the counts instead, after all this is what is asked


def solve_p2(input_str: str, nb_blinks: int) -> int:
    stones_counts = Counter(map(int, input_str.split()))
    for _ in range(nb_blinks):
        stones_counts = blink_p2(stones_counts)

    ans = sum(stones_counts.values())
    print(ans)
    return ans


def blink_p2(stones_counts: Counter) -> Counter:
    new = Counter()
    for stone_val, stone_count in stones_counts.items():
        if stone_val == 0:
            new[1] += stone_count
        elif len(str(stone_val)) % 2 == 0:
            stone_1, stone_2 = int(str(stone_val)[len(str(stone_val)) // 2 :]), int(
                str(stone_val)[: len(str(stone_val)) // 2]
            )
            new[stone_1] += stone_count
            new[stone_2] += stone_count
        else:
            new[stone_val * 2024] += stone_count

    return new


if __name__ == "__main__":
    assert solve_p1(example_input, 1) == 7
    assert solve_p1(example_input_2, 6) == 22
    assert solve_p1(example_input_2, 25) == 55_312
    solve_p1(actual_input, 25)
    solve_p2(actual_input, 75) # 237149922829154
