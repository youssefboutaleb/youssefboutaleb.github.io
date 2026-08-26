#!/usr/bin/env python3
"""Render the portfolio's static pages from a single layout and per-page content.

    python3 tools/build.py           # write pages to the repository root
    python3 tools/build.py --check   # fail if the committed pages are stale

Why a builder at all: the eight published pages share an identical head, brand
bar, navigation and footer. Hand-maintaining eight copies is how the
inconsistencies this repo had (three different contact blocks, two different
analytics tags, one canonical URL for every page) get in. The layout is the
single source of truth; the root *.html files are build output and must never
be edited by hand.

Deployment stays build-free: GitHub Pages serves the generated files directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
PARTIALS = SRC / "partials"
DATA = SRC / "data"

BANNER = (
    "<!-- GENERATED FILE: do not edit.\n"
    "     Source: src/layout.html + src/pages/{source} (content),\n"
    "             src/site.json + src/data/*.json (data).\n"
    "     Rebuild: python3 tools/build.py\n"
    "-->\n"
)

PLACEHOLDER = re.compile(r"\{\{\s*([a-zA-Z0-9_.]+)\s*\}\}")
FRONT_MATTER = re.compile(r"\A<!--\s*\n(.*?)\n-->\s*\n", re.DOTALL)


# --- templating -------------------------------------------------------------

def render(template: str, context: dict) -> str:
    """Substitute every {{ key }} in `template` with context[key].

    Unknown keys are a build error rather than a silently empty string: a typo
    in a template should break the build, not ship a hole in the page.
    """
    missing: list[str] = []

    def substitute(match: re.Match) -> str:
        key = match.group(1)
        if key not in context:
            missing.append(key)
            return ""
        return str(context[key])

    output = PLACEHOLDER.sub(substitute, template)
    if missing:
        raise KeyError(f"unknown template keys: {sorted(set(missing))}")
    return output


def render_items(partial_name: str, items: list[dict], prefix: str = "item") -> str:
    """Render one partial once per item and join the results."""
    template = (PARTIALS / partial_name).read_text(encoding="utf-8").rstrip("\n")
    chunks = []
    for item in items:
        chunks.append(render(template, {f"{prefix}.{k}": v for k, v in item.items()}))
    return "\n".join(chunks)


def parse_front_matter(raw: str) -> tuple[dict, str]:
    """Split a page fragment into its `key: value` header and its content."""
    match = FRONT_MATTER.match(raw)
    if not match:
        raise ValueError("page is missing its front-matter comment block")
    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, raw[match.end():]


def slugify(text: str) -> str:
    """Convert text into a safe HTML id anchor."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


class TocNode:
    def __init__(self, node_id: str, title: str = "", level: int = 1):
        self.id = node_id
        self.title = title
        self.level = level  # 1: Section, 2: Course/Entry, 3: Module/Group, 4: Lab
        self.children: list[TocNode] = []


