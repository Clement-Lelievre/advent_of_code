"""https://adventofcode.com/2020/day/25"""

actual_public_keys = [16915772, 18447943]
test_keys = [5764801, 17807724]


def solve(key1: int, key2: int) -> int:
    loop_size = find_loop_size(key1)
    encryption_key = create_key(loop_size=loop_size, subject_number=key2)
    print(encryption_key)
    return encryption_key


def create_key(subject_number: int = 7, loop_size: int = 8):
    """Make the key

    Args:
        subject_number (int, optional): _description_. Defaults to 7.
        loop_size (int, optional): _description_. Defaults to 8.

    Returns:
        _type_: _description_
    """
    # transform_subject_number
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value


def find_loop_size(target_key: int) -> int:
    """Determine the loop size

    Args:
        target_key (int): _description_

    Returns:
        int: _description_
    """
    value = 1
    loop_size = 0
    subject_number = 7
    while value != target_key:
        value *= subject_number
        value %= 20201227
        loop_size += 1
    return loop_size


if __name__ == "__main__":
    assert create_key(loop_size=8) == 5764801
    assert create_key(loop_size=11) == 17807724
    assert create_key(subject_number=17807724, loop_size=8) == 14897079
    assert create_key(subject_number=5764801, loop_size=11) == 14897079
    assert find_loop_size(target_key=5764801) == 8
    assert find_loop_size(target_key=17807724) == 11
    assert solve(5764801, 17807724) == 14897079
    solve(*actual_public_keys)
