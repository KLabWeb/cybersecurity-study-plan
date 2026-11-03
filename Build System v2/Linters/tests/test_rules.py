"""Tests for the domain rules: each rule is given a parsed module and returns its violations."""

import ast

import pytest

from code_rules.domain.rules import NoLoadTimeCode, NoMutableGlobals, StatelessClasses
from code_rules.domain.violation import Violation

PATH = "pkg/m.py"
NOTHING = ()
NO_CLASSES: frozenset[str] = frozenset()
ONLY_CACHE = frozenset(("Cache",))

type Lines = tuple[int, ...]

CLEAN_MODULE = '''"""Doc."""
import os
import re
LIMIT = 10
NAMES = ("a", "b")
PATTERN = re.compile("x")
def run() -> None:
    pass
class Thing:
    pass
if __name__ == "__main__":
    run()
'''
CONSTRUCTOR_WRITE = "class A:\n    def __init__(self) -> None:\n        self.x = 1\n"
METHOD_WRITE = (
    "class A:\n"
    "    def __init__(self) -> None:\n"
    "        self.x = 1\n"
    "    def bump(self) -> None:\n"
    "        self.x += 1\n"
)
CACHE_WRITE = "class Cache:\n    def put(self) -> None:\n        self.x = 1\n"
LOCAL_WRITE = "class A:\n    def run(self) -> None:\n        count = 1\n"
TYPED_WRITE = "class A:\n    def run(self) -> None:\n        self.x: int = 1\n"


def _lines(violations: list[Violation]) -> Lines:
    return tuple(violation.line for violation in violations)


@pytest.mark.parametrize(
    ("source", "expected"),
    (
        pytest.param(CLEAN_MODULE, NOTHING, id="definitions-constants-and-guard"),
        pytest.param("import sys\nprint('hi')\nsys.exit(1)\n", (2, 3), id="top-level-calls"),
        pytest.param("raw = open('f').read()\n", (1,), id="lowercase-variable"),
        pytest.param("for x in range(3):\n    pass\n", (1,), id="top-level-loop"),
        pytest.param("DATA = open('f').read()\n", (1,), id="constant-built-by-a-call"),
        pytest.param("DATA = make()()\n", (1,), id="constant-from-an-unnamed-call"),
        pytest.param("LIMIT: int = 10\n", NOTHING, id="typed-constant"),
        pytest.param("LIMIT: int\n", (1,), id="type-with-no-value"),
        pytest.param("config.limit = 1\n", (1,), id="attribute-assignment"),
        pytest.param("if DEBUG:\n    pass\n", (1,), id="if-without-comparison"),
        pytest.param("if 1 == __name__:\n    pass\n", (1,), id="if-comparing-to-a-constant"),
    ),
)
def test_load_time_code_is_reported_at_its_line(source: str, expected: Lines) -> None:
    tree = ast.parse(source)
    violations = NoLoadTimeCode().check(tree, PATH)
    assert _lines(violations) == expected


@pytest.mark.parametrize(
    ("source", "expected"),
    (
        pytest.param("A = []\nB = {}\nC = set()\nD = (1, 2)\n", (1, 2, 3), id="list-dict-set"),
        pytest.param("def f() -> None:\n    global X\n    X = 1\n", (2,), id="global-statement"),
        pytest.param("A = (1, 2)\nB = frozenset({1})\nC = 'text'\n", NOTHING, id="frozen-values"),
    ),
)
def test_mutable_globals_are_reported(source: str, expected: Lines) -> None:
    tree = ast.parse(source)
    violations = NoMutableGlobals().check(tree, PATH)
    assert _lines(violations) == expected


@pytest.mark.parametrize(
    ("source", "allowed", "expected"),
    (
        pytest.param(CONSTRUCTOR_WRITE, NO_CLASSES, NOTHING, id="write-in-constructor"),
        pytest.param(METHOD_WRITE, NO_CLASSES, (5,), id="write-in-a-method"),
        pytest.param(CACHE_WRITE, ONLY_CACHE, NOTHING, id="class-on-allowed-list"),
        pytest.param(LOCAL_WRITE, NO_CLASSES, NOTHING, id="local-variable-in-a-method"),
        pytest.param(TYPED_WRITE, NO_CLASSES, (3,), id="typed-write-in-a-method"),
    ),
)
def test_writes_after_construction_are_reported(
    source: str,
    allowed: frozenset[str],
    expected: Lines,
) -> None:
    tree = ast.parse(source)
    violations = StatelessClasses(allowed=allowed).check(tree, PATH)
    assert _lines(violations) == expected


def test_violation_names_its_rule_and_path() -> None:
    tree = ast.parse("print(1)\n")
    violation = NoLoadTimeCode().check(tree, PATH)[0]
    assert violation.path == PATH
    assert violation.rule == "no-load-time-code"
