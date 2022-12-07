from __future__ import annotations
from dataclasses import dataclass, field
from typing import NamedTuple
from enum import Enum


class ChdirTarget(Enum):
    ROOT = "/"
    PARENT = ".."


class ChdirCommand(NamedTuple):
    target: ChdirTarget | str


class ListCommand(NamedTuple):
    pass


class ListEntry:
    class File(NamedTuple):
        size: int
        name: str

    class Dir(NamedTuple):
        name: str


class Path(tuple[str, ...]):
    def __new__(cls, *elts: str):
        inst = super().__new__(cls, elts)
        return inst

    def cd(self, child: str) -> Path:
        return Path(*self, child)

    def __str__(self):
        return "/" + "/".join(self)

    @property
    @classmethod
    def ROOT(cls):
        return cls("/")

    @property
    def parent(self):
        return Path(*self[:-1])


@dataclass
class FileSystem:
    files: dict[Path, int | set[str]] = field(
        init=False, default_factory=lambda: {Path.ROOT: set()}
    )
    "int for file size, or set of children if directory"
    context: Path = Path.ROOT

    def cd(self, target: ChdirTarget | str):
        match target:
            case ChdirTarget.ROOT:
                self.context = Path.ROOT
            case ChdirTarget.PARENT:
                self.context = self.context.parent
            case str():
                target_path = self.context.cd(target)
                if target_path not in self.files:
                    raise FileNotFoundError(f"Unknown child {target} in {self.context}")
                if not isinstance(self.files[target_path], set):
                    raise NotADirectoryError(
                        f"child {target} is a file, not a directory within {self.context}"
                    )

                self.context = target_path

    def get_dir_handle(self, path: Path) -> set[str]:
        match self.files.get(path):
            case None:
                raise FileNotFoundError(f"no dir at {path} found")
            case int():
                raise NotADirectoryError(f"file at {path} was not a directory")
            case set() as children:
                return children

    def children_handle(self) -> set[str]:
        return self.get_dir_handle(self.context)

    def mkdir(self, name: str):
        children = self.children_handle()
        target_path = self.context.cd(name)

        if target_path in self.files:
            raise FileExistsError(f"entry {name} already exists within {self.context}")

        self.files[target_path] = set()
        children.add(name)

    def fallocate(self, name: str, size: int):
        children = self.children_handle()
        target_path = self.context.cd(name)

        if target_path in self.files:
            raise FileExistsError(f"entry {name} already exists within {self.context}")
        self.files[target_path] = size
