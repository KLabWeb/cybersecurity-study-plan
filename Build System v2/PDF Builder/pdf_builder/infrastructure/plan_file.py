"""The plan's data file: read into the plan of the domain."""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

from pdf_builder.domain.contents import ContentsEntries, ContentsEntry
from pdf_builder.domain.plan import BlockKind, Blocks, Cover, DocumentInfo, Plan, block_kind
from pdf_builder.infrastructure.builder_files import builder_folder

PLAN_FILE = "content/plan.toml"
BLOCKS = "block"
DOCUMENT = "document"
COVER = "cover"
SITE_LABELS = "site_labels"

# A table of the data file, as the TOML reader returns it.
type Table = dict[str, Any]


@dataclass(frozen=True)
class PlanFile:
    """The file that holds the plan."""

    path: Path

    @classmethod
    def of_builder(cls) -> Self:
        """Return the plan's data file of the PDF Builder."""
        return cls(builder_folder() / PLAN_FILE)

    def load(self) -> Plan:
        """Return the plan the file holds."""
        text = self.path.read_text(encoding="utf-8")
        return _plan(tomllib.loads(text))


def _plan(held: Table) -> Plan:
    blocks = tuple(held[BLOCKS])
    _refuse_unknown_kinds(blocks)
    return Plan(
        document=DocumentInfo(**held[DOCUMENT]),
        cover=_cover(held[COVER]),
        contents_entries=_contents_entries(blocks),
        site_labels=tuple(held[SITE_LABELS].items()),
        blocks=blocks,
    )


def _refuse_unknown_kinds(blocks: Blocks) -> None:
    """Raise UnknownBlockKindError for the first block whose kind the plan does not have."""
    for block in blocks:
        block_kind(block["kind"])


def _cover(held: Table) -> Cover:
    pills = tuple(
        tuple(pill)
        for pill in held["pills"]
    )
    title_lines = tuple(held["title_lines"])
    subtitle = held["subtitle"]
    return Cover(title_lines=title_lines, subtitle=subtitle, pills=pills)


def _contents_entries(blocks: Blocks) -> ContentsEntries:
    """Return the entries of the plan's contents block, each with the words that find its page."""
    return tuple(
        ContentsEntry(title=entry["title"], first_words=entry["first_words"])
        for block in blocks
        if block["kind"] == BlockKind.TABLE_OF_CONTENTS
        for entry in block["entries"]
    )
