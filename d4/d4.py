import re


def no_decreasing_digits(num):
    orig = list(str(num))
    sorted = orig.copy()
    sorted.sort()

    return sorted == orig


def has_double_digits(num):
    c = 0
    for d in str(num):
        if int(d) == c:
            return True
        c = int(d)
    return False


def has_exact_double_digits(num):
    s = str(num)
    p = s[0]
    c = 1
    for char in s[1:]:
        if char == p:
            c += 1
        else:
            if c == 2:
                return True
            c = 1
        p = char
    if c == 2:
        return True
    return False


def main():
    numbers = range(183564, 657474)
    numbers = filter(no_decreasing_digits, numbers)
    numbers = list(filter(has_double_digits, numbers))
    print("Part #1: {}".format(len(numbers)))

    numbers = range(183564, 657474)
    numbers = filter(no_decreasing_digits, numbers)
    numbers = list(filter(has_exact_double_digits, numbers))
    print("Part #2: {}".format(len(numbers)))


if __name__ == "__main__":
    main()
