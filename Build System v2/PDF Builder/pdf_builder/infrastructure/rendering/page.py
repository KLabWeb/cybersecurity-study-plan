"""The page of the plan PDF: its size, its margins and its fonts."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PAGE_WIDTH = letter[0]
PAGE_HEIGHT = letter[1]
# The binding edge of each page is the inner one; it has an inch, the other edges a little less.
OTHER_MARGINS_INCHES = 0.85
MARGIN_INSIDE = inch
MARGIN_OUTSIDE = OTHER_MARGINS_INCHES * inch
MARGIN_TOP = OTHER_MARGINS_INCHES * inch
MARGIN_BOTTOM = OTHER_MARGINS_INCHES * inch
# The width a table or box may take between the margins.
TEXT_WIDTH = PAGE_WIDTH - MARGIN_INSIDE - MARGIN_OUTSIDE - 2
# The text frame sits a little inside the page margins, below the header and above the footer.
TOP_EXTRA_INCHES = 0.25
BOTTOM_EXTRA_INCHES = 0.1
TEXT_TOP_ROOM = MARGIN_TOP + TOP_EXTRA_INCHES * inch
TEXT_BOTTOM_ROOM = MARGIN_BOTTOM + BOTTOM_EXTRA_INCHES * inch
# The DejaVu fonts draw the arrows and bullet marks the standard fonts lack.
FONTS = (("DejaVu", "DejaVuSans.ttf"), ("DejaVu-Bold", "DejaVuSans-Bold.ttf"))


def register_fonts() -> None:
    """Make the DejaVu fonts bundled beside this file known to the PDF."""
    folder = Path(__file__).parent / "fonts"
    for name, file_name in FONTS:
        font_file = folder / file_name
        pdfmetrics.registerFont(TTFont(name, str(font_file)))
