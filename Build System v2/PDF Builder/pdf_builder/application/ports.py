"""What a build and a delivery need from outside: rendering and reading files."""

from pathlib import Path
from typing import Protocol

from pdf_builder.domain.contents import Pages, PageTexts
from pdf_builder.domain.plan import Plan


class PlanRenderer(Protocol):
    """Writes the plan to a PDF file, with the page printed beside each contents entry."""

    def render(self, plan: Plan, pages: Pages, output: Path) -> None:
        """Write the plan to output."""


class PageReader(Protocol):
    """Reads the text of each page of a PDF file."""

    def page_texts(self, pdf: Path) -> PageTexts:
        """Return the text of each page, in page order."""


class PdfFiles(Protocol):
    """The files of the Study Plan's PDFs folder, by their path relative to it."""

    def paths(self) -> list[str]:
        """Return the path of every file, sorted."""

    def read(self, path: str) -> bytes:
        """Return the bytes of the file."""

    def write(self, path: str, file_bytes: bytes) -> None:
        """Write the file, with any folder it needs."""

