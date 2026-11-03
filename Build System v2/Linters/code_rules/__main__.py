"""Run the code rules: python -m code_rules <folder>. With no folder, the current one is checked."""

import sys
from pathlib import Path

from code_rules.interface.cli import run


def main(arguments: list[str]) -> int:
    """Return the exit code of a check of the folder named in the arguments."""
    folder = Path.cwd()
    if arguments:
        folder = Path(arguments[0])
    return run(folder, sys.stdout)


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
