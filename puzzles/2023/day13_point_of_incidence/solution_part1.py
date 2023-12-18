def main():
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
        # Check rows
        is_match = True
        for r in range(1, len(grid)):
            # Assemble columns above and below into lists,
            # then flip the list below so they can be properly compared
            is_match = True
            for c in range(len(grid[r])):
                step = 1
                while is_match and r - step >= 0 and r + (step - 1) < len(grid):
                    # Make sure we don't go too far above or below
                    above = grid[r - step][c]
                    below = grid[r + step - 1][c]
                    if above != below:
                        is_match = False
                    else:
                        step += 1
                if not is_match:
                    break

            if is_match:
                total_rows_above += r
                print(f"Rows above: {r}")
                break

        if not is_match:
            # Check columns
            grid_width = len(grid[0])
            for c in range(1, grid_width):
                is_match = True
                sz = min(c, grid_width - c)
                for r in range(len(grid)):
                    left = grid[r][c - sz:c]
                    right = grid[r][c:c + sz]
                    right.reverse()
                    if left != right:
                        is_match = False
                        break
                if is_match:
                    total_columns_to_left += c
                    print(f"Columns to left: {c}")
                    break

    print(total_columns_to_left + 100 * total_rows_above)


if __name__ == '__main__':
    main()
