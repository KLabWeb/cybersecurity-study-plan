"""The command a person runs to deliver the plan, with the date of the delivery."""

import sys

from pdf_builder.application.delivery import Delivery
from pdf_builder.domain.delivery_places import DeliveryPlaces
from pdf_builder.infrastructure.builder_files import FolderFiles, pdfs_folder

PASSED = 0
FAILED = 1


def main(arguments: list[str]) -> int:
    """Deliver the plan for the date given; return 0 when the dated PDF is a true copy."""
    date = arguments[0]
    pdf_files = FolderFiles(pdfs_folder())
    matches = Delivery(pdf_files).run(date)
    dated_pdf = DeliveryPlaces(date).dated_pdf
    sys.stdout.write(report_line(dated_pdf, matches=matches))
    return delivery_exit_code(matches)


def report_line(dated_pdf: str, *, matches: bool) -> str:
    """Return the line that tells where the dated PDF went and whether it equals the Final PDF."""
    return f"dated PDF {dated_pdf} equals the Final PDF: {matches}\n"


def delivery_exit_code(matches: bool) -> int:
    """Return 0 when the dated PDF equals the Final PDF, 1 when it does not."""
    if matches:
        return PASSED
    return FAILED


if __name__ == "__main__":
    exit_code = main(sys.argv[1:])
    sys.exit(exit_code)
