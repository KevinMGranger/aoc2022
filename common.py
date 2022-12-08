from typing import Iterable

def input(day: int) -> Iterable[str]:
    with open(f"inputs/day{day}.txt") as f:
        for line in f:
            yield line.strip()