class BookTocParser(HTMLParser):
    """Collect multi-level sections, courses, modules, and labs for book shortcuts navigation."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = TocNode("root", "Root", level=0)
        self._sec_node: TocNode | None = None
        self._entry_node: TocNode | None = None
        self._group_node: TocNode | None = None
        self._target_node: TocNode | None = None
        self._target_tag: str | None = None
        self._text_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        aria_lbl = a.get("aria-labelledby")
        tag_id = a.get("id")
        cls = a.get("class", "")

        if tag == "section" and aria_lbl:
            self._sec_node = TocNode(aria_lbl, "", level=1)
            self.root.children.append(self._sec_node)
            self._entry_node = None
            self._group_node = None

        if self._sec_node:
            if tag in {"h2", "h3"} and tag_id == self._sec_node.id:
                self._target_node = self._sec_node
                self._target_tag = tag
                self._text_buf = []

            elif tag == "li" and tag_id and ("entry" in cls or tag_id.startswith(("course-", "exp-", "edu-", "proj-", "pub-", "art-", "ws-", "award-"))):
                self._entry_node = TocNode(tag_id, "", level=2)
                self._sec_node.children.append(self._entry_node)
                self._group_node = None

            elif tag == "p" and "entry__title" in cls and self._entry_node:
                self._target_node = self._entry_node
                self._target_tag = tag
                self._text_buf = []

            elif tag == "div" and tag_id and ("entry__group" in cls or tag_id.startswith(("mod-", "hw-", "cap-", "grp-"))):
                parent = self._entry_node or self._sec_node
                self._group_node = TocNode(tag_id, "", level=3)
                parent.children.append(self._group_node)

            elif tag == "p" and "entry__group-title" in cls and self._group_node:
                self._target_node = self._group_node
                self._target_tag = tag
                self._text_buf = []

    def handle_data(self, data: str) -> None:
        if self._target_node:
            self._text_buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._target_node and tag == self._target_tag:
            text = " ".join("".join(self._text_buf).split())
            if "·" in text:
                parts = [p.strip() for p in text.split("·")]
                if self._target_node.id.startswith(("exp-", "edu-")) and len(parts) > 1 and parts[1]:
                    text = parts[1]
                else:
                    text = parts[0]

            text = text.replace("IEEEXtreme Programming Competition", "IEEEXtreme")
            text = text.replace("A2SV (Africa to Silicon Valley)", "A2SV")

            if text.startswith("Lab:"):
                lab_body = re.sub(r"<[^>]+>", "", text[4:]).strip()
                clause = re.split(r"[,;.]", lab_body)[0].strip()
                text = f"Lab: {clause[:35].strip()}"

            self._target_node.title = text.strip()
            self._target_node = None
            self._target_tag = None
            self._text_buf = []


def render_toc_node(node: TocNode) -> str:
    """Recursively render a TocNode and its children as HTML list items."""
    link_class = "book-toc__link" if node.level == 1 else "book-toc__sublink"
    title_text = node.title or node.id.replace("-", " ").title()
    link_html = f'<a class="{link_class}" href="#{escape(node.id, quote=True)}">{escape(title_text)}</a>'

    if not node.children:
        return f'<li class="book-toc__item book-toc__item--level-{node.level}">\n  {link_html}\n</li>'

    children_html = "\n".join(indent(render_toc_node(child), 2) for child in node.children)
    sublist_class = "book-toc__list" if node.level == 0 else f"book-toc__sublist book-toc__sublist--level-{node.level}"
    return (
        f'<li class="book-toc__item book-toc__item--level-{node.level}">\n'
        f'  {link_html}\n'
        f'  <ul class="{sublist_class}">\n'
        f'{children_html}\n'
        f'  </ul>\n'
        f'</li>'
    )


def render_page_context(content: str, source: Path) -> str:
    """Render the book shortcuts TOC navigation for sections and subsections."""
    parser = BookTocParser()
    parser.feed(content)
    parser.close()

    if not parser.root.children:
        return ""

    body = "\n".join(indent(render_toc_node(child), 2) for child in parser.root.children)
    return (
        '<nav class="book-toc" aria-label="On this page">\n'
        '  <div class="book-toc__header">\n'
        '    <svg class="book-toc__icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">\n'
        '      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>\n'
        '      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>\n'
        '    </svg>\n'
        '    <span class="book-toc__title">On this page</span>\n'
        '  </div>\n'
        '  <ul class="book-toc__list">\n'
        f'{body}\n'
        '  </ul>\n'
        '</nav>'
    )


# --- record metadata --------------------------------------------------------

# The single source of truth for how a record's metadata is described.
#
# A *model* is an ordered list of named categories. Every record on a page
# answers the same model in the same sequence, so a reader compares like with
# like without re-reading:
#
#     placement  ->  type       ->  scope    ->  scale
#     2nd Place      Hackathon      African      40 teams
#
#     format     ->  mode       ->  audience ->  host
#     Workshop       On-site        Students     IEEE Student Branch ENIS
#
# Two rules make that hold as records are added. Order comes from MODELS and
# nowhere else, so a page cannot choose its own. Colour comes from the *field*,
# not the value: each category has one .tag--<field> rule in main.css, so
# amber always means placement and violet always means delivery mode. A new
# category is added here, once, and every record on that page picks it up.
#
# Pages get their own model rather than sharing one: a workshop has no
# placement and an award has no audience, and forcing both onto one tuple is
# how a page ends up rendering empty or meaningless dimensions. Two models may
# share a category name only if they mean the same thing by it.
MODELS = {
    "awards": ("placement", "type", "scope", "scale", "duration", "track"),
    "workshops": ("format", "mode", "duration", "audience", "scale", "host"),
    "teaching": ("level", "workload", "scale"),
    "research": ("status", "authorship", "publisher"),
    "writing": ("format", "reach", "platform"),
    "projects": ("upstream", "kind", "stack"),
    "experience": ("domain", "engagement", "mode", "scale", "stack"),
    "education": ("programme", "focus", "accreditation"),
}

# Skills are the one block whose tags are *citations* rather than dimensions,
# so their model is declared apart from MODELS and read only by render_skill.
# Order runs strongest proof first and never varies, which is what lets the
# leading colour of a row be read as its standing: a row that starts green ran
# in production, a row that starts blue did not. skills.md carries the full
# argument, including why this is the one model where a category may repeat.
PROOF = ("production", "certification", "taught", "published", "applied")

# What each kind of proof is called when a reader hovers the group. The label
# is on the list, not on every chip, for the reason MODEL_LABELS exists.
PROOF_LABEL = "Evidence"

# The same five kinds, named for the reader rather than for the schema. They
# render once, as the key above the block.
#
# The colour code was documented in skills.md and shown to nobody: a visitor
# worked out that green meant production somewhere around the fourth row, if at
# all. A key is admissible here on the same ground CLAUDE.md section 7 admits
# the depth dial: it is a reading aid, not a control. It adds no state, no
# navigation and no content that exists only in one mode, and it makes a code
# the page was already using legible on the first row instead of the fourth.
PROOF_KEY = {
    "production": "Run in production",
    "certification": "Certified",
    "taught": "Taught",
    "published": "Published",
    "applied": "Applied",
}

# The tools line is the block's second chip family and is deliberately not part
# of the evidence run. `stack` is the site's established treatment for "a tool
# this was built with" (outlined, one chip per tool, regular weight) and Career
# and Projects already render it, so Home reusing it is one vocabulary rather
# than a third. It renders on its own line *above* the evidence, never merged
# into it: skills.md's colour-run reading is a claim about the colour of a row's
# FIRST chip, and an outlined tool chip in front of the run would destroy it.
TOOLS_LABEL = "Tools"

# Standing is derived from which kinds of proof a skill actually has, never
# typed into the data. A self-assessed level is the thing this block exists to
# replace: "advanced" is an opinion, "run in production and certified" is a
# pair of facts a reader can open in a new tab.
def standing(evidence: dict) -> str:
    shipped = bool(evidence.get("production"))
    outside = any(evidence.get(kind) for kind in ("certification", "taught", "published"))
    if shipped and outside:
        return "Production-proven"
    if shipped:
        return "Run in production"
    if outside:
        return "Verified: not yet in production"
    return "Applied &amp; studied"


# The order the standings rank in, and therefore the order the block renders.
# Which claim a capability serves, and the only hand-set field in the Skills
# block. `trunk` supports the Data Engineering claim directly; `branch` is real,
# proven, and supporting evidence for the trunk rather than the claim itself.
#
# It encodes *positioning*, never level, which is what keeps it out of the
# self-assessment skills.md exists to refuse: nothing here says how good anyone
# is at anything, and a branch skill still carries whatever standing its
# evidence earns. Machine learning is `branch` while holding six citations and
# the top standing the model awards; the field did not demote it, it filed it.
#
# It exists because the sort had no third key and the tie went to citation
# count, which put computer vision second on the front page of a site whose
# whole argument is CLAUDE.md section 3.
THREAD_ORDER = {"trunk": 0, "branch": 1}

STANDING_ORDER = {
    "Production-proven": 0,
    "Run in production": 1,
    "Verified: not yet in production": 2,
    "Applied &amp; studied": 3,
}

# Courses run on a two-semester year. Fall precedes Spring inside one academic
# year, so newest-first means sorting on (year, term) descending with Fall
# ranked below Spring, not on the year alone.
TERM_ORDER = {"Fall": 0, "Spring": 1}

# The accessible name of each model's tag list. It is what a screen reader
# announces before the tags themselves, which otherwise read as a bare run of
# nouns.
MODEL_LABELS = {
    "awards": "Achievement details",
    "workshops": "Workshop details",
    "teaching": "Course details",
    "research": "Publication details",
    "writing": "Article details",
    "projects": "Project details",
    "experience": "Role details",
    "education": "Programme details",
}

# The top three placements carry a medal disc. It replaces wording like
# "Winner" or "Runner-up", which reads as marketing and does not survive being
# skimmed; the disc is recognised before the label is read.
MEDALS = {1: "gold", 2: "silver", 3: "bronze"}

# Author position is stated as a word rather than a rank, because a paper is
# not a leaderboard: "Second Author" is a role in a collaboration, where "2nd"
# would read as a placing. Positions past the fifth fall back to the ordinal,
# which is the honest way to say "well down a long author list".
AUTHOR_POSITIONS = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth"}


# What a pull request against an upstream project actually means, stated rather
# than implied. An open PR is a submission and a merged one is an acceptance;
# the wording lives here so a record cannot quietly upgrade itself by being
# styled green. Per awards.md rule 6, prefer the plain fact over the claim.
UPSTREAM_STATES = {"open": "Submitted upstream", "merged": "Accepted upstream"}


def ordinal(number: int) -> str:
    """1 -> 1st, 2 -> 2nd, 21 -> 21st, 13 -> 13th, 1432 -> 1,432nd."""
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number:,}{suffix}"


def abbreviate(count: int) -> str:
    """Medium's own display convention: exact below 1,000, then K to one
    decimal with a trailing .0 dropped: 723 stays 723, 1,500 becomes 1.5K,
    3,000 becomes 3K.

    The site never prints more precision than its source gave it. Medium
    reports a large figure already rounded, so rendering "3,000 views" would
    invent three digits of accuracy nobody measured; the raw integer is stored
    so the value can be compared and summed, and this prints it back in the
    form it actually arrived in.
    """
    for limit, suffix in ((1_000_000, "M"), (1_000, "K")):
        if count >= limit:
            scaled = f"{count / limit:.1f}".rstrip("0").rstrip(".")
            return f"{scaled}{suffix}"
    return f"{count:,}"


def meta_label(field: str, value) -> tuple[str, str]:
    """Turn one raw metadata value into (medal markup, human label).

    Placements are stored as plain integers and rankings are spelled out here
    rather than in the data, so "1st Place" cannot become "1st place" or
    "First" in the next record someone adds.
    """
    if field == "placement" and isinstance(value, int):
        medal = MEDALS.get(value)
        badge = f'<span class="medal medal--{medal}" aria-hidden="true"></span>' if medal else ""
        return badge, f"{ordinal(value)} Place"
    if field == "level" and isinstance(value, int):
        return "", f"Master&rsquo;s Year {value}"
    if field == "workload":
        # The total is computed, never typed: a hand-written "32 h" beside a
        # breakdown that adds to 30 is the kind of contradiction nobody spots.
        total = sum(value.values())
        split = " + ".join(f"{hours} {kind}" for kind, hours in value.items())
        return "", f"{total} h &middot; {split}"
    if field == "scale":
        # Two kinds of imprecision, and they are not the same claim. A floor
        # ("150+ pipelines") says at least this many and is checkable upward;
        # an estimate ("~2,000 frames/second") says about this many and is
        # checkable in both directions. Rendering one as the other overstates
        # or understates a figure the bullets below state exactly, so the
        # record declares which it holds and neither is the default.
        count = f"{value['count']:,}"
        if value.get("minimum"):
            count = f"{count}+"
        elif value.get("approx"):
            count = f"~{count}"
        # The figure is bold inside an otherwise regular-weight chip, the same
        # emphasis every bullet on the site gives its numbers. It is a
        # treatment of the same part of every scale value, never of one value
        # over another, so awards.md rule 4 holds: 86 teams and 643rd of 7,094
        # are emphasised identically.
        return "", f"<b>{count}</b> {value['unit']}"
    if field == "upstream":
        return "", f"{UPSTREAM_STATES[value['state']]} &middot; PR #{value['pr']}"
    if field == "accreditation":
        # The label is the accreditation's own name; the link beside it is the
        # body that grants it. Stored as a pair for the same reason `upstream`
        # is: the claim and its evidence travel together or not at all.
        return "", value["name"]
    if field == "reach":
        # The pair is the unit, not two facts that happen to sit together.
        # Views alone counts everyone who opened the tab and reads alone hides
        # the ratio; it is the gap between them that says whether the piece
        # held up. A record carries both figures or neither: writing.md.
        return "", (f"{abbreviate(value['views'])} views"
                    f" &middot; {abbreviate(value['reads'])} reads")
    return "", str(value)


def meta_url(field: str, value) -> str | None:
    """The canonical source for a metadata value, where one exists.

    Most categories are plain facts with nowhere to point. An upstream
    submission is not: the pull request *is* the evidence for the claim the tag
    makes, and a reader who wants to check it should not have to go looking.
    The address is built from the stored repo and number rather than typed, for
    the reason research.md builds a DOI link: the identifier is the durable
    fact and the URL is derived from it.

    A linked tag keeps its category's colour. The link is a route to the
    evidence, not a different kind of tag, and awards.md rule 4 is that the
    treatment belongs to the category and never to the individual value.
    """
    if field == "upstream":
        return f"https://github.com/{value['repo']}/pull/{value['pr']}"
    if field == "accreditation":
        return value["url"]
    return None


def render_meta(record: dict, model: str, extra: tuple[str, ...] = (), extra_head: tuple[str, ...] = ()) -> str:
    """The metadata tag list for one record, always in its model's order.

    A field the record does not carry is omitted rather than filled with a
    placeholder: a contest that never published a rank shows three tags, not an
    invented placement.

    `extra` holds already-rendered utility tags: a link to an artefact, say.
    Those are not dimensions of the record, so they carry no ordering rule and
    are appended after the model's tags rather than sequenced among them.
    `extra_head` holds leading utility tags placed before the model's tags.
    """
    tags = list(extra_head)
    for field in MODELS[model]:
        if field not in record:
            continue
        if field == "stack":
            # The one category that renders a chip per value instead of one
            # chip holding all of them. It is admissible because `stack` is
            # always the *last* category in its model, so a run whose length
            # varies shifts nothing before it and the positional reading of
            # every earlier category survives intact. It is also the only way
            # the value fits a phone: a joined stack ran to 58 characters in a
            # chip that cannot wrap. career.md section 1.
            tags.extend(
                f'<li class="tag tag--stack">{tool}</li>' for tool in record[field]
            )
            continue
        badge, label = meta_label(field, record[field])
        url = meta_url(field, record[field])
        if url:
            # Whether a linked tag opens away from the page is derived from the
            # address, never declared beside it: the same rule render_credentials
            # follows, and the reason CLAUDE.md section 9 gives for not writing a
            # separate honesty rule when the data model can enforce it. A pull
            # request leaves the site and is marked; a citation to another page
            # of this site does not, and marking it would tell the reader it
            # does.
            external = "://" in url
            marker = " link-external" if external else ""
            target = ' target="_blank" rel="noopener"' if external else ""
            tags.append(
                f'<li><a class="tag tag--{field}{marker}" href="{url}"'
                f'{target}>{badge}{label}</a></li>'
            )
        else:
            tags.append(f'<li class="tag tag--{field}">{badge}{label}</li>')
    tags.extend(extra)
    if not tags:
        return ""
    body = "\n".join("  " + tag for tag in tags)
    return f'<ul class="tag-list" aria-label="{MODEL_LABELS[model]}">\n{body}\n</ul>'


IMPACT_LABEL = "Impact:"


def render_point(point, point_id: str = "") -> str:
    """One bullet, with the consequence of the work kept out of its sentence."""
    if isinstance(point, str):
        text, impact, anchor = point, "", ""
    else:
        text, impact = point["point"], point.get("impact", "")
        anchor = f' id="{point["id"]}"' if point.get("id") else ""
    if point_id and not anchor:
        anchor = f' id="{point_id}"'
    lab = text.startswith("<b>Lab:</b>") or text.startswith("<b>Lab :</b>")
    attrs = anchor + (' class="point--lab"' if lab else "")
    if impact:
        text += (
            f'\n  <span class="point__impact">'
            f"<b>{IMPACT_LABEL}</b> {impact}</span>"
        )
    return f"<li{attrs}>{text}</li>"


def render_points(points: list, lab_prefix: str = "") -> str:
    """A run of bullets as the site-wide `.points` list."""
    rendered = []
    lab_idx = 1
    for point in points:
        pt_text = point if isinstance(point, str) else point.get("point", "")
        pt_id = ""
        if lab_prefix and (pt_text.startswith("<b>Lab:</b>") or pt_text.startswith("<b>Lab :</b>")):
            pt_id = f"{lab_prefix}-lab-{lab_idx}"
            lab_idx += 1
        rendered.append(indent(render_point(point, pt_id), 2))
    items = "\n".join(rendered)
    return f'<ul class="points">\n{items}\n</ul>'


def render_group(title: str, points: list, modifier: str = "", group_id: str = "") -> str:
    """One `.entry__group`: a titled run of bullets inside a longer record."""
    group_class = f"entry__group {modifier}".strip() if modifier else "entry__group"
    attr_id = f' id="{group_id}"' if group_id else ""
    return (
        f'<div class="{group_class}"{attr_id}>\n'
        f'  <p class="entry__group-title">{title}</p>\n'
        f'{indent(render_points(points, lab_prefix=group_id), 2)}\n'
        "</div>"
    )


def render_award(record: dict) -> str:
    """One award as the site-wide .entry record."""
    title = record["title"]
    if record.get("url"):
        title = (
            f'<a class="link-external" href="{record["url"]}" target="_blank"'
            f' rel="noopener">{title}</a>'
        )
    if record.get("venue"):
        title += f'<span class="entry__role"> &middot; {record["venue"]}</span>'

    year = record["year"]
    parts = [
        f'<p class="entry__title">{title}</p>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "awards"),
    ]
    if record.get("points"):
        parts.append(render_points(record["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    award_id = f"award-{slugify(record['title'])}"
    return f'<li class="entry" id="{award_id}">\n{body}\n</li>'


def render_workshop(record: dict) -> str:
    """One workshop as the site-wide .entry record.

    Two things sit deliberately outside the metadata model. A repository link
    belongs to the title, because it points at the thing the title names. And
    a slide deck is an artefact, not a dimension of the session, so it renders
    as a utility tag appended after the model's four.
    """
    title = record["title"]
    if record.get("repo"):
        name = "Workshop materials on GitHub"
        title += (
            f'\n  <a class="icon-link" href="{record["repo"]}" target="_blank"'
            f' rel="noopener" title="{name}">'
            f'<img class="icon icon--sm" src="images/icons/github.svg" alt="{name}"'
            f' width="15" height="15"></a>\n'
        )

    extra = ()
    if record.get("slides"):
        extra = (
            f'<li><a class="tag tag--critical link-external" href="{record["slides"]}"'
            f' target="_blank" rel="noopener" title="View slides in PowerPoint Online">'
            f'<img class="icon icon--xs" src="images/icons/powerpoint.svg" alt=""'
            f' width="12" height="12">Slides (.pptx)</a></li>',
        )

    year = record["year"]
    parts = [
        f'<p class="entry__title">{title}</p>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "workshops", extra),
    ]
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        parts.append(render_points(record["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    ws_id = f"ws-{slugify(record['title'])}"
    return f'<li class="entry" id="{ws_id}">\n{body}\n</li>'


def publication_sort_key(record: dict) -> int:
    """Newest first; a paper with no year yet sorts last.

    An unpublished record has no publication year to sort on, and guessing one
    from the year the work started would put it above papers that are actually
    out. Nothing is invented: it simply sorts behind everything with a date.

    Shared with the Technical Articles block, which orders on the same rule.
    The two blocks are sorted separately and never merged: what they order is
    identical, what they claim is not.
    """
    return record.get("year", 0)


def author_position(record: dict) -> str | None:
    """Which author the site's owner was on a paper, derived not written.

    The data marks one entry of `authors` with `"self": true` and the label is
    computed from its index, for the same reason placements are: a hand-typed
    "Second Author" survives an author list being reordered, and then quietly
    says the wrong thing.
    """
    for position, author in enumerate(record["authors"], start=1):
        if author.get("self"):
            return f"{AUTHOR_POSITIONS.get(position, ordinal(position))} Author"
    return None


def render_authors(authors: list[dict]) -> str:
    """The author list, Scholar-linked where a profile exists.

    The site's owner is bolded: the ordinary convention on a publication list,
    and the thing that makes the page scannable for the reason it exists. An
    author with no `scholar` renders as plain text rather than as a dead link.
    """
    names = []
    for author in authors:
        name = author["name"]
        if author.get("self"):
            name = f"<b>{name}</b>"
        if author.get("scholar"):
            name = (
                f'<a href="{author["scholar"]}" target="_blank" rel="noopener"'
                f' title="Google Scholar profile">{name}</a>'
            )
        names.append(name)

    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + f", and {names[-1]}"


def render_publication(record: dict) -> str:
    """One paper as the site-wide .entry record.

    The paper's title is the `entry__title`, not the author list, because the
    component puts identity first on every other page and a reader scanning
    this one is looking for what the work was. The citation line beneath it
    carries the authors and the journal.

    The journal name is deliberately not a tag. It is already in the citation
    line one row above, and `awards.md` rule 1 is that a fact stated once is
    not restated, so the model asks who the author was and who published it,
    which the citation does not answer.
    """
    link = record.get("url")
    if record.get("doi"):
        link = f"https://doi.org/{record['doi']}"

    title = record["title"]
    if link:
        title = (
            f'<a class="link-external" href="{link}" target="_blank"'
            f' rel="noopener">{title}</a>'
        )

    parts = [f'<p class="entry__title">{title}</p>']

    # A paper that is not out yet has no publication year. Per awards.md rule 5
    # the line is dropped rather than filled with the year it was started.
    if record.get("year"):
        year = record["year"]
        parts.append(f'<p class="entry__period"><time datetime="{year}">{year}</time></p>')

    citation = render_authors(record["authors"])
    if record.get("venue"):
        citation += f' &middot; <i>{record["venue"]}</i>'
    parts.append(f'<p class="entry__meta">{citation}</p>')

    position = author_position(record)
    parts.append(render_meta({**record, "authorship": position} if position else record,
                             "research"))

    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        parts.append(render_points(record["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    pub_id = f"pub-{slugify(record['title'])}"
    return f'<li class="entry" id="{pub_id}">\n{body}\n</li>'


def render_article(record: dict) -> str:
    """One self-published technical article as the site-wide .entry record.

    It shares the .entry component with a paper but deliberately not the paper
    model. `status` and `publisher` would be the same two words making a
    materially different claim, and `authorship` says nothing on a piece with
    one author, so writing gets its own model rather than borrowing one that
    degrades, exactly as the comment on MODELS requires.

    What survives is the parallel that matters: `platform` takes the quiet grey
    terminal position that `publisher` takes one block above it, so the reader
    who has learned that the last tag says who stands behind the work reads
    *Medium* there against *Elsevier*: the distinction the page exists to make
    honestly, stated by the layout rather than argued in prose.

    The title carries the link for the same reason it does on a publication:
    the two blocks are read one after the other, and a trailing icon on one of
    them would break the column the eye is already following.
    """
    title = record["title"]
    if record.get("url"):
        title = (
            f'<a class="link-external" href="{record["url"]}" target="_blank"'
            f' rel="noopener">{title}</a>'
        )

    year = record["year"]
    parts = [
        f'<p class="entry__title">{title}</p>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "writing"),
    ]
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        parts.append(render_points(record["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    art_id = f"art-{slugify(record['title'])}"
    return f'<li class="entry" id="{art_id}">\n{body}\n</li>'


def project_sort_key(record: dict) -> int:
    """Newest first. Ties keep their order in the file.

    `sorted` is stable, so two projects from the same year stay in the order
    they were written down rather than being reshuffled on every build. The
    file is the tie-breaker precisely because nothing else is: a month would
    have to be invented for records that only ever carried a year.
    """
    return record["year"]


def render_project(record: dict, articles: dict) -> str:
    """One project as the site-wide .entry record.

    Two things sit outside the metadata model, on the same reasoning that
    governs a workshop. The repository link belongs to the title, because it
    points at the thing the title names. The write-up is an artefact of the
    work rather than a dimension of it, so it renders as a utility tag after
    the model's three.

    That article is looked up by id in `writing.json` rather than repeated
    here: it is one URL, so it is declared in one file, and a project can no
    longer end up pointing at an address the Research page has since changed.
    """
    title = record["title"]
    if record.get("repo"):
        name = "GitHub repository"
        title += (
            f'\n  <a class="icon-link" href="{record["repo"]}" target="_blank"'
            f' rel="noopener" title="{name}">'
            f'<img class="icon icon--sm" src="images/icons/github.svg" alt="{name}"'
            f' width="15" height="15"></a>\n'
        )

    extra_head = []
    extra_tail = []
    if record.get("demo"):
        demo = record["demo"]
        demo_url = demo["url"] if isinstance(demo, dict) else demo
        demo_label = demo.get("label", "Live Demo on Hugging Face") if isinstance(demo, dict) else "Live Demo on Hugging Face"
        extra_head.append(
            f'<li><a class="tag tag--upstream link-external" href="{demo_url}"'
            f' target="_blank" rel="noopener">{demo_label}</a></li>'
        )
    if record.get("slides"):
        extra_tail.append(
            f'<li><a class="tag tag--critical link-external" href="{record["slides"]}"'
            f' target="_blank" rel="noopener" title="View slides in PowerPoint Online">Slides (.pptx)</a></li>'
        )
    if record.get("article"):
        article = articles[record["article"]]
        extra_tail.append(
            f'<li><a class="tag tag--success link-external" href="{article["url"]}"'
            f' target="_blank" rel="noopener">Article on {article["platform"]}</a></li>'
        )

    year = record["year"]
    parts = [
        f'<p class="entry__title">{title}</p>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "projects", extra=tuple(extra_tail), extra_head=tuple(extra_head)),
    ]
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        parts.append(render_points(record["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    proj_id = f"proj-{slugify(record['title'])}"
    return f'<li class="entry" id="{proj_id}">\n{body}\n</li>'


def course_sort_key(record: dict) -> tuple[int, int]:
    """Newest first, by academic year then by term within it."""
    return (record["year"], TERM_ORDER[record["term"]])


def render_course(record: dict) -> str:
    """One taught course as the site-wide .entry record."""
    course_slug = slugify(record["title"])
    course_id = f"course-{course_slug}"
    year, term = record["year"], record["term"]
    period = f"{term} {year}-{year + 1}"

    parts = [
        f'<p class="entry__title">{record["title"]}</p>',
        f'<p class="entry__period">{period}</p>',
        render_meta(record, "teaching"),
    ]
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')

    for number, module in enumerate(record.get("syllabus", []), start=1):
        mod_id = f"{course_slug}-m{number}"
        parts.append(render_group(f"Module {number}: {module['title']}",
                                  module["points"], group_id=mod_id))
        homework = module.get("homework")
        if homework:
            hw_id = f"{course_slug}-m{number}-hw"
            parts.append(render_group(
                f"Module {number} Homework: {homework['title']}",
                homework["points"],
                modifier="entry__group--homework",
                group_id=hw_id))

    capstone = record.get("capstone")
    if capstone:
        cap_id = f"{course_slug}-project"
        parts.append(render_group(f"Final Project: {capstone['title']}",
                                  capstone["points"],
                                  modifier="entry__group--capstone",
                                  group_id=cap_id))

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry" id="{course_id}">\n{body}\n</li>'


# --- career -----------------------------------------------------------------

# Months are abbreviated here and never in the data, so a record cannot be
# stored as "Aug 2024" in one row and "August 2024" in the next: awards.md
# rule 7, the same mechanism that turns `1` into `1st Place`.
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

# A role with no end date is the one being held now. The word is produced by
# the renderer rather than typed into `end`, because "Present" is not a date
# and storing it as one is how a leaver's record keeps claiming a job.
ONGOING = "Present"


def month_year(value: str) -> str:
    """Render a stored "YYYY-MM" as "Aug 2024"."""
    year, month = value.split("-")
    return f"{MONTHS[int(month) - 1]} {year}"


def tenure(start: str, end: str | None) -> str:
    """How long a role lasted, as "3 months", "1 year", "2 years 3 months".

    Derived from the same two stored dates the period is rendered from, never
    typed, for the reason `month_year` exists: a stored "2 years" keeps saying
    two the year after it was written, and a duration beside a live end date is
    the easiest contradiction on the page to introduce and the hardest to see.

    **A finished role counts inclusively and a current one does not.** Feb 2024
    to Jul 2024 is six months, because both endpoint months were worked. Aug
    2024 to a Present falling in Aug 2026 is twenty-four, not twenty-five: the
    month in progress is not finished and counting it would round every current
    role up. Where the two conventions disagree the shorter one wins, because
    the number is a claim about how long somebody has been employed and it is
    read by people who will check it.

    Rendered in the dateline rather than as a tag: it is a "when" fact, it is
    derivable from the range printed beside it, and awards.md rule 1 is that a
    fact already in the record does not get a category invented for it.
    career.md section 4.
    """
    start_year, start_month = (int(part) for part in start.split("-"))
    if end:
        end_year, end_month = (int(part) for part in end.split("-"))
        months = (end_year - start_year) * 12 + (end_month - start_month) + 1
    else:
        today = date.today()
        months = (today.year - start_year) * 12 + (today.month - start_month)
    months = max(months, 1)

    years, rest = divmod(months, 12)
    parts = []
    if years:
        parts.append(f"{years} year" + ("s" if years > 1 else ""))
    if rest:
        parts.append(f"{rest} month" + ("s" if rest > 1 else ""))
    return " ".join(parts)


def tenure_sort_key(record: dict) -> str:
    """Newest first, on the start date.

    Sorting on the *start* rather than the end is what keeps the current role
    at the top: it is the only record with no end date, and ordering on a field
    it does not have would need a sentinel that outranks every real date.
    Stored as "YYYY-MM", so a plain string comparison is a chronological one.
    """
    return record["start"]


def render_experience_role(role: dict) -> str:
    """One dated role nested beneath its company record.

    OEM is the only current employer with two distinct positions. Keeping the
    company context once and nesting the progression beneath it makes the
    relationship visible without repeating the company, domain, and product
    description as two unrelated jobs.

    The roles are wrapped by `render_experience` in a single `.entry__roles`
    container, which carries the vertical connector. See career.md section 1,
    "A company with more than one role", for why it is a left rule.
    """
    end = month_year(role["end"]) if role.get("end") else ONGOING
    period = (f'{month_year(role["start"])} - {end}'
              f' ({tenure(role["start"], role.get("end"))})')

    dateline = []
    if role.get("location"):
        dateline.append(f'<span class="entry__location">{role["location"]}</span>')
    dateline.append(period)

    parts = [
        (f'<p class="entry__group-title">\n'
         f'  <span class="entry__subrole">{role["role"]}</span>\n'
         '</p>'),
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
        render_meta(role, "experience"),
    ]
    if role.get("points"):
        parts.append(render_points(role["points"]))
    for group in role.get("groups", []):
        parts.append(render_group(group["title"], group["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<div class="entry__group entry__group--role">\n{body}\n</div>'


def render_experience(record: dict) -> str:
    """One company or job as the site-wide .entry record.

    Formatted as two lines: `Role &middot; Company` as the title, then
    `Location &middot; Period` as the period line, which is the record
    anatomy every other page already uses (DESIGN.md section 9).
    Followed by company description / role summary.
    """
    company = record["company"]
    if record.get("url"):
        company = (
            f'<a href="{record["url"]}" target="_blank" rel="noopener">{company}</a>'
        )

    end = month_year(record["end"]) if record.get("end") else ONGOING
    period = (f'{month_year(record["start"])} - {end}'
              f' ({tenure(record["start"], record.get("end"))})')

    title_parts = []
    if record.get("role"):
        title_parts.append(f'<span class="entry__role">{record["role"]}</span>')
    title_parts.append(f'<span class="entry__company">{company}</span>')

    dateline = []
    if record.get("location"):
        dateline.append(f'<span class="entry__location">{record["location"]}</span>')
    dateline.append(period)

    parts = [
        f'<p class="entry__title">\n  {" &middot; ".join(title_parts)}\n</p>',
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
    ]
    meta = render_meta(record, "experience")
    if meta:
        parts.append(meta)
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        parts.append(render_points(record["points"]))
    for group in record.get("groups", []):
        parts.append(render_group(group["title"], group["points"]))
    roles = record.get("roles", [])
    if roles:
        # One wrapper, so the connector down the left is a single unbroken line
        # rather than one detached segment per role. The wrapper is what says
        # "these belong to the company above"; a per-role border could not.
        nested = "\n".join(indent(render_experience_role(r), 2) for r in roles)
        parts.append(f'<div class="entry__roles">\n{nested}\n</div>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    exp_id = f"exp-{slugify(record['company'])}"
    return f'<li class="entry" id="{exp_id}">\n{body}\n</li>'


def render_education(record: dict) -> str:
    """One qualification as the site-wide .entry record.

    The degree is the title and the institution trails it, because a degree is
    read for what it is before where it is from: the same ordering the CV this
    page descends from used.

    The institution is printed in full, never as an abbreviation: a reader
    outside Tunisia cannot expand "ENIS", and a school nobody can name is a
    credential nobody can weigh (CLAUDE.md section 4, on not glossing Tunisian
    context but keeping it legible).

    Location and period share one line, in that order, which is the dateline
    `render_experience` already uses. Career reads as one page, so a
    qualification and a job state where and when in the same shape.
    """
    institution = record["institution"]
    if record.get("url"):
        institution = (
            f'<a href="{record["url"]}" target="_blank" rel="noopener">'
            f'{institution}</a>'
        )

    dateline = []
    if record.get("location"):
        dateline.append(f'<span class="entry__location">{record["location"]}</span>')
    # The same parenthetical the jobs above carry, from the same reasoning:
    # a reader should not have to subtract. Education stores plain years, so
    # the span is the difference between them and no month arithmetic applies.
    years = record["end"] - record["start"]
    length = f"{years} year" + ("s" if years > 1 else "")
    dateline.append(f'{record["start"]}-{record["end"]} ({length})')

    parts = [
        f'<p class="entry__title">\n  {record["degree"]}\n'
        f'  <span class="entry__role">&middot; {institution}</span>\n</p>',
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
        render_meta(record, "education"),
    ]
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        parts.append(render_points(record["points"]))
    for group in record.get("groups", []):
        parts.append(render_group(group["title"], group["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    edu_id = f"edu-{slugify(record['institution'])}"
    return f'<li class="entry" id="{edu_id}">\n{body}\n</li>'


def render_credentials(record: dict, field: str) -> str:
    """One issuer's or platform's credentials, as an `.issuer`-headed group.

    Credentials carry no metadata model. The grouping *is* the metadata: who
    granted it is the only dimension a certificate has that the reader needs,
    and it is already the heading, so a tag restating it would break the rule
    that a fact stated once is not restated.

    `field` is `issuer` on a certification and `platform` on a course. They are
    kept apart for writing.md's reason: both name who stands behind the entry,
    but an issuer examined the holder and a platform hosted the lessons, and
    one word for both would let the second borrow the first's authority.

    Every credential row carries `.link-external`. The marker means "this
    opens away from the page", which is true of all of them: they share one
    `target="_blank"`, whether the link is the issuer's own record or a scan
    of a certificate this site serves. An earlier version derived the marker
    from the URL scheme so that the hosted scans rendered bare, which left the
    two Microsoft rows looking like the only unclickable names in the block.
    """
    icon = f'images/icons/{record["icon"]}'
    heading = (
        '<p class="issuer">\n'
        f'  <img class="icon icon--md" src="{icon}" alt="" width="18" height="18">\n'
        f'  {record[field]}\n'
        "</p>"
    )

    items = []
    for credential in record["credentials"]:
        items.append(
            f'  <li><a class="link-external" href="{credential["url"]}"'
            f' target="_blank" rel="noopener">{credential["name"]}</a></li>'
        )
    body = "\n".join(items)

    parts = [heading, f'<ul class="points">\n{body}\n</ul>']
    return '<li class="entry">\n' + "\n".join(indent(p, 2) for p in parts) + "\n</li>"


# --- home -------------------------------------------------------------------


def render_credential_row(certifications: list) -> str:
    """The `Certified` row of Home's fact strip: one issuer, one link, and a
    count above one.

    It replaces four hand-written strings in `site.json` that summarised the
    ten records in `certifications.json`. The four agreed with the ten, and
    nothing made them stay in agreement: exactly the drift surface Selected
    Impact was rebuilt to close, sitting in the first screen of the site. Home
    now derives the summary from the records Career renders, so the two pages
    cannot disagree about what has been earned.

    Issuers keep the order they are written in, for the reason the Career
    block gives: an issuer group has no date to sort on, and grouping by
    issuer is the ordering. Sorting by count here would put the strip and the
    block it links to in two different orders.

    The count is the point. Three Datadog certificates and one MuleSoft are
    not the same claim, and a bare list of issuers flattens them into one.

    This is the one row where `&middot;` is still doing the separating, and it
    is the right tool here: five short peers, no internal structure of their
    own. Languages needed a grid instead because each of its items is itself a
    pair, and one separator cannot both divide the list and bind each pair.
    """
    links = []
    for record in certifications:
        count = len(record["credentials"])
        suffix = f" &times;{count}" if count > 1 else ""
        links.append(
            f'<a href="career.html#certifications">{record["issuer"]}{suffix}</a>'
        )
    return (
        '<div class="hero-facts__row">\n'
        "  <dt>Certified</dt>\n"
        f'  <dd>{" &middot; ".join(links)}</dd>\n'
        "</div>"
    )


def render_language_row(languages: list) -> str:
    """The `Languages` row of Home's fact strip: a name, a level, and proof.

    Languages was the last block on Home and the last thing on the site with
    nothing a reader could check. It moved into the opening because it is a
    hiring filter and a filter reached last is a filter applied by guessing,
    and it started citing records because `teaching.html` had been stating the
    instruction language in its spec strip the whole time. That citation is
    what makes this data rather than a string in `site.json`:
    [`DESIGN.md`](DESIGN.md) section 10, a list becomes data when it restates
    facts held elsewhere on the site.

    Arabic carries no evidence and that is left visible. Every alternative
    (dropping the row, or finding it something to link to) is worse than a
    native language simply saying so.

    The proficiency wording is LinkedIn's scale and is the author's. CEFR was
    considered for the EU market and declined. Do not convert it.
    """
    rows = []
    for record in languages:
        proof = ""
        if record.get("evidence"):
            links = " &middot; ".join(
                f'<a href="{item["href"]}">{item["text"]}</a>'
                for item in record["evidence"]
            )
            proof = f'\n    <span class="hero-facts__proof">{links}</span>'
        rows.append(
            '  <div class="hero-facts__lang">\n'
            f'    <dt>{record["name"]}</dt>\n'
            f'    <dd>{record["level"]}{proof}</dd>\n'
            "  </div>"
        )
    body = "\n".join(rows)
    return (
        '<div class="hero-facts__row">\n'
        "  <dt>Languages</dt>\n"
        "  <dd>\n"
        '    <dl class="hero-facts__langs">\n'
        + indent(body, 4)
        + "\n    </dl>\n"
        "  </dd>\n"
        "</div>"
    )


def render_current_role(record: dict) -> str:
    """Home's Currently block: the top of the Experience list, and nothing else.

    A *projection*, in the sense home.md gives the word. Every string it prints
    is the same string Career prints, read from the same record, so the two
    pages cannot come to disagree about the job the author is doing now. It is
    not a summary of that record and must never be given content of its own:
    the moment somebody types a company name or a figure into this block, Home
    is back to restating, and Selected Impact is the only block on the page
    licensed to do that.

    What it drops is the substance: three groups of bullets with their Impact
    lines, and the eighty-word company description. Those are Career's job and
    a reader who wants them has a tag that goes there. What it keeps is the
    layer a hiring manager reads in the first twenty seconds, which is exactly
    the record anatomy DESIGN.md section 9 fixes for every page: title, then
    dateline, then the scan line of tags.

    The sentence beneath comes from `home_summary`, a field that exists for
    this block alone and lives *on the record*, next to the `summary` it is the
    short version of. A record without one renders no sentence rather than
    falling back: an eighty-word company description is not a Home sentence,
    and a silent fallback is how it would become one.
    """
    company = record["company"]
    if record.get("url"):
        company = (
            f'<a href="{record["url"]}" target="_blank" rel="noopener">{company}</a>'
        )

    end = month_year(record["end"]) if record.get("end") else ONGOING
    period = (f'{month_year(record["start"])} - {end}'
              f' ({tenure(record["start"], record.get("end"))})')

    title_parts = []
    if record.get("role"):
        title_parts.append(f'<span class="entry__role">{record["role"]}</span>')
    title_parts.append(f'<span class="entry__company">{company}</span>')

    dateline = []
    if record.get("location"):
        dateline.append(f'<span class="entry__location">{record["location"]}</span>')
    dateline.append(period)

    # The route back to the substance, as a utility tag: the same mechanism
    # render_project uses for a write-up, and for the same reason. It is an
    # artefact attached to the record, not a dimension of it, so it renders
    # after the model's categories and carries no ordering rule.
    more = (
        '<li><a class="tag tag--neutral" href="career.html#experience">'
        'Full role on Career</a></li>'
    )

    parts = [
        f'<p class="entry__title">\n  {" &middot; ".join(title_parts)}\n</p>',
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
        render_meta(record, "experience", extra=(more,)),
    ]
    if record.get("home_summary"):
        parts.append(f'<p class="entry__summary">{record["home_summary"]}</p>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


def cite_index(experience: list[dict]) -> dict[str, dict]:
    """Every bullet that carries an `id`, with the record and page it lives on.

    Built so Home's Selected Impact can *cite* a bullet rather than paraphrase
    it. The block used to hold a hand-written sentence beside a hand-written
    figure, both restating a bullet that already existed in `experience.json`,
    which is two copies of one fact kept in agreement by a person. home.md
    records the two occasions that failed.

    An id is added to a bullet only when Home cites it, so the index is a
    handful of entries rather than every bullet on the site: an anchor nothing
    points at is a URL promise the author did not mean to make.
    """
    index: dict[str, dict] = {}

    def walk(points: list, owner: dict) -> None:
        for point in points:
            if isinstance(point, dict) and point.get("id"):
                key = point["id"]
                if key in index:
                    raise KeyError(f"duplicate bullet id: {key}")
                index[key] = {"point": point, "owner": owner}

    def scan(record: dict, owner: dict) -> None:
        walk(record.get("points", []), owner)
        for group in record.get("groups", []):
            walk(group["points"], owner)

    for record in experience:
        scan(record, record)
        for role in record.get("roles", []):
            # A sub-role inherits its company from the record above it, and
            # keeps its own dates: OEM's two roles ran in different summers.
            scan(role, {**record, **role})
    return index


def upstream_result(pr_numbers: list[int], projects: list[dict]) -> str:
    """What a set of pull requests currently amounts to, read from Projects.

    This exists because the same fact was written down twice and the two copies
    disagreed in the shipped build: `projects.json` had both Kanboard pull
    requests `merged`, Projects rendered *Accepted upstream*, and Home's Impact
    block still said *submitted upstream, both open*. The front page was
    understating work the site could already prove.

    The weakest state wins. A pair of pull requests is only *accepted* when both
    are; one merged and one open is a submission with a merge in it, and calling
    that "accepted" is the overclaim in the other direction.
    """
    states = {
        project["upstream"]["state"]
        for project in projects
        if project.get("upstream") and project["upstream"]["pr"] in pr_numbers
    }
    missing = set(pr_numbers) - {
        project["upstream"]["pr"]
        for project in projects
        if project.get("upstream")
    }
    if missing:
        raise KeyError(
            f"impact record cites pull requests no project carries: {sorted(missing)}"
        )
    for state in ("open", "merged"):          # weakest first
        if state in states:
            return UPSTREAM_STATES[state]
    raise KeyError(f"no upstream state for pull requests {pr_numbers}")


def figure_label(figure: dict) -> str:
    """The figure as it renders, so the lint and the tag agree on one string."""
    return f"<b>{figure['value']}</b> {figure['unit']}"


def check_figure(record: dict, *sources: str) -> None:
    """The figure's value must appear verbatim in the evidence it cites.

    The one hand-written claim left on Home, and this is what stops it drifting
    without resorting to a parser. Deriving "100x faster" from a bullet means
    parsing prose, and a parser that guesses is a worse liar than a person who
    checks. Asserting that the string `100&times;` appears in the bullet the
    record cites costs nothing and catches the failure that actually happens:
    the bullet is edited, the figure on Home is not.

    Case-insensitive, because a figure is capitalised at the head of a tag
    ("Zero data lost") and lowercase mid-sentence ("guaranteed zero feedback
    data loss"), and that difference is typography rather than a discrepancy.
    """
    needle = record["figure"]["value"].lower()
    if not any(needle in source.lower() for source in sources):
        raise ValueError(
            f'{record["title"]}: figure "{record["figure"]["value"]}" does not '
            "appear in the evidence it cites. Either the bullet changed and the "
            "figure did not, or the figure is phrased differently from its source."
        )


def render_impact(record: dict, page_labels: dict, projects: list[dict],
                  citations: dict[str, dict]) -> str:
    """One Selected Impact record: the figure, its consequence, its provenance.

    This block is the one place on the site that restates facts held elsewhere,
    so it is the one place a claim can drift away from its record without
    anything noticing. It has drifted twice, in both directions, and home.md
    opens on both.

    **The sentence is not written here.** A record names a bullet with `cite`,
    and the bullet's own `impact` line is what renders: the register DESIGN.md
    section 9.2 defines for exactly this ("what changed because it shipped")
    lifted to the altitude Home reads at. A bullet with no impact line renders
    its `point` text instead, which is still the source's own words and never a
    summary of them. The old `evidence` field was a hand-written merge of the
    two, and keeping it in agreement with the bullet was a job nobody was ever
    going to do reliably.

    The provenance line and the citation link are derived from the same lookup,
    so a record cannot be dated to one job and linked to another, and the link
    lands on the bullet rather than at the top of a long page.

    **The figure leads, and that is the whole shape.** This was an `.entry`
    until it was not: `.entry` is the component for a dated record living on
    its own page, and it forced a title (so a topic had to be invented for the
    most prominent slot), a period line (so the company repeated what Currently
    already projects) and a metadata row (so the number rendered at 12px under
    a 17px topic). On a block whose subject is results, the reader was scanning
    categories. `.result` puts the figure in the slot the title had, at the
    size the title had. DESIGN.md section 9.3.

    `title` still exists on every record and no longer renders. It is the
    record's handle: what a build error names, and what tells a person editing
    `impact.json` which row they are in. `figure` is the one claim written by
    hand, and check_figure asserts its value appears verbatim in the text it
    cites, which is a lint rather than a parser: the failure that happens in
    practice is a bullet edited without its figure.

    An **aggregate** record is the one exception and it is narrow. The
    open-source line stands for two pull requests across two project records,
    so no single bullet's words can describe it; it declares `upstream_prs`,
    keeps a hand-written `evidence`, and takes its state from `projects.json`
    through the same UPSTREAM_STATES table Projects renders from. That derived
    state is what its provenance line carries, where a cited record carries the
    company. A record with both `cite` and `evidence`, or neither, is a build
    error.
    """
    figure = record["figure"]
    lead = f'<b>{figure["value"]}</b> {figure["unit"]}'

    if record.get("cite"):
        if record.get("evidence") or record.get("source"):
            raise ValueError(
                f'{record["title"]}: `cite` derives the sentence and the source, '
                "so writing `evidence` or `source` beside it invites the two to "
                "disagree, which is the whole reason `cite` exists."
            )
        citation = citations[record["cite"]]
        point, owner = citation["point"], citation["owner"]
        sentence = point.get("impact") or point["point"]
        check_figure(record, point["point"], point.get("impact", ""))
        context = owner["company"]
        href = f'career.html#{record["cite"]}'
        label = page_labels["career.html"]
    else:
        if not record.get("upstream_prs"):
            raise ValueError(
                f'{record["title"]}: an impact record cites a bullet with `cite`, '
                "or aggregates project records with `upstream_prs`. There is no "
                "third kind."
            )
        sentence = record["evidence"]
        check_figure(record, sentence)
        context = upstream_result(record["upstream_prs"], projects)
        href = record["source"]
        label = page_labels[href]

    parts = [
        f'<p class="result__figure">{lead}</p>',
        f'<p class="result__consequence">{sentence}</p>',
        f'<p class="result__source">{context} &middot; '
        f'<a href="{href}">{label}</a></p>',
    ]
    body = "\n".join(indent(part, 2) for part in parts)
    return f'<li class="result">\n{body}\n</li>'


def render_volunteering(record: dict) -> str:
    """One volunteering record as the site-wide .entry component.

    It carries no metadata model (there is nothing a reader needs about it
    that the four lines do not already say) but it is an `.entry`, and every
    other `.entry` on the site is rendered from data. A single hand-written one
    is how the next one gets hand-written too.
    """
    title = record["organisation"]
    if record.get("branch"):
        title += f' <span class="entry__role">&middot; {record["branch"]}</span>'

    parts = [
        f'<p class="entry__title">{title}</p>',
        f'<p class="entry__period">{record["period"]}</p>',
        f'<p class="entry__summary">{record["summary"]}</p>',
    ]
    body = "\n".join(indent(part, 2) for part in parts)
    return f'<li class="entry">\n{body}\n</li>'


def render_proof_key() -> str:
    """The colour key, rendered once above the block.

    Chips, not a prose sentence, because the thing being explained is a chip:
    a legend that described the colours in words would make the reader hold a
    translation in their head, where five sample chips let them match by shape.
    They are `<li>` and not links: the key is the one place on this page where a
    chip is a specimen rather than a citation, and giving it an href would put
    five destinations on the page that prove nothing.
    """
    chips = "\n".join(
        f'  <li class="tag tag--{kind}">{label}</li>'
        for kind, label in PROOF_KEY.items()
    )
    return (f'<ul class="tag-list tag-list--key" aria-label="What the evidence'
            f' colours mean">\n{chips}\n</ul>')


def render_skill(record: dict) -> str:
    """One capability, its tools, and every record on the site that proves it.

    Two columns. The left is fixed width and holds what the capability *is*:
    the name, and beneath it the standing derived from the evidence. The right
    holds the proof, and flows.

    The split is the whole point of the layout. The block was previously one
    run per skill, capability and tools and forty citations all flowing from
    the same left edge, which meant the ranking `skill_sort_key` computes was
    invisible: nothing lined up well enough to look ordered. A fixed left column
    gives the eye a column to run down, and it is the same device
    `.contact-list` already uses for a label and its value.

    The chips are links, and that is the point of the component: a claim about
    what someone can do is worth what its evidence is worth, so the evidence is
    one click away rather than asserted. Tools sit above the evidence rather
    than inside it because Talend is not a skill: building pipelines is, and
    Talend is one of the things it is built with. They render on their own list
    for the reason TOOLS_LABEL records: merging them into the evidence run would
    put an outlined chip in front of it and break the colour-run reading
    skills.md gave up positional reading to buy.
    """
    evidence = record["evidence"]

    tools = "\n".join(
        f'  <li class="tag tag--stack">{tool}</li>' for tool in record["tools"]
    )
    chips = []
    for kind in PROOF:
        for item in evidence.get(kind, []):
            chips.append(
                f'  <li><a class="tag tag--{kind}" href="{item["href"]}">'
                f'{item["text"]}</a></li>'
            )

    head = (
        '<div class="skill__head">\n'
        f'  <p class="skill__name">{record["name"]}</p>\n'
        f'  <p class="skill__standing">{standing(evidence)}</p>\n'
        "</div>"
    )
    proof = (
        '<div class="skill__proof">\n'
        f'  <ul class="tag-list skill__tools" aria-label="{TOOLS_LABEL}">\n'
        + "\n".join("  " + line for line in tools.splitlines())
        + "\n  </ul>\n"
        f'  <ul class="tag-list" aria-label="{PROOF_LABEL}">\n'
        + "\n".join("  " + line for line in chips)
        + "\n  </ul>\n"
        "</div>"
    )

    body = "\n".join(indent(part, 2) for part in (head, proof))
    return f'<li class="skill">\n{body}\n</li>'


def skill_sort_key(record: dict) -> tuple[int, int]:
    """Strongest standing first, and within a standing, best evidenced first.

    Ordering is computed for the reason awards.md rule 2 gives: a hand-ordered
    list drifts the moment a record gains a certification, and the one thing
    this block must never do is rank a skill above the evidence it now has.

    `thread` sits between the two because standing and evidence count are both
    measures of *proof*, and with four skills tied at Production-proven the
    count alone decided the front page. It cannot reorder anything across a
    standing boundary: a branch skill still outranks every trunk skill proven
    less well than it is.
    """
    evidence = record["evidence"]
    return (STANDING_ORDER[standing(evidence)],
            THREAD_ORDER[record["thread"]],
            -sum(len(items) for items in evidence.values()))


# --- page assembly ----------------------------------------------------------

def indent(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in text.splitlines())


def json_ld(site: dict, meta: dict, canonical: str) -> str:
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": site["name"],
        "url": site["base_url"] + "/",
        "image": f"{site['base_url']}/{site['portrait']}",
        "jobTitle": site["role"],
        "description": site["description"],
        "email": site["contact"][0]["href"].replace("mailto:", ""),
        "sameAs": [s["href"] for s in site["socials"]],
    }
    page = {
        "@context": "https://schema.org",
        "@type": meta.get("schema_type", "WebPage"),
        "name": meta["title"],
        "url": canonical,
        "description": meta["description"],
        "isPartOf": {"@type": "WebSite", "name": site["name"], "url": site["base_url"] + "/"},
        "author": {"@type": "Person", "name": site["name"], "url": site["base_url"] + "/"},
    }
    payload = person if meta.get("nav") == "home" else page
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def build(check_only: bool = False) -> int:
    site = json.loads((SRC / "site.json").read_text(encoding="utf-8"))
    layout = (SRC / "layout.html").read_text(encoding="utf-8")

    # Cache-bust CSS and JS off their actual contents, so a redeploy never
    # serves a stale stylesheet and an unchanged one is never re-downloaded.
    fingerprint = hashlib.sha256()
    for asset in ("assets/css/main.css",):
        fingerprint.update((ROOT / asset).read_bytes())
    asset_version = fingerprint.hexdigest()[:12]

    site_context = {f"site.{k}": v for k, v in site.items() if isinstance(v, (str, int))}

    # Data-driven sections. A page fragment holds the section's heading and
    # prose; the records themselves come from src/data/, rendered through the
    # shared metadata rules so the tag order and colours are identical
    # everywhere. Indented to sit inside the <ul class="entries"> that the
    # fragment opens.
    awards = json.loads((DATA / "awards.json").read_text(encoding="utf-8"))
    competitions = [a for a in awards if a.get("type") == "Competitive Programming"]
    hackathons = [a for a in awards if a.get("type") == "Hackathon"]
    workshops = json.loads((DATA / "workshops.json").read_text(encoding="utf-8"))
    courses = sorted(
        json.loads((DATA / "teaching.json").read_text(encoding="utf-8")),
        key=course_sort_key,
        reverse=True,
    )
    publications = sorted(
        json.loads((DATA / "research.json").read_text(encoding="utf-8")),
        key=publication_sort_key,
        reverse=True,
    )
    articles = sorted(
        json.loads((DATA / "writing.json").read_text(encoding="utf-8")),
        key=publication_sort_key,
        reverse=True,
    )
    # The Projects split is a filter on `block`, exactly as Awards filters on
    # `type`. It differs in one respect, deliberately: `block` is not a
    # metadata category and never renders, so no record carries a tag
    # restating the heading it already sits under: the tension awards.md
    # records, resolved research.md's way.
    projects = sorted(
        json.loads((DATA / "projects.json").read_text(encoding="utf-8")),
        key=project_sort_key,
        reverse=True,
    )
    articles_by_id = {a["id"]: a for a in articles}
    # Career. Experience and Education sort newest-first on their start date;
    # credentials keep the order they are written in, because an issuer group
    # has no date to sort on and grouping by issuer is the ordering.
    experience = sorted(
        json.loads((DATA / "experience.json").read_text(encoding="utf-8")),
        key=tenure_sort_key,
        reverse=True,
    )
    education = sorted(
        json.loads((DATA / "education.json").read_text(encoding="utf-8")),
        key=lambda record: record["start"],
        reverse=True,
    )
    certifications = json.loads((DATA / "certifications.json").read_text(encoding="utf-8"))
    languages = json.loads((DATA / "languages.json").read_text(encoding="utf-8"))
    online_courses = json.loads((DATA / "courses.json").read_text(encoding="utf-8"))
    # Home. An impact line cites the page that evidences it, and the link text
    # comes from the navigation rather than from the record, so a citation
    # cannot name one page and point at another.
    page_labels = {entry["href"]: entry["label"] for entry in site["nav"]}
    impact = json.loads((DATA / "impact.json").read_text(encoding="utf-8"))
    volunteering = json.loads((DATA / "volunteering.json").read_text(encoding="utf-8"))
    citations = cite_index(experience)
    skills = sorted(
        json.loads((DATA / "skills.json").read_text(encoding="utf-8")),
        key=skill_sort_key,
    )
    open_source = [p for p in projects if p.get("block") == "open-source"]
    ml_projects = [p for p in projects if p.get("block") == "machine-learning"]
    blocks = {
        "build.credential_row": indent(render_credential_row(certifications), 8),
        "build.language_row": indent(render_language_row(languages), 8),
        "build.awards": indent("\n".join(render_award(a) for a in awards), 4),
        "build.competitions": indent("\n".join(render_award(a) for a in competitions), 4),
        "build.hackathons": indent("\n".join(render_award(a) for a in hackathons), 4),
        "build.workshops": indent("\n".join(render_workshop(w) for w in workshops), 4),
        "build.courses": indent("\n".join(render_course(c) for c in courses), 4),
        "build.publications": indent("\n".join(render_publication(p) for p in publications), 4),
        "build.articles": indent("\n".join(render_article(a) for a in articles), 4),
        "build.open_source": indent(
            "\n".join(render_project(p, articles_by_id) for p in open_source), 4),
        "build.ml_projects": indent(
            "\n".join(render_project(p, articles_by_id) for p in ml_projects), 4),
        "build.experience": indent(
            "\n".join(render_experience(e) for e in experience), 4),
        "build.education": indent(
            "\n".join(render_education(e) for e in education), 4),
        "build.certifications": indent(
            "\n".join(render_credentials(c, "issuer") for c in certifications), 4),
        "build.online_courses": indent(
            "\n".join(render_credentials(c, "platform") for c in online_courses), 4),
        # Home's Currently block is experience[0] after tenure_sort_key, never a
        # record named in the fragment and never one carrying a "featured" flag.
        # When a new job starts, the block follows, because the sort follows.
        "build.current_role": indent(render_current_role(experience[0]), 4),
        "build.impact": indent(
            "\n".join(
                render_impact(i, page_labels, projects, citations)
                for i in impact if i.get("home")), 4),
        "build.proof_key": indent(render_proof_key(), 2),
        "build.skills": indent(
            "\n".join(render_skill(s) for s in skills), 4),
        "build.volunteering": indent(
            "\n".join(render_volunteering(v) for v in volunteering), 4),
    }

    stale: list[str] = []
    written: list[str] = []

    for nav_entry in site["nav"]:
        source = PAGES / nav_entry["href"]   # content fragment mirrors its output name
        meta, content = parse_front_matter(source.read_text(encoding="utf-8"))
        content = render(content.strip(), {**site_context, **blocks})
        page_context = render_page_context(content, source)

        output_name = nav_entry["href"]
        canonical = f"{site['base_url']}/{'' if output_name == 'index.html' else output_name}"
        title_tag = meta["title"] if meta.get("nav") == "home" else f"{meta['title']} &middot; {site['name']}"

        nav_items = [
            {
                **item,
                "aria_current": ' aria-current="page"' if item["id"] == nav_entry["id"] else "",
            }
            for item in site["nav"]
        ]

        context = {
            **site_context,
            "page.title_tag": title_tag,
            "page.description": meta["description"],
            "page.canonical": canonical,
            "page.og_type": "profile" if meta.get("nav") == "home" else "article",
            "page.content": indent(content, 8),
            "build.page_context": indent(page_context, 8),
            "build.asset_version": asset_version,
            "build.json_ld": json_ld(site, meta, canonical),
            "build.nav": render_items("nav-item.html", nav_items),
        }

        page_html = BANNER.format(source=source.name) + render(layout, context)
        target = ROOT / output_name

        if check_only:
            current = target.read_text(encoding="utf-8") if target.exists() else ""
            if current != page_html:
                stale.append(output_name)
        else:
            target.write_text(page_html, encoding="utf-8")
            written.append(output_name)

    if check_only:
        if stale:
            print("stale (run: python3 tools/build.py): " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"up to date: {len(site['nav'])} pages")
        return 0

    print(f"built {len(written)} pages @ assets {asset_version}: " + ", ".join(written))
    return 0


def watch() -> int:
    """Watch src/ and assets/ for changes and rebuild automatically."""
    import time

    def get_snapshot() -> dict[Path, float]:
        snapshot: dict[Path, float] = {}
        for p in SRC.rglob("*"):
            if p.is_file():
                try:
                    snapshot[p] = p.stat().st_mtime
                except OSError:
                    pass
        for asset in ("assets/css/main.css",):
            p = ROOT / asset
            if p.exists():
                try:
                    snapshot[p] = p.stat().st_mtime
                except OSError:
                    pass
        return snapshot

    build()
    print("Watching src/ and assets/ for changes... (Press Ctrl+C to stop)")
    last_snapshot = get_snapshot()

    try:
        while True:
            time.sleep(0.3)
            current_snapshot = get_snapshot()
            if current_snapshot != last_snapshot:
                last_snapshot = current_snapshot
                try:
                    build()
                except Exception as e:
                    print(f"error during build: {e}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nStopped watch mode.")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify output is current")
    parser.add_argument("--watch", action="store_true", help="watch src/ and assets/ and rebuild automatically")
    args = parser.parse_args()
    if args.watch:
        sys.exit(watch())
    sys.exit(build(check_only=args.check))
