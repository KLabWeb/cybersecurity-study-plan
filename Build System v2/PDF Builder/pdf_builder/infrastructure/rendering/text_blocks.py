"""The blocks of running text: paragraphs, bullets, headings and sub-headings."""

from reportlab.lib.units import inch

from pdf_builder.domain.plan import Block, BlockKind
from pdf_builder.infrastructure.rendering.layout_context import BlockLayout, Layout
from pdf_builder.infrastructure.rendering.plan_writer import SUBHEADING_ROOM, paragraph


def text_layouts() -> dict[str, BlockLayout]:
    """Return how each kind of text block is laid out, by its kind."""
    return {
        BlockKind.PARAGRAPH: _paragraph,
        BlockKind.BULLET: _bullet,
        BlockKind.HEADING: _heading,
        BlockKind.SUBHEADING: _subheading,
    }


def _paragraph(layout: Layout, block: Block) -> None:
    style = layout.styles[block["style"]]
    layout.add(paragraph(block["text"], style))


def _bullet(layout: Layout, block: Block) -> None:
    text = block["text"]
    layout.add(layout.writer.bullet(text))


def _heading(layout: Layout, block: Block) -> None:
    layout.writer.heading(block["title"])


def _subheading(layout: Layout, block: Block) -> None:
    inches = block.get("reserve_inches", SUBHEADING_ROOM)
    room = inches * inch
    layout.writer.subheading(block["title"], room)
