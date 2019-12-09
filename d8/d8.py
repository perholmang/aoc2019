from typing import List
import functools
import numpy


def layer(data, i, len):
    return list(map(lambda x: int(x), list(data[i * len : (i + 1) * len])))


def load_image(data, w, h):
    layers = []
    for i in range(0, int(len(data) / (w * h))):
        layers.append(layer(data, i, w * h))

    return layers


def count_digits(layer: List[int], digit: int):
    return len(list(filter(lambda x: x == digit, layer)))


def cmp_minzeros(l1, l2):
    return count_digits(l1, 0) - count_digits(l2, 0)


def pixel(p):
    if p == 0:
        return " "
    elif p == 1:
        return "░"
    return " "


def matrix_filled(w, h, digit):
    output = []
    for i in range(0, h):
        output.append(list(map(lambda x: 2, list(range(0, w)))))
    return output


def render(layers: List[List[int]], w: int, h: int):
    output = matrix_filled(w, h, 2)

    for layer in layers:
        for y in range(0, h):
            for x in range(0, w):
                output[y][x] = layer[y * w + x] if output[y][x] == 2 else output[y][x]

    for row in output:
        for col in row:
            print(pixel(col), end="")
        print("")


def main():
    with open("image", "r") as f:
        contents = f.read()
        layers = load_image(contents, 25, 6)

        print("Part #1")
        [layer, *rest] = sorted(layers, key=functools.cmp_to_key(cmp_minzeros))
        print(count_digits(layer, 1) * count_digits(layer, 2))

        print("Part #2")
        render(layers, 25, 6)


if __name__ == "__main__":
    main()
