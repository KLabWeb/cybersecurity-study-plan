"""The command a person runs: build the plan PDF into the folder of the Study Plan's PDFs."""

import sys
from pathlib import Path

from pdf_builder.application.build import PlanBuild
from pdf_builder.domain.delivery import FINAL_PDF
from pdf_builder.infrastructure.builder_files import pdfs_folder
from pdf_builder.infrastructure.page_scan import PdfPageReader
from pdf_builder.infrastructure.plan_file import PlanFile
from pdf_builder.infrastructure.rendering.plan_document import PlanDocument

SETTLED = 0
UNSETTLED = 1


def main() -> int:
    """Build the plan into the PDFs folder; return 0 when the contents settled."""
    output = _final_pdf()
    plan = PlanFile.of_builder().load()
    settled = _plan_build().run(plan, output)
    sys.stdout.write(f"PDF: {output}\n")
    return exit_code(settled)


def exit_code(settled: bool) -> int:
    """Return 0 when the contents settled, 1 when they did not."""
    if settled:
        return SETTLED
    return UNSETTLED


def _plan_build() -> PlanBuild:
    """Return the build wired to the real renderer and page reader."""
    return PlanBuild(
        renderer=PlanDocument(),
        reader=PdfPageReader(),
        out=sys.stdout,
    )


def _final_pdf() -> Path:
    """Return the place of the Final PDF in the folder of the Study Plan's PDFs."""
    return pdfs_folder() / FINAL_PDF
