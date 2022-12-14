import dataclasses
import time
from typing import List


@dataclasses.dataclass
class Item:
    worry_level: int

    def multiply(self, factor: int) -> None:
        self.worry_level *= factor

    def add(self, factor) -> None:
        self.worry_level += factor

    def is_divisible(self, factor) -> bool:
        return self.worry_level % factor == 0


@dataclasses.dataclass
class Monkey:
    items: List[Item]
    operand_1: int
    op: str
    operand_2: int
    test: int
    true_monkey: int
    false_monkey: int
    inspections: int = 0

    def calc_worry_level(self, item: Item) -> None:
        op2 = item.worry_level if self.operand_2 == -999 else self.operand_2
        if self.op == '*':
            item.multiply(op2)
        elif self.op == '+':
            item.add(op2)

    def receive_item(self, item: Item) -> None:
        self.items.append(item)

    def apply_test(self, new_worry_level: int) -> bool:
        return new_worry_level % self.test == 0

    def evaluate(self) -> None:
        while self.items:
            item = self.items.pop(0)
            self.calc_worry_level(item)
            if item.worry_level > all_monkey_divisibility:
                item.worry_level = item.worry_level % all_monkey_divisibility

            if item.is_divisible(self.test):
                monkeys[self.true_monkey].receive_item(item)
            else:
                monkeys[self.false_monkey].receive_item(item)
            self.inspections += 1


monkeys = []
with open('input.txt') as f:
    starting_items = []
    operand_1 = None
    op = None
    operand_2 = None
    test = None
    true_monkey = None
    false_monkey = None
    for line in f.readlines():
        trimmed = line.strip()
        if trimmed.find('Starting items') > -1:
            items_str = str(trimmed[trimmed.find(':') + 1:]).strip()
            starting_items = [Item(int(x)) for x in items_str.split(', ')]
        elif trimmed.find('Operation: ') > -1:
            parts = str(trimmed[trimmed.find('=') + 1:]).strip().split(' ')
            if parts[0] != 'old':
                operand_1 = int(parts[0])
            else:
                operand_1 = -999
            if parts[2] != 'old':
                operand_2 = int(parts[2])
            else:
                operand_2 = -999
            op = parts[1]
        elif trimmed.find('Test: ') > -1:
            test = int(str(trimmed[trimmed.find('by') + 3:]))
        elif trimmed.find('If true') > -1:
            true_monkey = int(str(trimmed[trimmed.find('monkey ') + 7:]))
        elif trimmed.find('If false') > -1:
            false_monkey = int(str(trimmed[trimmed.find('monkey ') + 7:]))
            monkey = Monkey(starting_items, operand_1, op, operand_2, test, true_monkey, false_monkey)
            monkeys.append(monkey)

all_monkey_divisibility = 1
for m in monkeys:
    all_monkey_divisibility *= m.test

for r in range(0, 10000):
    start = time.time()
    for monkey in monkeys:
        monkey.evaluate()

monkey_business_factor = 1
for inspections in sorted([monkey.inspections for monkey in monkeys], reverse=True)[:2]:
    print(f'Inspections = {inspections}')
    monkey_business_factor *= inspections

print(monkey_business_factor)
