import os
from dataclasses import dataclass, field

supported_files = (".wav", ".mp3", ".aiff", ".aif",
                   ".aifc", ".ogg", ".flac", ".aac", ".m4a", ".mp4", ".mov")
ignored_files = (".mid", ".alc")


# frozen makes it hashable
@dataclass(frozen=True)
class Sample:
    path: str = field()


def is_subpath(path: str, of: str) -> bool:
    return path.startswith(of)


def get_unused_samplepacks(all_samplepacks: set[str], used_samples: set[Sample]) -> set[str]:
    used_samplepacks = set()
    for sample in used_samples:
        used_samplepacks.add(sample.samplepack)
    return all_samplepacks.difference(used_samplepacks)


def get_samplepacks(folder: str) -> set[str]:
    samplepacks = set()
    for child in os.listdir(folder):
        file = os.path.join(folder, child)
        if os.path.isdir(file):
            samplepacks.add(os.path.abspath(file))
    return samplepacks


def should_ignore(file: str) -> bool:
    is_ignored_file = file.lower().endswith(ignored_files)
    is_hidden_file = os.path.basename(file).startswith(".")
    return is_ignored_file or is_hidden_file


def is_media_file(file: str) -> bool:
    return file.lower().endswith(supported_files)
