import operator
from enum import Enum
import json
from typing import List


class Operator(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMPIFTRUE = 5
    JUMPIFFALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    RELBASE_OFFSET = 9
    HALT = 99


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


PARAM_LENGTHS = {
    Operator.ADD: 4,
    Operator.MULTIPLY: 4,
    Operator.INPUT: 2,
    Operator.OUTPUT: 2,
    Operator.JUMPIFTRUE: 3,
    Operator.JUMPIFFALSE: 3,
    Operator.LESS_THAN: 4,
    Operator.EQUALS: 4,
    Operator.RELBASE_OFFSET: 2,
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
        ParameterMode(nth_digit(p, 3)),
        ParameterMode(nth_digit(p, 4)),
        ParameterMode(nth_digit(p, 5)),
    ]
    return (opcode, modes)


def get_params(intcodes, pos: int, num: int):
    return intcodes[pos + 1 : pos + 1 + num]


def get_values(intcodes, params, modes):
    return [intcodes[x] if modes[i] else x for i, x in enumerate(params)]


def alloc(intcodes: List[int], idx: int):
    for i in range(len(intcodes), idx + 1):
        intcodes.append(0)


def get_param_value(intcodes: List[int], relbase: int, p: int, m: ParameterMode):
    if m is ParameterMode.POSITION:
        return intcodes[p]
    elif m == ParameterMode.IMMEDIATE:
        return p
    elif m == ParameterMode.RELATIVE:
        return intcodes[p + relbase]


def get_addr(intcodes: List[int], r: int, mode: ParameterMode, relbase: int):
    if mode is ParameterMode.POSITION:
        return r
    elif mode is ParameterMode.RELATIVE:
        alloc(intcodes, r + relbase)
        return r + relbase


def process(intcodes, inputs=[]):
    pos = 0
    relbase = 0
    outputs = []
    inputcount = 0

    while pos < len(intcodes):
        (opcode, modes) = parse_opcode(intcodes[pos])
        [m1, m2, m3] = modes
        op = Operator(opcode)
        params = get_params(intcodes, pos, PARAM_LENGTHS[op] - 1)

        if op is Operator.HALT:
            return outputs  # intcodes[:orglen]
        elif op is Operator.JUMPIFTRUE:
            [p1, p2] = params
            v1 = get_param_value(intcodes, relbase, p1, m1)
            v2 = get_param_value(intcodes, relbase, p2, m2)
            if v1:
                pos = v2
            else:
                pos += PARAM_LENGTHS[op]
        elif op is Operator.JUMPIFFALSE:
            [p1, p2] = params
            v1 = get_param_value(intcodes, relbase, p1, m1)
            v2 = get_param_value(intcodes, relbase, p2, m2)
            if not v1:
                pos = v2
            else:
                pos += PARAM_LENGTHS[op]
        elif op is Operator.LESS_THAN:
            [p1, p2, r] = params
            v1 = get_param_value(intcodes, relbase, p1, m1)
            v2 = get_param_value(intcodes, relbase, p2, m2)
            r = get_addr(intcodes, r, m3, relbase)
            intcodes[r] = 1 if v1 < v2 else 0
            pos += PARAM_LENGTHS[op]
        elif op is Operator.EQUALS:
            [p1, p2, r] = params
            if m1 == 0:
                alloc(intcodes, p1)
            if m2 == 0:
                alloc(intcodes, p2)
            alloc(intcodes, r)
            v1 = get_param_value(intcodes, relbase, p1, m1)
            v2 = get_param_value(intcodes, relbase, p2, m2)
            r = get_addr(intcodes, r, m3, relbase)
            intcodes[r] = 1 if v1 == v2 else 0
            pos += PARAM_LENGTHS[op]
        elif op is Operator.INPUT:
            [r] = params
            if len(inputs) > inputcount:
                i = inputs[inputcount]
                inputcount += 1
            else:
                i = int(input("input: "))

            r = get_addr(intcodes, r, m1, relbase)
            print("storing {} at {}".format(i, r))
            intcodes[r] = i
            pos += PARAM_LENGTHS[op]
        elif op is Operator.OUTPUT:
            [p1] = params
            v1 = get_param_value(intcodes, relbase, p1, m1)
            outputs.append(v1)
            pos += PARAM_LENGTHS[op]
        elif op is Operator.RELBASE_OFFSET:
            [p1] = params
            v1 = get_param_value(intcodes, relbase, p1, m1)
            relbase += v1
            pos += PARAM_LENGTHS[op]
        else:
            [p1, p2, r] = params
            if m1 == 0:
                alloc(intcodes, p1)
            if m2 == 0:
                alloc(intcodes, p2)
            alloc(intcodes, r)
            v1 = get_param_value(intcodes, relbase, p1, m1)
            v2 = get_param_value(intcodes, relbase, p2, m2)
            r = get_addr(intcodes, r, m3, relbase)
            intcodes[r] = ops[op](v1, v2)
            pos += PARAM_LENGTHS[op]

    return outputs


def main():
    with open("d9.json", "r") as f:
        intcodes = json.load(f)
        print(process(intcodes[:], [2]))


if __name__ == "__main__":
    main()
