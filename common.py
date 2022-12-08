from typing import Iterable
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

__all__ = ["input", "dedent"]