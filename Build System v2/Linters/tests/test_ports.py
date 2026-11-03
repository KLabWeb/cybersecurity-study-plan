"""Tests that the ports are Protocols, with no abstract base class or coverage exclusion left."""

import re
from pathlib import Path
from typing import Protocol

import pytest

from code_rules.application.ports import SourceProvider
from code_rules.domain.rules import CodeRule

ENCODING = "utf-8"
CONFIG_NAME = "pyproject.toml"
# Whole words only, so a name that merely holds the letters, such as ABCs, is not counted.
ABC_WORD = re.compile(r"\bABC\b")
NOT_IMPLEMENTED_WORD = re.compile(r"\bNotImplementedError\b")
ABSTRACT_WORDS = (ABC_WORD, NOT_IMPLEMENTED_WORD)


def _linters() -> Path:
    return Path(__file__).parents[1]


def _linter_code() -> str:
    this_test = Path(__file__)
    paths = _linters().rglob("*.py")
    others = [path for path in paths if path != this_test]
    texts = [path.read_text(encoding=ENCODING) for path in others]
    return "".join(texts)


@pytest.mark.parametrize("port", (SourceProvider, CodeRule))
def test_the_port_is_a_protocol(port: type) -> None:
    assert Protocol in port.__mro__


def test_no_abstract_base_is_left() -> None:
    code = _linter_code()
    found = [word for word in ABSTRACT_WORDS if word.search(code)]
    assert not found


def test_no_coverage_exclusion_is_left() -> None:
    config = _linters().parent / CONFIG_NAME
    settings = config.read_text(encoding=ENCODING)
    assert "NotImplementedError" not in settings
