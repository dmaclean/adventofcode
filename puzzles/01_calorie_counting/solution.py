def main():
    elves = []  # Used to track total calories for each elf.  We'll sort this later to find the top-n elves.

    with open("input.txt") as f:
        curr_elf = []
        for line in f.readlines():
            if line.strip() == '':
                # This line only contains whitespace, which indicates we've reached the end of our current elf
                # Sum up all the calories collected so far and add that value to our elves list
                total_cals = sum(curr_elf)
                elves.append(total_cals)
                curr_elf = []
                continue
            item = int(line.replace('\n', ''))
            curr_elf.append(item)

    # Sort the calorie values in descending order to yield the top-n list
    sorted_elves = sorted(elves, reverse=True)
    print(sum(sorted_elves[:3]))


if __name__ == '__main__':
    main()
