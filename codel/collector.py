import os
from colored import attr, fg
from .config import UnifiedConfiguration
from typing import Iterable, List
from .utils import IgnoreParser
from tqdm import tqdm
from multiprocessing import Pool, Manager, Process

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
    def __init__(self, directory_path: str, safe: bool = True, verbose: bool = False, multiproc: bool = False):
        if safe:
            assert os.path.isdir(directory_path)

        self.exists = os.path.exists(directory_path)
        self.directory_path = os.path.abspath(directory_path)
        self.directory_name = os.path.split(directory_path)

        files = os.listdir(self.directory_path)

        if verbose:
            print('Collecting files...')
            progress_bar = tqdm(total=len(files))

        self.objects = []  # Files, Directories

        def add_item_to_objects(file_path: str, objects: list = self.objects):
            if os.path.isfile(file_path):
                obj = File(file_path)
                objects.append(obj)
            elif os.path.isdir(file_path):
                obj = Directory(file_path)
                objects.append(obj)

        if not multiproc:
            for file_name in files:
                file_path = os.path.join(self.directory_path, file_name)
                if os.path.isfile(file_path):
                    obj = File(file_path)
                    self.objects.append(obj)
                elif os.path.isdir(file_path):
                    obj = Directory(file_path)
                    self.objects.append(obj)
                else:
                    continue
                if verbose:
                    progress_bar.update()

        if multiproc:
            with Manager() as manager:
                
                objects = manager.list()
                for file_name in files:
                    file_path = os.path.join(self.directory_path, file_name)
                    proc = Process(target=add_item_to_objects, args=(file_path, objects))
                    proc.start()
                    proc.join()
                    if verbose:
                        progress_bar.update()
                self.objects = list(objects)
                
        if verbose:
            progress_bar.close()

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
                 extensions: List[str] = None,
                 multiproc: bool = False):
        self.multiproc = multiproc
        self.folder_path: str
        if folder_path is None:
            self.folder_path = os.getcwd()
        else:
            self.folder_path = os.path.abspath(folder_path)
        self.folder_name = os.path.split(self.folder_path)[-1]
        self.directory = Directory(
            directory_path=self.folder_path, 
            verbose=True, 
            multiproc=self.multiproc
        )
        self.ignore = ignore if ignore else []
        self.extensions = extensions if extensions else []

    def __iter__(self):
        ignore_parser = IgnoreParser(self.ignore)
        for file in self.directory:
            if file.file_ext in self.extensions:
                if not ignore_parser.matches(file.file_path):
                    yield file
