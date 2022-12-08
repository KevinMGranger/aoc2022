from __future__ import annotations
from typing import Iterable, NamedTuple


class Assignment:
    # all inclusive
    lower: int
    upper: int

    def __init__(self, lower: int, upper: int):
        if lower > upper:
            raise ValueError(f"{lower=} must be lower than {upper=}")

        super().__init__()

        self.lower = lower
        self.upper = upper

    def __contains__(self, other: object) -> bool:
        if not isinstance(other, Assignment):
            return NotImplemented
        return self.lower <= other.lower and other.upper <= self.upper

    def overlaps_with(self, other: Assignment) -> bool:
        lower_touches = self.lower >= other.lower and self.lower <= other.upper
        upper_touches = self.upper >= other.lower and self.upper <= other.upper
        return lower_touches or upper_touches

    @classmethod
    def from_str(cls, str_: str):
        left, right = str_.strip().split("-")
        return cls(int(left), int(right))

    def __str__(self):
        return f"{self.lower}-{self.upper}"


def assignment_pairs(f: Iterable[str]) -> Iterable[tuple[Assignment, Assignment]]:
    for line in f:
        line = line.strip()
        left, right = line.split(",")
        yield Assignment.from_str(left), Assignment.from_str(right)


def assignments(f: Iterable[str]) -> Iterable[Assignment]:
    for line in f:
        line = line.strip()
        left, right = line.split(",")

        yield Assignment.from_str(left)
        yield Assignment.from_str(right)


PART1_TEST_INPUT = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

PART1_TEST_ANSWER = 2


# def all_fully_contained(
#     assignments: Iterable[tuple[Assignment],
# ) -> Iterable[tuple[Assignment, Assignment]]:
#     for left, right in itertools.combinations(assignments, 2):
#         if left in right or right in left:
#             yield left, right


def all_fully_contained(
    assignments: Iterable[tuple[Assignment, Assignment]]
) -> Iterable[tuple[Assignment, Assignment]]:
    for left, right in assignments:
        if left in right or right in left:
            yield left, right


def touch_at_all(
    assignments: Iterable[tuple[Assignment, Assignment]]
) -> Iterable[tuple[Assignment, Assignment]]:
    for left, right in assignments:
        if left.overlaps_with(right) or right.overlaps_with(left):
            yield left, right


def test_part1():
    print(
        sum(
            1
            for _x in all_fully_contained(
                assignment_pairs(PART1_TEST_INPUT.splitlines())
            )
        )
    )


def test_part2():
    print(
        sum(1 for _x in touch_at_all(assignment_pairs(PART1_TEST_INPUT.splitlines())))
    )


def part1():
    with open("inputs/day4.txt") as f:
        print(sum(1 for _x in all_fully_contained(assignment_pairs(f))))

def part2():
    with open("inputs/day4.txt") as f:
        print(sum(1 for _x in touch_at_all(assignment_pairs(f))))

# all_fully_contained(PART1_TEST_INPUT.splitlines())
