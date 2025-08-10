#!/usr/bin/env python3

import os
from argparse import ArgumentParser
from multiprocessing import Pool

from alsafedel.cli import clear_line, down, print_progress_bar, up
from alsafedel.project import get_project_files, process_project_file
from alsafedel.samples import (get_samplepacks, get_samples,
                               get_unused_samplepacks)


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

    samplepacks = get_samplepacks(args.sampledir)
    if args.debug:
        print(f'Found {len(samplepacks)} samplepacks')

    samples = get_samples(args.sampledir)
    if args.debug:
        print(f'Found {len(samples)} samples')

    project_files = get_project_files(
        args.projdir, args.recursive, args.include_backups)

    project_samples = set()
    total_files = len(project_files)
    processed = 0
    with Pool(processes=4) as p:
        for result in p.imap_unordered(process_project_file, project_files):
            project_samples.update(result)
            processed += 1
            print_progress_bar(processed, total_files,
                               prefix="Progress", length=32)
    clear_line()

    used_samples = set(samples.keys()).intersection(project_samples)
    used_samples = set(
        map(lambda sample_path: samples[sample_path], used_samples))
    if args.debug:
        print(
            f'Found {len(used_samples)} samples in use across {len(project_files)} project files')

    unused_samplepacks = get_unused_samplepacks(samplepacks, used_samples)
    print_unused(args.sampledir, unused_samplepacks)


def print_unused(root_folder: str, unused_samplepacks: set[str]):
    print(root_folder)
    if len(unused_samplepacks) == 0:
        print("   There are no samplepacks that can be deleted in this folder")
        return
    for samplepack in unused_samplepacks:
        print(f"|-- {os.path.basename(samplepack)}")


if __name__ == "__main__":
    main()
