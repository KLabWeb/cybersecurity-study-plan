"""Questions about the methods of a class and what they assign to."""

import ast

from code_rules.domain.names import is_name

STATE_WRITERS = frozenset(("__init__", "__post_init__", "__new__"))
METHOD_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)

type Method = ast.FunctionDef | ast.AsyncFunctionDef


def ordinary_methods(class_node: ast.ClassDef) -> list[Method]:
    """Return the methods of a class, leaving out the ones that build the object."""
    methods = [
        node
        for node in class_node.body
        if isinstance(node, METHOD_NODES)
    ]
    return [method for method in methods if method.name not in STATE_WRITERS]


def assignment_targets(method: Method) -> list[ast.expr]:
    """Return everything the method assigns to, in the order the statements appear."""
    targets: list[ast.expr] = []
    for node in ast.walk(method):
        targets.extend(_targets_of(node))
    return targets


def is_self_attribute(target: ast.expr) -> bool:
    """Return True for an attribute of the object itself, such as self.count."""
    if not isinstance(target, ast.Attribute):
        return False
    return is_name(target.value, "self")


def _targets_of(node: ast.AST) -> list[ast.expr]:
    """Return what one statement assigns to, or nothing when it is not an assignment."""
    if isinstance(node, ast.Assign):
        return node.targets
    if isinstance(node, (ast.AugAssign, ast.AnnAssign)):
        return [node.target]
    return []
