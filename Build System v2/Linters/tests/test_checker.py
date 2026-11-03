"""Tests for the application checker: it runs every rule over every source it is given."""

from collections.abc import Iterator

from code_rules.application.checker import CodeRuleChecker
from code_rules.domain.rules import NoLoadTimeCode, NoMutableGlobals
from code_rules.domain.source import SourceFile
from code_rules.domain.violation import Violation

type Findings = list[tuple[str, str]]


class _FakeSources:
    """Source files held in memory, standing in for files on disk."""

    def __init__(self, *files: SourceFile) -> None:
        self._files = files

    def files(self) -> Iterator[SourceFile]:
        return iter(self._files)


def _checker_with_two_rules() -> CodeRuleChecker:
    return CodeRuleChecker(rules=(NoLoadTimeCode(), NoMutableGlobals()))


def _findings(violations: list[Violation]) -> Findings:
    pairs = [(violation.path, violation.rule) for violation in violations]
    return sorted(pairs)


def test_runs_every_rule_over_every_file() -> None:
    mutable_list = SourceFile("a.py", "X = []\n")
    top_level_call = SourceFile("b.py", "print(1)\n")
    violations = _checker_with_two_rules().violations(_FakeSources(mutable_list, top_level_call))
    expected = [("a.py", "no-mutable-globals"), ("b.py", "no-load-time-code")]
    assert _findings(violations) == expected


def test_reports_a_file_that_does_not_parse() -> None:
    broken = SourceFile("bad.py", "def (:\n")
    violations = _checker_with_two_rules().violations(_FakeSources(broken))
    assert _findings(violations) == [("bad.py", "syntax-error")]


def test_returns_nothing_for_clean_code() -> None:
    clean = SourceFile("ok.py", "LIMIT = 3\n")
    violations = _checker_with_two_rules().violations(_FakeSources(clean))
    assert not violations
