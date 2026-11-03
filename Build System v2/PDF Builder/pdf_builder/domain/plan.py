"""The plan: its blocks in the order the PDF prints them, and the page of each contents entry."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from pdf_builder.domain.contents import ContentsEntries

# One block of the plan, such as a heading, a step or a table, with its kind and its fields.
type Block = dict[str, Any]
type Blocks = tuple[Block, ...]
# A pill of the cover: the phase numeral and the two lines of its label.
type Pill = tuple[str, str, str]
# The words a further site of a resource entry is linked on, by a piece of its address.
type SiteLabels = tuple[tuple[str, str], ...]


class BlockKind(StrEnum):
    """The kinds of block the plan is made of."""

    BANNER = "banner"
    BULLET = "bullet"
    CONCEPT = "concept"
    TABLE_OF_CONTENTS = "contents"
    HEADING = "heading"
    NOTE = "note"
    PAGE_BREAK = "page_break"
    PAGE_ROOM = "page_room"
    PARAGRAPH = "paragraph"
    RESOURCE = "resource"
    RULE = "rule"
    SCHEDULE = "schedule"
    SPACE = "space"
    STEP = "step"
    SUBHEADING = "subheading"
    TIMELINE = "timeline"


class UnknownBlockKindError(ValueError):
    """A block names a kind the plan does not have."""


def block_kind(text: str) -> BlockKind:
    """Return the kind a block's kind text names; raise UnknownBlockKindError for any other text."""
    try:
        return BlockKind(text)
    except ValueError as error:
        raise UnknownBlockKindError(text) from error


@dataclass(frozen=True)
class DocumentInfo:
    """What the PDF file says about itself, and the month the plan started."""

    title: str
    author: str
    subject: str
    start: str


@dataclass(frozen=True)
class Cover:
    """The words of the cover: its title lines, the line beneath them, and one pill per phase."""

    title_lines: tuple[str, ...]
    subtitle: str
    pills: tuple[Pill, ...]


@dataclass(frozen=True)
class Plan:
    """The whole plan, as its data file holds it."""

    document: DocumentInfo
    cover: Cover
    contents_entries: ContentsEntries
    site_labels: SiteLabels
    blocks: Blocks
