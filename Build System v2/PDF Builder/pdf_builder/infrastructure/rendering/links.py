"""Turn the web addresses printed in a text into links, leaving links already written alone."""

import re

LINK_COLOUR = "#3A7AB8"
WEB_ADDRESS = re.compile(
    r"(?<![\w@])((?:[A-Za-z0-9-]+\.)+(?:com|org|net|io|dev|cloud|gov|edu)(?:/[^\s,;)\]<]*)?)",
)
WRITTEN_LINK = re.compile(r"<a\b[^>]*>.*?</a>", re.DOTALL)
# Marks that end a sentence after an address, and so are no part of it.
TRAILING_MARKS = ".,;:"
WEB_SCHEMES = ("http://", "https://")


def linkify(text: str) -> str:
    """Return the text with each printed web address outside a written link made a link."""
    pieces = []
    last = 0
    for written in WRITTEN_LINK.finditer(text):
        before = text[last:written.start()]
        pieces.append(WEB_ADDRESS.sub(_as_link, before))
        pieces.append(written.group(0))
        last = written.end()
    rest = text[last:]
    pieces.append(WEB_ADDRESS.sub(_as_link, rest))
    return "".join(pieces)


def _as_link(found: re.Match[str]) -> str:
    printed = found.group(1)
    address = printed.rstrip(TRAILING_MARKS)
    tail = printed[len(address):]
    target = address if address.startswith(WEB_SCHEMES) else f"https://{address}"
    return f'<a href="{target}" color="{LINK_COLOUR}">{address}</a>{tail}'
