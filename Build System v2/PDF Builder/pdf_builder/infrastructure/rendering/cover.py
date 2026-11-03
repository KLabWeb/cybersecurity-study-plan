"""The cover of the plan PDF: its background, its title and subtitle, and its row of pills."""

from dataclasses import dataclass

from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate

from pdf_builder.domain.plan import Cover
from pdf_builder.infrastructure.rendering.cover_pills import draw_pills
from pdf_builder.infrastructure.rendering.page import (
    MARGIN_INSIDE,
    MARGIN_OUTSIDE,
    PAGE_HEIGHT,
    PAGE_WIDTH,
)
from pdf_builder.infrastructure.rendering.palette import ACCENT, COVER_LINE, DARK, GOLD, SOFT_BLUE

# The blue upper part of the cover starts at this share of the page height.
SPLIT_SHARE = 0.38
UPPER_SHARE = 0.62
STRIPE_HEIGHT = 4
# Boxes as left edge, bottom edge, width and height, in points.
GROUND = (0, 0, PAGE_WIDTH, PAGE_HEIGHT)
SPLIT_HEIGHT = PAGE_HEIGHT * SPLIT_SHARE
UPPER_HEIGHT = PAGE_HEIGHT * UPPER_SHARE
UPPER_PART = (0, SPLIT_HEIGHT, PAGE_WIDTH, UPPER_HEIGHT)
STRIPE = (
    MARGIN_INSIDE,
    SPLIT_HEIGHT - STRIPE_HEIGHT,
    PAGE_WIDTH - MARGIN_INSIDE - MARGIN_OUTSIDE,
    STRIPE_HEIGHT,
)
# A faint line down the cover, a little more than halfway into the inner margin.
MARGIN_LINE_SHARE = 0.55
MARGIN_LINE_LEFT = MARGIN_INSIDE * MARGIN_LINE_SHARE
MARGIN_LINE_WIDTH = 0.5
TITLE_FONT = "Helvetica-Bold"
TITLE_SIZE = 36
TITLE_HEIGHTS = (433.5, 388.5)
SUBTITLE_FONT = "Helvetica"
SUBTITLE_SIZE = 13
SUBTITLE_HEIGHT = 364.3
UNDERLINE_HEIGHT = 329.0
UNDERLINE_INCHES = 3.5
UNDERLINE_END = MARGIN_INSIDE + UNDERLINE_INCHES * inch
UNDERLINE_WIDTH = 1.5

type Box = tuple[float, float, float, float]


@dataclass(frozen=True)
class CoverPage:
    """The cover of the plan, drawn with the words the plan gives it."""

    cover: Cover

    def draw(self, canvas: Canvas, _doc: BaseDocTemplate) -> None:
        """Draw the whole cover on the first page."""
        _draw_ground(canvas)
        _draw_titles(canvas, self.cover.title_lines)
        _draw_subtitle(canvas, self.cover.subtitle)
        draw_pills(canvas, self.cover.pills)


def _fill(canvas: Canvas, colour: str, box: Box) -> None:
    canvas.setFillColor(HexColor(colour))
    canvas.rect(*box, 0, 1)


def _draw_ground(canvas: Canvas) -> None:
    _fill(canvas, DARK, GROUND)
    _fill(canvas, ACCENT, UPPER_PART)
    _fill(canvas, GOLD, STRIPE)
    canvas.setStrokeColor(HexColor(COVER_LINE))
    canvas.setLineWidth(MARGIN_LINE_WIDTH)
    canvas.line(MARGIN_LINE_LEFT, 0, MARGIN_LINE_LEFT, PAGE_HEIGHT)


def _draw_titles(canvas: Canvas, lines: tuple[str, ...]) -> None:
    canvas.setFont(TITLE_FONT, TITLE_SIZE)
    canvas.setFillColor(white)
    placed = zip(TITLE_HEIGHTS, lines, strict=True)
    for height, line in placed:
        canvas.drawString(MARGIN_INSIDE, height, line)


def _draw_subtitle(canvas: Canvas, subtitle: str) -> None:
    canvas.setFont(SUBTITLE_FONT, SUBTITLE_SIZE)
    canvas.setFillColor(HexColor(SOFT_BLUE))
    canvas.drawString(MARGIN_INSIDE, SUBTITLE_HEIGHT, subtitle)
    canvas.setStrokeColor(HexColor(GOLD))
    canvas.setLineWidth(UNDERLINE_WIDTH)
    canvas.line(MARGIN_INSIDE, UNDERLINE_HEIGHT, UNDERLINE_END, UNDERLINE_HEIGHT)
