from __future__ import annotations
from common import input
from dataclasses import dataclass, field, replace
from typing import (
    NamedTuple,
    Self,
    overload,
    TypeVar,
    Generic,
)
from collections.abc import (
    Callable,
    Sequence,
    Iterable,
    Iterator,
    Reversible,
)
from enum import Enum, auto
from functools import partial, reduce
import operator
from textwrap import dedent
from itertools import product

# TODO: much of this was overcomplicated because I misidentified the problem in visible_in_dimension.

# COORDINATE SYSTEM:
# y / row-major, with the top being 0
# x / column-minor, with the leftmost being 0


class Coordinate(NamedTuple):
    x: int  # i.e. which column
    y: int  # i.e. which row

    @property
    def row(self):
        return self.y

    @property
    def column(self):
        return self.x


class Axis(Enum):
    X = auto()  # i.e. which columns
    Y = auto()  # i.e. which rows

    ROW = Y
    COLUMN = X


@dataclass
class CoordinateLine(Sequence[Coordinate], Reversible[Coordinate]):
    axis: Axis
    """
    locked coordinate dimension
    """

    fixed: int
    """
    Locked coordinate of axis.
    """

    start: int
    end_exclusive: int

    @property
    def forward(self) -> bool:
        return self.start <= self.end_exclusive

    def __iter__(self):
        nums = range(self.start, self.end_exclusive, 1 if self.forward else -1)

        return (
            (Coordinate(x=self.fixed, y=y) for y in nums)
            if self.axis is Axis.X
            else (Coordinate(x=x, y=self.fixed) for x in nums)
        )

    def __len__(self):
        return self.end_exclusive - self.start

    def __getitem__(self, index: int) -> Coordinate:
        return (
            Coordinate(x=self.fixed, y=index)
            if self.axis is Axis.X
            else Coordinate(x=index, y=self.fixed)
        )

    def __contains__(self, value: int | Coordinate) -> bool:
        if isinstance(value, int):
            return self.start <= value < self.end_exclusive
        elif isinstance(value, Coordinate):
            if self.axis is Axis.X:
                return self.fixed == value.x and value.y in self
            else:
                return self.fixed == value.y and value.x in self
        else:
            return NotImplemented

    def __reversed__(self) -> Self:
        if self.forward:
            # e.x. (1, 3) -> 1, 2
            # reversed: 2, 1 <- (2, 0, -1)
            return replace(
                self,
                start=self.end_exclusive - 1,
                end_exclusive=self.start - 1,
            )
        else:
            # e.x. (2, 0, -1) -> 2, 1
            # reversed (forwarded): (1, 3) -> 1, 2
            return replace(
                self,
                start=self.end_exclusive + 1,
                end_exclusive=self.start + 1,
            )


Data = TypeVar("Data")
T = TypeVar("T")


@dataclass
class SquareGrid(Generic[Data]):
    """
    An equal-two-dimensional, row-major grid.
    """

    rows: tuple[tuple[Data, ...], ...]

    def __len__(self):
        return len(self.rows)  # len(row) == len(column) always

    def __getitem__(self, coordinate: tuple[int, int]) -> Data:
        x, y = coordinate
        return self.rows[y][x]

    def row(self, row_num: int):
        return self.over(Axis.ROW, row_num)

    def column(self, column_num: int):
        return self.over(Axis.COLUMN, column_num)

    def over(self, axis: Axis, num: int):
        return SquareGridIterable(self, CoordinateLine(axis, num, 0, len(self)))

    @classmethod
    def from_rows(cls, list_: list[list[Data]]):
        return cls(tuple(tuple(x) for x in list_))

    def map(self, f: Callable[[Data], T]) -> tuple[tuple[T, ...], ...]:
        return tuple(tuple(f(data) for data in row) for row in self.rows)


@dataclass(frozen=True)
class SquareGridIterable(Reversible[tuple[Coordinate, Data]]):
    grid: SquareGrid[Data]

    coords: CoordinateLine

    def __len__(self):
        return len(self.grid)

    def __iter__(self) -> Iterator[tuple[Coordinate, Data]]:
        for coord in self.coords:
            data = self.grid[coord]
            yield coord, data

    def __reversed__(self):
        return replace(self, coords=reversed(self.coords))


