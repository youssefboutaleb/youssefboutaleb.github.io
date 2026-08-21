#!/usr/bin/env python3
"""Render the portfolio's static pages from a single layout and per-page content.

    python3 tools/build.py           # write pages to the repository root
    python3 tools/build.py --check   # fail if the committed pages are stale

Why a builder at all: the seven published pages share an identical head,
sidebar, navigation and footer. Hand-maintaining seven copies is how the
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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
PAGES = SRC / "pages"
PARTIALS = SRC / "partials"
DATA = SRC / "data"

BANNER = (
    "<!-- GENERATED FILE — do not edit.\n"
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
# not the value — each category has one .tag--<field> rule in main.css, so
# amber always means placement and violet always means delivery mode. A new
# category is added here, once, and every record on that page picks it up.
#
# Pages get their own model rather than sharing one: a workshop has no
# placement and an award has no audience, and forcing both onto one tuple is
# how a page ends up rendering empty or meaningless dimensions. Two models may
# share a category name only if they mean the same thing by it.
MODELS = {
    "awards": ("placement", "type", "scope", "scale"),
    "workshops": ("format", "mode", "audience", "host"),
    "teaching": ("level", "workload", "scale"),
    "research": ("status", "authorship", "publisher"),
    "writing": ("format", "reach", "platform"),
    "projects": ("upstream", "kind", "stack"),
}

# Courses run on a two-semester year. Fall precedes Spring inside one academic
# year, so newest-first means sorting on (year, term) descending with Fall
# ranked below Spring — not on the year alone.
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
    decimal with a trailing .0 dropped — 723 stays 723, 1,500 becomes 1.5K,
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
        return "", f"{value['count']:,} {value['unit']}"
    if field == "stack":
        # One category, one value: the stack renders as a single tag rather
        # than one chip per tool. teaching.md removed a `stack` category that
        # rendered a tag each, because a run whose length changes per record
        # destroys the positional reading the fixed order exists to give.
        return "", " &middot; ".join(value)
    if field == "upstream":
        return "", f"{UPSTREAM_STATES[value['state']]} &middot; PR #{value['pr']}"
    if field == "reach":
        # The pair is the unit, not two facts that happen to sit together.
        # Views alone counts everyone who opened the tab and reads alone hides
        # the ratio; it is the gap between them that says whether the piece
        # held up. A record carries both figures or neither — writing.md.
        return "", (f"{abbreviate(value['views'])} views"
                    f" &middot; {abbreviate(value['reads'])} reads")
    return "", str(value)


def meta_url(field: str, value) -> str | None:
    """The canonical source for a metadata value, where one exists.

    Most categories are plain facts with nowhere to point. An upstream
    submission is not: the pull request *is* the evidence for the claim the tag
    makes, and a reader who wants to check it should not have to go looking.
    The address is built from the stored repo and number rather than typed, for
    the reason research.md builds a DOI link — the identifier is the durable
    fact and the URL is derived from it.

    A linked tag keeps its category's colour. The link is a route to the
    evidence, not a different kind of tag, and awards.md rule 4 is that the
    treatment belongs to the category and never to the individual value.
    """
    if field == "upstream":
        return f"https://github.com/{value['repo']}/pull/{value['pr']}"
    return None


def render_meta(record: dict, model: str, extra: tuple[str, ...] = ()) -> str:
    """The metadata tag list for one record, always in its model's order.

    A field the record does not carry is omitted rather than filled with a
    placeholder: a contest that never published a rank shows three tags, not an
    invented placement.

    `extra` holds already-rendered utility tags — a link to an artefact, say.
    Those are not dimensions of the record, so they carry no ordering rule and
    are appended after the model's tags rather than sequenced among them.
    """
    tags = []
    for field in MODELS[model]:
        if field not in record:
            continue
        badge, label = meta_label(field, record[field])
        url = meta_url(field, record[field])
        if url:
            tags.append(
                f'<li><a class="tag tag--{field} link-external" href="{url}"'
                f' target="_blank" rel="noopener">{badge}{label}</a></li>'
            )
        else:
            tags.append(f'<li class="tag tag--{field}">{badge}{label}</li>')
    tags.extend(extra)
    if not tags:
        return ""
    body = "\n".join("  " + tag for tag in tags)
    return f'<ul class="tag-list" aria-label="{MODEL_LABELS[model]}">\n{body}\n</ul>'


def render_award(record: dict) -> str:
    """One award as the site-wide .entry record."""
    title = record["title"]
    if record.get("venue"):
        title += f'<span class="entry__role"> &mdash; {record["venue"]}</span>'

    year = record["year"]
    parts = [
        f'<p class="entry__title">{title}</p>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "awards"),
    ]
    if record.get("points"):
        points = "\n".join(f"  <li>{point}</li>" for point in record["points"])
        parts.append(f'<ul class="points">\n{points}\n</ul>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


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
        points = "\n".join(f"  <li>{point}</li>" for point in record["points"])
        parts.append(f'<ul class="points">\n{points}\n</ul>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


def publication_sort_key(record: dict) -> int:
    """Newest first; a paper with no year yet sorts last.

    An unpublished record has no publication year to sort on, and guessing one
    from the year the work started would put it above papers that are actually
    out. Nothing is invented — it simply sorts behind everything with a date.

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

    The site's owner is bolded — the ordinary convention on a publication list,
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
    not restated — so the model asks who the author was and who published it,
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
        citation += f' &mdash; <i>{record["venue"]}</i>'
    parts.append(f'<p class="entry__meta">{citation}</p>')

    position = author_position(record)
    parts.append(render_meta({**record, "authorship": position} if position else record,
                             "research"))

    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        points = "\n".join(f"  <li>{point}</li>" for point in record["points"])
        parts.append(f'<ul class="points">\n{points}\n</ul>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


def render_article(record: dict) -> str:
    """One self-published technical article as the site-wide .entry record.

    It shares the .entry component with a paper but deliberately not the paper
    model. `status` and `publisher` would be the same two words making a
    materially different claim, and `authorship` says nothing on a piece with
    one author — so writing gets its own model rather than borrowing one that
    degrades, exactly as the comment on MODELS requires.

    What survives is the parallel that matters: `platform` takes the quiet grey
    terminal position that `publisher` takes one block above it, so the reader
    who has learned that the last tag says who stands behind the work reads
    *Medium* there against *Elsevier* — the distinction the page exists to make
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
        points = "\n".join(f"  <li>{point}</li>" for point in record["points"])
        parts.append(f'<ul class="points">\n{points}\n</ul>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


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

    extra = ()
    if record.get("article"):
        article = articles[record["article"]]
        extra = (
            f'<li><a class="tag tag--success link-external" href="{article["url"]}"'
            f' target="_blank" rel="noopener">Article on {article["platform"]}</a></li>',
        )

    year = record["year"]
    parts = [
        f'<p class="entry__title">{title}</p>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "projects", extra),
    ]
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')
    if record.get("points"):
        points = "\n".join(f"  <li>{point}</li>" for point in record["points"])
        parts.append(f'<ul class="points">\n{points}\n</ul>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


def course_sort_key(record: dict) -> tuple[int, int]:
    """Newest first, by academic year then by term within it."""
    return (record["year"], TERM_ORDER[record["term"]])


def render_course(record: dict) -> str:
    """One taught course as the site-wide .entry record.

    The body is a syllabus rather than a list of achievements, so it uses
    .entry__group — the component the Career page already uses to subdivide a
    long record. Module numbers are produced here rather than written into the
    data, for the same reason placements are: hand-numbered lists are how a
    reordered syllabus ends up with two Module 3s.

    Technologies are named inside the module that teaches them. They carry no
    tag of their own: a row of tool names crowds out the three fixed positions
    in front of it, and a tool means more beside the thing it was used for than
    it does in a list.

    The capstone is its own group rather than a trailing module, because it is
    not one: the workload states five lecture modules and one project session,
    and a sixth numbered module would contradict the hours it is counted in.
    """
    year, term = record["year"], record["term"]
    period = f"{term} {year} &ndash; {year + 1}"

    parts = [
        f'<p class="entry__title">{record["title"]}</p>',
        f'<p class="entry__period">{period}</p>',
        render_meta(record, "teaching"),
    ]
    if record.get("summary"):
        parts.append(f'<p class="entry__summary">{record["summary"]}</p>')

    def group(title: str, points: list[str]) -> str:
        items = "\n".join(f"    <li>{point}</li>" for point in points)
        return (
            '<div class="entry__group">\n'
            f'  <p class="entry__group-title">{title}</p>\n'
            f'  <ul class="points">\n{items}\n  </ul>\n'
            "</div>"
        )

    for number, module in enumerate(record.get("syllabus", []), start=1):
        parts.append(group(f"Module {number} &mdash; {module['title']}", module["points"]))

    capstone = record.get("capstone")
    if capstone:
        parts.append(group(f"Final Project &mdash; {capstone['title']}", capstone["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


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
    # restating the heading it already sits under — the tension awards.md
    # records, resolved research.md's way.
    projects = sorted(
        json.loads((DATA / "projects.json").read_text(encoding="utf-8")),
        key=project_sort_key,
        reverse=True,
    )
    articles_by_id = {a["id"]: a for a in articles}
    open_source = [p for p in projects if p.get("block") == "open-source"]
    ml_projects = [p for p in projects if p.get("block") == "machine-learning"]
    blocks = {
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
    }

    stale: list[str] = []
    written: list[str] = []

    for nav_entry in site["nav"]:
        source = PAGES / nav_entry["href"]   # content fragment mirrors its output name
        meta, content = parse_front_matter(source.read_text(encoding="utf-8"))
        content = render(content.strip(), {**site_context, **blocks})

        output_name = nav_entry["href"]
        canonical = f"{site['base_url']}/{'' if output_name == 'index.html' else output_name}"
        title_tag = meta["title"] if meta.get("nav") == "home" else f"{meta['title']} — {site['name']}"

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
            "build.asset_version": asset_version,
            "build.json_ld": json_ld(site, meta, canonical),
            "build.nav": render_items("nav-item.html", nav_items),
            "build.contact": render_items("contact-item.html", site["contact"]),
            "build.socials": render_items("social-link.html", site["socials"]),
            "build.credentials": render_items(
                "credential.html", [{"text": c} for c in site["credentials"]]
            ),
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
        print(f"up to date — {len(site['nav'])} pages")
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
