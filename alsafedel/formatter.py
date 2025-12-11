import os

from alsafedel.scanner import Node, UsageType


class Formatter:
    def __init__(self, tab_width: int = 2):
        self.tab_width = tab_width
        self.indentation = 0

    def print_unused(self, node: Node):
        if node.usage == UsageType.USED:
            return
        basename = " " * (self.indentation * self.tab_width + 4) + \
            "|-- " + os.path.basename(node.path)
        if node.usage == UsageType.UNUSED:
            print(basename + "/*")
            return
        print(basename)
        for child in node.children:
            self.indentation += 1
            self.print_unused(child)
            self.indentation -= 1
