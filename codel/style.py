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


class _FolderNameStylizerBlock(_CollectorApplicable):
    def apply(self, collector: FilesCollector) -> str:
        return '{}{}Directory:{} {}'.format(
            fg(149),
            attr(1),
            attr(0),
            collector.folder_name
        )


class _FolderPathStylizerBlock(_CollectorApplicable):
    def apply(self, collector: FilesCollector) -> str:
        return '{}{}Path:{} {}'.format(
            fg(149),
            attr(1),
            attr(0),
            collector.folder_path
        )


class _ExtensionsStylizerBlock(_CollectorApplicable):
    def apply(self, collector: FilesCollector) -> str:
        return '{}{}Extensions:{} {}'.format(
            fg(149),
            attr(1),
            attr(0),
            ', '.join(collector.extensions)
        )


class _IgnoreStylizerBlock(_CollectorApplicable):
    def apply(self, collector: FilesCollector) -> str:
        return '{}{}Ignore: {}{}'.format(
            fg(149),
            attr(1),
            attr(0),
            ', '.join(collector.ignore)
        )


