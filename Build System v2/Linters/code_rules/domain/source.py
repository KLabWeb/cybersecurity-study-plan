"""A source file as the rules see it."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceFile:
    """One Python file: its path relative to the checked folder, and its text."""

    path: str
    text: str
