LINE_CLEAR = '\x1b[2K'


# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def print_progress_bar(iteration, total, prefix="", suffix="", decimals=1, length=100, fill='█', end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=end)


def up(lines: int = 1):
    print(end=f'\x1b[{lines}A')


def down(lines: int = 1):
    print(end=f'\x1b[{lines}B')


def clear_line():
    print(end=LINE_CLEAR)
