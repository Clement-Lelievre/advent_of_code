"""https://adventofcode.com/2024/day/21"""

from itertools import permutations, product
from typing import Generator

actual_input = ["140A", "180A", "176A", "805A", "638A"]

# the problem is estimated "hardcore" on both parts by Le wagon x AoC's Slackbot Djikstra

# personal notes:

# beware mixing up A from the numeric keypad and A on directional keypads
# avoid the empty gap on keypads
# robots start with their arm pointed at A (do they reset their arm position for all new codes ie go back to A if they aren't already pointed at A?) yes because they finish pressing A
# A on the numeric keypad means typing an actual A in the code, while in the directional keypad it means pressing a button


# the numeric keypad
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

# the directional keypad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+


def get_move(src: tuple[int, int], dest: tuple[int, int], pad: str) -> str:
    """Used to populate the moves dicts for both the numeric and directional keypads.
    This way moves are cached.

    Args:
        src (tuple[int,int]): _description_
        dest (tuple[int,int]): _description_
        pad (str): numeric OR directional

    Returns:
        str: the sequence, e.g. '<^>>A<A'
    """
    if pad not in ("numeric", "directional"):
        raise ValueError(f"Bad pad type: {pad}")
    curr = src
    seq = ""
    while curr != dest:
        x_curr, y_curr, x_dest, y_dest = *curr, *dest
        curr_neighs = [
            coord
            for coord in (
                numeric_keypad.values()
                if pad == "numeric"
                else directional_keypad.values()
            )
            if abs(coord[0] - x_curr) + abs(coord[1] - y_curr) == 1
        ]
        next_ = min(
            curr_neighs,
            key=lambda coord: abs(x_dest - coord[0]) + abs(y_dest - coord[1]),
        )
        if next_[0] == x_curr - 1:
            seq += "^"
        elif next_[0] == x_curr + 1:
            seq += "v"
        elif next_[1] == y_curr - 1:
            seq += "<"
        elif next_[1] == y_curr + 1:
            seq += ">"
        else:
            raise ValueError(f"Bad neighbor: {curr=} {next_=}")
        curr = next_
    return seq


numeric_keypad: dict[str, tuple[int, int]] = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
numeric_keypad_moves: dict[tuple[tuple[int, int], tuple[int, int]], str] = {
    (src, dest): get_move(src, dest, pad="numeric")
    for (src, dest) in permutations(numeric_keypad.values(), 2)
}


directional_keypad = {"^": (0, 1), "v": (1, 1), "<": (1, 0), ">": (1, 2), "A": (0, 2)}
directional_keypad_moves: dict[tuple[tuple[int, int], tuple[int, int]], str] = {
    (src, dest): get_move(src, dest, pad="directional")
    for (src, dest) in permutations(directional_keypad.values(), 2)
}


def optimized_paths_generator(path_: str) -> Generator[str, None, None]:
    """Yields all the optimized paths from `path`.
    This is essentially grouping charcaters (to avoid back and forth trips) and trying all possibilities of orders.
    For example, a stair-shaped path from bottom right to upper left cannot be optimized because the upper level'd get wasted back and forth trips
    Instead, we leverage the fact of pointing at a button and being able to press it several times in a row.

    Args:
        path (str): a path such as '<^>vvAv...'

    Yields:
        Generator[str, None, None]: the optimized paths
    """
    intermediate_routes = path_.split("A")
    p = []
    for elem in intermediate_routes:
        if not elem:
            continue  # the trailing empty strings added by python
        e = "".join(sorted(elem))
        p.append((e, e[::-1]))

    for path_data in product(*p):
        # make sure this path does not go over the gap area of the keypad
        # only up and left could get the robot's arm pointing at the forbidden gap area because the gap is at (0,0)
        candidate_path = "A".join(path_data) + "A"
        yield candidate_path


def code_to_seq(code_: str) -> str:
    """From a code, get the sequence to give to the robot handling the numeric keypad"""
    current_pos = numeric_keypad["A"]
    seq = ""
    for char in code_:
        dest = numeric_keypad[char]
        if (
            current_pos != dest
        ):  # alternatively, could add an empty string as value to (pos, pos) keys in the numeric_keypad_moves dict
            seq += numeric_keypad_moves[(current_pos, dest)]
            current_pos = dest
        seq += "A"
    return seq


