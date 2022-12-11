from common import input
from dataclasses import dataclass, field
from typing import Callable, NamedTuple, TypeAlias, Iterable, Self, TextIO
from io import StringIO
from functools import partial
import operator
from collections import deque
import sys


class Targets(NamedTuple):
    true: int
    false: int

    def to(self, result: bool) -> int:
        return self.true if result else self.false

class InspectionResult(NamedTuple):
    item: int
    target: int


Operation: TypeAlias = Callable[[int], int]
Test: TypeAlias = Callable[[int], bool]


@dataclass
class Monke:
    items: deque[int]
    operation: Operation
    test: Test
    targets: Targets

    inspection_count: int = field(init=False, default=0)

    @classmethod
    def parse(cls, spec: Iterable[str]) -> Self:
        speciter = iter(spec)

        starting_items = deque(
            int(item.strip()) for item in next(speciter).split(":")[1].strip().split(",")
            )
        op_spec = next(speciter).split("=").strip()
        test_num = int(next(speciter).split()[-1])
        true = int(next(speciter).split()[-1])
        false = int(next(speciter).split()[-1])

        return cls(starting_items, compile_op(op_spec), compile_test(test_num), Targets(true, false))

    def inspect_one(self) -> InspectionResult | None:
        try:
            item = self.items.popleft()
        except IndexError:
            return None

        item = self.operation(item)
        item //= 3

        result = self.test(item)
        target = self.targets.to(result)

        self.inspection_count += 1

        return InspectionResult(item, target)

    def take_turn(self) -> Iterable[InspectionResult]:
        while (result := self.inspect_one()) is not None:
            yield result


TOKEN_TO_OP: dict[str, Callable[[int, int], int]] = {
    "+": operator.add,
    "/": operator.floordiv,
    "-": operator.sub,
    "*": operator.mul,
}
OLD = "old"


def compile_op(op_spec: str) -> Operation:
    left, op_token, right = op_spec.strip().split()
    op = TOKEN_TO_OP[op_token]

    def _test(item: int) -> int:
        l = item if left == OLD else int(left)
        r = item if right == OLD else int(right)
        return op(l, r)

    return _test


def compile_test(divisor: int) -> Test:
    return lambda item: (item % divisor) == 0

@dataclass
class Circus:
    monkeys: list[Monke]
    rounds: int = field(init=False, default=0)

    @classmethod
    def parse(self, lines: Iterable[str]) -> Self:
        line_iter = iter(lines)

        next(line_iter) # skip first monke line

        monke_spec = []

        monkeys = []
        
        for line in line_iter:
            if line.startswith("Monke"):
                monkeys.append(Monke.parse(monke_spec))
                monke_spec = []
            else:
                monke_spec.append(line.strip())

        return cls(monkeys)

    def do_inspection_for(self, monke_id: int):
        monke = self.monkeys[monke_id]
        for item, target in monke.take_turn():
            self.monkeys[target].items.append(item)

    def do_round(self):
        for i in range(0, len(self.monkeys)):
            self.do_inspection_for(i)

        self.round += 1

    def status(self, out: TextIO = sys.stdout):
        for i, monkey in enumerate(self.monkeys):
            print("Monkey ", i, ": ", sep="", end="", file=out)
            print(*monkey.items, sep=", ", file=out)
        



class TEST:
    DATA = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

    EXAMPLE_STATUSES = """After round 1, the monkeys are holding items with these worry levels:

Monkey 0: 20, 23, 27, 26
Monkey 1: 2080, 25, 167, 207, 401, 1046
Monkey 2: 
Monkey 3: 


After round 2, the monkeys are holding items with these worry levels:
Monkey 0: 695, 10, 71, 135, 350
Monkey 1: 43, 49, 58, 55, 362
Monkey 2: 
Monkey 3: 

After round 3, the monkeys are holding items with these worry levels:
Monkey 0: 16, 18, 21, 20, 122
Monkey 1: 1468, 22, 150, 286, 739
Monkey 2: 
Monkey 3: 

After round 4, the monkeys are holding items with these worry levels:
Monkey 0: 491, 9, 52, 97, 248, 34
Monkey 1: 39, 45, 43, 258
Monkey 2: 
Monkey 3: 

After round 5, the monkeys are holding items with these worry levels:
Monkey 0: 15, 17, 16, 88, 1037
Monkey 1: 20, 110, 205, 524, 72
Monkey 2: 
Monkey 3: 

After round 6, the monkeys are holding items with these worry levels:
Monkey 0: 8, 70, 176, 26, 34
Monkey 1: 481, 32, 36, 186, 2190
Monkey 2: 
Monkey 3: 

After round 7, the monkeys are holding items with these worry levels:
Monkey 0: 162, 12, 14, 64, 732, 17
Monkey 1: 148, 372, 55, 72
Monkey 2: 
Monkey 3: 

After round 8, the monkeys are holding items with these worry levels:
Monkey 0: 51, 126, 20, 26, 136
Monkey 1: 343, 26, 30, 1546, 36
Monkey 2: 
Monkey 3: 

After round 9, the monkeys are holding items with these worry levels:
Monkey 0: 116, 10, 12, 517, 14
Monkey 1: 108, 267, 43, 55, 288
Monkey 2: 
Monkey 3: 

After round 10, the monkeys are holding items with these worry levels:
Monkey 0: 91, 16, 20, 98
Monkey 1: 481, 245, 22, 26, 1092, 30
Monkey 2: 
Monkey 3: 

...

After round 15, the monkeys are holding items with these worry levels:
Monkey 0: 83, 44, 8, 184, 9, 20, 26, 102
Monkey 1: 110, 36
Monkey 2: 
Monkey 3: 

...

After round 20, the monkeys are holding items with these worry levels:
Monkey 0: 10, 12, 14, 26, 34
Monkey 1: 245, 93, 53, 199, 115
Monkey 2: 
Monkey 3:"""