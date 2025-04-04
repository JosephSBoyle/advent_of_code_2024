"""
Each tick, the stones each simultaneously change according to the first applicable rule in this list:

1. If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.

2. If the stone is engraved with a number that has an even number of **digits**, it is replaced by two stones.
The left half of the digits are engraved on the new left stone, and the right half of the digits are
engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become
stones 10 and 0.)

3. If none of the other rules apply, the stone is replaced by a new stone; the old stone's
number multiplied by 2024 is engraved on the new stone.

No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.

"""

from functools import cache


str2int2str = lambda s: str(int(s))


@cache
def tick_stone(stone: str) -> list[str]:
    o = []
    if stone == "0":
        o.append("1")
    elif (len(stone) % 2) == 0:  # Stone has even length
        new_stone_len = len(stone) // 2

        s1 = "".join(list(stone)[:new_stone_len])
        s2 = "".join(list(stone)[new_stone_len:])
        o.append(str2int2str(s1))
        o.append(str2int2str(s2))
    else:
        o.append(str(int(stone) * 2024))
    return o


@cache
def compute_stones_after_n_ticks(stone: str, ticks: int) -> int:
    # Special case: bottom of the recursion
    if ticks == 1:
        if (len(stone) % 2) == 0:  # Stone has even length
            return 2
        else:
            return 1
    else:
        n = 0
        # General case -- more than one tick
        stones = tick_stone(stone)
        for stone in stones:
            n += compute_stones_after_n_ticks(stone, ticks - 1)

        return n


def compute_from_stones(stones: list[str], ticks: int) -> int:
    n = 0
    for stone in stones:
        n += compute_stones_after_n_ticks(stone, ticks)
    return n


STONES: list[str] = open("day_11.txt").read().split()


question_one_answer = compute_from_stones(STONES, 25)
question_two_answer = compute_from_stones(STONES, 75)

print(f"{question_one_answer=}")
print(f"{question_two_answer=}")

assert question_one_answer == 186_424
assert question_two_answer == 219_838_428_124_832
