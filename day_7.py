"""
1. ops are evaluated from left to right rather
    than precedence order
2. only add and multiply ops allowed.
3. if the LHS and RHS of the colon can be equal with any
    combination of ops, increment the sum by that amount.
"""

lines = open("day_7_data.txt").readlines()
total_part_two = 0
total_part_one = 0

ALLOWED_OPS_PART_ONE = (int.__add__, int.__mul__)


def _combinations(n_ops: int):
    # Use a binary representation:
    # 0,0,0; 0,0,1; 0,1,0; 0,1,1; ...; 1,1,1
    for value in range(2**n_ops):
        binary_representation = bin(value)[2:].zfill(n_ops)
        yield binary_representation


def _op_combinations_part_one(n_ops: int):
    for c in _combinations(n_ops):
        c = [ALLOWED_OPS_PART_ONE[int(o)] for o in c]
        yield c


def _can_reach_equality(
    lhs: int,
    rhs: list[int],
    combinations_generator,
) -> list[int] | None:
    """Return `True` if the rhs can be made to equal the lhs
    through a combination of the allowed operations"""

    # If there are n items in rhs, there are n-1 operators.
    n_operators = len(rhs) - 1
    for op_combination in combinations_generator(n_operators):
        rhs_running_total = rhs[0]

        for operand_two_index, op in enumerate(op_combination, start=1):
            rhs_running_total = op(rhs_running_total, rhs[operand_two_index])

        if lhs == rhs_running_total:
            return lhs


int_concat = lambda a, b: int(str(a) + str(b))
assert int_concat(1, 22) == 122
ALLOWED_OPS_PART_TWO = (int.__add__, int.__mul__, int_concat)


def _combinations_part_two(n: int):
    combinations = ["0", "1", "2"]
    for _ in range(n - 1):
        new_combinations = []
        for combo in combinations:
            new_combinations.append(combo + "0")
            new_combinations.append(combo + "1")
            new_combinations.append(combo + "2")
        combinations = new_combinations
    return combinations


def _op_combinations_part_two(n_ops: int):
    for c in _combinations_part_two(n_ops):
        c = [ALLOWED_OPS_PART_TWO[int(o)] for o in c]
        yield c


for l in lines:
    lhs, rhs = l.split(":")
    lhs = int(lhs)
    rhs = [int(x) for x in rhs.split()]

    if value := _can_reach_equality(lhs, rhs, _op_combinations_part_one):
        total_part_one += value

    if value := _can_reach_equality(lhs, rhs, _op_combinations_part_two):
        total_part_two += value

print(f"{total_part_one=}")
print(f"{total_part_two=}")
