import dataclasses
import re
from typing import List


@dataclasses.dataclass
class Lens:
    label: str
    focal_length: int

    def __str__(self):
        return f"[{self.label} {self.focal_length}]"


@dataclasses.dataclass
class Box:
    number: int
    lenses: List[Lens]

    def remove_lens(self, label: str) -> None:
        if not self.lenses:
            return
        for i in range(len(self.lenses)):
            lens = self.lenses[i]
            if lens.label == label:
                self.lenses.remove(lens)
                return

    def add_replace_lens(self, lens: Lens) -> None:
        for i in range(len(self.lenses)):
            if self.lenses[i].label == lens.label:
                self.lenses[i] = lens
                return

        # If we're here, that means we didn't find an existing lens
        # with the same label.  Just add this lens to the end
        self.lenses.append(lens)

    def calculate_focusing_power(self):
        power = 0
        for i in range(len(self.lenses)):
            power += (1 + self.number) * (i + 1) * self.lenses[i].focal_length
        return power

    def __str__(self):
        return f"Box {self.number} " + " ".join([lens.__str__() for lens in self.lenses])


def main():
    with open("input.txt") as f:
        inputs = f.read().strip().split(",")

    boxes = {i: Box(i, []) for i in range(256)}
    for i in inputs:
        parts = re.split("[=-]", i)
        label = parts[0]
        box_num = do_hash(label)

        box = boxes[box_num]
        if i.find("-") > -1:
            # Remove existing lens from box
            box.remove_lens(label)
        else:
            # Add or replace lens from box
            focal_length = int(parts[1])
            lens = Lens(label, focal_length)
            box.add_replace_lens(lens)
        print(box)

    print(sum([box.calculate_focusing_power() for box in boxes.values()]))


def print_boxes(boxes: List[Box]) -> None:
    for b in boxes:
        if not b.lenses:
            continue
        print(b)


def do_hash(input_str: str) -> int:
    val = 0
    for c in input_str:
        # print(f"\n\nProcessing {c}")
        ascii_code = ord(c)
        # print(f"ASCII code for {c} is {ascii_code}")
        val += ascii_code
        # print(f"Current value is now {val} after incrementing by ASCII code")
        val *= 17
        # print(f"Current value is now {val} after multiplying by 17")
        val %= 256
        # print(f"Current value is now {val} after modding by 256")
    return val


if __name__ == '__main__':
    main()
