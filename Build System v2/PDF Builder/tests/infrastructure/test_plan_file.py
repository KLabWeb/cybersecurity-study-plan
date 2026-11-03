"""The plan's data file is read into the plan of the domain."""

from pathlib import Path

import pytest

from pdf_builder.domain.contents import ContentsEntry
from pdf_builder.domain.plan import UnknownBlockKindError
from pdf_builder.infrastructure.plan_file import PlanFile

SMALL_PLAN = """
[document]
title = "A Plan"
author = "An Author"
subject = "A Subject"
start = "A Month"

[cover]
title_lines = ["A", "Plan"]
subtitle = "By an author"
pills = [["0", "Pre-", "Study"]]

[site_labels]
"docs.tool.dev" = "the docs"

[[block]]
kind = "contents"

[[block.entries]]
title = "Intro"
first_words = "Intro words"
page = "3"
subsections = []

[[block]]
kind = "heading"
title = "Intro"
"""


def test_contents_entries_carry_their_words(tmp_path: Path) -> None:
    plan_file = tmp_path / "plan.toml"
    plan_file.write_text(SMALL_PLAN, encoding="utf-8")
    plan = PlanFile(plan_file).load()
    entry = ContentsEntry(title="Intro", first_words="Intro words")
    assert plan.contents_entries == (entry,)


def test_an_unknown_block_kind_is_refused(tmp_path: Path) -> None:
    plan_file = tmp_path / "plan.toml"
    misspelled = SMALL_PLAN.replace('kind = "heading"', 'kind = "headng"')
    plan_file.write_text(misspelled, encoding="utf-8")
    with pytest.raises(UnknownBlockKindError, match="headng"):
        PlanFile(plan_file).load()
