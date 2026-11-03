"""Tests that the coverage record goes into a cache folder, never at the Build System top."""

import tomllib
from pathlib import Path, PurePosixPath

ENCODING = "utf-8"
CONFIG_NAME = "pyproject.toml"
RECORD_NAME = ".coverage"


def _system() -> Path:
    return Path(__file__).parents[2]


def _record_setting() -> str:
    config = _system() / CONFIG_NAME
    settings = tomllib.loads(config.read_text(encoding=ENCODING))
    coverage = settings["tool"]["coverage"]
    return str(coverage["run"]["data_file"])


def test_the_record_goes_to_a_cache_folder() -> None:
    top_folder = PurePosixPath(_record_setting()).parts[0]
    assert "cache" in top_folder


def test_no_coverage_record_at_the_top() -> None:
    record = _system() / RECORD_NAME
    assert not record.exists()
