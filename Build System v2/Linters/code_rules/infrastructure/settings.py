"""Reads the code rules' settings from the [tool.code_rules] table of pyproject.toml."""

import tomllib
from pathlib import Path


def load_allowed_stateful(config_path: Path) -> frozenset[str]:
    """Return the classes allowed to hold changing state, or none when the table is absent."""
    with config_path.open("rb") as config_file:
        settings = tomllib.load(config_file)

    tool_tables = settings.get("tool", {})
    code_rules_table = tool_tables.get("code_rules", {})

    return frozenset(code_rules_table.get("allowed_stateful", ()))
