import operator
from enum import Enum
import json
import itertools


class Operator(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMPIFTRUE = 5
    JUMPIFFALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


PARAM_LENGTHS = {
    Operator.ADD: 4,
    Operator.MULTIPLY: 4,
    Operator.INPUT: 2,
    Operator.OUTPUT: 2,
    Operator.JUMPIFTRUE: 3,
    Operator.JUMPIFFALSE: 3,
    Operator.LESS_THAN: 4,
    Operator.EQUALS: 4,
    Operator.HALT: 0,
}


ops = {
    Operator.ADD: operator.add,
    Operator.MULTIPLY: operator.mul,
}


def nth_digit(p: int, n: int):
    return int((p / (10 ** (n - 1))) % 10)


def parse_opcode(p: int):
    opcode = p % 100
    modes = [
        nth_digit(p, 3),
        nth_digit(p, 4),
        nth_digit(p, 5),
    ]
    return (opcode, modes)


def get_params(intcodes, pos: int, num: int):
    return intcodes[pos + 1 : pos + 1 + num]


def get_values(intcodes, params, modes):
    return [intcodes[x] if modes[i] else x for i, x in enumerate(params)]


def process(intcodes, inputs=[]):
    pos = 0
    inputcount = 0
    outputs = []

    while pos < len(intcodes):
        (opcode, modes) = parse_opcode(intcodes[pos])
        [m1, m2, _] = modes
        op = Operator(opcode)

        params = get_params(intcodes, pos, PARAM_LENGTHS[op] - 1)

        if op is Operator.HALT:
            return outputs
        elif op is Operator.JUMPIFTRUE:
            [p1, p2] = params
            v1 = intcodes[p1] if m1 is 0 else p1
            v2 = intcodes[p2] if m2 is 0 else p2
            if v1:
                pos = v2
            else:
                pos += PARAM_LENGTHS[op]
        elif op is Operator.JUMPIFFALSE:
            [p1, p2] = params
            v1 = intcodes[p1] if m1 is 0 else p1
            v2 = intcodes[p2] if m2 is 0 else p2
            if not v1:
                pos = v2
            else:
                pos += PARAM_LENGTHS[op]
        elif op is Operator.LESS_THAN:
            [p1, p2, r] = params
            v1 = intcodes[p1] if m1 is 0 else p1
            v2 = intcodes[p2] if m2 is 0 else p2
            intcodes[r] = 1 if v1 < v2 else 0
            pos += PARAM_LENGTHS[op]
        elif op is Operator.EQUALS:
            [p1, p2, r] = params
            v1 = intcodes[p1] if m1 is 0 else p1
            v2 = intcodes[p2] if m2 is 0 else p2
            intcodes[r] = 1 if v1 == v2 else 0
            pos += PARAM_LENGTHS[op]
        elif op is Operator.INPUT:
            [r] = params
            if len(inputs) > inputcount:
                i = inputs[inputcount]
                inputcount += 1
            else:
                i = int(input("input: "))
            intcodes[r] = i
            pos += PARAM_LENGTHS[op]
        elif op is Operator.OUTPUT:
            [p1] = params
            print(intcodes[p1] if m1 is 0 else p1)
            outputs.append(intcodes[p1] if m1 is 0 else p1)
            pos += PARAM_LENGTHS[op]
        else:
            [p1, p2, r] = params
            v1 = intcodes[p1] if m1 is 0 else p1
            v2 = intcodes[p2] if m2 is 0 else p2
            intcodes[r] = ops[op](v1, v2)
            pos += PARAM_LENGTHS[op]
    return outputs


def amplify(intcodes, phase_setting):
    output = 0
    for p in phase_setting:
        [output] = process(intcodes, [p, output])
    return output


def main():
    m = 0
    with open("d7.json", "r") as f:
        intcodes = json.load(f)
        for p in list(itertools.permutations([0, 1, 2, 3, 4])):
            m = max(m, amplify(intcodes, p))

        print(m)


if __name__ == "__main__":
    main()
