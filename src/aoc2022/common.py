from __future__ import annotations
from typing import Iterable, NamedTuple
import traceback
import inspect
from textwrap import dedent


def _line_iter(path: str) -> Iterable[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()


def input(day: int | None = None) -> Iterable[str]:
    if day is None:
        stack = traceback.extract_stack()
        caller = stack[-2]
        caller_mod_name = inspect.getmodulename(caller.filename)
        if caller_mod_name is None:
            raise RuntimeError(
                f"can't get module name for caller at {caller.filename=}"
            )
        day = int(caller_mod_name.lstrip("day"))

    # a separate function / generator so the traceback or error is more predictable
    return _line_iter(f"inputs/day{day}.txt")



# COORDINATE SYSTEM:
# y / row-major, with the top being 0
# x / column-minor, with the leftmost being 0


class Vector(NamedTuple):
    x: int  # i.e. which column
    y: int  # i.e. which row

    @property
    def row(self):
        return self.y

    @property
    def column(self):
        return self.x
    
    def __sub__(self, other: Vector) -> Vector:
        x, y = self
        ox, oy = other
        return Vector(x - ox, y - oy)

__all__ = ["input", "dedent"]
