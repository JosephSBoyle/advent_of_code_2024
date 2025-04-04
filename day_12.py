MAP = {
    (i + 1j * j): char
    for i, line in enumerate(open("day_12.txt").readlines())
    for j, char in enumerate(line)
}

# 1. For each unique *value* (crop type) in M, find each of the contiguous
# plots.
# 2. For each of the plots, compute the area and the external perimeter.
# 3. Sum the product of the area and perimeter
# 4. Return the total of these sums for each plot, for each plot type.

T = set(MAP.values())
DIRECTIONS = (-1, +1, -1j, +1j)


def expand_plot(plot_stack: list[complex], perimeter: int = 0) -> set[complex]:
    """Recursively explore the map to get a plot of the type at position `m`."""
    position = plot_stack[-1]

    t = MAP[position]
    for direction in DIRECTIONS:
        next_tile = position + direction

        if next_tile in plot_stack:
            # We've already expanded the proposed 'next' tile.
            continue

        next_tile_value = MAP.get(next_tile)

        if next_tile_value == t:
            # Add this to the plot
            # expand that tile
            plot_stack.append(next_tile)
            plot_stack, perimeter = expand_plot(plot_stack, perimeter)
        else:
            perimeter += 1
    return plot_stack, perimeter


plot, perimeter = expand_plot([38 + 0j])
plot_area = len(plot)

assert plot_area == 1
assert perimeter == 4

# expanded_tiles = set()
checked_tiles: set[complex] = set()
for plot_type in T:
    # Find plots:
    for position in MAP:
        if position in checked_tiles:
            continue
        # recursively get

        checked_tiles.add(position)
