"""Input is a map like:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............

Antennae are digits/characters (upper or lower cased).
Antennae of the same frequency are denoted by the same character.

Let `v` be the vector from the first to the second node of a given
freq. Anti-nodes of two antennae of the same freq. occur at `-v`
and `+2v` (the latter is equivalent to `+v` from the second node).

Antinodes are shown with hashes below:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.

Note that the topmost A also has an antinode (from 0s), but it is
not shown.

Compute the total number of **unique** antinodes on the map (including those with
antennae on the same position).
"""

from collections import defaultdict
from itertools import combinations


def read_input() -> dict[str, list[complex]]:
    character_position_map = defaultdict(list)
    lines = list(open("day_8_data.txt").read().split("\n"))
    grid_length = len(lines)
    for i, line in enumerate(lines):
        assert len(line) == grid_length, breakpoint()

        for j, char in enumerate(line):
            if char == ".":
                continue

            argand_position = i + (1j * j)
            character_position_map[char].append(argand_position)
    return character_position_map, grid_length


char_to_argand, grid_length = read_input()


def compute_antinode_positions(
    char_to_argand: dict[str, list[complex]],
) -> list[complex]:

    antinode_positions = []
    for argands in char_to_argand.values():
        for n1, n2 in combinations(argands, 2):
            n1_to_n2 = n2 - n1
            antinode1 = n1 - n1_to_n2
            antinode2 = n1 + 2 * n1_to_n2

            # sanity check vector maths
            assert antinode2 == n2 + n1_to_n2

            antinode_positions.append(antinode1)
            antinode_positions.append(antinode2)
    return antinode_positions


def is_in_grid(position: complex, max_real: int, max_imaginary: int) -> bool:
    """Return True for a value in [0..max_real) + [0..max_imaginary)j"""
    return all(
        (
            position.real >= 0,
            position.imag >= 0,
            position.real < max_real,
            position.imag < max_imaginary,
        )
    )


antinode_positions = compute_antinode_positions(char_to_argand)
unique_positions = set(antinode_positions)

part_one_solution = len(
    [
        x
        for x in unique_positions
        if is_in_grid(x, max_real=grid_length, max_imaginary=grid_length)
    ]
)
print(f"{part_one_solution=}")


"""Instead of antinodes occuring at -v and +2v, now they occur at any integer
multiple of v, including at +0v. Consequently, there are infinitely many antinodes
for any given pair. Fortunately, you can stop generating once you generate a node
which is not on the grid (any further nodes *in that direction* will also not be
on the grid)."""


def compute_antinode_positions_part_two(char_to_argand) -> list[complex]:
    antinode_positions = []
    for argands in char_to_argand.values():
        for n1, n2 in combinations(argands, 2):
            n1_to_n2 = n2 - n1
            coefficient = 0
            # generate antinodes in the negative direction
            while True:
                position = n1 + (coefficient * n1_to_n2)
                if not is_in_grid(position, grid_length, grid_length):
                    break

                antinode_positions.append(position)
                coefficient -= 1

            # generate antinodes in the positive direction
            # start from one -- we already have n1 in our antinode list
            # (minor optimisation since we will filter duplicates in any case)
            coefficient = 1
            while True:
                position = n1 + (coefficient * n1_to_n2)
                if not is_in_grid(position, grid_length, grid_length):
                    break

                antinode_positions.append(position)
                coefficient += 1
    return antinode_positions


antinode_positions_part_two = compute_antinode_positions_part_two(char_to_argand)
unique_positions_part_two = len(set(antinode_positions_part_two))
print(f"{unique_positions_part_two=}")
