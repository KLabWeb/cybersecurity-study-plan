"""Questions about a single top-level statement of a module."""

import ast

from code_rules.domain.expressions import is_constant, is_mutable, is_string_constant
from code_rules.domain.names import is_name, is_upper_name


def is_main_guard(statement: ast.stmt) -> bool:
    """Return True for the block 'if __name__ == "__main__":'."""
    if not isinstance(statement, ast.If):
        return False
    test = statement.test
    if not isinstance(test, ast.Compare):
        return False
    return is_name(test.left, "__name__")


def is_module_docstring(index: int, statement: ast.stmt) -> bool:
    """Return True for a text written as the first statement of a module."""
    is_first = index == 0
    return is_first and _is_text(statement)


def is_constant_assignment(statement: ast.stmt) -> bool:
    """Return True when the statement gives a capital name a constant value."""
    if isinstance(statement, ast.Assign):
        return _is_plain_constant(statement)
    if isinstance(statement, ast.AnnAssign):
        return _is_typed_constant(statement)
    return False


def is_mutable_assignment(statement: ast.stmt) -> bool:
    """Return True when the statement gives a name a list, dict or set."""
    if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
        return False
    return is_mutable(statement.value)


def _is_text(statement: ast.stmt) -> bool:
    """Return True for a statement that is only a piece of text."""
    if not isinstance(statement, ast.Expr):
        return False
    return is_string_constant(statement.value)


def _is_plain_constant(statement: ast.Assign) -> bool:
    """Return True for a statement such as LIMIT = 10."""
    targets = statement.targets
    names_are_upper = all(is_upper_name(target) for target in targets)
    return names_are_upper and is_constant(statement.value)


def _is_typed_constant(statement: ast.AnnAssign) -> bool:
    """Return True for a statement such as LIMIT: int = 10."""
    # A type with no value, such as LIMIT: int, sets nothing, so it is not a constant.
    if statement.value is None:
        return False
    name_is_upper = is_upper_name(statement.target)
    return name_is_upper and is_constant(statement.value)
