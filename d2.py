import operator
import json


ops = {
    1: operator.add,
    2: operator.mul,
}


def process(intcodes):
    pos = 0
    while pos < len(intcodes):
        op = intcodes[pos]
        if op is 99:
            return intcodes

        p1 = intcodes[pos + 1]
        p2 = intcodes[pos + 2]
        r = intcodes[pos + 3]

        intcodes[r] = ops[op](intcodes[p1], intcodes[p2])
        pos += 4
    return intcodes


def main():
    with open("d2.json", "r") as f:
        intcodes = json.load(f)
        r = process(intcodes[:])
        print(r[0])

    for i in range(0, 99):
        for j in range(0, 99):
            a = intcodes[:]
            a[1] = i
            a[2] = j
            r = process(a)
            if r[0] == 19690720:
                print("noun: {}, verb: {}".format(i, j))


if __name__ == "__main__":
    main()

