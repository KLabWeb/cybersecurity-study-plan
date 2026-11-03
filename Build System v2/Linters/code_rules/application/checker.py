"""The checker: runs every rule over every source file and gathers the violations."""

import ast
from dataclasses import dataclass

from code_rules.application.ports import SourceProvider
from code_rules.domain.rules import CodeRule
from code_rules.domain.source import SourceFile
from code_rules.domain.violation import Violation

SYNTAX_ERROR = "syntax-error"


@dataclass(frozen=True)
class CodeRuleChecker:
    """Runs every rule over every source file."""

    rules: tuple[CodeRule, ...]

    def violations(self, sources: SourceProvider) -> list[Violation]:
        """Return every violation found in every source file."""
        violations: list[Violation] = []
        for source in sources.files():
            violations.extend(self._file_violations(source))
        return violations

    def _file_violations(self, source: SourceFile) -> list[Violation]:
        """Return one file's violations, or one syntax error when the file does not parse."""
        try:
            tree = ast.parse(source.text, filename=source.path)
        except SyntaxError as parse_failure:
            return [_syntax_violation(source.path, parse_failure)]
        return self._rule_violations(tree, source.path)

    def _rule_violations(self, tree: ast.Module, path: str) -> list[Violation]:
        """Return what every rule finds in one parsed file."""
        violations: list[Violation] = []
        for rule in self.rules:
            violations.extend(rule.check(tree, path))
        return violations


def _syntax_violation(path: str, parse_failure: SyntaxError) -> Violation:
    """Return the violation that reports a file Python cannot parse."""
    line = parse_failure.lineno or 0
    return Violation(path, line, SYNTAX_ERROR, parse_failure.msg)
