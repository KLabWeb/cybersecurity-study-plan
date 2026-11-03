"""No file of the Build System names the scratchpad or a place outside the Build System."""

import re
from pathlib import Path

type Pattern = re.Pattern[str]

# Folders of tools and caches, which the Build System's own code does not write by hand.
SKIPPED_FOLDERS = frozenset((
    ".venv", "__pycache__", ".git",
    ".complexipy_cache", ".mypy_cache", ".ruff_cache", ".pytest_cache",
))
# The private records of the work, kept out of git, which name machine paths by design.
PRIVATE_FOLDERS = frozenset((
    "Work Records", "Plan Validator/content", "Plan Validator/sources",
))
# An absolute path: a slash and one of the standard top folders of a Linux machine. The list is
# fixed, so the test means the same on every machine.
MACHINE_PATH = (
    r"(?<![\w.)\]}>$*-])/(?:bin|boot|dev|etc|home|lib|media|mnt|opt|proc|root|run|sbin"
    r"|srv|sys|tmp|usr|var)(?![\w.-])"
)
HOME_PATH = r"(?<![\w.-])~(?=/)|\$\{?HOME\b"
OLD_WORDS = (
    r"scratchpad|Study Plan Drafts|appsec_build_files|(?<![\w-])inventory/"
    r"|(?<![\w-])tools/(?!skills)|room\.html"
)
# Not a place of the machine: the null device, the script launcher line, web addresses,
# and the exam target's own path that the plan quotes.
NOT_A_PLACE = re.compile(
    r"/dev/null|^#!.*|https?://\S+|\{PS\}/\S+|portswigger\.net/\S+|/home/carlos/|desktop/tools/",
)
# Files that quote the old words they search for are held to the rule on machine paths only.
QUOTING_FILES = frozenset(("PDF Builder/tests/test_build_system_paths.py",))


def _place_pattern(*more_words: str) -> Pattern:
    """Return the pattern of an outside place: an absolute path, the home folder, more words."""
    parts = [MACHINE_PATH, HOME_PATH, *more_words]
    return re.compile("|".join(parts))


def _is_skipped(system: Path, path: Path) -> bool:
    relative = path.relative_to(system)
    if any(relative.is_relative_to(private) for private in PRIVATE_FOLDERS):
        return True
    folders = relative.parts[:-1]
    return any(name in SKIPPED_FOLDERS for name in folders)


def _text_files(system: Path) -> list[Path]:
    paths = system.rglob("*")
    kept = [
        path
        for path in paths
        if path.is_file() and not _is_skipped(system, path)
    ]
    return [path for path in kept if b"\0" not in path.read_bytes()]


def _hits(label: str, text: str, pattern: Pattern) -> list[str]:
    lines = [
        NOT_A_PLACE.sub(" ", line)
        for line in text.splitlines()
    ]
    found = [
        (number, place.group(0))
        for number, line in enumerate(lines, 1)
        for place in pattern.finditer(line)
    ]
    return [
        f"{label}:{number}: {word}"
        for number, word in found
    ]


def _file_hits(system: Path, path: Path) -> list[str]:
    label = str(path.relative_to(system))
    more_words = () if label in QUOTING_FILES else (OLD_WORDS,)
    pattern = _place_pattern(*more_words)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    return _hits(label, text, pattern)


def test_no_file_names_an_outside_place() -> None:
    system = Path(__file__).parents[2]
    hits = [
        hit
        for path in _text_files(system)
        for hit in _file_hits(system, path)
    ]
    assert not hits


def test_sample_paths_are_found() -> None:
    home_path = "/".join(("open ~", "notes"))
    top_folder = "/".join(("", "srv"))
    sample = f"{home_path}\nsee the scratchpad\nhttps://example.org/a\nin {top_folder}/notes\n"
    expected = ["sample:1: ~", "sample:2: scratchpad", f"sample:4: {top_folder}"]
    assert _hits("sample", sample, _place_pattern(OLD_WORDS)) == expected

