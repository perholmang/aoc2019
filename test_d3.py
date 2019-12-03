from d3 import build_grid, build_wires, closest_intersection


def test_build_wires():
    assert build_wires(0, 0, dx=2) == [(0, 0), (1, 0), (2, 0)]
    assert build_wires(1, 0, dx=2) == [(1, 0), (2, 0), (3, 0)]
    assert build_wires(0, 0, dy=3) == [(0, 0), (0, 1), (0, 2), (0, 3)]


def test_build_grid():
    assert build_grid("U1,R1,D1,L1") == [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert build_grid("U2,R2,D2,L2") == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 2),
        (2, 2),
        (2, 1),
        (2, 0),
        (1, 0),
    ]
    assert build_grid("R2,U2,L2,D2") == [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (1, 2),
        (0, 2),
        (0, 1),
    ]


def test_get_closest_intersection():
    assert (
        closest_intersection(
            build_grid("R75,D30,R83,U83,L12,D49,R71,U7,L72"),
            build_grid("U62,R66,U55,R34,D71,R55,D58,R83"),
        )
        == 159
    )
    assert (
        closest_intersection(
            build_grid("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"),
            build_grid("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),
        )
        == 135
    )