class TreeWithHeight(tuple[int, int, int]):
    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def height(self):
        return self[2]

    @overload
    def __new__(cls, coord: Coordinate, height: int, /) -> Self:
        ...

    @overload
    def __new__(cls, x: int, y: int, height: int, /) -> Self:
        ...

    def __new__(cls, *args):
        match args:
            case Coordinate(x, y), int() as height:
                return super().__new__(cls, (x, y, height))
            case int() as x, int() as y, int() as height:
                return super().__new__(cls, (x, y, height))
            case _:
                raise TypeError

    @property
    def coordinate(self) -> Coordinate:
        return Coordinate(self.x, self.y)

    @property
    def coord(self):
        return self.coordinate

    def __repr__(self):
        return f"TreeWithCoordinate(x={self.x}, y={self.y}, height={self.height})"


@dataclass
class Forest(SquareGrid[int]):
    @classmethod
    def parse(cls, input: Iterable[str]):
        rows: list[list[int]] = []

        for row in input:
            row = row.strip()
            rows.append([int(num) for num in row])

        return cls.from_rows(rows)


class TEST:
    DATA = dedent(
        """
    30373
    25512
    65332
    33549
    35390
    """.strip()
    )
    ROW_1 = "30373"
    COLUMN_1 = "32633"


def visible_in_dimension(forest: Forest, axis: Axis, num: int) -> set[Coordinate]:
    """
    Coords of all trees visible across the line of forest given.
    Does _not_ include trees on edge.
    """
    trees = tuple(TreeWithHeight(*x) for x in forest.over(axis, num))

    current_max_height = trees[0].height
    visible_left: set[Coordinate] = set((trees[0].coord,))
    for tree in trees[1:-1]:
        if tree.height > current_max_height:
            visible_left.add(tree.coordinate)
            current_max_height = tree.height

    current_max_height = trees[-1].height
    visible_right: set[Coordinate] = set((trees[-1].coord,))
    for tree in trees[-1:0:-1]:
        if tree.height > current_max_height:
            visible_right.add(tree.coordinate)
            current_max_height = tree.height

    return visible_left | visible_right


def all_visible(forest: Forest) -> set[Coordinate]:
    visibles: list[set[Coordinate]] = []
    for i in range(0, len(forest)):
        visibles.append(visible_in_dimension(forest, Axis.ROW, i))
        visibles.append(visible_in_dimension(forest, Axis.COLUMN, i))

    return reduce(operator.or_, visibles)


def part1():
    forest = Forest.parse(input(8))
    print(sum(1 for _ in all_visible(forest)))


def scenic_score_for(forest: Forest, tree: TreeWithHeight) -> int:
    score = 1

    for axis, forward in product(Axis, (True, False)):
        match (axis, forward):
            case Axis.X, True:
                fixed = tree.x
                start = tree.y + 1
                end = len(forest)
            case Axis.X, False:
                fixed = tree.x
                start = tree.y - 1
                end = -1
            case Axis.Y, True:
                fixed = tree.y
                start = tree.x + 1
                end = len(forest)
            case Axis.Y, False:
                fixed = tree.y
                start = tree.x - 1
                end = -1
            case _:
                raise ValueError

        line = CoordinateLine(axis, fixed, start, end)

        can_see = 0
        for coord in line:
            can_see += 1

            height = forest[coord]
            if height >= tree.height:
                break

        score *= can_see

    return score


def scores(forest: Forest) -> Iterable[tuple[Coordinate, int]]:
    for x, y in product(range(0, len(forest)), range(0, len(forest))):
        tree = TreeWithHeight(x, y, forest[x, y])

        yield tree.coord, scenic_score_for(forest, tree)


def top_score(forest: Forest) -> tuple[Coordinate, int]:
    return max(scores(forest), key=lambda x: x[1])


def part2():
    forest = Forest.parse(input(8))
    print(top_score(forest)[1])
