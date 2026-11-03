"""The three code rules. Each is given a parsed module and returns the violations it finds."""

import ast
from dataclasses import dataclass
from typing import ClassVar, Protocol

from code_rules.domain.methods import (
    Method,
    assignment_targets,
    is_self_attribute,
    ordinary_methods,
)
from code_rules.domain.statements import (
    is_constant_assignment,
    is_main_guard,
    is_module_docstring,
    is_mutable_assignment,
)
from code_rules.domain.violation import Violation

DEFINITIONS = (
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.TypeAlias,
)


class CodeRule(Protocol):
    """A rule. It judges one parsed module; each rule supplies both parts."""

    # The rule's name, printed beside each violation. Each rule sets it once, for the class.
    name: ClassVar[str]

    def check(self, tree: ast.Module, path: str) -> list[Violation]:
        """Return the violations of this rule in the module."""


@dataclass(frozen=True)
class NoLoadTimeCode:
    """No code runs when a module is loaded: only definitions, constants and the main guard."""

    name: ClassVar[str] = "no-load-time-code"

    def check(self, tree: ast.Module, path: str) -> list[Violation]:
        """Return a violation for every top-level statement that runs code on load."""
        violations = []
        for index, statement in enumerate(tree.body):
            if not _is_allowed_at_load(index, statement):
                violations.append(self._violation(statement, path))
        return violations

    def _violation(self, statement: ast.stmt, path: str) -> Violation:
        kind = type(statement).__name__
        return Violation(path, statement.lineno, self.name, f"code runs on load: {kind}")


@dataclass(frozen=True)
class NoMutableGlobals:
    """No module-level list, dict or set, and no global statement."""

    name: ClassVar[str] = "no-mutable-globals"

    def check(self, tree: ast.Module, path: str) -> list[Violation]:
        """Return a violation for every mutable module-level value and every global statement."""
        mutable_values = self._mutable_values(tree, path)
        global_statements = self._global_statements(tree, path)
        return sorted(mutable_values + global_statements, key=_line_of)

    def _mutable_values(self, tree: ast.Module, path: str) -> list[Violation]:
        statements = [node for node in tree.body if is_mutable_assignment(node)]
        message = "mutable value at module level"
        return [
            Violation(path, node.lineno, self.name, message)
            for node in statements
        ]

    def _global_statements(self, tree: ast.Module, path: str) -> list[Violation]:
        statements = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Global)
        ]
        message = "global statement"
        return [
            Violation(path, node.lineno, self.name, message)
            for node in statements
        ]


@dataclass(frozen=True)
class StatelessClasses:
    """No method writes to its object outside the constructor, unless the class is allowed."""

    allowed: frozenset[str]
    name: ClassVar[str] = "stateless-classes"

    def check(self, tree: ast.Module, path: str) -> list[Violation]:
        """Return a violation for every write to the object made outside the constructor."""
        violations = []
        for class_node in self._checked_classes(tree):
            class_name = class_node.name
            for method in ordinary_methods(class_node):
                found = self._method_violations(class_name, method, path)
                violations.extend(found)
        return violations

    def _checked_classes(self, tree: ast.Module) -> list[ast.ClassDef]:
        classes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]
        return [
            class_node
            for class_node in classes
            if class_node.name not in self.allowed
        ]

    def _method_violations(self, class_name: str, method: Method, path: str) -> list[Violation]:
        method_name = method.name
        message = f"{class_name}.{method_name} writes object state"
        writes = [
            target
            for target in assignment_targets(method)
            if is_self_attribute(target)
        ]
        return [
            Violation(path, target.lineno, self.name, message)
            for target in writes
        ]


def _is_allowed_at_load(index: int, statement: ast.stmt) -> bool:
    """Return True for a top-level statement that runs no program logic when loaded."""
    if isinstance(statement, DEFINITIONS):
        return True
    if is_main_guard(statement) or is_constant_assignment(statement):
        return True
    return is_module_docstring(index, statement)


def _line_of(violation: Violation) -> int:
    """Return the line a violation stands on, to sort violations in file order."""
    return violation.line
