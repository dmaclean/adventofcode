MSG_LENGTH = 14
with open('input.txt') as f:
    data = f.readline()
    signal = list(data)
    start = 0
    while start < len(signal):
        if len(set(signal[start:start + MSG_LENGTH])) == MSG_LENGTH:
            # Converting the list slice to a set will eliminate any duplicate letters, so if
            # taking a slice of size four and converting it to a set yields the same size,
            # we know there are no duplicate letters.
            print(start + MSG_LENGTH)
            exit()
        start += 1