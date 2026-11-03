"""Tests for the command line: it reports each violation and returns a failing exit code."""

import io
from pathlib import Path

import pytest

from code_rules.__main__ import main
from code_rules.interface.cli import run

ENCODING = "utf-8"
SETTINGS = "[tool.code_rules]\nallowed_stateful = []\n"


def _project(folder: Path, code: str) -> Path:
    settings_file = folder / "pyproject.toml"
    settings_file.write_text(SETTINGS, encoding=ENCODING)
    code_file = folder / "m.py"
    code_file.write_text(code, encoding=ENCODING)
    return folder


def test_clean_code_returns_zero(tmp_path: Path) -> None:
    out = io.StringIO()
    exit_code = run(_project(tmp_path, "LIMIT = 1\n"), out)
    assert exit_code == 0
    assert "0 violations" in out.getvalue()


def test_each_violation_is_listed(tmp_path: Path) -> None:
    out = io.StringIO()
    exit_code = run(_project(tmp_path, "print(1)\n"), out)
    assert exit_code == 1
    assert "m.py:1: no-load-time-code" in out.getvalue()


def test_entry_checks_the_folder_named(tmp_path: Path) -> None:
    folder = _project(tmp_path, "print(1)\n")
    assert main([str(folder)]) == 1


def test_no_folder_checks_the_current_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(_project(tmp_path, "LIMIT = 1\n"))
    assert main([]) == 0
