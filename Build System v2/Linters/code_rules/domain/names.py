"""Questions about a plain name in the code, such as self or LIMIT."""

import ast


def is_name(node: ast.AST, name: str) -> bool:
    """Return True when the node is the plain name given, such as self."""
    if not isinstance(node, ast.Name):
        return False
    return node.id == name


def is_upper_name(node: ast.AST) -> bool:
    """Return True for a plain name written in capitals, such as LIMIT."""
    if not isinstance(node, ast.Name):
        return False
    return node.id.isupper()
