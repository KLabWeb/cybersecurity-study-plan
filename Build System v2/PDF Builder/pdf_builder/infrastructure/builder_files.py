"""The files of the PDF Builder folder and of the PDFs folder on disk."""

from dataclasses import dataclass
from pathlib import Path

PDFS_FOLDER = "Study Plan PDFs"


def builder_folder() -> Path:
    """Return the PDF Builder folder, two levels above this package."""
    return Path(__file__).parents[2]


def pdfs_folder() -> Path:
    """Return the folder of the Study Plan's PDFs, in the Study Plan beside the Build Systems."""
    return builder_folder().parents[1] / PDFS_FOLDER


@dataclass(frozen=True)
class FolderFiles:
    """The files under a folder, by their path relative to it, written with forward slashes."""

    root: Path

    def paths(self) -> list[str]:
        """Return the path of every file under the folder, sorted."""
        return sorted(
            found.relative_to(self.root).as_posix()
            for found in self.root.rglob("*")
            if found.is_file()
        )

    def read(self, path: str) -> bytes:
        """Return the bytes of the file."""
        return (self.root / path).read_bytes()

    def write(self, path: str, file_bytes: bytes) -> None:
        """Write the file, with any folder it needs."""
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(file_bytes)

