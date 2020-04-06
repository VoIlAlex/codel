from .collector import FilesCollector
from abc import ABC, abstractmethod
from colored import fg, attr
import shutil


class _CollectorApplicable(ABC):
    @abstractmethod
    def apply(self, collector: FilesCollector) -> str:
        pass


class _Stylizer(_CollectorApplicable):
    def apply(self, collector: FilesCollector) -> str:
        result = ''
        for block in self.stylizer_blocks:
            result += block.apply(collector) + '\n'
        return result
