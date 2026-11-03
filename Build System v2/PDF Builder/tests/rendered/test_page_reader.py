"""The page reader returns the text of every page of the rendered plan."""

from pathlib import Path

from pdf_builder.infrastructure.page_scan import PdfPageReader


def test_pdf_page_reader_reads_every_page(rendered_plan: Path) -> None:
    page_texts = PdfPageReader().page_texts(rendered_plan)
    assert len(page_texts) > 1


INDENT = "    "


def _is_indented(line: str) -> bool:
    if not line.strip():
        return False
    return line.startswith(INDENT)


def test_the_laid_out_text_has_every_page(rendered_plan: Path) -> None:
    reader = PdfPageReader()
    laid_out = reader.layout_texts(rendered_plan)
    plain = reader.page_texts(rendered_plan)
    assert len(laid_out) == len(plain)


def test_the_laid_out_text_keeps_the_indents(rendered_plan: Path) -> None:
    pages = PdfPageReader().layout_texts(rendered_plan)
    lines = "\n".join(pages).split("\n")
    assert any(map(_is_indented, lines))
