"""What a rule reports."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Violation:
    """One break of one rule, at one line of one file."""

    path: str
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        """Return the violation as one report line: path:line: rule: message."""
        location = f"{self.path}:{self.line}"
        return f"{location}: {self.rule}: {self.message}"
