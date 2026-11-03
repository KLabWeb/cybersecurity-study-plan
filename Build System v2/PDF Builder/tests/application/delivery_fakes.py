"""A fake part for tests of a delivery: the files of the PDFs folder, kept in memory."""

from dataclasses import dataclass, field

type Held = dict[str, bytes]


@dataclass(frozen=True)
class FakeFiles:
    """The files of the PDFs folder, by their path."""

    held: Held = field(default_factory=dict)

    def paths(self) -> list[str]:
        """Return the path of every file, sorted."""
        return sorted(self.held)

    def read(self, path: str) -> bytes:
        """Return the bytes of the file."""
        return self.held[path]

    def write(self, path: str, file_bytes: bytes) -> None:
        """Write the file."""
        self.held[path] = file_bytes


def sample_files() -> FakeFiles:
    """Return a small PDFs folder: a Final PDF and one other file."""
    return FakeFiles(
        {
            "Study_Plan_-_Final.pdf": b"%PDF final",
            "pdf_builder/domain/plan.py": b"plan code",
        },
    )
