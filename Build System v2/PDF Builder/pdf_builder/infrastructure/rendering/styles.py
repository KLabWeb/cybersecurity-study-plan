"""The paragraph styles of the plan PDF, read from the style data beside this file."""

import json
from pathlib import Path
from typing import Any

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

from pdf_builder.infrastructure.rendering import palette

STYLE_FILE = "data/styles.json"
ALIGNMENTS = (
    ("left", TA_LEFT),
    ("center", TA_CENTER),
    ("justify", TA_JUSTIFY),
)
# The colours the style data may name, by their name in the palette.
COLOURS = (
    ("DARK", palette.DARK),
    ("ACCENT", palette.ACCENT),
    ("MID_GRAY", palette.MID_GRAY),
    ("SOFT_BLUE", palette.SOFT_BLUE),
    ("NOTE_TEXT", palette.NOTE_TEXT),
    ("LINK_BLUE", palette.LINK_BLUE),
    ("CAPTION_GRAY", palette.CAPTION_GRAY),
    ("WHITE", palette.WHITE),
)

type Settings = dict[str, Any]


def plan_styles() -> dict[str, ParagraphStyle]:
    """Return every paragraph style of the plan, each named by its key in the style data."""
    style_file = Path(__file__).parent / STYLE_FILE
    table: dict[str, Settings] = json.loads(style_file.read_text(encoding="utf-8"))
    return {
        name: _style(name, settings)
        for name, settings in table.items()
    }


def _style(name: str, settings: Settings) -> ParagraphStyle:
    options = dict(settings)
    colour = dict(COLOURS)[options["textColor"]]
    options["textColor"] = HexColor(colour)
    alignment = options.get("alignment")
    if alignment is not None:
        options["alignment"] = dict(ALIGNMENTS)[alignment]
    parent = getSampleStyleSheet()["Normal"]
    return ParagraphStyle(name, parent=parent, **options)
