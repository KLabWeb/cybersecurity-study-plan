"""Lay a step's bullets out, nested lists included, with their links and arrows drawn."""

import re
from dataclasses import dataclass
from typing import Self

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable, KeepTogether, Paragraph, Spacer

from pdf_builder.infrastructure.rendering.links import linkify

ARROW = "→"
# The arrow and the bullet mark, drawn in the font that has them.
DRAWN_ARROW = '<font name="DejaVu">→</font>'
BULLET_MARK = '<font name="DejaVu">•</font>'
# A step bullet may carry a nested list: [[lvl]] starts a level line such as "Apprentice:",
# and [[li]] starts one entry under it.
NESTED_MARK = "[["
LEVEL_LINE = "[[lvl]]"
LEVEL_KIND = "lvl"
NESTED_PART = re.compile(r"\[\[(lvl|li)\]\]")
# How many flowables of a step's first bullet stay on the page with the step title.
KEPT_WITH_TITLE = 3
STEP_GAP = 4
BULLET_GAP = 2
ENTRY_INDENT = 36

type Flowables = list[Flowable]
type Styles = dict[str, ParagraphStyle]
type Lines = list[str]


@dataclass(frozen=True)
class StepBullets:
    """Turns a step's bullets into flowables, in the plan's styles."""

    styles: Styles

    def bullet(self, text: str) -> Paragraph:
        """Return the text as a bullet, its web addresses linked and its arrows drawn."""
        marked = f"{BULLET_MARK} {drawn(text)}"
        return Paragraph(marked, self.styles["bullet"])

    def flowables(self, text: str) -> Flowables:
        """Return a bullet, followed by its nested list when it carries one."""
        if NESTED_MARK not in text:
            return [self.bullet(text)]
        parts = NESTED_PART.split(text)
        sub_style = self.styles["small_bullet"]
        if LEVEL_LINE in text:
            nested = NestedStyles.levelled(sub_style)
        else:
            nested = NestedStyles.flat(sub_style)
        head = self.bullet(parts[0].strip())
        entries = nested.entries(parts)
        return [head, *entries, Spacer(1, BULLET_GAP)]

    def step_flowables(self, title: Paragraph, bullets: Lines) -> Flowables:
        """Return a step's flowables: the title kept with its first bullet, then the rest."""
        if not bullets:
            return [title, Spacer(1, STEP_GAP)]
        first = self.flowables(bullets[0])
        first_lines = first[:KEPT_WITH_TITLE]
        kept = KeepTogether([title, *first_lines])
        rest = first[KEPT_WITH_TITLE:]
        later = [
            flowable
            for text in bullets[1:]
            for flowable in self.flowables(text)
        ]
        later.append(Spacer(1, STEP_GAP))
        return [kept, *rest, *later]


@dataclass(frozen=True)
class NestedStyles:
    """The styles of a nested list's level lines and of its entries."""

    level: ParagraphStyle
    entry: ParagraphStyle

    @classmethod
    def flat(cls, sub_style: ParagraphStyle) -> Self:
        """Return the styles of a nested list with no level lines: entries in the sub style."""
        return cls(cls._level_style(sub_style), sub_style)

    @classmethod
    def levelled(cls, sub_style: ParagraphStyle) -> Self:
        """Return the styles of a nested list with level lines: entries indented under them."""
        entry = ParagraphStyle(
            "bullet_label",
            parent=sub_style,
            leftIndent=ENTRY_INDENT,
            spaceAfter=1,
        )
        return cls(cls._level_style(sub_style), entry)

    def paragraph(self, kind: str, text: str) -> Paragraph:
        """Return one level line, or one entry with its bullet mark."""
        drawn_text = drawn(text.strip())
        if kind == LEVEL_KIND:
            return Paragraph(drawn_text, self.level)
        return Paragraph(f"{BULLET_MARK} {drawn_text}", self.entry)

    def entries(self, parts: Lines) -> Flowables:
        """Return the level lines and entries of a bullet split at its nested-list marks."""
        kinds = parts[1::2]
        texts = parts[2::2]
        return [
            self.paragraph(kind, text)
            for kind, text in zip(kinds, texts, strict=True)
        ]

    @classmethod
    def _level_style(cls, sub_style: ParagraphStyle) -> ParagraphStyle:
        return ParagraphStyle("bullet_level", parent=sub_style, spaceAfter=1)


def drawn(text: str) -> str:
    """Return the text with its web addresses linked and its arrows drawn in the arrow's font."""
    linked = linkify(text)
    return linked.replace(ARROW, DRAWN_ARROW)
