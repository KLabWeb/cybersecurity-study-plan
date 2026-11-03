"""The safety net: a PDF rendered from the plan source holds exactly the text of the reference."""

from pathlib import Path

from pdf_builder.infrastructure.page_scan import PdfPageReader

ENCODING = "utf-8"


def _reference_text() -> str:
    reference = Path(__file__).parent / "reference" / "plan_text.txt"
    return reference.read_text(encoding=ENCODING)


def _pdf_text(pdf_path: Path) -> str:
    pages = PdfPageReader().page_texts(pdf_path)
    return "\n".join(pages)


def test_rendered_plan_matches_the_reference(rendered_plan: Path) -> None:
    assert _pdf_text(rendered_plan) == _reference_text()
