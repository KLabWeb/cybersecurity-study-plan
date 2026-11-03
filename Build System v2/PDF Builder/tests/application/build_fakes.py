"""Fake parts for tests of the build: a renderer and a page reader."""

from dataclasses import dataclass, field
from pathlib import Path

from pdf_builder.domain.contents import Pages, PageTexts
from pdf_builder.domain.plan import Plan


@dataclass(frozen=True)
class FakeRenderer:
    """Records the pages each render was given."""

    rendered: list[Pages] = field(default_factory=list)

    def render(self, _plan: Plan, pages: Pages, _output: Path) -> None:
        """Record the pages of this render."""
        self.rendered.append(dict(pages))


@dataclass(frozen=True)
class FakeReader:
    """Returns the page texts given, one set per render, the last set from then on."""

    renders: list[PageTexts]

    def page_texts(self, _pdf: Path) -> PageTexts:
        """Return the texts of the next render."""
        if len(self.renders) > 1:
            return self.renders.pop(0)
        return self.renders[0]

