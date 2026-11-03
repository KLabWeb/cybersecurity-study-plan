"""The paragraph styles of the plan have plain names, and each style is named by its key."""

from pdf_builder.infrastructure.rendering.styles import plan_styles

STYLE_NAMES = frozenset((
    "banner_duration",
    "body",
    "bullet",
    "caption",
    "contents_entry",
    "contents_subsection",
    "heading",
    "note_text",
    "section_numeral",
    "section_title",
    "small_bullet",
    "subsection_heading",
    "table_cell",
    "table_cell_centred",
    "table_header",
))


def test_the_styles_have_plain_names() -> None:
    assert frozenset(plan_styles()) == STYLE_NAMES


def test_each_style_is_named_by_its_key() -> None:
    mismatched = [
        key
        for key, style in plan_styles().items()
        if style.name != key
    ]
    assert not mismatched
