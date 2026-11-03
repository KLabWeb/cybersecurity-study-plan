"""The step bullets lay a step out: a step with no bullets is its title and a gap."""

from reportlab.platypus import Paragraph, Spacer

from pdf_builder.infrastructure.rendering.step_bullets import StepBullets
from pdf_builder.infrastructure.rendering.styles import plan_styles


def test_a_bare_step_is_its_title_and_a_gap() -> None:
    styles = plan_styles()
    title = Paragraph("A step", styles["body"])
    flowables = StepBullets(styles).step_flowables(title, [])
    assert flowables[0] is title
    assert isinstance(flowables[1], Spacer)
    assert len(flowables) == 2
