# Get the sum of the middle page numbers for all valid updates
# Not all rules need to apply to a given update.
# There are potentially many rules and updates.
# X|Y and X|Z ... are possible

test_input = \
"""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

def _parse_rules(rules : str) -> dict:
    """Parse rules in format X|Y\nX|Z into a map X : [Y,Z]
    Exits when two succesive newlines are reached.
    """
    from collections import defaultdict
    precedences = defaultdict(list)
    for row in rules.split("\n"):
        left, right = map(int, row.split("|"))
        precedences[left].append(right)

    return precedences

from typing import Iterator

def _update_is_valid(update_pages, precedences) -> int:
    for index, update_page in enumerate(update_pages):
            # Pages which must be after the current page
        rule_after_pages = precedences[update_page]

        for update_before_page in update_pages[:index]:
            if update_before_page in rule_after_pages:
                return False
    return True

def _check_updates(updates : str, precedences : dict[int, list[int]]) -> Iterator[tuple[list[int], bool]]:
    """Return valid updates"""

    for update in updates.split("\n"):
        update_pages = list(map(int, update.split(",")))
        yield update_pages, _update_is_valid(update_pages, precedences)

def _sort_update(update_pages : list[int], precedences : dict) -> list[int]:
    """Apply ordering rules and return a valid update."""
    for update_index, update_page in enumerate(update_pages):
        rule_after_pages = precedences[update_page]

        for update_before_index, update_before_page in enumerate(update_pages[:update_index]):
            for rule_after_page in rule_after_pages:
                if rule_after_page == update_before_page:
                    # Invalid update.
                    # Swap positions
                    update_pages[update_index       ] = update_before_page
                    update_pages[update_before_index] = update_page
                    print(f"Swapping {update_before_page}@{update_before_index} with {update_page}@{update_index}")

                    # Reload values
                    update_page   = update_pages[update_index]
                    update_before = update_pages[update_before_index]


    # if _update_is_valid(update_pages, precedences):
    return update_pages

def _compute_sum_of_valid_update_middle_page_numbers(data : str, valid_updates : bool) -> int:
    rules, updates = data.split("\n\n")
    
    precedences  : dict                             = _parse_rules(rules)
    update_pairs : Iterator[tuple[list[int], bool]] = _check_updates(updates, precedences)

    if valid_updates:
        valid_updates = [update_pair[0] for update_pair in update_pairs if update_pair[1]]
        return sum(map(lambda update: update[len(update) // 2], valid_updates))
    else:
        invalid_updates = [update_pair[0] for update_pair in update_pairs if not update_pair[1]]
        from functools import partial
        valid_updates = map(partial(_sort_update, precedences=precedences), invalid_updates)
        return sum(map(lambda update: update[len(update) // 2], valid_updates))


test_output = _compute_sum_of_valid_update_middle_page_numbers(test_input, valid_updates=True)
assert test_output == 143, test_output 

input_ = open("day_5_data.txt", "r").read()

output_task_1 = _compute_sum_of_valid_update_middle_page_numbers(input_, valid_updates=True)
print(f"{output_task_1=}")

def _test_part_two(test_data : str):
    rules, updates = test_data.split("\n\n")
    
    precedences  : dict                             = _parse_rules(rules)

    s1 = _sort_update([75,97,47,61,53], precedences)
    s2 = _sort_update([61,13,29]      , precedences)
    s3 = _sort_update([97,13,75,29,47], precedences)
    assert s1 == [97,75,47,61,53], s1
    assert s2 == [61,29,13], s2
    assert s3 == [97,75,47,29,13], s3

_test_part_two(test_input)

output_task_2 = _compute_sum_of_valid_update_middle_page_numbers(input_, valid_updates=False)
print(f"{output_task_2=}")
