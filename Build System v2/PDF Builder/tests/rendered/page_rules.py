"""The rules a rendered page of the plan is held to: no orphan, stray heading or bare address."""

import itertools
import re
from dataclasses import dataclass
from typing import Self

PAGE_CHROME = re.compile(r"^\s*(?:Application Security Engineering .*August 2026|\d{1,2})\s*$")
STEP_TITLE = re.compile(r"^\s*\d{2}\. [A-Z][A-Z +/&:\N{EM DASH}-]*[:\N{MIDDLE DOT}]")
LOWER_START = re.compile(r"^[a-z(\N{LEFT SINGLE QUOTATION MARK}\N{RIGHT SINGLE QUOTATION MARK}']")
WHOLE_SENTENCE = re.compile(r"^[A-Za-z].*[.!?\N{RIGHT SINGLE QUOTATION MARK}']\s*$")
ENDS_CLOSED = re.compile(r"[.!?\N{RIGHT SINGLE QUOTATION MARK})\]\"]\s*$")
INDENTED = re.compile(r"^\s{4,}\S")
CONTINUES = re.compile(r"^\s*[a-z(]")
DOMAIN = re.compile(
    r"(?<![\w@/])((?:[a-z0-9-]+\.)+(?:com|org|net|io|dev|cloud|shop|wiki)(?:/[\w\-./#?=&%+]*)?)",
)
BULLET = "\N{BULLET}"
HEADINGS = frozenset((
    "Learning Resources",
    "Concepts and Their Use on the Job",
    "Projects & Writings",
    "Application Strategy",
    "First Two Weeks",
    "What You Bring on Day One",
    "Core Groups",
    "Conferences",
    "Philadelphia AppSec Community",
    "Phase Timeline",
    "Study Methodology",
    "Note-Taking: Notes \N{RIGHTWARDS ARROW} Note Cards",
    "Portfolio: Writeups & Project Site",
    "Local & Regional Events",
))
HEADING_STARTS = (
    "Projects & Writings ",
    "Pre-Study Schedule ",
    "AppSec Intro ",
    "Web & Network Foundations ",
    "Core Vulnerability Classes ",
    "Security Testing & Tooling ",
    "Cloud Security Fundamentals ",
    "Secure Code Review ",
    "CompTIA Security+ Certification ",
    "Interview Preparation ",
)
# Product names that are also web addresses, allowed in the text.
ALLOWED_ADDRESSES = (
    "localhost",
    "169.254.169.254",
    "flaws.cloud",
    "flaws2.cloud",
    "interviewing.io",
    "typebot.io",
)
# The cover and the contents pages.
FEWEST_LINES = 8


@dataclass(frozen=True)
class Page:
    """One page of the rendered plan, without its running header and page number."""

    lines: tuple[str, ...]

    @classmethod
    def from_text(cls, text: str) -> Self:
        """Return the page's content lines."""
        lines = text.split("\n")
        kept = [
            line
            for line in lines
            if line.strip() and not PAGE_CHROME.match(line)
        ]
        return cls(tuple(kept))

    def faults(self) -> list[str]:
        """Return the names of the layout faults on this page."""
        bottom = self.lines[-2:]
        stranded = any(map(_is_heading, bottom))
        checks = (
            ("near-blank page", len(self.lines) < FEWEST_LINES),
            ("orphan fragment at top", self._has_orphan_top()),
            ("heading stranded at page bottom", stranded),
            ("step title without a bullet", self._has_step_without_bullet()),
            ("unbalanced parentheses", self._has_unbalanced_entry()),
        )
        return [name for name, found in checks if found]

    def starts_alone(self) -> bool:
        """Return True when the first line stands alone before a heading or a bullet."""
        if len(self.lines) == 1:
            return True
        second = self.lines[1]
        return _is_heading(second) or _is_bullet(second)

    def leaves_one_line_on(self, after: Self) -> bool:
        """Return True when this page's last entry leaves a single line on the next page."""
        last = self.lines[-1]
        if not after.lines or not _is_open_entry(last):
            return False
        first_next = after.lines[0]
        continues = bool(CONTINUES.match(first_next))
        return continues and after.starts_alone()

    def _has_orphan_top(self) -> bool:
        first = self.lines[0].strip()
        lower = LOWER_START.match(first)
        whole = WHOLE_SENTENCE.match(first)
        return bool(lower or whole) and self.starts_alone()

    def _has_step_without_bullet(self) -> bool:
        bullets = [
            index
            for index, line in enumerate(self.lines)
            if _is_bullet(line)
        ]
        last_bullet = max(bullets, default=-1)
        after_last_bullet = self.lines[last_bullet + 1:]
        return any(STEP_TITLE.match(line) for line in after_last_bullet)

    def _has_unbalanced_entry(self) -> bool:
        # An entry starts at a bullet or a heading; its parentheses must close before the next.
        starts = [
            _is_bullet(line) or _is_heading(line)
            for line in self.lines
        ]
        starts.append(True)
        deltas = [
            line.count("(") - line.count(")")
            for line in self.lines
        ]
        depths = itertools.accumulate(deltas, initial=0)
        return any(
            depth
            for depth, start in zip(depths, starts, strict=True)
            if start
        )


def _is_heading(line: str) -> bool:
    text = line.strip()
    if text in HEADINGS:
        return True
    if text.startswith(HEADING_STARTS):
        return True
    return bool(STEP_TITLE.match(line))


def _is_bullet(line: str) -> bool:
    return line.strip().startswith(BULLET)


def _is_open_entry(line: str) -> bool:
    if ENDS_CLOSED.search(line):
        return False
    indented = bool(INDENTED.match(line))
    return _is_bullet(line) or indented


def bare_addresses(text: str) -> list[str]:
    found = DOMAIN.findall(text)
    bare = {address.rstrip(".,;)") for address in found}
    for allowed in ALLOWED_ADDRESSES:
        bare = {address for address in bare if allowed not in address}
    return sorted(bare)
