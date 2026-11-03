"""Build the plan PDF: render it again until each contents entry shows the page it lands on.

A changed page number can move later pages, so the plan is rendered, read and rendered
again with the pages found until no contents entry changes. Each build starts from no pages;
nothing is carried from one build to the next.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from pdf_builder.application.ports import PageReader, PlanRenderer
from pdf_builder.domain.contents import Pages, changed_entries, contents_pages
from pdf_builder.domain.plan import Plan

MAX_PASSES = 8


@dataclass(frozen=True)
class PlanBuild:
    """A build of the plan PDF, with the parts it renders and reads pages with."""

    renderer: PlanRenderer
    reader: PageReader
    out: TextIO

    def run(self, plan: Plan, output: Path) -> bool:
        """Render the plan to output until its contents pages settle; return whether they did."""
        pages: Pages = {}
        for number in range(1, MAX_PASSES + 1):
            self.renderer.render(plan, pages, output)
            texts = self.reader.page_texts(output)
            found = contents_pages(texts, plan.contents_entries)
            changed = changed_entries(pages, found)
            if not changed:
                self._tell_settled(number, len(texts))
                return True
            self._tell(f"Pass {number}: {changed} contents page numbers corrected.")
            pages = found
        self._tell(f"The contents did not settle after {MAX_PASSES} passes.")
        return False

    def _tell_settled(self, number: int, page_count: int) -> None:
        self._tell(f"Pass {number}: the contents match the pages, {page_count} pages.")

    def _tell(self, line: str) -> None:
        self.out.write(f"{line}\n")

