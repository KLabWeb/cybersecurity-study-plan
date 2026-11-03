"""The blocks of the phases: steps, resource entries and concept boxes."""

from pdf_builder.domain.plan import Block, BlockKind
from pdf_builder.infrastructure.rendering.layout_context import BlockLayout, Layout, fields
from pdf_builder.infrastructure.rendering.plan_writer import Step

STEP_FIELDS = ("number", "label", "time", "bullets")
RESOURCE_FIELDS = ("title", "details")
CONCEPT_FIELDS = ("name", "text")


def plan_layouts() -> dict[str, BlockLayout]:
    """Return how each kind of phase block is laid out, by its kind."""
    return {
        BlockKind.STEP: _step,
        BlockKind.RESOURCE: _resource,
        BlockKind.CONCEPT: _concept,
    }


def _step(layout: Layout, block: Block) -> None:
    step = Step(*fields(block, STEP_FIELDS))
    layout.writer.step(step)


def _resource(layout: Layout, block: Block) -> None:
    layout.writer.resource(*fields(block, RESOURCE_FIELDS))


def _concept(layout: Layout, block: Block) -> None:
    layout.writer.concept(*fields(block, CONCEPT_FIELDS))
