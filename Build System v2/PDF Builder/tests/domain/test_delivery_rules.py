"""Where a delivery puts the plan's PDFs, inside the folder of the Study Plan's PDFs."""

import pytest

from pdf_builder.domain.delivery import FINAL_PDF
from pdf_builder.domain.delivery_places import DeliveryPlaces, InvalidDeliveryDateError


def test_final_pdf_sits_atop_the_pdfs_folder() -> None:
    assert FINAL_PDF == "Study_Plan_-_Final.pdf"


def test_a_delivery_date_must_be_a_calendar_date() -> None:
    with pytest.raises(InvalidDeliveryDateError, match="22-10-2026"):
        DeliveryPlaces("22-10-2026")


def test_a_delivery_date_names_its_folder() -> None:
    assert DeliveryPlaces("2026-10-22").folder == "Cyb Study Plan (2026-10-22)"


def test_the_dated_pdf_sits_in_its_folder() -> None:
    dated_pdf = DeliveryPlaces("2026-10-22").dated_pdf
    assert dated_pdf == "Cyb Study Plan (2026-10-22)/Study_Plan_-_2026-10-22.pdf"
