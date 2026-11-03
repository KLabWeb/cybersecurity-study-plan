"""The build renders the plan again until each contents entry shows the page it lands on."""

import io
from pathlib import Path

from build_fakes import FakeReader, FakeRenderer

from pdf_builder.application.build import MAX_PASSES, PlanBuild
from pdf_builder.domain.contents import ContentsEntry, Pages, PageTexts
from pdf_builder.domain.plan import Cover, DocumentInfo, Plan

INTRO = "Intro"
COVER = "cover"
CONTENTS_PAGE = "x ........ 2"
OUTPUT = "plan.pdf"


def _plan() -> Plan:
    return Plan(
        document=DocumentInfo(
            title="T",
            author="A",
            subject="S",
            start="M",
        ),
        cover=Cover(title_lines=("T",), subtitle="S", pills=()),
        contents_entries=(ContentsEntry(title=INTRO, first_words=INTRO),),
        site_labels=(),
        blocks=(),
    )


def _settled_texts() -> list[PageTexts]:
    return [(COVER, CONTENTS_PAGE, INTRO)]


def _settled_pages() -> Pages:
    return {INTRO: 2}


def _build(reader: FakeReader, renderer: FakeRenderer) -> bool:
    plan_build = PlanBuild(
        renderer=renderer,
        reader=reader,
        out=io.StringIO(),
    )
    return plan_build.run(_plan(), Path(OUTPUT))


def test_build_starts_from_no_pages_and_settles() -> None:
    renderer = FakeRenderer()
    settled = _build(FakeReader(_settled_texts()), renderer)
    assert settled
    assert renderer.rendered[0] == {}


def test_second_render_uses_the_found_pages() -> None:
    renderer = FakeRenderer()
    _build(FakeReader(_settled_texts()), renderer)
    assert renderer.rendered == [{}, _settled_pages()]


def test_build_stops_after_the_last_pass() -> None:
    later: PageTexts = (COVER, CONTENTS_PAGE, "y", INTRO)
    moving: list[PageTexts] = [later, *_settled_texts()]
    renderer = FakeRenderer()
    reader = FakeReader(moving * MAX_PASSES)
    settled = _build(reader, renderer)
    assert not settled
    assert len(renderer.rendered) == MAX_PASSES
