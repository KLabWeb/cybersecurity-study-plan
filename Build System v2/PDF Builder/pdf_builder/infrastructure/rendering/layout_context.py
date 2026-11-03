"""What every block of the plan is laid out with: the story of the PDF, the styles and the pages."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable

from pdf_builder.domain.contents import Pages
from pdf_builder.domain.plan import Block, SiteLabels
from pdf_builder.infrastructure.rendering.boxes import PlanBoxes
from pdf_builder.infrastructure.rendering.plan_writer import PlanWriter

type Story = list[Flowable]
type Names = tuple[str, ...]
type FieldValues = list[Any]


@dataclass(frozen=True)
class Layout:
    """The story of the PDF, the plan's styles, and the scanned page of each contents entry."""

    story: Story
    styles: dict[str, ParagraphStyle]
    pages: Pages
    site_labels: SiteLabels

    def add(self, *flowables: Flowable) -> None:
        """Add the flowables to the end of the story."""
        self.story.extend(flowables)

    @property
    def writer(self) -> PlanWriter:
        """Return the writer that adds headings, steps, concepts and entries to the story."""
        return PlanWriter(self.story, self.styles, self.site_labels)

    @property
    def boxes(self) -> PlanBoxes:
        """Return the builder of note boxes and phase banners in the plan's styles."""
        return PlanBoxes(self.styles)


type BlockLayout = Callable[[Layout, Block], None]


def fields(block: Block, names: Names) -> FieldValues:
    """Return the block's fields of the names given, in that order."""
    return [
        block[name]
        for name in names
    ]
