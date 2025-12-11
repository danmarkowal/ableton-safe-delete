#!/usr/bin/env python3

import os
from argparse import ArgumentParser

from alsafedel.formatter import Formatter
from alsafedel.scanner import Scanner
from alsafedel.cli import print_progress_bar, clear_line


def dir_path(arg):
    if os.path.isdir(arg):
        return arg
    else:
        raise NotADirectoryError(arg)


def main():
    parser = ArgumentParser(prog="alsafedel",
                            description="A CLI tool for finding unused sample packs")
    parser.add_argument("-p", "--projdir", type=dir_path, required=True)
    parser.add_argument("-s", "--sampledir", type=dir_path, required=True)
    # maybe in the future
    # parser.add_argument("-d", "--delete", action='store_true')
    parser.add_argument("-r", "--recursive", action='store_true')
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--include-backups", action="store_true")

    try:
        args = parser.parse_args()
    except NotADirectoryError as e:
        print(f"Folder not found: '{e}'")
        return

    scanner = Scanner(lambda project_index, project_count: print_progress_bar(
        project_index, project_count, prefix="Progress", length=32))
    scanner.scan(args.projdir, args.sampledir,
                 args.recursive, args.include_backups)
    clear_line()

    formatter = Formatter()
    formatter.print_unused(scanner.result.root)


if __name__ == "__main__":
    main()
