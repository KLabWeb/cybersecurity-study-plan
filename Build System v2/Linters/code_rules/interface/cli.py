"""The command line: checks every Python file under a folder and prints each violation."""

from pathlib import Path
from typing import TextIO

from code_rules.application.checker import CodeRuleChecker
from code_rules.domain.rules import CodeRule, NoLoadTimeCode, NoMutableGlobals, StatelessClasses
from code_rules.domain.violation import Violation
from code_rules.infrastructure.file_sources import FileSystemSources
from code_rules.infrastructure.settings import load_allowed_stateful

CONFIG_NAME = "pyproject.toml"
EXCLUDED = frozenset((".venv", "__pycache__"))
CLEAN = 0
FAILED = 1


def run(project_dir: Path, out: TextIO) -> int:
    """Check the folder, print what was found, and return 0 when clean or 1 when not."""
    allowed = load_allowed_stateful(project_dir / CONFIG_NAME)
    checker = CodeRuleChecker(rules=_rules(allowed))
    sources = FileSystemSources(root=project_dir, excluded=EXCLUDED)
    violations = checker.violations(sources)
    _report(violations, out)
    if violations:
        return FAILED
    return CLEAN


def _rules(allowed: frozenset[str]) -> tuple[CodeRule, ...]:
    """Return the three rules, the stateless rule told which classes are exempt."""
    return (NoLoadTimeCode(), NoMutableGlobals(), StatelessClasses(allowed=allowed))


def _report(violations: list[Violation], out: TextIO) -> None:
    """Write one line per violation, then the count."""
    for violation in violations:
        out.write(f"{violation}\n")
    count = len(violations)
    out.write(f"{count} violations\n")
