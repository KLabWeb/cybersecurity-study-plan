"""Tests that the removed plan-content checks stay gone, and the kept tests stay."""

from pathlib import Path

from removed_plan_checks import REMOVED_HELPERS, REMOVED_TESTS

KEPT_TESTS = (
    "test_build_system_paths.py",
    "infrastructure/test_plan_file.py",
    "application/test_plan_build.py",
    "rendered/conftest.py",
)


def _exists(name: str) -> bool:
    path = Path(__file__).parent / name
    return path.exists()


def test_the_removed_checks_and_helpers_are_gone() -> None:
    names = REMOVED_TESTS + REMOVED_HELPERS
    files = [f"{name}.py" for name in names]
    left = [name for name in files if _exists(name)]
    assert not left


def test_the_data_folder_is_gone() -> None:
    assert not _exists("data")


def test_the_kept_tests_stay() -> None:
    missing = [name for name in KEPT_TESTS if not _exists(name)]
    assert not missing
