"""Deliver the plan: copy the Final PDF to its dated folder and check the copy."""

from dataclasses import dataclass

from pdf_builder.application.ports import PdfFiles
from pdf_builder.domain.delivery import FINAL_PDF
from pdf_builder.domain.delivery_places import DeliveryPlaces


class MissingFinalPdfError(Exception):
    """The Final PDF is missing: the build must run before a delivery."""


@dataclass(frozen=True)
class Delivery:
    """A delivery of the plan, with the files it reads and writes."""

    files: PdfFiles

    def run(self, date: str) -> bool:
        """Copy the Final PDF to the dated folder of the date; return whether the copy is true."""
        dated_pdf = DeliveryPlaces(date).dated_pdf
        if FINAL_PDF not in self.files.paths():
            raise MissingFinalPdfError(FINAL_PDF)
        final_pdf = self.files.read(FINAL_PDF)
        self.files.write(dated_pdf, final_pdf)
        return self.files.read(dated_pdf) == final_pdf
