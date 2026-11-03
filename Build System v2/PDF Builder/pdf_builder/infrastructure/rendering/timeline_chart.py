"""The phase timeline chart: one coloured column per phase, with its numeral, name and weeks."""

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

from pdf_builder.infrastructure.rendering.boxes import ALL_CELLS, Command
from pdf_builder.infrastructure.rendering.page import TEXT_WIDTH

ROW_HEIGHTS = (24, 38, 24)
CELL_PADDING_END = 2
CELL_PADDING_SIDE = 1
NUMERAL_SIZE = 10.5
NUMERAL_LEADING = 13
LABEL_SIZE = 7
LABEL_LEADING = 8.5

type Rows = list[list[str]]


def timeline_chart(rows: Rows, colours: list[str], caption_style: ParagraphStyle) -> Table:
    """Return the chart: numerals, names and weeks in rows, each phase's column in its colour."""
    cells = _all_cells(rows, caption_style)
    widths = _widths(colours)
    heights = list(ROW_HEIGHTS)
    chart = Table(cells, colWidths=widths, rowHeights=heights)
    chart.setStyle(TableStyle(_commands(colours)))
    return chart


def _all_cells(rows: Rows, caption_style: ParagraphStyle) -> list[list[Paragraph]]:
    row_styles = _row_styles(caption_style)
    return [
        _cells(row, style)
        for row, style in zip(rows, row_styles, strict=True)
    ]


def _widths(colours: list[str]) -> list[float]:
    width = TEXT_WIDTH / len(colours)
    return [width for _colour in colours]


def _cells(row: list[str], style: ParagraphStyle) -> list[Paragraph]:
    return [Paragraph(text, style) for text in row]


def _row_styles(caption_style: ParagraphStyle) -> list[ParagraphStyle]:
    numeral = ParagraphStyle(
        "timeline_numeral",
        parent=caption_style,
        fontSize=NUMERAL_SIZE,
        leading=NUMERAL_LEADING,
        fontName="Helvetica-Bold",
        textColor=white,
        alignment=TA_CENTER,
    )
    name = _label_style("timeline_name", caption_style)
    weeks = _label_style("timeline_weeks", caption_style)
    return [numeral, name, weeks]


def _label_style(name: str, caption_style: ParagraphStyle) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        parent=caption_style,
        fontSize=LABEL_SIZE,
        leading=LABEL_LEADING,
        alignment=TA_CENTER,
        textColor=white,
    )


def _commands(colours: list[str]) -> list[Command]:
    commands: list[Command] = [
        ("VALIGN", *ALL_CELLS, "MIDDLE"),
        ("ALIGN", *ALL_CELLS, "CENTER"),
        ("TOPPADDING", *ALL_CELLS, CELL_PADDING_END),
        ("BOTTOMPADDING", *ALL_CELLS, CELL_PADDING_END),
        ("LEFTPADDING", *ALL_CELLS, CELL_PADDING_SIDE),
        ("RIGHTPADDING", *ALL_CELLS, CELL_PADDING_SIDE),
    ]
    for column, colour in enumerate(colours):
        column_cells = ((column, 0), (column, -1))
        background = HexColor(colour)
        commands.append(("BACKGROUND", *column_cells, background))
    return commands
