from d2 import process


def test_process():
    assert (process([1, 0, 0, 0, 99])) == [2, 0, 0, 0, 99]
    assert (process([2, 3, 0, 3, 99])) == [2, 3, 0, 6, 99]
    assert (process([2, 4, 4, 5, 99, 0])) == [2, 4, 4, 5, 99, 9801]
    assert (process([1, 1, 1, 4, 99, 5, 6, 0, 99])) == [30, 1, 1, 4, 2, 5, 6, 0, 99]

