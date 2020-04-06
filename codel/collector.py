import os
from colored import attr, fg
from .config import UnifiedConfiguration
from typing import Iterable, List
from .utils import IgnoreParser


class File:
    def __init__(self, file_path: str, safe: bool = True):
        if safe:
            assert os.path.isfile(file_path)
        self.exists = os.path.exists(file_path)
        self.file_path = os.path.abspath(file_path)
        self.file_name = os.path.split(file_path)[-1]
        self.file_ext = os.path.splitext(file_path)[-1]

    def count_lines(self) -> int:
        with open(self.file_path) as f:
            try:
                return sum(1 for _ in f)
            except Exception:
                return 0

    def __str__(self):
        return "{}{}{} - {}".format(
            fg(112) if self.exists else fg(196),
            self.file_name,
            attr(0),
            self.file_path)


