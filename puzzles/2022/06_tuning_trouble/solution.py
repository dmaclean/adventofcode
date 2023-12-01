with open('input.txt') as f:
    data = f.readline()
    signal = list(data)
    start = 0
    while start < len(signal):
        if len(set(signal[start:start + 4])) == 4:
            print(start + 4)
            exit()
        start += 1