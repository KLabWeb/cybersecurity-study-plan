"""Reads the Python files under a folder, skipping the folders it is told to skip."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from code_rules.domain.source import SourceFile

ENCODING = "utf-8"


@dataclass(frozen=True)
class FileSystemSources:
    """The Python files under one folder, each with its path relative to that folder."""

    root: Path
    excluded: frozenset[str]

    def files(self) -> Iterator[SourceFile]:
        """Return each Python file in path order, leaving out the excluded folders."""
        for path in sorted(self.root.rglob("*.py")):
            if not self._is_excluded(path):
                yield self._read(path)

    def _is_excluded(self, path: Path) -> bool:
        """Return True when any folder on the file's path is one to skip."""
        folders = path.relative_to(self.root).parts
        return any(folder in self.excluded for folder in folders)

    def _read(self, path: Path) -> SourceFile:
        """Return the file's text with its path written with forward slashes."""
        relative = path.relative_to(self.root).as_posix()
        return SourceFile(relative, path.read_text(encoding=ENCODING))
