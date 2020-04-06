import argparse
import os
from .collector import FilesCollector
from .style import DefaultStylizer
from .config import UnifiedConfiguration
from typing import List
from colored import attr, fg


def _setup_config_parser(subparsers: argparse._SubParsersAction):
    config_parser = subparsers.add_parser('config')
    config_parser.add_argument(
        '-e', '--extensions',
        nargs='+',
        help='file extensions to count lines for to use by default.',
        required=False
    )
    config_parser.add_argument(
        '-i', '--ignore',
        nargs='+',
        help='patterns to ignore (gitignore-like) to use by default.',
        required=False
    )
    config_parser.add_argument(
        '-g', '--global',
        action='store_true',
        dest='use_global',
        help='whether to apply config globally.'
    )
    config_parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='list all the configurations.'
    )
    config_parser.add_argument(
        '-d', '--delete',
        help='delete specified config option.',
        nargs='+',
        required=False
    )


def _setup_count_parser(subparsers: argparse._SubParsersAction):
    count_parser = subparsers.add_parser('count')
    count_parser.add_argument(
        '-e', '--extensions',
        nargs='+',
        help='file extensions to count lines for.',
        required=False
    )
    count_parser.add_argument(
        '-i', '--ignore',
        nargs='+',
        help='patterns to ignore (gitignore-like).',
        required=False
    )
    count_parser.add_argument(
        '-f', '--folder',
        help='folder to work with.',
        default=os.getcwd()
    )


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    _setup_count_parser(subparsers)
    _setup_config_parser(subparsers)

    args = parser.parse_args()
    return args


def cli():
    args = parse_args()
    config = UnifiedConfiguration()

    if args.command == 'config':
        if args.list:
            print(config)
            return

        config = config.user_config if args.use_global else config.folder_config

        if args.delete:
            for option in args.delete:
                if option in config['DEFAULT']:
                    del config['DEFAULT'][option]
                else:
                    print("Couldn't delete the variable {}{}{}{}. It's not presented in configuration file.".format(
                        fg(149),
                        attr(1),
                        option,
                        attr(0)
                    ))
            return

        if args.extensions is not None:
            config['DEFAULT']['extensions'] = str(args.extensions)

        if args.ignore is not None:
            config['DEFAULT']['ignore'] = str(args.ignore)

    elif args.command == 'count':
        # Items to ignore
        ignore: List[str]
        if args.ignore is None:
            defaults = config['DEFAULT']
            if 'ignore' in defaults:
                ignore = eval(defaults['ignore'])
            else:
                ignore = []
        else:
            ignore = args.ignore

        # Extensions to count for
        extensions: List[str]
        if args.extensions is None:
            defaults = config['DEFAULT']
            if 'extensions' in defaults:
                extensions = eval(defaults['extensions'])
            else:
                print("Couldn't clarify extensions to count for.")
                exit(-1)
        else:
            extensions = args.extensions

        collector = FilesCollector(
            folder_path=args.folder,
            ignore=ignore,
            extensions=extensions
        )
        stylizer = DefaultStylizer()
        print(stylizer.apply(collector))


if __name__ == "__main__":
    cli()
