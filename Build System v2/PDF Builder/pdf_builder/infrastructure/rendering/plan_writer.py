"""Lay the plan's pieces of text into the story of the PDF, in the plan's styles."""

from dataclasses import dataclass

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import CondPageBreak, HRFlowable, KeepTogether, Paragraph, Spacer

from pdf_builder.domain.plan import SiteLabels
from pdf_builder.infrastructure.rendering.palette import ACCENT
from pdf_builder.infrastructure.rendering.resource_links import resource_text
from pdf_builder.infrastructure.rendering.step_bullets import (
    Flowables,
    Lines,
    StepBullets,
    Styles,
    drawn,
)

RULE_SPACE_ABOVE = 4
RULE_SPACE_BELOW = 8
ON_THE_JOB = "<b>On the job:</b>"
# Room, in inches, that a heading, a sub-heading and a step need left on the page.
HEADING_ROOM = 1.3
SUBHEADING_ROOM = 1.4
STEP_ROOM = 1.2


@dataclass(frozen=True)
class Step:
    """A step of a phase: its number, its label, its time and its bullets."""

    number: str
    label: str
    time: str
    bullets: Lines


@dataclass(frozen=True)
class PlanWriter:
    """Adds the plan's headings, steps, concepts and resource entries to the story of the PDF."""

    story: Flowables
    styles: Styles
    site_labels: SiteLabels

    def bullet(self, text: str) -> Paragraph:
        """Return the text as a bullet, its web addresses linked and its arrows drawn."""
        return StepBullets(self.styles).bullet(text)

    def heading(self, title: str) -> None:
        """Add a section heading and its rule, never alone at the foot of a page."""
        self._titled(title, "heading", HEADING_ROOM * inch)

    def subheading(self, title: str, room: float) -> None:
        """Add a sub-heading and its rule, with room, in points, left below it on the page."""
        self._titled(title, "subsection_heading", room)

    def step(self, step: Step) -> None:
        """Add a step: its title, kept on the page with its first bullet, then its bullets."""
        room = STEP_ROOM * inch
        title = _step_title(step, self.styles["body"])
        bullets = StepBullets(self.styles)
        flowables = bullets.step_flowables(title, step.bullets)
        page_break = CondPageBreak(room)
        self.story.extend([page_break, *flowables])

    def concept(self, name: str, text: str) -> None:
        """Add a concept box; its use on the job starts a paragraph of its own."""
        body = _concept_body(text, self.styles["small_bullet"])
        bold_name = f"<b>{name}</b>"
        name_line = paragraph(bold_name, self.styles["bullet"])
        box = KeepTogether([name_line, *body])
        self.story.append(box)

    def resource(self, title: str, details: str) -> None:
        """Add a resource entry, its name linked to its site."""
        text = resource_text(title, details, self.site_labels)
        self.story.append(self.bullet(text))

    def _titled(self, title: str, style_name: str, room: float) -> None:
        line = paragraph(title, self.styles[style_name])
        flowables = [CondPageBreak(room), line, *section_rule()]
        self.story.extend(flowables)


def paragraph(text: str, style: ParagraphStyle) -> Paragraph:
    """Return the text as a paragraph, its web addresses linked and its arrows drawn."""
    return Paragraph(drawn(text), style)


def section_rule() -> Flowables:
    """Return the line drawn under a heading, with its space above and below."""
    line = HRFlowable(
        width="100%",
        thickness=1,
        color=HexColor(ACCENT),
        spaceAfter=RULE_SPACE_BELOW,
    )
    return [Spacer(1, RULE_SPACE_ABOVE), line]


def _step_title(step: Step, style: ParagraphStyle) -> Paragraph:
    heading = f"{step.number}. {step.label}:"
    text = f"<b>{heading}</b> {step.time}"
    return paragraph(text, style)


def _concept_body(text: str, style: ParagraphStyle) -> Flowables:
    parts = text.split(f" {ON_THE_JOB}", 1)
    uses = [f"{ON_THE_JOB}{use}" for use in parts[1:]]
    pieces = (parts[0], *uses)
    return [paragraph(piece, style) for piece in pieces]
