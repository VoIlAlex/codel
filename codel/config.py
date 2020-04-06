import os
import sys
import configparser
import shutil
import itertools
from colored import attr, fg

CONFIG_FOLDER = '.codel'
CONFIG_REL_PATH = 'codel.ini'


class FolderConfiguration:
    def __init__(self,
                 folder: str = None,
                 auto_commit: bool = True,
                 absence_safe: bool = True,
                 name: str = 'Folder configuration'):
        self.name = name
        self.config_parser = configparser.ConfigParser()
        self.folder = folder if folder else os.getcwd()
        self.auto_commit = auto_commit
        self.absence_safe = absence_safe

        # Read config if exists
        config_file_path = os.path.join(
            self.folder,
            CONFIG_FOLDER,
            CONFIG_REL_PATH
        )
        if os.path.exists(config_file_path):
            self.config_parser.read(config_file_path)

    def commit(self):
        config_file_folder = os.path.join(self.folder, CONFIG_FOLDER)
        if not os.path.exists(config_file_folder):
            os.makedirs(config_file_folder)
        config_file_path = os.path.join(config_file_folder, CONFIG_REL_PATH)
        with open(config_file_path, 'w+') as config_file:
            self.config_parser.write(config_file)

    def exists(self):
        config_file_path = os.path.join(self.folder, CONFIG_REL_PATH)
        return os.path.exists(config_file_path)

    def __getitem__(self, section: str):
        try:
            return self.config_parser[section]
        except Exception as e:
            if self.absence_safe:
                self.config_parser[section] = {}
                return self.config_parser[section]
            else:
                raise e

    def __iter__(self):
        return iter(self.config_parser)

    def __setitem__(self, section: str, value: dict):
        self.config_parser[section] = value

    def __str__(self):
        terminal_size = shutil.get_terminal_size()
        result = ''
        result += '{}{}{}{}\n'.format(
            fg(149),
            attr(1),
            self.name,
            attr(0)
        )
        result += (terminal_size.columns - 1) * '-' + '\n'
        for section in self.config_parser:
            result += '{}[{}]{}\n'.format(attr(1), section, attr(0))
            for i, (option, value) in enumerate(self.config_parser[section].items()):
                if i != 0:
                    result += '\n'
                result += '{}={}'.format(option, value)
        return result

    def __del__(self):
        if self.auto_commit:
            self.commit()


class UserConfiguration(FolderConfiguration):
    def __init__(self):
        if sys.platform == 'linux':
            user_folder = os.getenv('HOME')
        else:  # Windows
            user_folder = os.getenv('USERPRIFILE')
        FolderConfiguration.__init__(
            self,
            user_folder,
            name='User configuration'
        )


class UnifiedConfiguration:
    def __init__(self, folder: str = None):
        self.folder_config = FolderConfiguration(folder)
        self.user_config = UserConfiguration()

    def commit(self):
        self.folder_config.commit()
        self.user_config.commit()

    def __getitem__(self, section: str):
        result = {}
        if section in self.user_config:
            result.update(self.user_config[section])
        if section in self.folder_config:
            result.update(self.folder_config[section])
        return result

    def __iter__(self):
        return itertools.chain(
            iter(self.folder_config),
            iter(self.user_config)
        )

    def __str__(self):
        return f'\n{self.folder_config}\n\n\n{self.user_config}'
