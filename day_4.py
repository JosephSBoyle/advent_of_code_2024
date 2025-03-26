import numpy as np

test_input_1 = \
"""....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX"""
test_input_2 = \
"""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def _check_arrays_are_equal(a : np.array, b : np.array) -> bool:
    return (len(a) == len(b)) and (a == b).all()

def _count_xmas_occurrences(string : str) -> int:
    """There are eight allowed patterns:

    XMAS

    SMAX
    
    X
    M
    A
    S

    S
    A
    M
    X

    X
     M
      A
       S

       X
      M
     A
    S

    S
     A
      M
       X

       S
      A
     M
    X
    """
    # Load string into array
    array = np.array([[char for char in row] for row in string.split("\n")])
    print(array.shape)

    def _count_patterns(array : np.array, x : int, y : int) -> int:
        """Count the number of `XMAS` patterns eminating from `X` at `x`,`y`."""
        count = 0
        # Exclude `X` because our (x,y) coords start on an `X`
        pattern = np.array(["M", "A", "S"])

        # Patterns 1-4 (right/left/down/up) #
        right = array[y, (x + 1):(x+4)]
        count += _check_arrays_are_equal(right, pattern)
        
        left = array[y, (x-3):x]
        count += _check_arrays_are_equal(left , pattern[::-1])
        
        down = array[(y+1):(y+4), x]
        count += _check_arrays_are_equal(down , pattern)
        up   = array[(y-3):y, x]
        count += _check_arrays_are_equal(up   , pattern[::-1])

        #####################################
        # Patterns 5-8 (up_and_right/down_and_right/up_and_left/down_and_left)
        def _get_diagonal_array(array : np.array, x_ascending : bool, y_ascending : bool):
            
            try:
                values = []
                for i in range(1, 4):
                    y1 = y + i if y_ascending else y - i
                    x1 = x + i if x_ascending else x - i

                    if (y1 < 0) or (x1 < 0):
                        # Don't wrap around!
                        raise IndexError
                    values.append(array[y1, x1])
                return np.array(values)

            except IndexError:
                return np.array([])

        up_and_right = _get_diagonal_array(array,   x_ascending=True, y_ascending=False)
        count += _check_arrays_are_equal(up_and_right,   pattern)

        down_and_right = _get_diagonal_array(array, x_ascending=True, y_ascending=True)
        count += _check_arrays_are_equal(down_and_right, pattern)

        up_and_left = _get_diagonal_array(array,    x_ascending=False, y_ascending=False)
        count += _check_arrays_are_equal(up_and_left,    pattern)

        down_and_left = _get_diagonal_array(array,  x_ascending=False, y_ascending=True)
        count += _check_arrays_are_equal(down_and_left,  pattern)

        return count

    total_count = 0
    letter_X_positions : tuple[np.array, np.array] = np.where(array == "X")
    for y, x in zip(*letter_X_positions):
        assert array[y, x] == "X"

        count : int = _count_patterns(array, x, y)
        if count > 0:
            print(x, y, count)
        total_count += count

    # Always start with 'X' and check each pattern.
    # One 'X' can form multiple instances of XMAS
    # i.e. one up one down and so on.

    return total_count

test_output_1 = _count_xmas_occurrences(test_input_1)
test_output_2 = _count_xmas_occurrences(test_input_2)

assert test_output_1 == 18, test_output_1
assert test_output_2 == 18, test_output_2


input_ = open("day_4_data.txt", "r").read()
xmas_occurences = _count_xmas_occurrences(input_)

print(f"{xmas_occurences=}")
assert xmas_occurences == 2599

task_2_test_input = \
""".M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
.........."""

def _count_x_shaped_occurences(string : str) -> int:
    array = np.array([[char for char in row] for row in string.split("\n")])
    total_count = 0
    
    pattern_1 = np.array(["M","S"])
    pattern_2 = np.array(["S","M"])

    def _get_diagonal(array : np.array, x : int, y : int, main : bool) -> np.array:
        """Return a diagonal about point (x,y), with a point before and after.
        """
        try:
            if main:
                y0 = y - 1
                x0 = x - 1
                y1 = y + 1
                x1 = x + 1
            else:
                y0 = y - 1
                x0 = x + 1
                y1 = y + 1
                x1 = x - 1
            if any((
                y0 < 0,
                x0 < 0,
                y1 < 0,
                x1 < 0,
            )):
                raise IndexError
            return np.array([array[y0, x0], array[y1, x1]])
        except IndexError:
            return np.array([])

    def _count_patterns_around_central_point(
        array : np.array, x : int, y : int,
    ) -> int:
        count = 0

        main_diagonal = _get_diagonal(array, x, y, main=True) # in a matrix this is top-left to bottom-right
        off_diagonal  = _get_diagonal(array, x, y, main=False)
        if _check_arrays_are_equal(main_diagonal, pattern_1) or \
            _check_arrays_are_equal(main_diagonal, pattern_2):
            if _check_arrays_are_equal(off_diagonal, pattern_1) or \
                _check_arrays_are_equal(off_diagonal, pattern_2):
                count += 1
        return count

    letter_A_positions : tuple[np.array, np.array] = np.where(array == "A")
    for y, x in zip(*letter_A_positions):
        assert array[y, x] == "A"
        count : int = _count_patterns_around_central_point(array, x, y)
        total_count += count

    return total_count

assert _count_x_shaped_occurences(task_2_test_input) == 9
task_2_output = _count_x_shaped_occurences(input_)
print(f"{task_2_output=}")
