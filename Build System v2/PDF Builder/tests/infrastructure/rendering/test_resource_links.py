"""A resource entry links its name to its site, and each further site on the label it is given."""

from pdf_builder.infrastructure.rendering.resource_links import resource_text

TITLE = "A Tool"
DETAILS = "tool.dev · docs.tool.dev — A tool for scanning code."
LABELS = (("docs.tool.dev", "the docs"),)


def test_further_site_is_linked_on_its_label() -> None:
    text = resource_text(TITLE, DETAILS, LABELS)
    assert ">the docs</a>" in text


def test_unlabelled_site_is_linked_on_its_address() -> None:
    text = resource_text(TITLE, DETAILS, ())
    assert ">docs.tool.dev</a>" in text
