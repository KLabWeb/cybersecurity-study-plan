"""The header and footer that every page after the cover draws around its text."""

from dataclasses import dataclass

from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate

from pdf_builder.domain.plan import DocumentInfo
from pdf_builder.infrastructure.rendering.page import (
    MARGIN_BOTTOM,
    MARGIN_INSIDE,
    MARGIN_OUTSIDE,
    MARGIN_TOP,
    PAGE_HEIGHT,
    PAGE_WIDTH,
)
from pdf_builder.infrastructure.rendering.palette import ACCENT, MID_GRAY

FRAME_FONT = "Helvetica"
FRAME_FONT_SIZE = 8
FRAME_LINE = 1.5
# Where the header and footer lines and texts stand, in points from the foot of the page.
LINE_GAP = 6
HEADER_TEXT_GAP = 10
FOOTER_TEXT_GAP = 14
HEADER_LINE_HEIGHT = PAGE_HEIGHT - MARGIN_TOP + LINE_GAP
HEADER_TEXT_HEIGHT = PAGE_HEIGHT - MARGIN_TOP + HEADER_TEXT_GAP
FOOTER_LINE_HEIGHT = MARGIN_BOTTOM - LINE_GAP
FOOTER_TEXT_HEIGHT = MARGIN_BOTTOM - FOOTER_TEXT_GAP
RIGHT_EDGE = PAGE_WIDTH - MARGIN_OUTSIDE


@dataclass(frozen=True)
class PageFrame:
    """The header and footer of the plan's pages, with the plan's title and start month."""

    document: DocumentInfo

    def draw(self, canvas: Canvas, doc: BaseDocTemplate) -> None:
        """Draw the header and footer of a page, with its printed page number."""
        canvas.saveState()
        number = doc.page - 1
        _draw_header(canvas, self.document)
        _draw_footer(canvas, number)
        canvas.restoreState()


def _draw_header(canvas: Canvas, document: DocumentInfo) -> None:
    canvas.setStrokeColor(HexColor(ACCENT))
    canvas.setLineWidth(FRAME_LINE)
    canvas.line(MARGIN_INSIDE, HEADER_LINE_HEIGHT, RIGHT_EDGE, HEADER_LINE_HEIGHT)
    _set_frame_font(canvas)
    canvas.drawString(MARGIN_INSIDE, HEADER_TEXT_HEIGHT, document.title)
    canvas.drawRightString(RIGHT_EDGE, HEADER_TEXT_HEIGHT, document.start)


def _draw_footer(canvas: Canvas, number: int) -> None:
    canvas.setStrokeColor(HexColor(ACCENT))
    canvas.line(MARGIN_INSIDE, FOOTER_LINE_HEIGHT, RIGHT_EDGE, FOOTER_LINE_HEIGHT)
    _set_frame_font(canvas)
    # Odd pages carry their number on the left, even pages on the right.
    if number % 2 == 1:
        canvas.drawString(MARGIN_INSIDE, FOOTER_TEXT_HEIGHT, str(number))
    else:
        canvas.drawRightString(RIGHT_EDGE, FOOTER_TEXT_HEIGHT, str(number))


def _set_frame_font(canvas: Canvas) -> None:
    canvas.setFont(FRAME_FONT, FRAME_FONT_SIZE)
    canvas.setFillColor(HexColor(MID_GRAY))
