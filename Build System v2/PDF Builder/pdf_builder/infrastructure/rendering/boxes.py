"""The boxed pieces of the plan PDF: note boxes, phase banners and grid tables."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle

from pdf_builder.infrastructure.rendering.page import TEXT_WIDTH
from pdf_builder.infrastructure.rendering.palette import (
    ACCENT,
    BANNER_DIVIDER,
    GRID_GRAY,
    LIGHT_BG,
    SOFT_BLUE,
)

# The cells a table command covers: from the first column and row to the last.
FIRST_CELL = (0, 0)
LAST_CELL = (-1, -1)
ALL_CELLS = (FIRST_CELL, LAST_CELL)
HEADER_ROW = (FIRST_CELL, (-1, 0))
BODY_ROWS = ((0, 1), LAST_CELL)
NUMERAL_COLUMN = (FIRST_CELL, (0, -1))
TITLE_COLUMN = ((1, 0), LAST_CELL)
NOTE_PADDING_SIDE = 10
NOTE_PADDING_END = 8
NOTE_BORDER = 0.5
NUMERAL_INCHES = 0.9
BANNER_NUMERAL_WIDTH = NUMERAL_INCHES * inch
BANNER_PADDING = 12
BANNER_TITLE_PADDING = 14
BANNER_NUMERAL_RIGHT = 6
GRID_PADDING_END = 5
GRID_PADDING_SIDE = 6
GRID_LINE = 0.4

type Rows = Sequence[list[Any]]
type Cells = tuple[tuple[int, int], tuple[int, int]]
type Command = tuple[str, tuple[int, int], tuple[int, int], *tuple[Any, ...]]


@dataclass(frozen=True)
class PlanBoxes:
    """Builds the note boxes and phase banners of the plan, in the plan's styles."""

    styles: dict[str, ParagraphStyle]

    def note(self, text: str) -> Table:
        """Return the text in a light box the width of the page's text."""
        cell = Paragraph(text, self.styles["note_text"])
        box = Table([[cell]], colWidths=[TEXT_WIDTH])
        commands: list[Command] = [
            ("BACKGROUND", *ALL_CELLS, HexColor(LIGHT_BG)),
            ("BOX", *ALL_CELLS, NOTE_BORDER, HexColor(SOFT_BLUE)),
            *_padding(ALL_CELLS, NOTE_PADDING_SIDE, NOTE_PADDING_END),
        ]
        box.setStyle(TableStyle(commands))
        return box

    def banner(self, numeral: str, title: str, duration: str) -> Table:
        """Return a phase banner: its numeral, then its title above its duration."""
        numeral_cell = Paragraph(numeral, self.styles["section_numeral"])
        title_cell = [
            Paragraph(title, self.styles["section_title"]),
            Paragraph(duration, self.styles["banner_duration"]),
        ]
        widths = [BANNER_NUMERAL_WIDTH, TEXT_WIDTH - BANNER_NUMERAL_WIDTH]
        banner = Table([[numeral_cell, title_cell]], colWidths=widths)
        banner.setStyle(_banner_style())
        return banner


def grid_table(rows: Rows, widths: list[float]) -> Table:
    """Return a table with a coloured header row, banded rows and a light grid."""
    table = Table(rows, colWidths=widths)
    bands = [white, HexColor(LIGHT_BG)]
    commands: list[Command] = [
        ("BACKGROUND", *HEADER_ROW, HexColor(ACCENT)),
        ("ROWBACKGROUNDS", *BODY_ROWS, bands),
        ("GRID", *ALL_CELLS, GRID_LINE, HexColor(GRID_GRAY)),
        ("VALIGN", *ALL_CELLS, "TOP"),
        *_padding(ALL_CELLS, GRID_PADDING_SIDE, GRID_PADDING_END),
    ]
    table.setStyle(TableStyle(commands))
    return table


def _padding(cells: Cells, side: float, end: float) -> list[Command]:
    """Return the commands that pad the cells: side padding left and right, end padding top."""
    return [
        ("LEFTPADDING", *cells, side),
        ("RIGHTPADDING", *cells, side),
        ("TOPPADDING", *cells, end),
        ("BOTTOMPADDING", *cells, end),
    ]


def _banner_style() -> TableStyle:
    return TableStyle([
        ("BACKGROUND", *ALL_CELLS, HexColor(ACCENT)),
        ("VALIGN", *ALL_CELLS, "MIDDLE"),
        ("LEFTPADDING", *NUMERAL_COLUMN, BANNER_PADDING),
        ("RIGHTPADDING", *NUMERAL_COLUMN, BANNER_NUMERAL_RIGHT),
        ("LEFTPADDING", *TITLE_COLUMN, BANNER_TITLE_PADDING),
        ("TOPPADDING", *ALL_CELLS, BANNER_PADDING),
        ("BOTTOMPADDING", *ALL_CELLS, BANNER_PADDING),
        ("LINEAFTER", *NUMERAL_COLUMN, 1, HexColor(BANNER_DIVIDER)),
    ])
