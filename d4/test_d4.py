from d4 import no_decreasing_digits, has_double_digits, has_exact_double_digits


def test_no_decreasing_digits():
    assert (no_decreasing_digits("123456")) == True
    assert (no_decreasing_digits("111111")) == True
    assert (no_decreasing_digits("112111")) == False


def test_has_double_digits():
    assert (has_double_digits("1123456")) == True
    assert (has_double_digits("123456")) == False
    assert (has_double_digits("101010")) == False


def test_has_exact_double_digits():
    assert (has_exact_double_digits("112233")) == True
    assert (has_exact_double_digits("123444")) == False
    assert (has_exact_double_digits("111122")) == True
