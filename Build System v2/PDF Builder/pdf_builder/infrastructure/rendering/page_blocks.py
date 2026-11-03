"""The blocks that shape the page: breaks, room, spaces, rules, phase banners and note boxes."""

from reportlab.lib.units import inch
from reportlab.platypus import CondPageBreak, PageBreak, Spacer

from pdf_builder.domain.plan import Block, BlockKind
from pdf_builder.infrastructure.rendering.layout_context import BlockLayout, Layout, fields
from pdf_builder.infrastructure.rendering.plan_writer import section_rule

BANNER_FIELDS = ("numeral", "title", "duration")


def page_layouts() -> dict[str, BlockLayout]:
    """Return how each page-shaping kind of block is laid out, by its kind."""
    return {
        BlockKind.PAGE_BREAK: _page_break,
        BlockKind.PAGE_ROOM: _page_room,
        BlockKind.SPACE: _space,
        BlockKind.RULE: _rule,
        BlockKind.BANNER: _banner,
        BlockKind.NOTE: _note,
    }


def _page_break(layout: Layout, _block: Block) -> None:
    layout.add(PageBreak())


def _page_room(layout: Layout, block: Block) -> None:
    room = block["inches"] * inch
    layout.add(CondPageBreak(room))


def _space(layout: Layout, block: Block) -> None:
    layout.add(Spacer(1, block["points"]))


def _rule(layout: Layout, _block: Block) -> None:
    layout.add(*section_rule())


def _banner(layout: Layout, block: Block) -> None:
    banner_fields = fields(block, BANNER_FIELDS)
    banner = layout.boxes.banner(*banner_fields)
    layout.add(banner)


def _note(layout: Layout, block: Block) -> None:
    text = block["text"]
    layout.add(layout.boxes.note(text))
