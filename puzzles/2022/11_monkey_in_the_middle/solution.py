import dataclasses
import re
from typing import List, Union


@dataclasses.dataclass
class Monkey:
    items: List[int]
    operand_1: Union[str, int]
    op: str
    operand_2: Union[str, int]
    test: int
    true_monkey: int
    false_monkey: int
    inspections: int = 0

    def calc_worry_level(self, old_worry_level: int) -> Union[int, float]:
        op1 = (old_worry_level if self.operand_1 == 'old' else self.operand_1)
        op2 = (old_worry_level if self.operand_2 == 'old' else self.operand_2)
        if self.op == '*':
            return op1 * op2
        elif self.op == '/':
            return op1 / op2
        elif self.op == '-':
            return op1 - op2
        elif self.op == '+':
            return op1 + op2

    def receive_item(self, item: int) -> None:
        self.items.append(item)

    def apply_test(self, new_worry_level: int) -> bool:
        return new_worry_level % self.test == 0

    def evaluate(self, monkeys: List["Monkey"]) -> None:
        while self.items:
            item = self.items.pop(0)
            new_worry_level = self.calc_worry_level(item)
            new_worry_level //= 3

            if self.apply_test(new_worry_level):
                monkeys[self.true_monkey].receive_item(new_worry_level)
            else:
                monkeys[self.false_monkey].receive_item(new_worry_level)
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
            starting_items = [int(x) for x in items_str.split(', ')]
        elif trimmed.find('Operation: ') > -1:
            parts = str(trimmed[trimmed.find('=') + 1:]).strip().split(' ')
            if parts[0] != 'old':
                operand_1 = int(parts[0])
            else:
                operand_1 = parts[0]
            if parts[2] != 'old':
                operand_2 = int(parts[2])
            else:
                operand_2 = parts[0]
            op = parts[1]
        elif trimmed.find('Test: ') > -1:
            test = int(str(trimmed[trimmed.find('by') + 3:]))
        elif trimmed.find('If true') > -1:
            true_monkey = int(str(trimmed[trimmed.find('monkey ') + 7:]))
        elif trimmed.find('If false') > -1:
            false_monkey = int(str(trimmed[trimmed.find('monkey ') + 7:]))
            monkey = Monkey(starting_items, operand_1, op, operand_2, test, true_monkey, false_monkey)
            monkeys.append(monkey)

for r in range(0, 20):
    for monkey in monkeys:
        monkey.evaluate(monkeys)

monkey_business_factor = 1
for inspections in sorted([monkey.inspections for monkey in monkeys], reverse=True)[:2]:
    print(f'Inspections = {inspections}')
    monkey_business_factor *= inspections

print(monkey_business_factor)
