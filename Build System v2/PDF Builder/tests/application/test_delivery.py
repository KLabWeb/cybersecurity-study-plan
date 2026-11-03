"""A delivery copies the Final PDF to its dated folder and checks the copy."""

import pytest
from delivery_fakes import FakeFiles, sample_files

from pdf_builder.application.delivery import Delivery, MissingFinalPdfError

DATE = "2026-10-21"
DATED_PDF = "Cyb Study Plan (2026-10-21)/Study_Plan_-_2026-10-21.pdf"
FINAL_PDF = b"%PDF final"


def test_final_pdf_is_copied_to_the_dated_folder() -> None:
    files = sample_files()
    Delivery(files).run(DATE)
    assert files.read(DATED_PDF) == FINAL_PDF


def test_a_true_copy_passes_the_check() -> None:
    assert Delivery(sample_files()).run(DATE)


def test_missing_final_pdf_stops_the_delivery() -> None:
    files = FakeFiles({"pdf_builder/domain/plan.py": b"plan code"})
    with pytest.raises(MissingFinalPdfError):
        Delivery(files).run(DATE)
