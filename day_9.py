"""Disk map

Alternates between digits representing file-size and
free-space size.

Each file as an associated incrementing integer ID,
starting at 0.

The map `12345` represents a disk with data blocks
(chars) and free-space blocks, denoted by `.`, for
example:

    `0..111....22222`

Move the file blocks from the end of the disk to the
first (leftmost) free space block until no space
remains. That is, until all blocks are contiguous and
all space blocks are on the right-hand side. i.e.

    `0..111....22222`
becomes
    `022111222......`

Once the disk blocks are compacted as above, find the first
block for each ID. Sum the product of it's position
(zero-indexed) with it's ID. Empty blocks do not contribute
to this sum.
"""

test_input_map = "12345"
test_case = "0..111....22222"


def read_disk_map(map_: str) -> list:
    id_ = 0  # incremental ID
    output = []
    for i, char in enumerate(map_):
        n = int(char)
        if i % 2 == 0:
            # even (incl. 0) -- data blocks
            output += [str(id_) for _ in range(n)]
            id_ += 1
        else:
            # odd -- space-blocks
            output += ["." for _ in range(n)]

    return output


blocks = read_disk_map(test_input_map)
assert blocks == list(test_case), blocks


def organise_blocks(blocks: list[str]) -> list[str]:
    """Re-organise blocks into a contiguous structure"""

    blocks = list(blocks)
    min_empty_block_index = 0
    for i in reversed(range(len(blocks))):
        char = blocks[i]
        if char == ".":
            continue

        # Iterate from the RHS to find the first non-empty block

        # Iterate from LHS up to the block we're trying to move
        # to find first empty block
        for j in range(min_empty_block_index, i):
            candidate_block = blocks[j]
            if candidate_block == ".":
                # swap the two blocks
                blocks[j] = char
                blocks[i] = "."

                # save where we found the empty block + 1-- this
                # is where we ought to begin our search next time!
                min_empty_block_index = j + 1

                # Only do exactly one 'swap'.
                break
    return blocks


def compute_checksum(blocks: str) -> int:
    # can use functools.reduce here alternatively.
    return sum([i * int(x) for i, x in enumerate(blocks) if x != "."])


test_case_organised = organise_blocks(test_case)
assert test_case_organised == list("022111222......"), test_case_organised

test_case_answer = compute_checksum("0099811188827773336446555566..............")
assert test_case_answer == 1928, test_case_answer


question_one_input = open("day_9_data.txt").read()
print("reading disk map...")
question_one_blocks = read_disk_map(question_one_input)

print("organising blocks...")
question_one_organised_blocks = organise_blocks(question_one_blocks)

print("computing checksum...")
question_one_answer = compute_checksum(question_one_organised_blocks)

print(f"{question_one_answer=}")
