from itertools import combinations
from functools import reduce


example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

Point = tuple[int, int, int]


def three_d_euclidean_distance(point1: Point, point2: Point) -> float:
    distance = (
        (point2[0] - point1[0]) ** 2
        + (point2[1] - point1[1]) ** 2
        + (point2[2] - point1[2]) ** 2
    ) ** 0.5
    return distance


def p1(inp: str, nb_connections: int) -> int:
    points = [
        Point(map(int, line.split(","))) for line in inp.splitlines() if line.strip()
    ]
    connections = sorted(
        combinations(points, 2), key=lambda x: three_d_euclidean_distance(x[0], x[1])
    )[:nb_connections]
    circuits: list[set[Point]] = []
    for conn in connections:
        pt_a, pt_b = conn
        circuits_to_merge: list[int] = []
        for ind, circuit in enumerate(circuits):
            if pt_a in circuit or pt_b in circuit:
                circuits_to_merge.append(ind)
        if not circuits_to_merge:
            circuits.append({pt_a, pt_b})
        else:
            merged_circuit = {pt_a, pt_b}
            for i in circuits_to_merge:
                merged_circuit |= circuits[i]

            circuits = [
                c for i, c in enumerate(circuits) if i not in circuits_to_merge
            ] + [merged_circuit]
    largest_three = sorted(map(len, circuits))[-3:]
    ans = reduce(lambda x, y: x * y, largest_three)
    print(ans)
    return ans


def p1_with_clustering(): ...


def p2(inp: str) -> int:
    points = [
        Point(map(int, line.split(","))) for line in inp.splitlines() if line.strip()
    ]
    connections = sorted(
        combinations(points, 2), key=lambda x: three_d_euclidean_distance(x[0], x[1])
    )
    circuits: list[set[Point]] = [{pt} for pt in points]
    prev_nb_circuits = 0
    for ind, conn in enumerate(connections):
        pt_a, pt_b = conn
        circuits_to_merge: list[int] = []
        for ind, circuit in enumerate(circuits):
            if pt_a in circuit or pt_b in circuit:
                circuits_to_merge.append(ind)
        merged_circuit = {pt_a, pt_b}
        for i in circuits_to_merge:
            merged_circuit |= circuits[i]
        circuits = [
            c for i, c in enumerate(circuits) if i not in circuits_to_merge
        ] + [merged_circuit]
        if len(circuits) == 1 and prev_nb_circuits != 1:
            ans = pt_a[0] * pt_b[0]
            prev_nb_circuits = 1
        elif len(circuits) > 1:
            prev_nb_circuits = len(circuits)
    print(ans)
    return ans


if __name__ == "__main__":
    # assert p1(example, 10) == 40
    # p1(open("data/day8.txt", "r").read(), 1000)
    assert p2(example) == 25_272
    p2(open("data/day8.txt", "r").read())
