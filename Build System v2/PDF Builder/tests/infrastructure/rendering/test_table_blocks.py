"""A contents entry is laid out with dots up to the page it lands on."""

from reportlab.platypus import Paragraph

from pdf_builder.domain.plan import BlockKind
from pdf_builder.infrastructure.rendering.layout_context import Layout
from pdf_builder.infrastructure.rendering.styles import plan_styles
from pdf_builder.infrastructure.rendering.table_blocks import table_layouts


def _laid_out_contents() -> list[Paragraph]:
    scanned_pages = {"Intro": 3}
    layout = Layout(
        story=[],
        styles=plan_styles(),
        pages=scanned_pages,
        site_labels=(),
    )
    entry = {"title": "Intro", "page": "9", "subsections": ["Why"]}
    contents_block = {"kind": "contents", "entries": [entry]}
    table_layouts()[BlockKind.TABLE_OF_CONTENTS](layout, contents_block)
    return [flowable for flowable in layout.story if isinstance(flowable, Paragraph)]


def test_an_entry_shows_its_scanned_page() -> None:
    entry_line = _laid_out_contents()[0].text
    assert entry_line.startswith("<b>Intro</b>")
    assert entry_line.endswith("</font>3")


def test_a_subsection_follows_its_entry() -> None:
    assert _laid_out_contents()[1].text.endswith("Why")
