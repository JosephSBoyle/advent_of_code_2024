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

str2int2str = lambda s:  str(int(s))

def tick(l: list[str]) -> list[str]:
    """One tick AKA one blink."""
    o = []
    for stone in l:
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


tick_1 = tick(["125", "17"])
assert tick_1 == ["253000", "1", "7"], tick_1
tick_2 = tick(tick_1)

assert tick_2 == ["253", "0", "2024", "14168"], tick_2



def q1():
    l: list[str] = open("day_11.txt").read().split()
    for _ in range(25):
        l = tick(l)
    return len(l)


question_one_answer = q1()
print(f"{question_one_answer=}")
assert question_one_answer == 186_424
