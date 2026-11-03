"""Lay every block of the plan out into the story of the PDF."""

from pdf_builder.domain.contents import Pages
from pdf_builder.domain.plan import Plan
from pdf_builder.infrastructure.rendering.layout_context import BlockLayout, Layout, Story
from pdf_builder.infrastructure.rendering.page_blocks import page_layouts
from pdf_builder.infrastructure.rendering.plan_blocks import plan_layouts
from pdf_builder.infrastructure.rendering.styles import plan_styles
from pdf_builder.infrastructure.rendering.table_blocks import table_layouts
from pdf_builder.infrastructure.rendering.text_blocks import text_layouts


def lay_out_plan(story: Story, plan: Plan, pages: Pages) -> None:
    """Add every block of the plan to the story; pages holds the scanned page of each entry."""
    layout = Layout(story, plan_styles(), pages, plan.site_labels)
    layouts: dict[str, BlockLayout] = {}
    for group in (page_layouts, text_layouts, plan_layouts, table_layouts):
        layouts.update(group())
    for block in plan.blocks:
        layouts[block["kind"]](layout, block)
