"""Questions about a single expression: what it calls, and whether it is constant or mutable."""

import ast

CONSTANT_CALLS = frozenset(("frozenset", "tuple", "re.compile"))
MUTABLE_CALLS = frozenset(("list", "dict", "set", "bytearray", "defaultdict"))
MUTABLE_LITERALS = (
    ast.List,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
)


def callee_name(call: ast.Call) -> str:
    """Return what a call calls as dotted text, such as 're.compile', or '' when unnamed."""
    function = call.func
    if isinstance(function, ast.Name):
        return function.id
    if isinstance(function, ast.Attribute):
        return _attribute_name(function)
    return ""


def is_constant(expression: ast.expr) -> bool:
    """Return True when every call inside the expression is one that builds a constant."""
    nodes = ast.walk(expression)
    return all(_builds_constant(node) for node in nodes)


def is_mutable(expression: ast.expr | None) -> bool:
    """Return True for a list, dict or set, written out or built by a call."""
    if isinstance(expression, MUTABLE_LITERALS):
        return True
    if not isinstance(expression, ast.Call):
        return False
    return callee_name(expression) in MUTABLE_CALLS


def is_string_constant(node: ast.AST) -> bool:
    """Return True for a piece of text written straight into the code."""
    if not isinstance(node, ast.Constant):
        return False
    return isinstance(node.value, str)


def _attribute_name(attribute: ast.Attribute) -> str:
    """Return 're.compile' for re.compile, or '' when the owner is not a plain name."""
    owner = attribute.value
    if not isinstance(owner, ast.Name):
        return ""
    return ".".join((owner.id, attribute.attr))


def _builds_constant(node: ast.AST) -> bool:
    """Return True for any node that is not a call, and for a call known to build a constant."""
    if not isinstance(node, ast.Call):
        return True
    return callee_name(node) in CONSTANT_CALLS
