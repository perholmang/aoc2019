from d9 import process
import math


def n_digits(num: int):
    return math.floor(math.log10(num) + 1)


def test_d9():
    assert (
        process(
            [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        )
    ) == [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

    r = process([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    assert (n_digits(r[0])) == 16

    r = process([104, 1125899906842624, 99])
    assert r[0] == 1125899906842624

