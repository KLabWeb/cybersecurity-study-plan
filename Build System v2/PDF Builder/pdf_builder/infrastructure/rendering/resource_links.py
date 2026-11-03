"""Write a resource entry with its name linked to its site, in place of a printed site address."""

import re

from pdf_builder.domain.plan import SiteLabels
from pdf_builder.infrastructure.rendering.links import LINK_COLOUR

# A site address as the plan prints it, such as portswigger.net/web-security.
ADDRESS = r"(?:[a-z0-9-]+\.)+[a-z]{2,}[^\s\u2014\u00b7)]*"
# Details that open with the site, then more sites after middle dots, then a long dash.
FURTHER_SITES = rf"((?:\s*\u00b7\s*{ADDRESS})*)"
SITES_FIRST_PATTERN = rf"^({ADDRESS}){FURTHER_SITES}\s*\u2014\s*(.*)$"
SITES_FIRST = re.compile(SITES_FIRST_PATTERN, re.DOTALL)
# Details that name the site in brackets before a long dash.
SITE_IN_BRACKETS = re.compile(rf"^(.*?)\s*\(({ADDRESS})\)\s*\u2014\s*(.*)$", re.DOTALL)
SITE = re.compile(ADDRESS)
# Sites served over plain HTTP: the two AWS wargame sites.
HTTP_ONLY = "flaws"


def link_to(text: str, address: str) -> str:
    """Return the text as a link to the site address."""
    scheme = "http" if address.startswith(HTTP_ONLY) else "https"
    return f'<a href="{scheme}://{address}" color="{LINK_COLOUR}">{text}</a>'


def resource_text(title: str, details: str, labels: SiteLabels) -> str:
    """Return the text of a resource entry, its name linked where the details print its site."""
    sites_first = SITES_FIRST.match(details)
    if sites_first:
        return _with_sites(title, sites_first, labels)
    in_brackets = SITE_IN_BRACKETS.match(details)
    if in_brackets:
        return _with_bracketed_site(title, in_brackets)
    return f"<b>{title}</b> \u2014 {details}"


def _with_sites(title: str, found: re.Match[str], labels: SiteLabels) -> str:
    name = link_to(title, found.group(1))
    further = [
        f" ({link_to(_label(address, labels), address)})"
        for address in SITE.findall(found.group(2))
    ]
    own = found.group(3)
    rest = "".join((own, *further))
    return f"<b>{name}</b> \u2014 {rest}"


def _with_bracketed_site(title: str, found: re.Match[str]) -> str:
    before, address, after = found.groups()
    name = link_to(title, address)
    return f"<b>{name}</b> \u2014 {before} \u2014 {after}"


def _label(address: str, labels: SiteLabels) -> str:
    matching = [
        label
        for piece, label in labels
        if piece in address
    ]
    site = address.split("/", 1)[0]
    matching.append(site)
    return matching[0]
