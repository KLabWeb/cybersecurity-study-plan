"""A web address printed in a text becomes a link; a link already written stays as it is."""

from pdf_builder.infrastructure.rendering.links import linkify


def test_bare_address_becomes_a_link() -> None:
    linked = linkify("see example.org/a.")
    assert linked == 'see <a href="https://example.org/a" color="#3A7AB8">example.org/a</a>.'


def test_written_link_is_left_alone() -> None:
    written = '<a href="https://x.com">x.com</a>'
    assert linkify(written) == written
