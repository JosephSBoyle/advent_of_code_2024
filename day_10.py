"""The input comrpises a topographical map of integer digits.
Each digit represents an altitude, 0-9, indicating the altitude
of the given tile.

hiking trail:
- as long as possible
- up down left or right steps only (no diagonals)
- up by one altitude each step.

A trailhead is the beginning of a set of trails. It's score is
the number of `9` height positions which are reachable via a hiking
trail.

Compute the sum of scores for all trailheads.
"""

MapType = dict[complex, int]
"""Topographical of position (complex) to altitude (int)."""


def read_input(topographical_map: str) -> MapType:
    output = {}
    for i, line in enumerate(topographical_map.splitlines()):
        for j, char in enumerate(line):
            key = complex(i, j)
            output[key] = int(char)
    return output


def get_trailheads(map_: MapType) -> list[complex]:
    return [x for x in map_.keys() if map_[x] == 0]


def compute_reachable_tiles(
    map_: MapType,
    position: complex,
    reachable_tiles: set[complex] = None,
) -> set[complex]:
    """Compute the set of tile positions which are reachable given the
    requirement that each successive tile be of exactly `1` greater
    altitude than the last.
    """
    MOVES = (+1, -1, +1j, -1j)

    def compute_candidate_tiles(map_: MapType, position: complex) -> list[complex]:
        tiles = []
        desired_alt = map_[position] + 1
        for move in MOVES:
            try:
                candidate_alt = map_[(new_position := position + move)]
            except KeyError:
                continue
            if candidate_alt == desired_alt:
                tiles.append(new_position)
        return tiles

    if reachable_tiles is None:
        reachable_tiles = set()

    for tile in compute_candidate_tiles(map_, position):
        if tile not in reachable_tiles:
            compute_reachable_tiles(map_, tile, reachable_tiles)
            reachable_tiles.add(tile)
    return reachable_tiles


def compute_trail_tails(map_: MapType, reachable_tiles: set[complex]) -> int:
    tail_value = 9
    n = 0
    for position in reachable_tiles:
        if map_[position] == tail_value:
            n += 1
    return n


def part_one(map_: MapType) -> int:
    """Return the sum of scores for all trailheads"""
    n = 0
    for trailhead in get_trailheads(map_):
        reachable_tiles = compute_reachable_tiles(map_, trailhead)
        trail_tails = compute_trail_tails(map_, reachable_tiles)
        n += trail_tails
    return n


def part_two(map_: MapType) -> int:
    """A new way of valuing trailheads is their *rating*: the number of
    distinct trails which begin at the given trailhead.

    * positions can be used in multiple trails

    """

    class NoAddSet(set):
        def add(self, value) -> None:
            pass

    n = 0
    for trailhead in get_trailheads(map_):
        reachable_tiles = compute_reachable_tiles(
            map_, trailhead, reachable_tiles=NoAddSet()
        )
        trail_tails = compute_trail_tails(map_, reachable_tiles)
        n += trail_tails

    return n


with open("day_10.txt") as f:
    map_ = read_input(f.read())
    part_one_answer = part_one(map_)
    assert part_one_answer == 587
    print(f"{part_one_answer}")

    part_two_answer = part_one(map_)
    print(f"{part_two_answer}")
