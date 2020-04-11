from .collector import FilesCollector
from abc import ABC, abstractmethod
from colored import fg, attr
import shutil
from tqdm import tqdm


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


class _LinesStylizerBlock(_CollectorApplicable):
    def __init__(self, short: bool = False):
        self.short = short

    def apply(self, collector: FilesCollector) -> str:
        result = ''

        # Sort files by extension
        files = [f for f in collector]
        files.sort(key=lambda f: f.file_ext)

        # Info about screen to
        # make result prettier
        terminal_size = shutil.get_terminal_size()

        print('Counting lines')
        progress_bar = tqdm(total=len(files))

        # Resultant variables
        lines_mean = None
        total_lines = 0

        # Temp variables
        # for current extension
        current_ext = None
        extension_result = ''
        extension_lines = 0
        extension_files_count = 0

        for i, file in enumerate(files, 0):
            if file.file_ext != current_ext:
                if i != 0:
                    # Complete extension result
                    # with header (summary)
                    extension_result = (
                        terminal_size.columns - 1) * '-' + '\n' + extension_result
                    extension_result = '\n{}{} - {} files - {} lines{}\n'.format(
                        attr(1),
                        current_ext,
                        extension_files_count,
                        extension_lines, attr(0)
                    ) + extension_result

                    # Save to overall variables
                    result += extension_result
                    total_lines += extension_lines

                    # Refresh temp variables
                    extension_result = ''
                    extension_lines = 0
                    extension_files_count = 0

                current_ext = file.file_ext

            file_lines = file.count_lines()

            # Update mean of lines count
            if lines_mean is None:
                lines_mean = file_lines
            else:
                lines_mean = (lines_mean * i + file_lines) / (i + 1)

            # Write info about each
            # file to result if required
            if not self.short:
                extension_result += '{: <40} -> {}\n'.format(
                    file.file_name, file_lines)

            # Update extension variables
            extension_lines += file_lines
            extension_files_count += 1

            # Move progress bar
            progress_bar.update()

        else:
            # Save extension variables
            # to resultant variables
            extension_result = (
                terminal_size.columns - 1) * '-' + '\n' + extension_result
            extension_result = '\n{}{} - {} files - {} lines{}\n'.format(
                attr(1),
                current_ext,
                extension_files_count,
                extension_lines, attr(0)
            ) + extension_result
            result += extension_result
            total_lines += extension_lines
            if lines_mean is None:
                lines_mean = 0

        result += '\n'

        result += '{}{}Files{} -> {}{}{}\n'.format(
            fg(149),
            attr(1),
            attr(0),
            attr(1),
            len(files),
            attr(0)
        )
        result += '{}{}Lines/File{} -> {}{}{}\n'.format(
            fg(149),
            attr(1),
            attr(0),
            attr(1),
            lines_mean,
            attr(0)
        )
        result += '{}{}Total Count{} -> {}{}{}'.format(
            fg(149),
            attr(1),
            attr(0),
            attr(1),
            total_lines,
            attr(0)
        )

        progress_bar.close()

        return result


class _BlankLineStylizerBlock(_CollectorApplicable):
    def apply(self, collector: FilesCollector) -> str:
        return '\n'


class DefaultStylizer(_Stylizer):
    def __init__(self, short: bool = False):
        self.stylizer_blocks = [
            _BlankLineStylizerBlock(),
            _FolderNameStylizerBlock(),
            _FolderPathStylizerBlock(),
            _ExtensionsStylizerBlock(),
            _IgnoreStylizerBlock(),
            _LinesStylizerBlock(short=short)
        ]
