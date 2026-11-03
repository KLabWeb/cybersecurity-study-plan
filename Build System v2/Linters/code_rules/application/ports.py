"""What the checker needs from the outside world, defined here so the checker never reads disk."""

from collections.abc import Iterator
from typing import Protocol

from code_rules.domain.source import SourceFile


class SourceProvider(Protocol):
    """A source of files to check. The infrastructure layer has the real one."""

    def files(self) -> Iterator[SourceFile]:
        """Return the source files, one at a time."""
