import dataclasses
import math
import time
from typing import List


@dataclasses.dataclass
class Item:
    base: int
    exponent: int
    multiplier: int
    remainder: int
    real_val: int

    def calc_val(self):
        if self.multiplier == 0:
            return (self.base ** self.exponent) + self.remainder
        return (self.base ** self.exponent) * self.multiplier + self.remainder

    def multiply(self, factor) -> None:
        if isinstance(factor, Item):
            # Passing the item itself, which means we're squaring it
            self.exponent *= 2
            self.multiplier = self.multiplier ** 2
            self.real_val *= self.real_val
            print(f'({self.base} - {factor}) after squaring: {self.real_val} vs {self.calc_val()}')

        else:
            self.real_val *= factor
            if self.multiplier == 0:
                self.multiplier = factor
            else:
                self.multiplier *= factor
            self.remainder *= factor
            # if self.remainder >= self.base:
            #     self.multiplier += self.remainder // self.base
            #     self.remainder = self.remainder % self.base
            # if self.multiplier >= self.base ** self.exponent:
            # Roll the multiplier up into an exponent
            # while
            # self.exponent += self.multiplier // self.base
            # self.multiplier = self.multiplier % self.base

            print(f'({self.base} - {factor}) after mult: {self.real_val} vs {self.calc_val()}')
        temp = 1

    def add(self, factor) -> None:
        self.real_val += factor
        self.remainder += factor
        # if self.remainder >= self.base:
        #     self.multiplier += self.remainder // self.base
        #     self.remainder = self.remainder % self.base
        print(f'({self.base} - {factor}) after adding: {self.real_val} vs {self.calc_val()}')

    def is_divisible(self, factor) -> bool:
        # if (self.base % factor == 0 or self.multiplier % factor == 0) and self.remainder == 0:
        # Either the base is divisible or the multiplier is
        # We can ignore the exponent because for any value it is still a multiple of the base
        #    return True
        #if self.repeated_squaring(factor) + self.remainder % factor == 0:
        if self.calc_val() % factor == 0:
            if self.real_val % factor != 0:
                print('we fucked up')
            return True
        if self.real_val % factor == 0:
            print('we fucked up')
        return False

    def repeated_squaring(self, modulo):
        mods = {
            0: 1
        }
        base_exp = 1
        while self.exponent >= base_exp:
            if base_exp == 1:
                mods[base_exp] = self.base % modulo
            else:
                mods[base_exp] = (mods[base_exp / 2] ** 2) % modulo
            base_exp *= 2

        bin_val = bin(self.exponent).replace('0b', '')
        bin_val_as_list = list(bin_val)
        bin_val_as_list.reverse()
        total = 1
        for i in range(0, len(bin_val_as_list)):
            mod = mods[int(math.pow(2, i))]
            val = int(bin_val_as_list[i])
            if val != 0:
                total *= val * mod

        if self.multiplier > 0:
            total *= (self.base * self.multiplier % modulo)
        return total % modulo


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
        op2 = item if self.operand_2 == -999 else self.operand_2
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

            if item.is_divisible(self.test):
                monkeys[self.true_monkey].receive_item(item)
            else:
                monkeys[self.false_monkey].receive_item(item)
            self.inspections += 1


# item = Item(7, 29, 0, 0)
# result = item.repeated_squaring(17)

monkeys = []
with open('sample_input.txt') as f:
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
            starting_items = [Item(int(x), 1, 0, 0, int(x)) for x in items_str.split(', ')]
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

for r in range(0, 20):
    start = time.time()
    for monkey in monkeys:
        monkey.evaluate()

monkey_business_factor = 1
for inspections in sorted([monkey.inspections for monkey in monkeys], reverse=True)[:2]:
    print(f'Inspections = {inspections}')
    monkey_business_factor *= inspections

print(monkey_business_factor)
