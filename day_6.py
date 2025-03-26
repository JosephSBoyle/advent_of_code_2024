import numpy as np


test_input = \
"""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def _count_positions_visited(data : str) -> int:
    """A guard starts facing upwards, denoted by `^`.

    She walks forwards unless there is an obstacle denoted by `#` in the
    direction she is facing, in which case she turns right, ^, >, v, <.

    Eventually she leaves the area by moving outside of the map.
    Count the number of positions she visits in total (including her
    starting position).
    """
    def _get_positions(array):
        for character, next_character, move in (
                ("^", ">", (0, -1)),
                (">", "v", (+1, 0)),
                ("v", "<", (0, +1)),
                ("<", "^", (-1, 0)),
            ):
            xy = np.where(array == character)
            try:
                # The character was found
                x = xy[0][0]
                y = xy[1][0]
                x_next = x + move[1]
                y_next = y + move[0]
                return character, next_character, x, y, x_next, y_next
            except IndexError:
                pass
        raise ValueError("No character found in the array %s", array)
 
    array = np.array([list(row) for row in data.split()])

    while 1:
        character, next_character, x, y, x_next, y_next = _get_positions(array)
        # print(character, next_character, x, y, x_next, y_next)

        try:
            if array[x_next, y_next][0] == "#":
                array[x, y] = next_character
            else:
                array[x, y] = "X"
                # move to the next position
                array[x_next, y_next] = character
        except IndexError:
            # The last position will not have an `X`
            return (array == "X").sum() + 1

print(test_input)
test_output = _count_positions_visited(test_input)
assert test_output == 41, test_output

data          = open("day_6_data.txt", "r").read()
part_1_output = _count_positions_visited(data)
print(f"{part_1_output=}")


# Part 2
...
