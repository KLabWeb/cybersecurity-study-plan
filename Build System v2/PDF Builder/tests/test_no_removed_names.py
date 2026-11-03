"""Tests that no code or setting of the Build System still names a removed plan-content check."""

from pathlib import Path

from removed_plan_checks import REMOVED_DATA, REMOVED_HELPERS, REMOVED_TESTS

ENCODING = "utf-8"
SEARCHED_FOLDERS = ("PDF Builder", "Linters")
SEARCHED_FILES = ("pyproject.toml", "setup.cfg")
SKIPPED_FOLDERS = frozenset((".venv", "__pycache__"))
# The changelog keeps the history of the removal; the list of removed names quotes them.
SKIPPED_FILES = frozenset(("CHANGELOG_APPLIED.md", "removed_plan_checks.py"))


def _is_skipped_folder(name: str) -> bool:
    return name in SKIPPED_FOLDERS or "cache" in name


def _is_searched(path: Path) -> bool:
    if path.name in SKIPPED_FILES or not path.is_file():
        return False
    folders = path.parts[:-1]
    return not any(_is_skipped_folder(name) for name in folders)


def _candidates() -> list[Path]:
    system = Path(__file__).parents[2]
    found = [system / name for name in SEARCHED_FILES]
    for name in SEARCHED_FOLDERS:
        found.extend((system / name).rglob("*"))
    return found


def _names_a_removed_file(path: Path) -> bool:
    raw = path.read_bytes()
    if b"\0" in raw:
        return False
    text = raw.decode(ENCODING, errors="ignore")
    names = REMOVED_TESTS + REMOVED_HELPERS + REMOVED_DATA
    return any(name in text for name in names)


def test_nothing_names_a_removed_file() -> None:
    searched = [path for path in _candidates() if _is_searched(path)]
    naming = [path for path in searched if _names_a_removed_file(path)]
    assert not naming
