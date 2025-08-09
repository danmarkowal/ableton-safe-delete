import os

supported_files = (".wav", ".mp3", ".aiff", ".aif",
                   ".aifc", ".ogg", ".flac", ".aac", ".m4a", ".mp4", ".mov")
ignored_files = (".mid", ".alc")


def is_subpath(path: str, of: str):
    return path.startswith(of)


def get_unused_samplepacks(samplepacks: set[str], used_samples: set[str]):
    marked_samplepacks = set()
    for sample in used_samples:
        for samplepack in samplepacks:
            if is_subpath(sample, samplepack):
                marked_samplepacks.add(samplepack)
    return samplepacks.difference(marked_samplepacks)


def get_samplepacks(folder: str):
    samplepacks = set()
    for child in os.listdir(folder):
        file = os.path.join(folder, child)
        if os.path.isdir(file):
            samplepacks.add(os.path.abspath(file))
    return samplepacks


def should_ignore(file: str):
    is_ignored_file = file.lower().endswith(ignored_files)
    is_hidden_file = os.path.basename(file).startswith(".")
    return is_ignored_file or is_hidden_file


def is_media_file(file: str):
    return file.lower().endswith(supported_files)


def get_samples(folder: str):
    samples = set()
    for child in os.listdir(folder):
        file = os.path.join(folder, child)
        if os.path.isdir(file):
            samples.update(get_samples(file))
        elif os.path.isfile(file) and is_media_file(file):
            # ensure path is absolute
            samples.add(os.path.abspath(file))
    return samples
