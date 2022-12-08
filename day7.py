from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generator, Iterable, Iterator, NamedTuple, Sequence, TypeAlias
from functools import reduce
from enum import Enum, auto
import io

Dir: TypeAlias = "dict[str, int | Dir]"
Path: TypeAlias = tuple[str, ...]

# TODO: would this be better with an immutable walker?
@dataclass
class FileSystem:
    children: Dir = field(init=False, default_factory=dict)
    "int for file size, or dict of children if dir"

    context: list[str] = field(init=False, default_factory=list)
    "dirs relative to root (empty list)"

    @property
    def cur_dir(self) -> Dir:
        cur = self.children
        for part in self.context:
            match cur.get(part):
                case None:
                    raise FileNotFoundError
                case int():
                    raise NotADirectoryError
                case dict() as children:
                    cur = children
                case _:
                    raise TypeError
        return cur

    def cd(self, target: str):
        match target:
            case "/":
                self.context.clear()
            case "..":
                self.context.pop()
            case _:
                self.context.append(target)
                # just to check.
                # this could be nicer. maybe related descriptors?
                _ = self.cur_dir

    def mkdir(self, name: str):
        curdir = self.cur_dir

        if name in curdir:
            raise FileExistsError(f"entry {name} already exists within {self.context}")

        curdir[name] = {}

    def fallocate(self, name: str, size: int):
        curdir = self.cur_dir

        if name in curdir:
            raise FileExistsError(f"entry {name} already exists within {self.context}")

        curdir[name] = size

    def parse(self, input: Iterable[str]):
        for line in input:
            line = line.strip()
            match line.split():
                case "$", "cd", target:
                    self.cd(target)
                case "$", "ls":
                    # the results are actually context-free, so we can skip this
                    pass
                case "dir", dirname:
                    self.mkdir(dirname)
                case size, name:
                    self.fallocate(name, int(size))

    def __str__(self):
        buf = io.StringIO()

        def print_tree(dir: Dir, indent: int):
            for name, member in sorted(dir.items(), key=lambda i: i[0]):
                if isinstance(member, int):
                    print(
                        " " * indent,
                        "- ",
                        name,
                        f" (file, size={member})",
                        sep="",
                        file=buf,
                        flush=True,
                    )
                elif isinstance(member, dict):
                    print(
                        " " * indent, "- ", name, " (dir)", sep="", file=buf, flush=True
                    )
                    print_tree(member, indent + 2)
                else:
                    raise TypeError

        print("- / (dir)", file=buf)
        print_tree(self.children, 2)

        return buf.getvalue()


def _all_file_sizes_below(dir: Dir) -> Iterable[int]:
    for member in dir.values():
        if isinstance(member, int):
            yield member
        elif isinstance(member, dict):
            yield from _all_file_sizes_below(member)
        else:
            raise TypeError


def dir_size(dir: Dir) -> int:
    return sum(_all_file_sizes_below(dir))


DIR_MAX_SIZE_TO_CONSIDER = 100_000


def _dir_size_depth_first(
    dir: Dir, path: tuple[str, ...]
) -> Generator[tuple[tuple[str, ...], int], None, int]:
    this_dir_sum = 0
    for name, member in dir.items():
        if isinstance(member, int):
            this_dir_sum += member
        elif isinstance(member, dict):
            member_sum = yield from _dir_size_depth_first(member, (*path, name))
            this_dir_sum += member_sum
        else:
            raise TypeError

    yield path, this_dir_sum
    return this_dir_sum


def sum_of_dirs_below_max(dir: Dir, path: tuple[str, ...]) -> int:
    return sum(
        (
            size
            for _, size in _dir_size_depth_first(dir, path)
            if size < DIR_MAX_SIZE_TO_CONSIDER
        )
    )


def part1():
    fs = FileSystem()
    with open("inputs/day7.txt") as f:
        fs.parse(f)
    print(sum_of_dirs_below_max(fs.children, tuple()))


TOTAL_DISK_SPACE = 70_000_000
NEEDED_FOR_UPDATE = 30_000_000


def _deletion_candidates(
    dir: Dir, current_available: int
) -> Iterable[tuple[Path, int]]:
    for path, size in _dir_size_depth_first(dir, tuple()):
        if size + current_available >= NEEDED_FOR_UPDATE:
            yield path, size


def smallest_that_fits(dir: Dir, current_available: int) -> int:
    return min((size for _, size in _deletion_candidates(dir, current_available)))


def part2():
    fs = FileSystem()
    with open("inputs/day7.txt") as f:
        fs.parse(f)

    used = dir_size(fs.children)

    print(smallest_that_fits(fs.children, TOTAL_DISK_SPACE - used))


class TEST:
    ROOT_SIZE = 48_381_165
    SUM_OF_DIRS_BELOW_MAX = 95_437
    AVAILABLE = 21_618_835
    assert AVAILABLE == TOTAL_DISK_SPACE - ROOT_SIZE

    DATA = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
