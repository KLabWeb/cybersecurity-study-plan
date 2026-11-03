"""The build command's exit code: 0 when the contents settled, 1 when they did not."""

import pytest

from pdf_builder.interface.cli import exit_code

OUTCOMES = ((True, 0), (False, 1))


@pytest.mark.parametrize(("settled", "expected"), OUTCOMES)
def test_exit_code_tells_if_contents_settled(settled: bool, expected: int) -> None:
    assert exit_code(settled) == expected
