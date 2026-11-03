"""Shared test fixtures: the plan built once for the whole test run."""

import io
from pathlib import Path

import pytest

from pdf_builder.application.build import PlanBuild
from pdf_builder.infrastructure.page_scan import PdfPageReader
from pdf_builder.infrastructure.plan_file import PlanFile
from pdf_builder.infrastructure.rendering.plan_document import PlanDocument


@pytest.fixture(scope="session")
def rendered_plan(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Return a PDF built from the plan source into a temporary folder, its contents settled."""
    output = tmp_path_factory.mktemp("render") / "plan.pdf"
    plan = PlanFile.of_builder().load()
    plan_build = PlanBuild(
        renderer=PlanDocument(),
        reader=PdfPageReader(),
        out=io.StringIO(),
    )
    assert plan_build.run(plan, output)
    return output


@pytest.fixture(scope="session")
def rendered_page_texts(rendered_plan: Path) -> list[str]:
    """Return the text of each page of the rendered plan, laid out as on the page."""
    texts = PdfPageReader().layout_texts(rendered_plan)
    return list(texts)
