"""The page each contents entry lands on, found from the text of the rendered pages."""

from pdf_builder.domain.contents import (
    ContentsEntries,
    ContentsEntry,
    changed_entries,
    contents_pages,
)

INTRO = "Intro"
PHASE = "Phase I"
PHASE_WORDS = "First phase"
COVER = "cover"
CONTENTS_PAGE = "Intro ........ 2"


def _entries() -> ContentsEntries:
    return (
        ContentsEntry(title=INTRO, first_words=INTRO),
        ContentsEntry(title=PHASE, first_words=PHASE_WORDS),
    )


def test_entry_lands_after_the_contents_pages() -> None:
    texts = [COVER, CONTENTS_PAGE, INTRO, PHASE_WORDS]
    pages = contents_pages(texts, _entries())
    assert pages == {INTRO: 2, PHASE: 3}


def test_entry_is_found_after_the_one_before() -> None:
    texts = [COVER, CONTENTS_PAGE, f"{PHASE_WORDS} {INTRO}", PHASE_WORDS]
    pages = contents_pages(texts, _entries())
    assert pages == {INTRO: 2, PHASE: 3}


def test_entry_on_no_page_is_left_out() -> None:
    texts = [COVER, CONTENTS_PAGE, PHASE_WORDS]
    pages = contents_pages(texts, _entries())
    assert pages == {PHASE: 2}


def test_no_contents_page_starts_on_page_two() -> None:
    texts = [INTRO, PHASE_WORDS, INTRO, PHASE_WORDS]
    pages = contents_pages(texts, _entries())
    assert pages == {INTRO: 2, PHASE: 3}


def test_an_entry_moved_counts_as_changed() -> None:
    shown = {INTRO: 2, PHASE: 3}
    found = {INTRO: 2, PHASE: 4}
    assert changed_entries(shown, found) == 1
