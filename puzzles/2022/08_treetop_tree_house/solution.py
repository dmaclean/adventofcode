trees = []
with open('input.txt') as f:
    for line in f.readlines():
        stripped = line.strip()
        if stripped == '':
            continue
        trees.append([int(tree) for tree in list(stripped)])

visible_trees = set()
num_cols = len(trees[0])
num_rows = len(trees)

# look at trees from left
r_idx = 0
for row in trees:
    c_idx = 0
    tallest = None
    for col in row:
        if tallest is None or tallest < col:
            visible_trees.add((r_idx, c_idx))
            tallest = col
        c_idx += 1
    r_idx += 1

# look at trees from right
for i in range(0, num_rows):
    # c_idx = 0
    tallest = None
    for j in range(num_cols - 1, -1, -1):
        val = trees[i][j]
        if tallest is None or tallest < val:
            visible_trees.add((i, j))
            tallest = val
        c_idx += 1
    r_idx += 1

# look at trees from top
for i in range(0, num_cols):
    tallest = None
    for j in range(0, num_rows):
        val = trees[j][i]
        if tallest is None or tallest < val:
            visible_trees.add((j, i))
            tallest = val

# look at trees from top
for i in range(0, num_cols):
    tallest = None
    for j in range(num_rows - 1, -1, -1):
        val = trees[j][i]
        if tallest is None or tallest < val:
            visible_trees.add((j, i))
            tallest = val

print(len(visible_trees))
print(visible_trees)
