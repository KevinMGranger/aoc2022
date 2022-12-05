from __future__ import annotations
import enum
import re
from typing import Iterable, NamedTuple, NewType, TypeAlias
from dataclasses import dataclass


class Instruction(NamedTuple):
    "An instruction to move crates."

    PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")

    count: int
    source: int
    target: int

    @classmethod
    def from_match(cls, match: re.Match):
        count, source, target = match.groups()
        return cls(int(count), int(source), int(target))

    @classmethod
    def from_line(cls, line: str):
        if not (match := cls.PATTERN.search(line)):
            raise ValueError(f"line didn't match pattern: {line}")
        else:
            return cls.from_match(match)


class LineType(NamedTuple):
    """
    What type of line was read from the file.
    """

    line: str

    @staticmethod
    def inspect(line: str) -> CrateLine | InstructionLine | ColumnNumbersLine | None:
        """
        Get the line type, or None if it's just an empty line.
        """
        if not line:
            return None

        match line.lstrip()[0]:
            case "1":
                return ColumnNumbersLine(line)
            case "[":
                return CrateLine(line)
            case "m":
                return InstructionLine(line)
            case _:
                raise ValueError("unknown line type")


class CrateLine(LineType):
    pass


class InstructionLine(LineType):
    pass


class ColumnNumbersLine(LineType):
    pass


Crate = NewType("Crate", str)

RowWiseCrates: TypeAlias = list[list[Crate | None]]


def crates_for_line(line: str) -> list[Crate | None]:
    """
    Extract the crates for the given line.
    Will return a list with each entry being the crate in that column.
    None means no crate is present, and a single letter string will be present otherwise.
    """
    line_len = len(line)
    crates: list[Crate | None] = []
    while len(line) >= 3:
        maybe_crate = line[:3]
        if maybe_crate == "   ":
            crates.append(None)
        else:
            crates.append(Crate(maybe_crate[1]))

        line = line[4:]  # 4 because of spaces in between

    if line:
        raise ValueError(f"line had unexpected number of characters: {line_len}")

    return crates


def crates_rowwise_to_columnwise(
    rowwise: RowWiseCrates,
) -> list[list[Crate]]:
    column_count = len(rowwise[0])
    columnwise: list[list[Crate]] = [list() for _count in range(0, column_count)]
    # go bottom up so we can just stack them
    for row in reversed(rowwise):
        for column_id in range(0, column_count):
            if (crate := row[column_id]) is None:
                continue
            else:
                columnwise[column_id].append(crate)

    return columnwise


@dataclass
class Warehouse:
    "A warehouse full of crates that can be moved around."

    crates: list[list[Crate]]
    "The crates by row and then column"

    def run(self, instructions: Iterable[Instruction]):
        for instruction in instructions:
            count, source, target = instruction

            # 1-ordinal to 0-indexing
            source -= 1
            target -= 1

            for _i in range(0, count):
                crate = self.crates[source].pop()
                self.crates[target].append(crate)
    
    def tops(self) -> str:
        msg = ""
        for column in self.crates:
            msg += column[len(column)-1]
        
        return msg



def parse(lines: Iterable[str]) -> tuple[Warehouse, list[Instruction]]:
    typed_lines = (
        line_type for line in lines if (line_type := LineType.inspect(line)) is not None
    )
    rowwise: RowWiseCrates = []
    columnwise: list[list[Crate]] = []
    instructions: list[Instruction] = []
    try:
        while isinstance(line := next(typed_lines), CrateLine):
            rowwise.append(crates_for_line(line.line))

        assert isinstance(line, ColumnNumbersLine)

        columnwise = crates_rowwise_to_columnwise(rowwise)

        while isinstance(line := next(typed_lines), InstructionLine):
            instructions.append(Instruction.from_line(line.line))

    except StopIteration:
        pass

    errs = []
    if not columnwise:
        errs.append(ValueError("no crates read"))
    if not instructions:
        errs.append(ValueError("didn't get instructions"))

    if errs:
        raise ExceptionGroup("parse error", errs)

    return Warehouse(columnwise), instructions


TEST_INPUT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

def part1():
    with open("inputs/day5.txt") as f:
        lines = (line.rstrip('\n') for line in f)
        warehouse, instructions = parse(lines)
    
    warehouse.run(instructions)

    print(warehouse.tops())