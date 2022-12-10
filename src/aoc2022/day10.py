from __future__ import annotations
from .common import input
from dataclasses import dataclass
from functools import partial
from typing import Generator, Callable, Iterable, Iterator, NamedTuple, TypeAlias

OpGen: TypeAlias = Generator[None, None, None]


class Sample(NamedTuple):
    cycle: int
    start: int
    end: int


SampleGen: TypeAlias = Generator[Sample, None, None]


@dataclass
class VM:
    cycle: int = 1
    x: int = 1

    def addx(self, augend: int) -> OpGen:
        yield
        yield
        self.x += augend

    def noop(self) -> OpGen:
        yield

    def decode(self, instruction: str) -> Callable[[], OpGen]:
        match instruction.split():
            case "addx", augend:
                return partial(self.addx, augend=int(augend))
            case "noop",:
                return self.noop
            case _:
                raise ValueError(f"unknown instruction {instruction}")

    def cyclerator(self, op: OpGen) -> SampleGen:
        # the timing / before-after stuff gets wonky with a for loop.
        op.send(None)
        while True:
            startx = self.x
            try:
                op.send(None)
            except StopIteration:
                break
            finally:
                yield Sample(self.cycle, startx, self.x)
                self.cycle += 1

    def execute(self, program: Iterable[str]) -> SampleGen:
        # yield Sample(self.cycle, self.x, self.x)
        for instruction in program:
            op = self.decode(instruction)()
            yield from self.cyclerator(op)


def sample_is_in_right_cycle(sample: Sample) -> bool:
    mod = (sample.cycle % 40) - 20
    return mod == 0
    # return -1 <=  <= 1


def sample_score(sample: Sample) -> int:
    print("scoring sample", sample.cycle)
    return sample.cycle * sample.start


def program_score(program: Iterator[Sample]) -> int:
    return sum(sample_score(sample) for sample in program)


def part1():
    vm = VM()
    program = filter(sample_is_in_right_cycle, vm.execute(input()))
    print(program_score(program))


class TEST:
    SHORT_PROGRAM = """noop
addx 3
addx -5"""

    SHORT_CYCLE_TO_VALUE = {1: 1, 2: 1, 3: 4, 4: 4, 5: -1}

    LARGE_PROGRAM = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
