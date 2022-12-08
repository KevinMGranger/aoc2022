from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generator, Iterable, Iterator, NamedTuple, Sequence, TypeAlias
from functools import reduce

Dir: TypeAlias = dict[str, int | "Dir"]


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
                case set() as children:
                    cur = children
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

def all_file_sizes_below(dir: Dir) -> Iterable[int]:
    for member in dir.values():
        if isinstance(member, int):
            yield member
        elif isinstance(member, dict):
            yield from all_file_sizes_below(member)


def dir_size(dir: Dir) -> int:
    return sum(all_file_sizes_below(dir))


DIR_MAX_SIZE_TO_CONSIDER = 100_000


def dirs_below_max_size_sizes(dir: Dir) -> Iterable[int]:
    ...


class TEST:
    ROOT_SIZE = 48381165
    ANSWER = 95437
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
