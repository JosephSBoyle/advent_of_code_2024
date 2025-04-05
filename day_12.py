MAP = {
    (i + 1j * j): char
    # for i, line in enumerate(open("day_12_test.txt").read().split())
    # for i, line in enumerate(open("day_12_test_2.txt").read().split())
    for i, line in enumerate(open("day_12.txt").read().split())
    for j, char in enumerate(line)
}
assert "\n" not in MAP  # otherwise you've parsed it wrong!

# 1. For each unique *value* (crop type) in M, find each of the contiguous
# plots.
# 2. For each of the plots, compute the area and the external perimeter.
# 3. Sum the product of the area and perimeter
# 4. Return the total of these sums for each plot, for each plot type.

T = set(MAP.values())
DIRECTIONS = (-1, +1, -1j, +1j)


def expand_plot(
    to_explore: list[complex],
    perimeter: int = 0,
    plot: list[complex] | None = None,
) -> set[complex]:
    """Recursively explore the map to get a plot of the type at position `m`."""
    if not plot:
        plot = to_explore.copy()

    while to_explore:
        position = to_explore.pop()
        tile_value = MAP[position]

        for direction in DIRECTIONS:
            next_tile = position + direction

            if next_tile in plot:
                # We've already expanded the proposed 'next' tile.
                continue

            if MAP.get(next_tile) == tile_value:
                # Add this to the plot and the list of tiles to explore
                plot.append(next_tile)
                to_explore.append(next_tile)
            else:
                perimeter += 1
    return plot, perimeter


EXPLORED: set[complex] = set()


cost = 0  # area * perimeter
n_plots = 0
for position in MAP:
    if position in EXPLORED:
        continue

    plot, perimeter = expand_plot([position])
    plot_fence_cost = len(plot) * perimeter
    type_ = MAP[position]
    print(f"{type_} area {len(plot)} * {perimeter=} = {plot_fence_cost=}")

    cost += plot_fence_cost
    n_plots += 1
    EXPLORED |= set(plot)

assert len(EXPLORED) == len(MAP)

print(f"{n_plots}")
print(f"{cost}")