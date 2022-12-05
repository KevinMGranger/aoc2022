from __future__ import annotations
import enum
import re
from typing import Iterable, NamedTuple
from dataclasses import dataclass


class Instruction(NamedTuple):
    count: int
    source: int
    target: int

    @classmethod
    def from_match(cls, match: re.Match):
        ...
        ...
        raise NotImplementedError("WIP")


def crates_for_line(line: str) -> list[str | None]:
    crates = []
    while len(line) >= 3:
        maybe_crate = line[:3]
        if maybe_crate == "   ":
            crates.append(None)
        else:
            crates.append(maybe_crate[1])

        line = line[4:]  # spaces in between

    if line:
        raise ValueError("line had unexpected number of characters")

    return crates


class LineType(enum.Enum):
    CRATES = enum.auto()
    INSTRUCTIONS = enum.auto()
    COLUMN_NUMBERS = enum.auto()

    @classmethod
    def inspect(cls, line: str) -> LineType | None:
        if not line:
            return None

        match line.lstrip()[0]:
            case "1":
                return cls.COLUMN_NUMBERS
            case "[":
                return cls.CRATES
            case "m":
                return cls.INSTRUCTIONS
            case _:
                raise ValueError("unknown line type")


INSTRUCTION_PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")

TEST_INPUT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


TEST_COLUMN_COUNT = 3
ACTUAL_COLUMN_COUNT = 9


@dataclass
class Warehouse:
    crates: list[list[str]]

    @classmethod
    def from_spec(cls, spec: Iterable[str]) -> Warehouse:
        lines = iter(spec)
        crate_lines = []
        # while 
        raise NotImplementedError("WIP")

    
    def run(self, instructions: Iterable[Instruction]):
        raise NotImplementedError("WIP")