"""The row of pills at the foot of the cover: one per phase, each with a two-line label."""

from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

from pdf_builder.domain.plan import Pill
from pdf_builder.infrastructure.rendering.page import MARGIN_INSIDE, TEXT_WIDTH
from pdf_builder.infrastructure.rendering.palette import GOLD, HIGHLIGHT, PILL_TEXT

PILL_GAP = 0.1 * inch
PILL_HEIGHT = 30.2
PILL_BOTTOM = 13.0
PILL_CORNER = 3
NUMERAL_FONT = "Helvetica-Bold"
NUMERAL_SIZE = 8
NUMERAL_HEIGHT = 33.3
LABEL_FONT = "Helvetica"
LABEL_SIZE = 6.5
LABEL_HEIGHTS = (21.9, 15.6)

type Lines = tuple[str, ...]


def draw_pills(canvas: Canvas, pills: tuple[Pill, ...]) -> None:
    """Draw the pills side by side across the width of the page's text."""
    count = len(pills)
    gaps = PILL_GAP * (count - 1)
    width = (TEXT_WIDTH - gaps) / count
    left = MARGIN_INSIDE
    for pill in pills:
        _draw_pill(canvas, left, width, pill)
        left += width + PILL_GAP


def _draw_pill(canvas: Canvas, left: float, width: float, pill: Pill) -> None:
    centre = left + width / 2
    canvas.setFillColor(HexColor(HIGHLIGHT))
    box = (left, PILL_BOTTOM, width, PILL_HEIGHT)
    canvas.roundRect(*box, PILL_CORNER, 0, 1)
    canvas.setFillColor(HexColor(GOLD))
    canvas.setFont(NUMERAL_FONT, NUMERAL_SIZE)
    canvas.drawCentredString(centre, NUMERAL_HEIGHT, pill[0])
    _draw_label(canvas, centre, pill[1:])


def _draw_label(canvas: Canvas, centre: float, lines: Lines) -> None:
    canvas.setFillColor(HexColor(PILL_TEXT))
    canvas.setFont(LABEL_FONT, LABEL_SIZE)
    placed = zip(LABEL_HEIGHTS, lines, strict=True)
    for height, line in placed:
        canvas.drawCentredString(centre, height, line)
