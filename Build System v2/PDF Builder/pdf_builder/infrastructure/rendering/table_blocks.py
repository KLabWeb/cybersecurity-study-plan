"""The blocks laid out as tables or lists: the contents, the weekly schedule and the timeline."""

from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer

from pdf_builder.domain.contents import Pages
from pdf_builder.domain.plan import Block, BlockKind
from pdf_builder.infrastructure.rendering.boxes import grid_table
from pdf_builder.infrastructure.rendering.layout_context import BlockLayout, Layout
from pdf_builder.infrastructure.rendering.page import TEXT_WIDTH
from pdf_builder.infrastructure.rendering.palette import CONTENTS_DOTS
from pdf_builder.infrastructure.rendering.plan_writer import paragraph
from pdf_builder.infrastructure.rendering.timeline_chart import timeline_chart

# The weekly schedule's columns: the day type, the days a week, the hours, and the notes,
# which take the rest of the text width.
DAY_TYPE_INCHES = 1.5
COUNT_INCHES = 0.85
OTHER_COLUMNS_INCHES = 3.2
DAY_TYPE_WIDTH = DAY_TYPE_INCHES * inch
COUNT_WIDTH = COUNT_INCHES * inch
NOTES_WIDTH = TEXT_WIDTH - OTHER_COLUMNS_INCHES * inch
SCHEDULE_WIDTHS = (DAY_TYPE_WIDTH, COUNT_WIDTH, COUNT_WIDTH, NOTES_WIDTH)
# A contents entry is filled with dots to this many characters, and has at least two.
CONTENTS_LINE = 62
FEWEST_DOTS = 2
type Row = list[list[str]]
type Cells = list[Paragraph]

SUBSECTION_MARK = "\u2013"
ENTRY_GAP = 2


def table_layouts() -> dict[str, BlockLayout]:
    """Return how each kind of table or list block is laid out, by its kind."""
    return {
        BlockKind.TABLE_OF_CONTENTS: _contents_list,
        BlockKind.SCHEDULE: _schedule,
        BlockKind.TIMELINE: _timeline,
    }


def _contents_list(layout: Layout, block: Block) -> None:
    for entry in block["entries"]:
        _add_entry(layout, entry)
        layout.add(Spacer(1, ENTRY_GAP))


def _add_entry(layout: Layout, entry: Block) -> None:
    styles = layout.styles
    line = _dotted(entry, layout.pages)
    layout.add(paragraph(line, styles["contents_entry"]))
    sub_style = styles["contents_subsection"]
    for subsection in entry["subsections"]:
        marked = f"{SUBSECTION_MARK} {subsection}"
        layout.add(paragraph(marked, sub_style))


def _dotted(entry: Block, pages: Pages) -> str:
    title = entry["title"]
    page = pages.get(title, entry["page"])
    count = max(FEWEST_DOTS, CONTENTS_LINE - len(title))
    dots = "." * count
    return f'<b>{title}</b><font color="{CONTENTS_DOTS}">{dots}</font>{page}'


def _schedule(layout: Layout, block: Block) -> None:
    written_rows = block["rows"]
    rows = [_schedule_row(layout, row) for row in written_rows]
    widths = list(SCHEDULE_WIDTHS)
    layout.add(grid_table(rows, widths))


def _schedule_row(layout: Layout, row: Row) -> Cells:
    styles = layout.styles
    cells = []
    for text, style in row:
        cells.append(paragraph(text, styles[style]))
    return cells


def _timeline(layout: Layout, block: Block) -> None:
    rows = block["rows"]
    colours = block["colours"]
    chart = timeline_chart(rows, colours, layout.styles["caption"])
    layout.add(chart)
