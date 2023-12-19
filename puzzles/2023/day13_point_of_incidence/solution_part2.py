from typing import Optional, List, Tuple


def main():
    """
    The adjustment here for the second part is that we are forcing our solution to accept a
    match only if a smudge fix has taken place.  Any solutions that do not have the one smudge
    correction are ignored.
    """
    grids = []
    with open("input.txt") as f:
        grid = []
        for line in f.readlines():
            trimmed = line.strip()
            if trimmed == "":
                grids.append(grid)
                grid = []
            else:
                grid.append(list(trimmed))
        grids.append(grid)

    total_rows_above = 0
    total_columns_to_left = 0

    for grid in grids:
        columns_to_left, rows_above = process_grid(grid)
        total_rows_above += rows_above
        total_columns_to_left += columns_to_left

    print(total_columns_to_left + 100 * total_rows_above)


def evaluate_horizontal(grid: List[List[str]]) -> Optional[int]:
    """
    Check each horizontal line for possible reflections.

    This involves first iterating through the rows, and for each row evaluating the
    associated columns by taking one step away from the row being evaluated.  So, for
    row = 3, we'd evaluate reflections by comparing:
    - grid[2][col] and grid[3][col]
    - grid[1][col] and grid[4][col]
    - grid[0][col] and grid[5][col]

    We stop here because we've run out of space at the top of the grid.

    :param grid: The grid being evaluated
    :return: The row where we found a reflection, or None if no reflection found for horizontally.
    """

    for r in range(1, len(grid)):
        # Assemble columns above and below into lists,
        # then flip the list below so they can be properly compared
        is_match = True
        correction_made = False
        for c in range(len(grid[r])):
            step = 1
            while is_match and r - step >= 0 and r + (step - 1) < len(grid):
                # Make sure we don't go too far above or below
                above = grid[r - step][c]
                below = grid[r + step - 1][c]
                if above != below and correction_made:
                    # We've already encountered a correction for a smudge, so
                    # this can't be our solution.
                    is_match = False
                elif above != below:
                    # This is the first opportunity to fix a smudge.  Track the correction
                    # and continue on.
                    correction_made = True
                    step += 1
                else:
                    step += 1
            if not is_match:
                break

        if is_match and correction_made:
            # Only accept a solution if it's a match and a correction has been made.
            print(f"Rows above: {r}")
            return r
    return None


def evaluate_vertical(grid: List[List[str]]) -> Optional[int]:
    # Check columns
    grid_width = len(grid[0])
    for c in range(1, grid_width):
        is_match = True
        correction_made = False
        sz = min(c, grid_width - c)
        for r in range(len(grid)):
            left = grid[r][c - sz:c]
            right = grid[r][c:c + sz]
            right.reverse()
            if left != right and correction_made:
                # Correction has already been made.  Bail on this column.
                is_match = False
                break
            elif left != right:
                # Since we're grabbing entire row slices, we can't simply check for inequality, since
                # there could be multiple elements that are not equal.
                # Instead, iterate through the slices and track the mismatches to ensure we only have
                # one.
                bad_count = 0
                for i in range(len(left)):
                    if left[i] != right[i]:
                        bad_count += 1
                if bad_count > 1:
                    is_match = False
                    break
                else:
                    correction_made = True
        if is_match and correction_made:
            print(f"Columns to left: {c}")
            return c
    return None


def process_grid(grid: List[List[str]]) -> Tuple[int, int]:
    row_of_match = evaluate_horizontal(grid)
    if row_of_match:
        return 0, row_of_match
    else:
        col_of_match = evaluate_vertical(grid)
        return col_of_match, 0


if __name__ == '__main__':
    main()