def seq_to_seq(sequence_: str) -> str:
    """From a sequence of moves, get the next-level sequence to give to the robot handling the directional keypad"""
    current_pos = directional_keypad["A"]
    # group identical consecutive characters, so as to get the shortest path. for example, it's shorter to perform the route ^^> than ^>^
    # but I can't just sort the character grouped between 'A's, I need to compute the order that yields the minimum distance route

    # smart_sequence = "A".join(
    #     "".join(sorted(s)) for s in sequence_.split("A")
    # )  # to be improved, see the below TODO
    # TO DO: yield all smart sequences, because we don't which one will produce the shortest path at the highest level
    min_path_len = float("inf")
    best = None
    FORBIDDEN_SQUARE = (0, 0)  # the gap area on the directional keypad
    for smart_sequence in optimized_paths_generator(sequence_):
        seq = ""
        for char in smart_sequence:
            dest = directional_keypad[char]
            if current_pos != dest:
                seq += directional_keypad_moves[(current_pos, dest)]
                current_pos = dest
            seq += "A"
            if len(seq) > min_path_len:
                break
            if current_pos == FORBIDDEN_SQUARE:
                print("FORBIDDEN")
                break
        else:
            if (
                len(seq) < min_path_len
            ):  # what if there are ties ? will I need to try out all tied paths?
                min_path_len = len(seq)
                best = seq
                print(f"new best: {min_path_len=}")
    assert best is not None
    return best


def solve_p1(codes: list[str], nb_levels: int = 2) -> int:
    ans = 0
    for code_ in codes:
        sequence_ = code_to_seq(code_)
        for _ in range(nb_levels):
            sequence_ = seq_to_seq(sequence_)
        ans += complexity(sequence_, code_)
    print(f"Part 1: {ans}")
    return ans


def complexity(sequence_: str, code_: str) -> int:
    return len(sequence_) * int("".join(c for c in code_ if c.isdigit()))


if __name__ == "__main__":
    assert list(optimized_paths_generator("<>A^^>>>A")) == [
        "<>A>>>^^A",
        "<>A^^>>>A",
        "><A>>>^^A",
        "><A^^>>>A",
    ]

    test_complexities = {
        "029A": [
            "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
            68 * 29,
        ],
        "980A": [
            "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
            60 * 980,
        ],
        "179A": [
            "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
            68 * 179,
        ],
        "456A": [
            "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
            64 * 456,
        ],
        "379A": [
            "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
            64 * 379,
        ],
    }
    for test_code, (test_seq, expected_complexity) in test_complexities.items():
        assert complexity(test_seq, test_code) == expected_complexity
    assert numeric_keypad_moves[((0, 0), (0, 1))] == ">"
    assert numeric_keypad_moves[((3, 2), (0, 2))] == "^^^"
    assert code_to_seq("029A") in ("<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA")

    #  testing first call of seq_to_seq
    assert seq_to_seq("<A") == "<v<A>^>A"
    for numeric_pad_seq in ("<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA"):
        actual_seq = seq_to_seq(numeric_pad_seq)
        actual_seq = "A".join("".join(sorted(s)) for s in actual_seq.split("A"))
        expected = "A".join(
            "".join(sorted(s)) for s in "v<<A>>^A<A>AvA<^AA>A<vAAA>^A".split("A")
        )
        assert len(actual_seq) == len(expected), f"{expected=} {actual_seq=}"

    # testing 2nd call of seq_to_seq
    input_seq = "v<<A>>^A<A>AvA<^AA>A<vAAA>^A"
    actual = seq_to_seq(input_seq)
    # actual = "A".join("".join(sorted(s)) for s in actual.split("A"))
    expected = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    # expected = "A".join("".join(sorted(s)) for s in expected.split("A"))
    # assert len(actual) == len(expected)
    if len(actual) != len(expected):
        print(actual, expected, sep="\n")
        exit()

    # testing composed calls
    codes_full_seqs = {
        "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
        "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
        "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
        "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
        "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
    }
    for code, expected in codes_full_seqs.items():
        sequence = code_to_seq(code)
        print(f"from code {code}: ", sequence)
        for _ in range(2):
            sequence = seq_to_seq(sequence)
            print(f"after seq_to_seq #{_}: {sequence}")
        if len(sequence) != len(expected):
            print(sequence.split("A"), expected.split("A"), sep="\n")
            # exit()

    # integrated test
    assert solve_p1(test_complexities.keys()) == 126384

    solve_p1(actual_input)

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
# mine:     <v<AA>A^>AvAA<^A>A<v<A>^>AvA^A<vA^>A<v<A>^A>AvA^A<v<A>A^>AvA<^A>A
# expected: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
