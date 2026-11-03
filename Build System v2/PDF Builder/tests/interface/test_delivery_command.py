"""The delivery command reports the dated PDF and exits 0 only when the copy is true."""

import pytest

from pdf_builder.interface.delivery_cli import delivery_exit_code, report_line

OUTCOMES = ((True, 0), (False, 1))


@pytest.mark.parametrize(("matches", "expected"), OUTCOMES)
def test_exit_code_tells_if_the_copy_is_true(matches: bool, expected: int) -> None:
    assert delivery_exit_code(matches) == expected


def test_the_report_names_the_dated_pdf() -> None:
    line = report_line("x.pdf", matches=True)
    assert line == "dated PDF x.pdf equals the Final PDF: True\n"
