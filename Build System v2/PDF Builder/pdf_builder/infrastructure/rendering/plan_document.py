"""Render the plan into one PDF file, with the given page of each contents entry."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate

from pdf_builder.domain.contents import Pages
from pdf_builder.domain.plan import Plan
from pdf_builder.infrastructure.rendering.cover import CoverPage
from pdf_builder.infrastructure.rendering.layout_context import Story
from pdf_builder.infrastructure.rendering.page import (
    MARGIN_INSIDE,
    MARGIN_OUTSIDE,
    TEXT_BOTTOM_ROOM,
    TEXT_TOP_ROOM,
    register_fonts,
)
from pdf_builder.infrastructure.rendering.page_frame import PageFrame
from pdf_builder.infrastructure.rendering.plan_layout import lay_out_plan


class PlanDocument:
    """Renders the plan into a PDF file with the reportlab library."""

    def render(self, plan: Plan, pages: Pages, output: Path) -> None:
        """Write the plan to output; pages gives the page printed beside each contents entry."""
        _render(plan, pages, output)


def _render(plan: Plan, pages: Pages, output: Path) -> None:
    register_fonts()
    story: Story = []
    lay_out_plan(story, plan, pages)
    document = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=MARGIN_INSIDE,
        rightMargin=MARGIN_OUTSIDE,
        topMargin=TEXT_TOP_ROOM,
        bottomMargin=TEXT_BOTTOM_ROOM,
        title=plan.document.title,
        author=plan.document.author,
        subject=plan.document.subject,
    )
    first_page = CoverPage(plan.cover).draw
    later_pages = PageFrame(plan.document).draw
    document.build(story, onFirstPage=first_page, onLaterPages=later_pages)
