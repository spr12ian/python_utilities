#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pathlib import Path


class Tree:
    def __init__(self) -> None:
        self.ignoreList: list[str] = []
        self.file_suffixes = {}

    def ignore(self, patterns: list[str]) -> None:
        self.ignoreList.extend(patterns)

    def register(self, path: Path) -> None:
        if not path.is_dir():
            if len(path.suffix) > 0:
                suffix = path.suffix.lower()
            else:
                suffix = "No suffix"

            self.file_suffixes[suffix] = self.file_suffixes.get(suffix, 0) + 1

    def summary(self):
        return f"File types found: {len(self.file_suffixes)}\n" + \
               "\n".join(f"{ext}: {count}" for ext, count in sorted(self.file_suffixes.items()))

    def walk(self, directory: Path, prefix: str = "") -> None:
        entries = sorted([entry for entry in directory.iterdir() if not entry.name.startswith(".")])

        for index, entry in enumerate(entries):
            if entry.name in self.ignoreList:
                continue

            self.register(entry)

            connector = "└── " if index == len(entries) - 1 else "├── "
            print(prefix + connector + entry.name)

            if entry.is_dir():
                new_prefix = prefix + ("    " if index == len(entries) - 1 else "│   ")
                self.walk(entry, new_prefix)


if len(sys.argv) > 1:
    directory = Path(sys.argv[1]).resolve()
else:
    directory = Path(".").resolve()
print(f"Starting from: {directory}")
ignore_directories = [".git", ".hg", ".mypy_cache", ".svn", "__pycache__", "venv"]
print(f"Ignoring: {ignore_directories}")

tree = Tree()
tree.ignore(ignore_directories)
tree.walk(directory)
print("\n" + tree.summary())
