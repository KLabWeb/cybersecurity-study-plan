"""Read the text of each page of a rendered PDF with the pdfplumber library."""

from pathlib import Path

import pdfplumber
from pdfplumber.page import Page

from pdf_builder.domain.contents import PageTexts


class PdfPageReader:
    """Reads the text of each page of a PDF file."""

    def page_texts(self, pdf: Path) -> PageTexts:
        """Return the text of each page, in page order."""
        with pdfplumber.open(pdf) as opened:
            return [page.extract_text() or "" for page in opened.pages]

    def layout_texts(self, pdf: Path) -> PageTexts:
        """Return the text of each page laid out as on the page, its indents kept, in page order."""
        with pdfplumber.open(pdf) as opened:
            return [_laid_out(page) for page in opened.pages]


def _laid_out(page: Page) -> str:
    return page.extract_text(layout=True) or ""
