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


class Directory:
    def __init__(self, directory_path: str, safe: bool = True):
        if safe:
            assert os.path.isdir(directory_path)

        self.exists = os.path.exists(directory_path)
        self.directory_path = os.path.abspath(directory_path)
        self.directory_name = os.path.split(directory_path)

        files = os.listdir(self.directory_path)
        self.objects = []  # Files, Directories
        for file_name in files:
            file_path = os.path.join(self.directory_path, file_name)
            if os.path.isfile(file_path):
                obj = File(file_path)
            elif os.path.isdir(file_path):
                obj = Directory(file_path)
            else:
                continue
            self.objects.append(obj)

    def __iter__(self) -> Iterable[File]:
        for obj in self.objects:
            if isinstance(obj, File):
                yield obj
            if isinstance(obj, Directory):
                for file in obj:
                    yield file


class FilesCollector:
    def __init__(self,
                 folder_path: str = None,
                 ignore: List[str] = None,
                 extensions: List[str] = None):
        self.folder_path: str
        if folder_path is None:
            self.folder_path = os.getcwd()
        else:
            self.folder_path = os.path.abspath(folder_path)
        self.folder_name = os.path.split(self.folder_path)[-1]
        self.directory = Directory(self.folder_path)
        self.ignore = ignore if ignore else []
        self.extensions = extensions if extensions else []

    def __iter__(self):
        ignore_parser = IgnoreParser(self.ignore)
        for file in self.directory:
            if file.file_ext in self.extensions:
                if not ignore_parser.matches(file.file_path):
                    yield file
