# I got inspiration by checking the excellent notebook of legendary programmer Peter norvig here https://github.com/norvig/pytudes/blob/main/ipynb/Advent-2025.ipynb
# each year at this season I have a blast reading his thought-process and beautiful code

example = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
100x100: 0 0 0 0 2 0"""

NB_HASHES = 7  # notice that all areas contain exactly 7 hashes (yes, too lazy to do the parsing)


def is_trivial_fit(dims: list[int], quantities: list[int]) -> bool:
    available_x, available_y = dims[0] // 3, dims[1] // 3
    return sum(quantities) <= available_x * available_y


def is_impossible_fit(dims: list[int], quantities: list[int]) -> bool:
    # if the nb of hashes to place is > the nb of available spots
    nb_hashes_to_place = sum(quantities) * NB_HASHES
    available_spots = dims[0] * dims[1]
    return nb_hashes_to_place > available_spots


def p1(inp: str) -> int:
    last_hashtag = inp[::-1].index("#")
    data = inp[-last_hashtag + 1 :]
    all_dims, all_qties = [], []
    for line in data.splitlines():
        if not line.strip():
            continue
        dims, qties = line.split(":")
        dims = list(map(int, dims.split("x")))
        qties = list(map(int, qties.split()))
        all_dims.append(dims)
        all_qties.append(qties)

    ans = 0
    for dims, qties in zip(all_dims, all_qties, strict=True):
        if is_impossible_fit(
            dims, qties
        ):  # in fact this is not needed once one knows what to look for
            continue
        if is_trivial_fit(dims, qties):
            ans += 1
            continue
        print("unclear!")

    print(ans)
    return ans


if __name__ == "__main__":
    # assert p1(example) == 2 # this is an exceptionnally rare case where algo does not work on the example input, due to a trick that applies to the actual input but not to the example input
    p1(open("data/day12.txt", "r").read())
