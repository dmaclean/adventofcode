def main():
    with open("input.txt") as f:
        inputs = f.read().strip().split(",")

    print(sum([do_hash(i) for i in inputs]))


def do_hash(input_str: str) -> int:
    val = 0
    for c in input_str:
        print(f"\n\nProcessing {c}")
        ascii_code = ord(c)
        print(f"ASCII code for {c} is {ascii_code}")
        val += ascii_code
        print(f"Current value is now {val} after incrementing by ASCII code")
        val *= 17
        print(f"Current value is now {val} after multiplying by 17")
        val %= 256
        print(f"Current value is now {val} after modding by 256")
    return val


if __name__ == '__main__':
    main()
