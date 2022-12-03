from typing import Iterable


def appears_in_both(line: str) -> str:
    line = line.strip()
    front, back = line[: len(line) // 2], line[len(line) // 2 :]
    return next(iter(set(front) & set(back)))


def priority(item: str) -> int:
    if ord("a") <= ord(item) <= ord("z"):
        return ord(item) - ord("a") + 1
    elif ord("A") <= ord(item) <= ord("Z"):
        return ord(item) - ord("A") + 27
    else:
        raise Exception("unreachable")


def priority_sum(f: Iterable[str], /) -> int:
    return sum((priority(appears_in_both(line)) for line in f))


TEST_INPUT_PART1 = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

TEST_ANSWER_PART1 = 157


def test() -> int:
    return priority_sum(TEST_INPUT_PART1.splitlines())


def part1():
    with open("inputs/day3.txt") as f:
        print(sum((priority(appears_in_both(line)) for line in f)))


def elf_groups(f: Iterable[str], /) -> Iterable[tuple[str, str, str]]:
    lines = (line.strip() for line in f)
    try:
        while True:
            one = next(lines)
            two = next(lines)
            three = next(lines)
            yield one, two, three
    except StopIteration:
        return


def common_item(one: str, two: str, three: str) -> str:
    return next(iter(set(one) & set(two) & set(three)))


PART2_TEST_INPUT_GROUP_1 = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg"""
PART2_TEST_INPUT_GROUP_2 = """wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

PART2_TEST_ANSWER = 70


def part2():
    with open("inputs/day3.txt") as f:
        print(sum(priority(common_item(*group)) for group in elf_groups(f)))
