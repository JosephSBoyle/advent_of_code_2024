A_TOKENS = 3
B_TOKENS = 1
MAX_PRESSES = 100


def parse_into_machines_strings(input_: str) -> list[str]:
    return input_.split("\n\n")


def parse_machine(machine: str) -> tuple[complex]:
    # Assume no EOL char.
    # Assume positive only translations in both dims.
    # Assume translations of exactly two digits (10..99)
    a, b, target = machine.split("\n")

    # TODO: regex this
    a = int(a[-9:-6]), int(a[-2:])
    b = int(b[-9:-6]), int(b[-2:])
    target_x = int(target.split(",")[0].split("=")[1])
    target_y = int(target.rsplit("=")[-1])

    target = target_x, target_y
    return complex(*a), complex(*b), complex(*target)


def cheapest_solution_for_machine(a: complex, b: complex, target: complex) -> int:
    """Return the cheapest solution measured in tokens or zero, if no solN
    exists."""
    cheapest_solution = None
    # itertools product?
    for x1 in range(0, 101):
        for x2 in range(0, 101):
            position = (x1 * a) + (x2 * b)
            if position == target:
                cost = (x1 * A_TOKENS) + (x2 * B_TOKENS)
                if cheapest_solution is None or cost < cheapest_solution:
                    cheapest_solution = cost

    return cheapest_solution or 0


def part_one(input_ : list[str]):
    test_machines = [parse_machine(s) for s in parse_into_machines_strings(input_)]
    print(test_machines)

    total_tokens = 0
    for m in test_machines:
        total_tokens += cheapest_solution_for_machine(*m)
    print(f"{total_tokens=}")

part_one(open("day_13_test.txt").read())
part_one(open("day_13.txt").read())
