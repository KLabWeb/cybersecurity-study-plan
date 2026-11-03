"""Where a delivery of one date puts its PDF, relative to the folder of the Study Plan's PDFs."""

import re
from dataclasses import dataclass

CALENDAR_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


class InvalidDeliveryDateError(ValueError):
    """A delivery date is not written as a calendar date, YYYY-MM-DD."""


@dataclass(frozen=True)
class DeliveryPlaces:
    """Where a delivery of a date puts its PDF."""

    date: str

    def __post_init__(self) -> None:
        """Refuse a date that is not written as YYYY-MM-DD."""
        if not CALENDAR_DATE.fullmatch(self.date):
            raise InvalidDeliveryDateError(self.date)

    @property
    def folder(self) -> str:
        """Return the dated folder of the delivery."""
        return f"Cyb Study Plan ({self.date})"

    @property
    def dated_pdf(self) -> str:
        """Return the PDF of the delivery, named with its date."""
        return f"{self.folder}/Study_Plan_-_{self.date}.pdf"

