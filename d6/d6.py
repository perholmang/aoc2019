MEMO = {}


def number_orbits(data, o):
    for orbiter in data.items():
        (f, t) = orbiter
        if o in t:
            if not o in MEMO:
                MEMO[o] = 1 + number_orbits(data, f)
            return MEMO[o]
    return 0


def calculate_orbits(data):
    total = 0
    for orbiter in data.items():
        (f, orbiters) = orbiter
        for o in t:
            total += number_orbits(data, o)
    return total


def build_data(lines):
    data = {}
    for line in lines:
        [f, t] = line.split(")")
        if not f in data:
            data[f] = []
        data[f].append(t)

    return data


def read_file(path):
    with open(path, "r") as f:
        contents = f.read()
        lines = contents.split("\n")
        return lines


def main():
    lines = read_file("d6.txt")
    # lines = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L".split("\n")
    data = build_data(lines)
    orbits = calculate_orbits(data, data["COM"])
    # print(number_orbits(data, "L"))
    print(orbits)
    # print(data)


if __name__ == "__main__":
    main()
