import gzip
import os
import re
from enum import Enum, auto

from alsafedel.samples import Sample

# pre-compile regex
PATH_PATTERN = re.compile(
    r'<SampleRef>.*?<Path.*?Value="([^"]+?)".*?<\/SampleRef>', re.DOTALL)


class DirType(Enum):
    DEFAULT = auto()  # this folder contains nothing of interest but may contain project folders
    PROJECT = auto()  # this folder contains project files which should be scanned
    BACKUP = auto()  # this folder contains backups which may be skipped


def process_project_file(file: str) -> set[Sample]:
    with open(file, "rb") as f:
        text = f.read()
        try:
            xml = gzip.decompress(text).decode()
        except gzip.BadGzipFile:
            xml = text.decode()

    sample_paths = re.findall(PATH_PATTERN, xml)
    # ensure that paths are absolute
    return {Sample(os.path.abspath(path)) for path in sample_paths}


def is_project_file(file: str) -> bool:
    return file.lower().endswith(".als")


def is_project_dir(folder: str) -> bool:
    return any(is_project_file(child) for child in os.listdir(folder))


def is_backup_dir(folder: str) -> bool:
    return os.path.basename(folder) == "Backup"


def get_project_files(folder: str, recursive: bool, include_backups: bool, dir_type: DirType = DirType.DEFAULT) -> set[str]:
    # functions somewhat like a state machine
    # all directories are marked as DirType.DEFAULT by default
    # if a default directory has at least one project file then it is marked as DirType.PROJECT
    # if a directory inside a DirType.PROJECT directory is called 'Backup' then it is marked as DirType.BACKUP
    # DirType.BACKUP is skipped if backups are not included

    project_files = set()
    if dir_type is DirType.BACKUP and not include_backups:
        return project_files

    children = os.listdir(folder)

    if dir_type is DirType.DEFAULT and is_project_dir(folder):
        dir_type = DirType.PROJECT

    for child in children:
        file = os.path.join(folder, child)
        if os.path.isdir(file) and recursive:
            sub_dir_type = DirType.BACKUP if dir_type is DirType.PROJECT and is_backup_dir(
                file) else DirType.DEFAULT

            project_files.update(get_project_files(
                file, recursive, include_backups, sub_dir_type))
        elif os.path.isfile(file) and is_project_file(file):
            project_files.add(file)
    return project_files
