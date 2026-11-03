"""The contents of the plan: its entries, and the page each one lands on in the PDF."""

import re
from collections.abc import Sequence
from dataclasses import dataclass

# The page each contents entry is printed on, by the entry's title.
type Pages = dict[str, int]
# The text of each page of the PDF, in page order; a page's index is its printed number.
type PageTexts = Sequence[str]
# The entries of the contents, in the order the plan prints them.
type ContentsEntries = tuple["ContentsEntry", ...]

# A contents page is told by its dotted leaders.
CONTENTS_LEADER = re.compile(r"\.{6,}")
FIRST_CONTENT_PAGE = 2


@dataclass(frozen=True)
class ContentsEntry:
    """An entry of the contents: its title, and words printed on the first page of its section."""

    title: str
    first_words: str


def contents_pages(texts: PageTexts, entries: Sequence[ContentsEntry]) -> Pages:
    """Return the page of each entry: the first page after the one before that holds its words."""
    pages: Pages = {}
    after = _content_start(texts)
    for entry in entries:
        page = _first_page_with(entry.first_words, texts, after)
        if page is not None:
            pages[entry.title] = page
            after = page + 1
    return pages


def changed_entries(shown: Pages, found: Pages) -> int:
    """Return how many entries found show another page in the contents."""
    return sum(
        1
        for title, page in found.items()
        if shown.get(title) != page
    )


def _content_start(texts: PageTexts) -> int:
    contents_pages_found = [
        index
        for index, text in enumerate(texts)
        if CONTENTS_LEADER.search(text)
    ]
    if contents_pages_found:
        return max(contents_pages_found) + 1
    return FIRST_CONTENT_PAGE


def _first_page_with(words: str, texts: PageTexts, start: int) -> int | None:
    later = range(start, len(texts))
    found = (
        index
        for index in later
        if words in texts[index]
    )
    return next(found, None)
