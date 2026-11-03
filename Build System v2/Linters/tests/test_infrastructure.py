"""Tests for the infrastructure: reading source files and the settings."""

from pathlib import Path

from code_rules.infrastructure.file_sources import FileSystemSources
from code_rules.infrastructure.settings import load_allowed_stateful

ENCODING = "utf-8"
CONFIG_NAME = "pyproject.toml"
EXCLUDED = frozenset((".venv",))


def _write(folder: Path, name: str, text: str) -> None:
    folder.mkdir(exist_ok=True)
    target = folder / name
    target.write_text(text, encoding=ENCODING)


def test_sources_read_code_and_skip_excluded(tmp_path: Path) -> None:
    package = tmp_path / "pkg"
    _write(package, "a.py", "A = 1\n")
    _write(package, "notes.txt", "not code\n")
    _write(tmp_path / ".venv", "lib.py", "B = 2\n")
    sources = FileSystemSources(root=tmp_path, excluded=EXCLUDED)
    found = [
        (source.path, source.text)
        for source in sources.files()
    ]
    assert found == [("pkg/a.py", "A = 1\n")]


def test_settings_read_the_allowed_list(tmp_path: Path) -> None:
    _write(tmp_path, CONFIG_NAME, '[tool.code_rules]\nallowed_stateful = ["Cache"]\n')
    allowed = load_allowed_stateful(tmp_path / CONFIG_NAME)
    assert allowed == frozenset(("Cache",))


def test_settings_without_the_section_allow_none(tmp_path: Path) -> None:
    _write(tmp_path, CONFIG_NAME, "[tool.other]\n")
    allowed = load_allowed_stateful(tmp_path / CONFIG_NAME)
    assert not allowed
