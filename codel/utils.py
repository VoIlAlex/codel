import os
from gitignore_parser import (
    rule_from_pattern
)
from typing import List
from io import StringIO


def parse_gitignore_from_stream(stream, folder: str):
    rules = []
    counter = 0
    for line in stream:
        counter += 1
        line = line.rstrip('\n')
        rule = rule_from_pattern(line, folder,
                                 source=(os.path.join(folder, '.gitignore'), counter))
        if rule:
            rules.append(rule)
    return lambda file_path: any(r.match(file_path) for r in rules)


class IgnoreParser:
    def __init__(self, ignore: List[str], folder: str = None):
        self._ignore = ignore
        self._ignore_stream = StringIO('\n'.join(ignore))
        self._folder = folder if folder else os.getcwd()
        self._matches = parse_gitignore_from_stream(
            self._ignore_stream,
            self._folder
        )

    def matches(self, path: str):
        return self._matches(path)
