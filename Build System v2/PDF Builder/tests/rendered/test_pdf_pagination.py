"""The rendered plan reads cleanly: no stranded heading, orphan, near-blank page or bare address."""

import itertools

from page_rules import Page, bare_addresses

FRONT_PAGES = 2
SAMPLE_PAGE = "continued from before\n\N{BULLET} a bullet (never closed\n"


def _body_pages(rendered_page_texts: list[str]) -> list[Page]:
    return [
        page
        for page in map(Page.from_text, rendered_page_texts[FRONT_PAGES:])
        if page.lines
    ]


def test_rendered_pages_have_no_layout_faults(rendered_page_texts: list[str]) -> None:
    body = _body_pages(rendered_page_texts)
    faulty = [page for page in body if page.faults()]
    assert not faulty


def test_no_entry_leaves_one_line_behind(rendered_page_texts: list[str]) -> None:
    body = _body_pages(rendered_page_texts)
    carried = [
        page
        for page, after in itertools.pairwise(body)
        if page.leaves_one_line_on(after)
    ]
    assert not carried


def test_no_address_is_printed_bare(rendered_page_texts: list[str]) -> None:
    assert not bare_addresses("\n".join(rendered_page_texts))


def test_sample_page_shows_the_three_faults() -> None:
    expected = ["near-blank page", "orphan fragment at top", "unbalanced parentheses"]
    assert Page.from_text(SAMPLE_PAGE).faults() == expected


def test_sample_text_shows_its_bare_address() -> None:
    assert bare_addresses("read example.com/page now") == ["example.com/page"]
