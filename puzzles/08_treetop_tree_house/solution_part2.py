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

best_score = 0
for i in range(0, num_rows):
    for j in range(0, num_cols):
        val = trees[i][j]

        # Look to the right
        right_score = 0
        if j < num_cols - 1:
            for k in range(j + 1, num_cols):
                right_score += 1
                if trees[i][k] >= val:
                    break

        # Look to the left
        left_score = 0
        if j > 0:
            for k in range(j - 1, -1, -1):
                left_score += 1
                if trees[i][k] >= val:
                    break

        # Look up
        up_score = 0
        if i > 0:
            for k in range(i - 1, -1, -1):
                up_score += 1
                if trees[k][j] >= val:
                    break

        # Look down
        down_score = 0
        if i < num_rows - 1:
            for k in range(i + 1, num_rows):
                down_score += 1
                if trees[k][j] >= val:
                    break

        curr_score = right_score * left_score * up_score * down_score
        if curr_score > best_score:
            best_score = curr_score

print(best_score)
