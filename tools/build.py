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
import difflib
import fnmatch
import hashlib
import json
import re
import struct
import sys
import unicodedata
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path

# French groups thousands with a narrow no-break space, not a comma: 7,094 is
# 7 094. The character is U+202F, and it must not break across a line.
THIN_SPACE = "\u202f"

# The site's peer separator, per CLAUDE.md section 6. Named so a renderer
# joining two peers cannot quietly reach for a different glyph.
SEPARATOR = "&middot;"

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

# Everything between these is a comment, and every comment in src/ is a note to
# whoever edits src/ next.
COMMENT = re.compile(r"[ \t]*<!--.*?-->[ \t]*\n?", re.DOTALL)
BLANK_RUN = re.compile(r"\n[ \t]*\n[ \t]*\n+")


def strip_comments(markup: str) -> str:
    """Drop authoring comments on the way out of the build.

    The fragments and the layout are where this repository argues with itself:
    why the hero is one block and not two, which option document carried the
    finding, what a rule in CLAUDE.md was protecting. That reasoning is the
    point of `src/`, and none of it is addressed to a visitor.

    It was reaching them anyway. `index.html` was 14.8% comment bytes, and one
    of them opened *"INTERIM, awaiting the author's sentence"*, which is a note
    to the author sitting in the page source of the front page. The third
    reader in CLAUDE.md section 2 is the one who opens the source, so the
    audience for the draft notes was precisely the audience they were never
    written for.

    The BANNER survives, because it is the one comment written *to* a reader of
    the built file: it says the file is generated and names what to edit
    instead. It is added after this runs.
    """
    return BLANK_RUN.sub("\n\n", COMMENT.sub("", markup))

# How a brand logo survives the dark rendering. The SVGs ship as <img>, so the
# stylesheet cannot recolour their interiors; the modifier tells it what the
# mark is made of and main.css section 17 acts on that. Keyed by filename so a
# logo declares its treatment once instead of at every call site.
#
#   mono   single-colour black, inverts cleanly to white
#   plate  coloured mark carrying black ink, keeps its colours on a light ground
#
# Anything absent from this table needs no treatment: it is a coloured mark that
# already reads on either ground. Check a new logo before adding it, because a
# black one that is missed here goes invisible in dark mode and nothing fails.
ICON_TREATMENT = {
    "github.svg": "mono",
    "anthropic-light.svg": "mono",
    "medium.svg": "mono",
    "opencv.svg": "plate",
}


def icon_classes(filename: str, size: str) -> str:
    """The class attribute for one brand logo at one size."""
    treatment = ICON_TREATMENT.get(filename)
    classes = f"icon icon--{size}"
    return f"{classes} icon--{treatment}" if treatment else classes


# --- locales ----------------------------------------------------------------

# One source, two renderings, which is the whole of CLAUDE.md M4. English is
# the source and lives in src/data/; a translation is an *overlay* in
# src/i18n/<code>.json and never a second copy of the records.
#
# The overlay keys strings by `<record id>.<field>`, which is why record ids
# are generated from the English title and never from the translated one:
# impact.json cites bullets by id, skills.json carries forty citation targets,
# and the page context rail anchors on the same ids. Translating an id would
# break all three at once and silently, so structure, order, ids and every
# citation stay single-source and only display strings vary.
#
# A locale that is missing a string falls back to English rather than to a
# hole. That is deliberate: a half-translated page is readable and an empty one
# is not, and `--check` lists what is still missing so the gap is visible.

I18N = SRC / "i18n"


class Locale:
    """One rendering of the site: its language, its chrome, its overlay."""

    def __init__(self, code: str, config: dict) -> None:
        self.code = code                      # "en", "fr"
        self.lang = config.get("lang", code)
        self.og_locale = config.get("og_locale", "en_US")
        self.label = config.get("label", code)
        self.dir = "" if config.get("root") else f"{code}/"
        # "" from the site root, "../" from a locale subdirectory. Only assets
        # need it: a link from /fr/awards.html to career.html already resolves
        # to /fr/career.html, which is the French page, for free.
        self.up = "" if config.get("root") else "../"
        self.strings = config.get("strings", {})
        self.records = config.get("records", {})
        # Keys that are deliberately not translated: proper nouns, employers,
        # certification names, tech. Without this every build would list them
        # as missing forever, and a report that is mostly noise is a report
        # nobody reads. fnmatch patterns, so "*.title" covers a whole field.
        self.keep = tuple(config.get("keep", ()))
        # How this language builds an ordinal. English needs a table of
        # suffixes and a teens exception; French needs "1re" and "Ne". The
        # pilot found this the expensive way: with only placement.1, .2 and .3
        # in the overlay, a 13th and a 643rd placement stayed English on the
        # French page, and enumerating placement.643 is not a design.
        self.ordinal_forms = config.get("ordinal")
        self.group = config.get("group", ",")
        self.overrides = config.get("site", {})
        self.missing: set[str] = set()
        # For every key that IS translated, the fingerprint of the English it
        # was translated from. Compared against the lock file to catch the
        # failure a fallback cannot: a string translated once, then edited in
        # English, where the translation stays confidently wrong.
        self.seen: dict[str, str] = {}

    def number(self, value: int) -> str:
        """`value` with this language's thousands separator.

        English groups with a comma, French with a narrow no-break space:
        7,094 teams is 7 094 equipes. The separator is part of the language,
        not part of the figure, so the stored integer is never touched.
        """
        return f"{value:,}".replace(",", self.group)

    def ordinal(self, number: int) -> str:
        """`number` as an ordinal in this language."""
        if not self.ordinal_forms:
            return ordinal(number)
        form = self.ordinal_forms.get(str(number)) or self.ordinal_forms["other"]
        return form.replace("{n}", self.number(number))

    def witness(self, key: str, source) -> None:
        """Record what English this key was translated from."""
        self.seen[key] = fingerprint(source)

    def keeps(self, key: str) -> bool:
        """Is this key deliberately left in the source language?"""
        return any(fnmatch.fnmatch(key, pattern) for pattern in self.keep)

    def text(self, key: str, default: str) -> str:
        """A chrome string: navigation, buttons, aria labels, month names."""
        if key in self.strings:
            if self.code != "en":
                self.witness(key, default)
            return self.strings[key]
        if self.code != "en" and not self.keeps(key):
            self.missing.add(key)
        return default


def fingerprint(value) -> str:
    """A stable short hash of an English source value.

    json.dumps with sorted keys so a list of bullets fingerprints as a whole:
    reordering them or editing one is a change to the thing that was
    translated, and both should be caught.
    """
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def load_locales() -> list[Locale]:
    """English first, then every overlay in src/i18n, alphabetically.

    English is built from src/data/ alone and has no overlay file: it is the
    source, and giving it one would be the first step towards forking it.
    """
    locales = [Locale("en", {"lang": "en", "og_locale": "en_US",
                             "label": "English", "root": True})]
    if I18N.is_dir():
        # *.lock.json are the sync fingerprints, not languages. Without this
        # the glob discovered "fr.lock" as a locale, built a site at /fr.lock/
        # and wrote fr.lock.lock.json, which discovered "fr.lock.lock", and so
        # on: one build produced 48 pages across five imaginary languages.
        for path in sorted(I18N.glob("*.json")):
            if path.name.endswith(".lock.json"):
                continue
            locales.append(Locale(path.stem, json.loads(path.read_text(encoding="utf-8"))))
    return locales


# The locale being rendered. A module-level binding rather than a parameter
# threaded through every render_* function: this is a single-pass,
# single-threaded build, and the alternative was fifteen signatures growing an
# argument that fourteen of them would only pass along.
ACTIVE = Locale("en", {"lang": "en", "og_locale": "en_US", "label": "English", "root": True})


def asset(path: str) -> str:
    """A site asset, addressed from the page currently being written.

    Everything under images/ and data/ lives once at the site root, so a page
    in a locale directory reaches it through "../". Links *between* pages need
    no such help: awards.html from inside /fr/ already means /fr/awards.html,
    which is the French page, which is what was wanted.

    An absolute URL is returned untouched: some credentials link to the
    issuer's own record rather than to a scan this site serves.
    """
    if path.startswith(("http://", "https://", "//", "mailto:", "#")):
        return path
    return f"{ACTIVE.up}{path}"


def t(record: dict, field: str, default=None):
    """The value of `field` on `record`, in the active locale.

    Falls back to the English value. A record with no id cannot be overlaid,
    which is correct: the overlay addresses records by id and an unaddressable
    record has nothing to key on.
    """
    value = record.get(field, default)
    record_id = record.get("id")
    if ACTIVE.code == "en" or not record_id:
        return value
    key = f"{record_id}.{field}"
    if key in ACTIVE.records:
        ACTIVE.witness(key, value)
        return ACTIVE.records[key]
    # A list counts. This tested `isinstance(value, str)` only, so every
    # `points` array on the site fell through untranslated and was never
    # reported, which is most of the words on most of the pages. The
    # translation gate then measured those pages at 0% and could not say why.
    # A non-empty list. An empty one is a record that simply has no groups or
    # no sub-roles, and reporting it asks for a translation of nothing.
    translatable = bool(value) and isinstance(value, (str, list, dict)) and str(value).strip()
    if translatable and not ACTIVE.keeps(key):
        ACTIVE.missing.add(key)
    return value


def tr(key: str, default: str) -> str:
    """A chrome string in the active locale."""
    return ACTIVE.text(key, default)


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
    """Convert text into a safe HTML id anchor, ASCII only.

    Accents are folded rather than kept: `\\w` matches them, so an
    organisation written "Jeunes Ingenieurs de Djerba" (with the accent) used
    to produce an id carrying that accent. It works in a modern browser and it
    is wrong here for two reasons. Every other id on the site is ASCII, and an
    anchor is a durable name that gets pasted into citations, the page context
    rail and translation overlay keys: it should survive a copy through any
    tool that is careless about encoding.

    Folding is a no-op for every id that existed before it was added, because
    every source field was ASCII. It is here because the first accented record
    arrived from the English data, not from the French overlay, which is where
    it was expected.
    """
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


class TocNode:
    def __init__(self, node_id: str, title: str = "", level: int = 1):
        self.id = node_id
        self.title = title
        # 1: section, 2: record, 3: a part of a record (a course's modules).
        # There is no level 4. One was declared here for a "Lab" tier that was
        # never built, and it kept three CSS rules alive for years of nothing.
        self.level = level
        self.children: list[TocNode] = []


class BookTocParser(HTMLParser):
    """Collect sections, records and their parts for the page context rail."""

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

        # A record may name itself for the rail. That is how an abbreviation
        # gets in without this parser knowing anything about the content: two
        # award names used to be string-replaced here by hand, so renaming one
        # in awards.json silently stopped the replacement applying.
        toc_title = a.get("data-toc-title")

        # An id is an address, and not every address is a place worth listing.
        # The credential groups exist so Home's evidence chips can name one
        # issuer instead of the whole Certifications block; indexing them would
        # push eleven issuer and platform names into a Career rail that already
        # runs to fifteen entries, to say what the block heading says. The rail
        # is a contents page, not an index of every anchor on the page.
        # Membership, not a truth test: HTMLParser gives a valueless attribute
        # the value None, so `data-toc-skip` and `data-toc-skip=""` both read
        # as absent under `.get(...)`.
        if "data-toc-skip" in a:
            return

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

            # Both branches below used to carry an id-prefix allowlist beside
            # the class test (course-, exp-, edu-, ... and mod-, hw-, cap-,
            # grp-). Every record carries .entry and every indexed group
            # carries .entry__group, and no id on the site has ever begun with
            # one of those four group prefixes, so the lists matched nothing
            # and quietly promised that a new prefix would be handled.
            elif tag == "li" and tag_id and "entry" in cls.split():
                self._entry_node = TocNode(tag_id, toc_title or "", level=2)
                self._sec_node.children.append(self._entry_node)
                self._group_node = None

            elif tag in {"p", "h3"} and "entry__title" in cls and self._entry_node:
                self._target_node = self._entry_node
                self._target_tag = tag
                self._text_buf = []

            elif tag == "div" and tag_id and "entry__group" in cls.split():
                parent = self._entry_node or self._sec_node
                self._group_node = TocNode(tag_id, toc_title or "", level=3)
                parent.children.append(self._group_node)

            elif tag in {"p", "h4"} and "entry__group-title" in cls and self._group_node:
                self._target_node = self._group_node
                self._target_tag = tag
                self._text_buf = []

    def handle_data(self, data: str) -> None:
        if self._target_node:
            self._text_buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._target_node and tag == self._target_tag:
            # A node that named itself keeps that name: the whole point of
            # data-toc-title is that the record decides, not this parser.
            if self._target_node.title:
                self._target_node = None
                self._target_tag = None
                self._text_buf = []
                return

            text = " ".join("".join(self._text_buf).split())

            # An .entry__title joins peers with a middot: `Role &middot;
            # Company` on Career, `Title &middot; Venue` elsewhere. The rail
            # has room for one of them, and which one is the useful half
            # depends on the record: an employer is what a reader scans a
            # career for, a title is what they scan everything else for.
            if "·" in text:
                parts = [p.strip() for p in text.split("·")]
                if self._target_node.id.startswith(("exp-", "edu-")) and len(parts) > 1 and parts[1]:
                    text = parts[1]
                else:
                    text = parts[0]

            # A "Lab:" branch lived here, truncating a lab's title to 35
            # characters. No .entry__group-title on the site begins with
            # "Lab:", and labs are .point--lab list items that the rail never
            # indexes, so it shortened nothing. It belonged to the same
            # unbuilt level 4 as the dead CSS.
            self._target_node.title = text.strip()
            self._target_node = None
            self._target_tag = None
            self._text_buf = []


# Sections and the records inside them. Not the parts of a record.
#
# The rail indexed three levels because Teaching's data model puts an id on
# every module and every lab, which it does so Home's citations can reach them.
# The rail inherited that granularity and printed it: one top-level link over
# twenty-two module names, on a page whose h1 is one word. Density ran 22 to 1
# across the site for no reason a reader could act on.
#
# An id is an address and the rail is a contents page, not an index of every
# anchor: the two jobs came apart here and in `data-toc-skip`. Modules stay
# addressable and stop being listed.
TOC_DEPTH = 2


def render_toc_node(node: TocNode) -> str:
    """Recursively render a TocNode and its children as HTML list items."""
    if not node.title:
        raise ValueError(
            f"page context: no label found for #{node.id}. This used to fall "
            f"back to the id with its hyphens swapped for spaces and title "
            f"cased, so a record whose title failed to parse shipped a rail "
            f"entry reading 'Exp Jacquemus 1'. Give the record a heading the "
            f"parser can read, or a data-toc-title of its own."
        )

    link_class = "book-toc__link" if node.level == 1 else "book-toc__sublink"
    link_html = f'<a class="{link_class}" href="#{escape(node.id, quote=True)}">{escape(node.title)}</a>'

    # No --level-N modifier on either element. Every depth is styled the same
    # (one left hairline, one indent), so a per-level class carried nothing and
    # simply guaranteed that main.css kept rules for depths the parser had
    # stopped producing. The nesting is in the markup; the indent says the rest.
    if not node.children or node.level >= TOC_DEPTH:
        return f'<li class="book-toc__item">\n  {link_html}\n</li>'

    children_html = "\n".join(indent(render_toc_node(child), 2) for child in node.children)
    return (
        '<li class="book-toc__item">\n'
        f'  {link_html}\n'
        '  <ul class="book-toc__sublist">\n'
        f'{children_html}\n'
        '  </ul>\n'
        '</li>'
    )


def render_page_context(content: str, source: Path) -> str:
    """Render the page context rail: an index of this page's own records.

    Parses `content` *after* it has been rendered rather than reading the data
    that produced it. That is the cheaper of the two and also the safer one: an
    index built from the data would be asserting what the page contains, and
    this one observes it, so it cannot name a record that failed to render or
    an anchor that does not exist. It also means the rail costs nothing to
    maintain, since a record added to src/data/ appears in it with no second
    edit anywhere.

    Returns "" for a page with no sections, which is what keeps the aside empty
    rather than shipping a heading with nothing under it.

    DESIGN.md section 12.2 for what it renders, section 4 for why a rail is
    admissible here at all.
    """
    parser = BookTocParser()
    parser.feed(content)
    parser.close()

    if not parser.root.children:
        return ""

    # Two records with the same title are two identical links. Career listed
    # "Jeunes Ingenieurs de Djerba (JID)" twice, one 2023 and one 2022, and a
    # rail that cannot tell them apart is a rail that makes the reader click to
    # find out. Disambiguated here rather than in the data because it is a
    # property of the *pair*, not of either record: neither is ambiguous alone,
    # and hand-writing a data-toc-title on both means editing two records when
    # a third arrives.
    disambiguate(parser.root)

    body = "\n".join(indent(render_toc_node(child), 6) for child in parser.root.children)
    # A list of links, and nothing else that a reader could operate.
    #
    # This was a <details>, forced open above 1024px by two CSS declarations
    # while the element itself stayed closed. So the desktop rail painted its
    # whole tree while telling assistive technology the region was collapsed,
    # and left a focusable <summary> that did nothing visible when activated.
    # CLAUDE.md section 7 admits the rail on the ground that deleting it costs
    # the reader nothing but convenience; a control that lies about its own
    # state is not covered by that argument and was never argued for.
    #
    # It became affordable to delete once the tree stopped going three levels
    # deep. Teaching's rail was 1 link over 22 sublinks, roughly 668px of
    # navigation in front of the page's first word on a phone, which is what
    # the disclosure existed to fold away. Capped at records, it is four lines.
    #
    # The <nav> is labelled by the visible heading rather than carrying its own
    # aria-label. The aside, the nav and the heading previously gave a screen
    # reader three names for one region.
    return (
        '<nav class="book-toc" aria-labelledby="page-context-label">\n'
        f'  <p class="book-toc__header" id="page-context-label">{tr("chrome.contents", "Contents")}</p>\n'
        '  <ul class="book-toc__list">\n'
        f'{body}\n'
        '  </ul>\n'
        '</nav>'
    )


def disambiguate(node: TocNode) -> None:
    """Give siblings that share a title something to tell them apart by."""
    for child in node.children:
        disambiguate(child)
    seen: dict[str, list[TocNode]] = {}
    for child in node.children:
        seen.setdefault(child.title, []).append(child)
    for title, group in seen.items():
        if len(group) < 2:
            continue
        for child in group:
            # The id already carries whatever distinguishes them, because
            # with_ids slugifies a field the records do not share. The trailing
            # year is the useful half of it.
            tail = child.id.rsplit("-", 1)[-1]
            if tail.isdigit():
                child.title = f"{title} {tail}"


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
    # `type` was here and is not any more. The two blocks on Awards are a
    # filter on that field in build(), so every record inside a block carried a
    # chip repeating the heading three lines above it: `Competitive
    # Programming` on all seven, `Hackathon` on the one. awards.md logged this
    # as a known tension and noted research.md had already resolved the same
    # case the other way, keeping the type in the block heading and out of the
    # model. It is resolved that way here too. The field stays in the data,
    # because build() still filters on it; what goes is the chip, and with it
    # the widest chip on the page at 181px.
    #
    # `stack` arrives, and last, which is the condition render_meta states for
    # it: a run whose length varies has to sit after every category that is
    # read positionally. The hackathon is the one record on this page that
    # built something, and its tools were four <b> spans inside the prose,
    # which is the device Projects uses for a bullet's *topic*. CLAUDE.md
    # section 6: tools are outlined chips on Career, Projects and Home alike,
    # and one vocabulary for "a thing this was built with" is the whole point
    # of that sentence. A competition carries no `stack` and renders one tag
    # fewer, which is awards.md rule 5.
    "awards": ("placement", "distinction", "type", "scope", "scale", "duration", "track", "stack"),
    "workshops": ("format", "mode", "duration", "audience", "scale", "host"),
    # `workload` was here and is not any more. The specs panel at the top of
    # Teaching states "32 h per course" and breaks it into 20 lecture, 8 lab
    # and 4 project, because the figure is a constant of the appointment. Every
    # course record then carried a chip repeating that same breakdown, so one
    # page stated one fact four times. The panel owns it. A course that ever
    # differs from the panel is the case that earns the chip back.
    "teaching": ("level", "scale"),
    "research": ("status", "authorship", "publisher"),
    "writing": ("format", "reach", "platform"),
    "projects": ("upstream", "kind", "stack"),
    "experience": ("domain", "engagement", "mode", "scale", "stack"),
    "education": ("programme", "focus", "accreditation"),
}

# The `status` values that mean the work is not out yet. Read by the research
# renderer, which prints a target journal as *submitted to* rather than in the
# bare citation slot that means *published in*. Kept beside MODELS because it
# is a fact about the `status` vocabulary declared there, and research.md
# section "Vocabulary" is the other half of it.
PENDING_STATUS = ("Under Review", "In Progress")

# Skills are the one block whose tags are *citations* rather than dimensions,
# so their model is declared apart from MODELS and read only by render_skill.
# Order runs strongest proof first and never varies, which is what lets the
# leading colour of a row be read as its standing: a row that starts green ran
# in production, a row that starts blue did not. skills.md carries the full
# argument, including why this is the one model where a category may repeat.
PROOF = ("production", "certification", "taught", "published", "applied")

# What each kind of proof is called when a reader hovers the group. The label
# is on the list, not on every chip, for the reason MODEL_LABELS exists.
PROOF_LABEL_EN = "Evidence"

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
TOOLS_LABEL_EN = "Tools"

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
    return ACTIVE.number(count)


def meta_label(field: str, value) -> tuple[str, str]:
    """Turn one raw metadata value into (medal markup, human label).

    Placements are stored as plain integers and rankings are spelled out here
    rather than in the data, so "1st Place" cannot become "1st place" or
    "First" in the next record someone adds.
    """
    if field == "placement" and isinstance(value, int):
        medal = MEDALS.get(value)
        badge = f'<span class="medal medal--{medal}" aria-hidden="true"></span>' if medal else ""
        # "1st Place" in English, "1re place" in French. Two things vary and
        # both are language: how the ordinal is formed, and how the phrase is
        # built around it. Neither is a suffix that can be swapped.
        phrase = tr("placement.pattern", "{ordinal} Place")
        return badge, phrase.replace("{ordinal}", ACTIVE.ordinal(value))
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
        def figure(number: int) -> str:
            text = ACTIVE.number(number)
            if value.get("minimum"):
                return f"{text}+"
            if value.get("approx"):
                return f"~{text}"
            return text

        count = figure(value["count"])
        # `of` is scope against system size, and a record carrying both is
        # saying two different things with one chip. JACQUEMUS read "150+
        # pipelines" while the first bullet underneath said "20+ of a 150+
        # pipeline estate": a reader who scans chips and stops, which is
        # reader one in CLAUDE.md section 2, took the estate for the scope and
        # nothing on the page corrected them until the bullet. The chip now
        # carries the correction rather than depending on it.
        unit_name = value["unit"]
        unit_text = tr(f"unit.{unit_name}", unit_name)
        if value.get("of"):
            whole = figure(value["of"])
            joiner = tr("scale.of", "of")
            return "", f"<b>{count}</b> {joiner} <b>{whole}</b> {unit_text}"
        # The figure is bold inside an otherwise regular-weight chip, the same
        # emphasis every bullet on the site gives its numbers. It is a
        # treatment of the same part of every scale value, never of one value
        # over another, so awards.md rule 4 holds: 86 teams and 643rd of 7,094
        # are emphasised identically.
        return "", f"<b>{count}</b> {unit_text}"
    if field == "duration" and isinstance(value, int):
        # Stored as a number, spaced here, so `2h` and `20 h` cannot coexist.
        # They did: Workshops wrote `2h` and `4h` straight into the data while
        # Teaching's panel wrote `20 h` and `1.5-2 h`, which is the same unit
        # in one document spelled two ways. A value formatted at the call site
        # is a value that drifts from every other call site.
        return "", f"{ACTIVE.number(value)} {tr('unit.hours_short', 'h')}"
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
    # Everything else is a plain stored word: "Hackathon", "Regional",
    # "On-site". These are the site's metadata vocabulary rather than prose,
    # so they are translated by value and not by record: one entry in the
    # overlay does every award that says "Hackathon", and a value nobody has
    # translated falls through as English rather than as a gap.
    return "", tr(f"tag.{field}.{value}", str(value))


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
    return f'<ul class="tag-list" aria-label="{tr(f"model_label.{model}", MODEL_LABELS[model])}">\n{body}\n</ul>'


IMPACT_LABEL_EN = "Impact:"


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
            f"<b>{tr("label.impact", IMPACT_LABEL_EN)}</b> {impact}</span>"
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
        f'  <h4 class="entry__group-title">{title}</h4>\n'
        f'{indent(render_points(points, lab_prefix=group_id), 2)}\n'
        "</div>"
    )


# Each record type's anchor id, derived from the English source field. Held in
# one place because the page context rail, impact.json's citations,
# skills.json's forty proof links and every translation overlay key all address
# records by these strings: they are the site's stable names for its own
# contents, and they must not move when a page is translated.
ID_RULES = {
    "award": "title",
    "ws": "title",
    "pub": "title",
    "art": "title",
    "proj": "title",
    "exp": "company",
    "edu": "institution",
    # A tuple where one field is not unique on its own. Volunteering holds an
    # edition per record, following the same convention as TCPC 22 and TCPC 23
    # on Awards, so two JID records would otherwise collide on the
    # organisation and produce one id for both.
    "vol": ("organisation", "year"),
    # Everything below was rendering with an id the renderer computed for
    # itself and the record never saw, which is why none of it could be
    # translated: `t()` addresses a record by `record["id"]` and returned the
    # English every time because there was nothing to key on.
    "course": "title",
    "skill": "name",
    "cert": "issuer",
    "learn": "platform",
    "lang": "name",
    # Impact records are addressable so their `figure` can be translated. It
    # could not be, and check_figure compares that figure against the prose it
    # cites *in the active locale*: a French bullet reading "1 400 EUR" would
    # have been checked against the English "&euro;1,400" and failed the build,
    # and the unit beside it ("per month") was going to render in English on
    # the French front page regardless.
    "impact": "title",
}


def with_ids(records: list[dict], prefix: str) -> list[dict]:
    """Stamp each record with its anchor id, in place, before rendering.

    The renderers used to each derive this themselves. Naming it once and
    early means a record knows its own id before anything asks, which is what
    lets the translation overlay address it and the renderer stop recomputing.
    """
    fields = ID_RULES[prefix]
    if isinstance(fields, str):
        fields = (fields,)
    for record in records:
        parts = [str(record[f]) for f in fields if record.get(f)]
        record.setdefault("id", f"{prefix}-{slugify(' '.join(parts))}")
    return records


def entry_li(record: dict, entry_id: str, body: str) -> str:
    """Wrap a rendered record as the site's .entry list item.

    `short` is optional and does one job: it is the record's label in the page
    context rail, for a title too long to sit in a 240px track. It is data
    because the alternative was worse. The rail's parser used to carry the
    abbreviations itself, as two literal str.replace calls naming two awards,
    so renaming either one in awards.json silently stopped shortening it and
    nothing failed. A record that needs a short name now says so next to the
    long one, and the parser stays ignorant of what the site is about.
    """
    attributes = f'class="entry" id="{escape(entry_id, quote=True)}"'
    if t(record, "short"):
        attributes += f' data-toc-title="{escape(t(record, "short"), quote=True)}"'
    return f'<li {attributes}>\n{body}\n</li>'


# The performance spec on a contest record.
#
# These four facts used to be one hand-written sentence, `Solved 8 / 8 problems
# in 4h (Team of 2)`, in seven records, hand-translated into French seven more
# times. awards.md rule 7 says to store the raw fact and let the renderer
# produce the label, and the bullet rule three sections below it said to write
# that exact string, so the document contradicted itself and the page paid:
# the bullets spelled the hour unit `4h` while the hackathon's `duration` tag,
# produced by meta_label, spelled it `48 h`. One page, one unit, two spellings,
# which is precisely what the comment on `duration` in meta_label says must not
# happen. The French overlay had quietly corrected it to `4 h`, so the two
# languages disagreed about the format of the same figure.
#
# `duration` goes through the tag now, like every other duration on the site.
# What is left is a score and a team size, and those are measurements rather
# than filing categories, so they render as a label column instead of as chips:
# a tag says "this record is filed under X", which a solve count is not.
#
# The emphasis is on the whole figure and never on part of one, so 8 / 8 and
# 11 / 26 are set identically. awards.md rule 4: the treatment belongs to the
# category, never to the value.
def check_award_shape(record: dict) -> None:
    """A contest states its score; a hackathon states what it built. Not both.

    The two blocks on Awards are one model filtered on `type`, and the bullet
    rules distinguish them: a competition has a problem count and nothing else
    worth saying, a hackathon has no problem count and says what was delivered.
    A record carrying `performance` and `points` at once is a record saying one
    thing twice, which is how the hand-written sentence got there in the first
    place. awards.md, the bullet rules.
    """
    if record.get("performance") and record.get("points"):
        raise ValueError(
            f'{record["id"]}: an award carries `performance` or `points`, never '
            "both. The score, the duration and the team size are fields and the "
            "renderer labels them; bullets are for a hackathon, which has no "
            "problem count to state. awards.md, the bullet rules."
        )


def render_performance(record: dict) -> str:
    """A contest result's score and team size, as a label column."""
    check_award_shape(record)
    perf = record.get("performance")
    if not perf:
        return ""
    solved = ACTIVE.number(perf["solved"])
    problems = ACTIVE.number(perf["problems"])
    # No <b> here. `.perf__row > dd` is bold in full, unit included, which is
    # how `.spec__row` renders `20 h`: the label recedes and the value carries
    # the weight. Emphasising only the numerator would also have been awards.md
    # rule 4 broken, styling part of a value rather than the whole category.
    rows = [
        (
            tr("perf.problems", "Problems"),
            f'{solved} / {problems} {tr("perf.solved", "solved")}',
        ),
        (tr("perf.team", "Team"), ACTIVE.number(perf["team"])),
    ]
    body = "\n".join(
        f'  <div class="perf__row">\n'
        f"    <dt>{label}</dt>\n"
        f"    <dd>{value}</dd>\n"
        f"  </div>"
        for label, value in rows
    )
    return f'<dl class="perf">\n{body}\n</dl>'


def render_award(record: dict) -> str:
    """One award as the site-wide .entry record."""
    title = t(record, "title")
    if record.get("url"):
        title = (
            f'<a class="link-external" href="{record["url"]}" target="_blank"'
            f' rel="noopener">{title}</a>'
        )
    if t(record, "venue"):
        title += f'<span class="entry__role"> &middot; {t(record, "venue")}</span>'

    dateline = []
    if t(record, "location"):
        dateline.append(f'<span class="entry__location">{t(record, "location")}</span>')
    if record.get("date"):
        dt = record["date"]
        dateline.append(f'<time datetime="{dt}">{month_year(dt)}</time>')
    else:
        year = record["year"]
        dateline.append(f'<time datetime="{year}">{year}</time>')

    # The dataset the work ran on, as a utility tag rather than a hand-written
    # anchor inside a sentence. DESIGN.md section 7.2 already names "a dataset"
    # as a `.tag--artifact` case, and this one was a raw <a> in the middle of
    # the first bullet, carrying its own target and rel and *not* the
    # link-external marker the teammate link two bullets down did carry: one
    # record, two inline links, two treatments.
    #
    # The noun is a chrome string and the name is a record field, which is the
    # split awards.md rule 7 asks for. Written as `Dataset ({name})` it was an
    # English word emitted from a renderer with no `tr()` around it, so the
    # French page would have said `Dataset` in a chip beside `48 h` and
    # `Quart de finaliste`, which is the failure CLAUDE.md section 9 lists as
    # "a record field a renderer reads directly instead of through t()".
    extra_tags = []
    if record.get("performance"):
        perf = record["performance"]
        solved = ACTIVE.number(perf["solved"])
        problems = ACTIVE.number(perf["problems"])
        team_count = ACTIVE.number(perf["team"])
        solved_text = tr("perf.solved", "solved")
        team_label = tr("perf.team", "Team")
        extra_tags.append(
            f'<li class="tag tag--problems"><b>{solved} / {problems}</b> {solved_text}</li>'
        )
        extra_tags.append(
            f'<li class="tag tag--team">{team_label} <b>{team_count}</b></li>'
        )
    if record.get("dataset"):
        name = t(record, "dataset_label")
        label = tr("tag.dataset", "{name} dataset").replace("{name}", name)
        extra_tags.append(
            f'<li><a class="tag tag--artifact link-external"'
            f' href="{record["dataset"]}" target="_blank" rel="noopener">'
            f"{label}</a></li>"
        )
    parts = [
        f'<h3 class="entry__title">{title}</h3>',
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
        render_meta(record, "awards", extra=tuple(extra_tags)),
    ]
    # The framing sentences, in the slot DESIGN.md section 9 fixes for them:
    # what and when, then the scan line, then the framing, then the evidence.
    # This renderer was the only one of nine that skipped the rank, which is
    # why the hackathon's context had nowhere to go but into its bullets, and
    # then out of them when the bullets were sharpened.
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))

    body = "\n".join(indent(part, 2) for part in parts if part)
    award_id = record["id"]
    return entry_li(record, award_id, body)


# The scopes a result can reach, weakest first, which is also the order the
# strip reads in. Declared here rather than sorted out of the data, so a new
# scope value has to be placed deliberately instead of appearing wherever
# `sorted` happens to put it. The vocabulary is awards.md's, not a second one.
SCOPE_ORDER = ("Regional", "National", "African", "International")


def placement_rank(record: dict) -> tuple[int, int]:
    """Sort key for "which of these results was the best".

    An integer placement outranks a named stage, because 1st and 13th are
    comparable and "Quarter-finalist" is not comparable to either. Named
    stages keep the order the data gives them; there is one on the site today
    and inventing a ladder for a second would be inventing data.
    """
    placement = record.get("placement")
    if isinstance(placement, int):
        return (0, placement)
    return (1, 0)


def render_awards_summary(awards: list[dict]) -> str:
    """The Awards page's scope cards: the best result at every scope reached.

    A *projection*, in the sense home.md gives the word. Every string in it
    comes out of the same `meta_label` that renders the tags on the records
    below, read from the same fields, so a card cannot come to disagree with
    the entry it summarises. It writes no prose and holds no figure of its own.

    One card per scope, and one rule decides what the card shows:

      the best record carries a distinction   the distinction, counted when
                                              more than one record in the
                                              scope earned it
      it does not                             its placement and its field size

    That is what puts *2x National Finalist* on the National card rather than
    *13th Place*: two finals is the fact, and the placements are on the two
    records the card lists. It is also what keeps the International card
    honest at *643rd Place*, per CLAUDE.md section 5.

    **The card leads with the result, and holds nothing the record repeats.**
    It was a certifications card: a scope in the title slot, the winning
    record's own tag chips beneath it, and a `.points` list of the records. So
    the Regional card printed a gold disc, `1st Place` and `86 teams`, and the
    record 300px below printed a gold disc, `1st Place`, `Competitive
    Programming`, `Regional` and `86 teams`. Three of the card's four facts,
    in the same chips, in the same colours, inside one screen. A projection
    that is styled identically to its source does not read as a summary, it
    reads as the page saying everything twice.

    The fix is the one DESIGN.md section 9.3 made for Impact in Numbers, for
    the same reason: **put the figure in the slot the title had.** The scope
    was never the interesting half of a scope card, because the reader can see
    four cards and knows they are scopes; the result is. So the result carries
    title weight and the chips go entirely.

    **One fact per line, and that is a measurement rather than a preference.**
    The card ran two lines until the page context rail and the type scale
    caught up with it: at a 12rem track the text measure is 192px, and
    `643rd Place of 7,094 teams` needs about 215px at 17px, so the line broke
    wherever it landed and dropped `teams` on its own. French was worse, and
    the comment beside `.entries--grid--compact` in `main.css` had already
    recorded `Quart de finaliste sur 200 equipes` running 214px. A card whose
    whole job is to state one result cannot state it in orphans, so the
    sentence is now four short lines, each holding one fact: the scope, the
    result, the field size, the record.

    **The scope leads, and it is a label rather than a title.** It answers
    *which reach is this card* before the reader spends attention on the
    figure, and it is set at `.result__source`'s size and colour, so the 17px
    result underneath still carries every bit of the weight section 9.3 gave
    it. What was rejected above was a scope in the *title slot* with the
    result demoted to a chip, and that is not what a quiet label line above
    the figure does.

    The four classes are borrowed, not reinvented. `.result__figure` and
    `.result__source` mean *the figure* and *where this came from*, which is
    exactly what those two lines are; `.result__scope` and `.result__scale`
    extend the same component the way `.result__consequence` already does,
    which is to say Home uses some of it and this block uses the rest. Only
    `.result`'s two-column grid is Home's, and a grid property on a child of
    `.entries--grid > .entry` is inert, so nothing of that comes with them.

    **The medal disc is deliberately not here** and stays on the record. It
    exists to be recognised before the label is read (awards.md rule 4), which
    is worth a disc once and is a double-take twice.
    """
    cards = []
    for scope in SCOPE_ORDER:
        group = [a for a in awards if a.get("scope") == scope]
        if not group:
            continue
        best = min(group, key=placement_rank)
        distinction = best.get("distinction")
        scale = ""
        if distinction:
            cited = [a for a in group if a.get("distinction") == distinction]
            label = tr(f"tag.distinction.{distinction}", distinction)
            if len(cited) > 1:
                label = f"{len(cited)}&times; {label}"
            figure = f"<b>{label}</b>"
        else:
            cited = [best]
            # meta_label, not a format string: lesson 9 of the rework skill is
            # that a summary written through its own formatting is a summary
            # that drifts from the records it summarises, and this function is
            # where that was learned. The badge is discarded, nothing else is.
            _, label = meta_label("placement", best["placement"])
            figure = f"<b>{label}</b>"
            if best.get("scale"):
                _, size = meta_label("scale", best["scale"])
                scale = f'{tr("scale.of", "of")} {size}'
        records = f' {SEPARATOR} '.join(
            f'<a href="#{record["id"]}">'
            f'{t(record, "short") or t(record, "title")}</a>'
            for record in cited
        )
        scope_label = tr(f"tag.scope.{scope}", scope)
        # One fact per line, in reading order: which reach, what result, at
        # what field size, and where to check it. A card with no `scale`
        # renders three lines rather than four, which is rule 5 again: the
        # National card states two finals and there is no field size that
        # belongs to both records, so none is invented to square the shape.
        parts = [f'<p class="result__scope">{scope_label}</p>']
        parts.append(f'<p class="result__figure">{figure}</p>')
        if scale:
            parts.append(f'<p class="result__scale">{scale}</p>')
        parts.append(f'<p class="result__source">{records}</p>')
        cards.append(
            '<li class="entry">\n'
            + "\n".join(indent(part, 2) for part in parts)
            + "\n</li>"
        )
    return "\n".join(cards)


# The two sections on Workshops, and the only values `block` may take. Held
# here rather than in the fragment because the fragment places a rendered
# block by name and cannot see a record that reached neither.
WORKSHOP_BLOCKS = ("hardware", "algorithms")


def check_workshop_block(record: dict) -> None:
    """Every workshop names the section it renders in, or it renders nowhere.

    The page is two blocks filtered on `block`, so a record that omits the
    field or misspells it is not a record with a missing tag: it is a record
    that quietly leaves the site. Nothing downstream would have said so. The
    entry ids stay valid, `check.py` finds no dead link because nothing links
    to it, and the page simply comes back one workshop shorter.

    workshops.md carries which subject belongs in which block. The values live
    in WORKSHOP_BLOCKS above and never render, which is why they are not in
    that document's vocabulary tables.
    """
    if record.get("block") not in WORKSHOP_BLOCKS:
        raise ValueError(
            f'{record["id"]}: a workshop needs `block` set to one of '
            + " or ".join(repr(name) for name in WORKSHOP_BLOCKS)
            + f', not {record.get("block")!r}. The page filters its two '
            "sections on this field, so a record without it renders on no "
            "page at all. workshops.md, the page structure."
        )


def render_workshop(record: dict) -> str:
    """One workshop as the site-wide .entry record.

    Two things sit deliberately outside the metadata model. A repository link
    belongs to the title, because it points at the thing the title names. And
    a slide deck is an artefact, not a dimension of the session, so it renders
    as a utility tag appended after the model's four.
    """
    title = t(record, "title")
    if record.get("repo"):
        name = tr("link.workshop_repo", "Workshop materials on GitHub")
        github_icon = asset("images/icons/github.svg")
        title += (
            f'\n  <a class="icon-link" href="{record["repo"]}" target="_blank"'
            f' rel="noopener" title="{name}">'
            f'<img class="{icon_classes("github.svg", "sm")}"'
            f' src="{github_icon}" alt="{name}"'
            f' width="15" height="15"></a>\n'
        )

    extra = ()
    slides_icon = asset("images/icons/powerpoint.svg")
    if record.get("slides"):
        extra = (
            f'<li><a class="tag tag--artifact link-external" href="{record["slides"]}"'
            f' target="_blank" rel="noopener" title="View slides in PowerPoint Online">'
            f'<img class="icon icon--xs" src="{slides_icon}" alt=""'
            f' width="12" height="12">Slides (.pptx)</a></li>',
        )

    year = record["year"]
    parts = [
        f'<h3 class="entry__title">{title}</h3>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "workshops", extra),
    ]
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))
    # A session delivered in parts renders them as `.entry__group`, the same
    # shape Career gives a role's workstreams and Teaching gives a module. The
    # three bullets this replaced carried the structure inside their own text
    # (`<b>Part 1.a: Efficient data &amp; code execution:</b> ...`), so one
    # bullet held two bold spans and two colons, and the record was flat while
    # its own prose said it was not. The group title states the part; the
    # bullet keeps `<b>` for its topic, which is the one job that device has.
    for group in t(record, "groups", []) or []:
        parts.append(render_group(group["title"], group["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    ws_id = record["id"]
    return entry_li(record, ws_id, body)


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


def render_publication(record: dict, site: dict = None) -> str:
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

    title = t(record, "title")
    if link:
        title = (
            f'<a class="link-external" href="{link}" target="_blank"'
            f' rel="noopener">{title}</a>'
        )

    parts = [f'<h3 class="entry__title">{title}</h3>']

    if record.get("year"):
        year = record["year"]
        parts.append(f'<p class="entry__period"><time datetime="{year}">{year}</time></p>')
    else:
        # The dateline says *when*, and only when. It read "In progress (as of
        # August 2026)" while the `status` chip 40px below it read "In
        # Progress": one fact in two slots, in two capitalisations. The chip is
        # the model's declared home for a status (MODELS["research"]), so the
        # dateline keeps the half no chip carries, which is the same half every
        # other record puts here: a time. A published paper's dateline is
        # `2025`; an unpublished one's is the date this claim was last true.
        as_of = site.get("last_updated", "August 2026") if site else "August 2026"
        stamp = tr("research.as_of", f"as of {as_of}")
        parts.append(f'<p class="entry__period">{stamp}</p>')

    citation = render_authors(record["authors"])
    if t(record, "venue"):
        # The citation line is where a reader looks for *where this came out*,
        # so a bare "Authors &middot; <i>Journal</i>" asserts publication by
        # convention alone. On an unpublished record that is the same slot,
        # the same italics and the same journal as the published paper above
        # it, with only a chip 40px below to say otherwise. The journal is
        # still worth carrying (the target says something about the work), so
        # the fix is the verb, not the deletion: submitted, not published.
        # Derived from `status` rather than typed beside it, for the reason
        # `authorship` is (research.md): two fields that can disagree will.
        if record.get("status") in PENDING_STATUS:
            lead = tr("research.submitted_to", "Submitted to")
            citation += f' &middot; {lead} <i>{t(record, "venue")}</i>'
        else:
            citation += f' &middot; <i>{t(record, "venue")}</i>'
    parts.append(f'<p class="entry__meta">{citation}</p>')

    extra_tags = []
    if record.get("dataset"):
        d_url = record["dataset"]
        d_label = record.get("dataset_label", "Dataset")
        extra_tags.append(
            f'<li><a class="tag tag--artifact link-external" href="{d_url}"'
            f' target="_blank" rel="noopener">Dataset ({d_label})</a></li>'
        )

    position = author_position(record)
    parts.append(render_meta({**record, "authorship": position} if position else record,
                             "research", extra=tuple(extra_tags)))

    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))

    body = "\n".join(indent(part, 2) for part in parts if part)
    pub_id = record["id"]
    return entry_li(record, pub_id, body)


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
    title = t(record, "title")
    if record.get("url"):
        title = (
            f'<a class="link-external" href="{record["url"]}" target="_blank"'
            f' rel="noopener">{title}</a>'
        )

    check_reach(record)
    year = record["year"]
    parts = [
        f'<h3 class="entry__title">{title}</h3>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "writing"),
    ]
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))

    body = "\n".join(indent(part, 2) for part in parts if part)
    art_id = record["id"]
    return entry_li(record, art_id, body)


def reach_note(articles: list[dict]) -> str:
    """The provenance line under Technical Articles: when the figures were read.

    [`writing.md`](writing.md) has always carried this rule: the reach figures
    are copied by hand from Medium's stats page, nothing keeps them current,
    and **the figures and their date move together or neither moves**. A stale
    number that says when it was read stays honest as it ages; a stale number
    that says nothing starts lying the moment it drifts.

    The rule was written, the `.block__note` component was designed and styled
    for it, and neither was ever built. Two hand-copied figures shipped undated
    for as long as the page has existed, one of them quoted on Home as a skill
    citation, on a site whose third reader checks. The rule is now a build
    error rather than a paragraph: `check_reach` refuses a `reach` with no
    `as_of`, so a figure cannot be refreshed without its date, or dated without
    being refreshed, because both live in the same object.

    One note for the block, not one date per record. The date belongs to the
    reading, and the records were read in one sitting; per-record dates would
    invite exactly the drift of a fresh date over a stale number that the rule
    forbids. Where the records disagree, the note says the oldest, because that
    is the date the whole block can be trusted to.
    """
    stamps = sorted({a["reach"]["as_of"] for a in articles if a.get("reach")})
    if not stamps:
        return ""
    when = month_year(stamps[0])
    pattern = tr("writing.reach_note", "Reach figures read from Medium, {when}.")
    return f'<p class="block__note">{pattern.replace("{when}", when)}</p>'


def check_reach(record: dict) -> None:
    """A hand-copied figure says when it was copied, or it is not shown."""
    reach = record.get("reach")
    if reach and not reach.get("as_of"):
        raise ValueError(
            f'{record["id"]}: `reach` needs an `as_of` (YYYY-MM). A figure read '
            "by hand from a stats page and shown undated starts lying the "
            "moment it drifts, and nothing here refreshes it. writing.md, "
            "Refreshing the figures."
        )


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
    title = t(record, "title")
    if record.get("repo"):
        name = tr("link.repo", "GitHub repository")
        github_icon = asset("images/icons/github.svg")
        title += (
            f'\n  <a class="icon-link" href="{record["repo"]}" target="_blank"'
            f' rel="noopener" title="{name}">'
            f'<img class="{icon_classes("github.svg", "sm")}"'
            f' src="{github_icon}" alt="{name}"'
            f' width="15" height="15"></a>\n'
        )

    extra_head = []
    extra_tail = []
    if record.get("demo"):
        demo = record["demo"]
        demo_url = demo["url"] if isinstance(demo, dict) else demo
        demo_label = demo.get("label", "Live Demo on Hugging Face") if isinstance(demo, dict) else "Live Demo on Hugging Face"
        extra_head.append(
            f'<li><a class="tag tag--demo link-external" href="{demo_url}"'
            f' target="_blank" rel="noopener">{demo_label}</a></li>'
        )
    if record.get("slides"):
        extra_tail.append(
            f'<li><a class="tag tag--artifact link-external" href="{record["slides"]}"'
            f' target="_blank" rel="noopener" title="View slides in PowerPoint Online">Slides (.pptx)</a></li>'
        )
    if record.get("article"):
        article = articles[record["article"]]
        extra_tail.append(
            f'<li><a class="tag tag--article link-external" href="{article["url"]}"'
            f' target="_blank" rel="noopener">Article on {article["platform"]}</a></li>'
        )

    year = record["year"]
    parts = [
        f'<h3 class="entry__title">{title}</h3>',
        f'<p class="entry__period"><time datetime="{year}">{year}</time></p>',
        render_meta(record, "projects", extra=tuple(extra_tail), extra_head=tuple(extra_head)),
    ]
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))

    body = "\n".join(indent(part, 2) for part in parts if part)
    proj_id = record["id"]
    return entry_li(record, proj_id, body)


def course_sort_key(record: dict) -> tuple[int, int]:
    """Newest first, by academic year then by term within it."""
    return (record["year"], TERM_ORDER[record["term"]])


def render_course(record: dict) -> str:
    """One taught course as the site-wide .entry record."""
    # Slugged from the English title, via the id with_ids already stamped, and
    # never from t(): a French page slugging a French title would produce a
    # different anchor for the same course, breaking every citation that points
    # at it and the anchor parity check_fragment_parity enforces.
    course_id = record["id"]
    course_slug = course_id[len("course-"):]
    year, term = record["year"], record["term"]
    period = f"{term} {year}-{year + 1}"

    parts = [
        f'<h3 class="entry__title">{t(record, "title")}</h3>',
        f'<p class="entry__period">{period}</p>',
        render_meta(record, "teaching"),
    ]
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')

    for number, module in enumerate(t(record, "syllabus", []) or [], start=1):
        mod_id = f"{course_slug}-m{number}"
        parts.append(render_group(f'{tr("course.module", "Module")} {number}{tr("punct.colon", ": ")}{module["title"]}',
                                  module["points"], group_id=mod_id))
        homework = module.get("homework")
        if homework:
            hw_id = f"{course_slug}-m{number}-hw"
            parts.append(render_group(
                f'{tr("course.module", "Module")} {number}'
                f' {tr("course.homework", "Homework")}'
                f'{tr("punct.colon", ": ")}{homework["title"]}',
                homework["points"],
                modifier="entry__group--homework",
                group_id=hw_id))

    capstone = t(record, "capstone")
    if capstone:
        cap_id = f"{course_slug}-project"
        parts.append(render_group(
            f'{tr("course.capstone", "Final Project")}{tr("punct.colon", ": ")}{capstone["title"]}',
                                  capstone["points"],
                                  modifier="entry__group--capstone",
                                  group_id=cap_id))

    body = "\n".join(indent(part, 2) for part in parts if part)
    return entry_li(record, course_id, body)


# --- career -----------------------------------------------------------------

# Months are abbreviated here and never in the data, so a record cannot be
# stored as "Aug 2024" in one row and "August 2024" in the next: awards.md
# rule 7, the same mechanism that turns `1` into `1st Place`.
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

# A role with no end date is the one being held now. The word is produced by
# the renderer rather than typed into `end`, because "Present" is not a date
# and storing it as one is how a leaver's record keeps claiming a job.
ONGOING_EN = "Present"


def month_year(value: str) -> str:
    """Render a stored "YYYY-MM" as "Aug 2024"."""
    year, month = value.split("-")
    return f"{tr(f'month.{month}', MONTHS[int(month) - 1])} {year}"


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
    # Plurals are per language, not a trailing "s": French pluralises "ans"
    # but not "mois", so each locale supplies both forms rather than a rule.
    if years:
        parts.append(f"{years} " + tr("unit.year" if years == 1 else "unit.years",
                                      "year" if years == 1 else "years"))
    if rest:
        parts.append(f"{rest} " + tr("unit.month" if rest == 1 else "unit.months",
                                     "month" if rest == 1 else "months"))
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
    end = month_year(role["end"]) if role.get("end") else tr("date.present", ONGOING_EN)
    period = (f'{month_year(role["start"])} - {end}'
              f' ({tenure(role["start"], role.get("end"))})')

    dateline = []
    if role.get("location"):
        dateline.append(f'<span class="entry__location">{role["location"]}</span>')
    dateline.append(period)

    parts = [
        (f'<h4 class="entry__group-title">\n'
         f'  <span class="entry__subrole">{t(role, "role")}</span>\n'
         '</h4>'),
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
        render_meta(role, "experience"),
    ]
    if role.get("points"):
        parts.append(render_points(role["points"]))
    for group in t(role, "groups", []) or []:
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

    end = month_year(record["end"]) if record.get("end") else tr("date.present", ONGOING_EN)
    period = (f'{month_year(record["start"])} - {end}'
              f' ({tenure(record["start"], record.get("end"))})')

    title_parts = []
    if record.get("role"):
        title_parts.append(f'<span class="entry__role">{record["role"]}</span>')
    title_parts.append(f'<span class="entry__company">{company}</span>')

    dateline = []
    if t(record, "location"):
        dateline.append(f'<span class="entry__location">{t(record, "location")}</span>')
    dateline.append(period)

    parts = [
        f'<h3 class="entry__title">\n  {" &middot; ".join(title_parts)}\n</h3>',
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
    ]
    meta = render_meta(record, "experience")
    if meta:
        parts.append(meta)
    # Two facts with two different jobs, and they used to share one paragraph.
    # `context` says what this place is, `summary` says what was owned inside
    # it, and the company half ran 44 to 61 words in front of the first-person
    # clause on every record: a recruiter scanning "what did *you* do" read
    # employer boilerplate three times, in the highest-value scan positions of
    # the site's most important page. Splitting the field lets typography sort
    # them, so the context is furniture and the ownership is body copy. The
    # order is unchanged: a reader who wants the company still meets it first.
    if t(record, "context"):
        parts.append(f'<p class="entry__context">{t(record, "context")}</p>')
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))
    for group in t(record, "groups", []) or []:
        parts.append(render_group(group["title"], group["points"]))
    roles = t(record, "roles", []) or []
    if roles:
        # One wrapper, so the connector down the left is a single unbroken line
        # rather than one detached segment per role. The wrapper is what says
        # "these belong to the company above"; a per-role border could not.
        nested = "\n".join(indent(render_experience_role(r), 2) for r in roles)
        parts.append(f'<div class="entry__roles">\n{nested}\n</div>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    exp_id = record["id"]
    return entry_li(record, exp_id, body)


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
    if t(record, "location"):
        dateline.append(f'<span class="entry__location">{t(record, "location")}</span>')
    # The same parenthetical the jobs above carry, from the same reasoning:
    # a reader should not have to subtract. Education stores plain years, so
    # the span is the difference between them and no month arithmetic applies.
    years = record["end"] - record["start"]
    length = f"{years} year" + ("s" if years > 1 else "")
    dateline.append(f'{record["start"]}-{record["end"]} ({length})')

    parts = [
        f'<h3 class="entry__title">\n  {t(record, "degree")}\n'
        f'  <span class="entry__role">&middot; {institution}</span>\n</h3>',
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
        render_meta(record, "education"),
    ]
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))
    for group in t(record, "groups", []) or []:
        parts.append(render_group(group["title"], group["points"]))

    body = "\n".join(indent(part, 2) for part in parts if part)
    edu_id = record["id"]
    return entry_li(record, edu_id, body)


def render_credentials(record: dict, field: str, prefix: str) -> str:
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

    **Both levels carry an anchor, and that is what Home's evidence chips
    needed.** The block was the only thing addressable here, so eleven chips
    on Home saying `Talend Data Integration`, `MuleSoft Developer L1`,
    `Datadog &times;3` and so on all landed on the same heading and left the
    reader to find which row they meant. The group id serves a chip that
    counts (`Datadog &times;3` wants the Datadog group); the credential id
    serves a chip that names one certificate. A chip that cannot be checked in
    one move is a chip taken on trust, which is the one thing skills.md builds
    this block to avoid.
    """
    icon = asset(f'images/icons/{record["icon"]}')
    group_id = f'{prefix}-{slugify(record[field])}'
    heading = (
        '<h3 class="issuer">\n'
        f'  <img class="{icon_classes(record["icon"], "md")}"'
        f' src="{icon}" alt="" width="18" height="18">\n'
        f'  {record[field]}\n'
        "</h3>"
    )

    items = []
    for credential in record["credentials"]:
        # Online courses are not cited from anywhere, so they carry the group
        # anchor and no row of their own. Certifications are cited by name.
        row_id = f' id="{prefix}-{credential["id"]}"' if credential.get("id") else ""
        items.append(
            f'  <li{row_id}><a class="link-external" href="{asset(credential["url"])}"'
            f' target="_blank" rel="noopener">{credential["name"]}</a></li>'
        )
    body = "\n".join(items)

    parts = [heading, f'<ul class="points">\n{body}\n</ul>']
    return (f'<li class="entry" id="{group_id}" data-toc-skip>\n'
            + "\n".join(indent(p, 2) for p in parts) + "\n</li>")


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
        # Each issuer to its own group, not all five to the block heading.
        # Five links whose text differs and whose destination does not is a
        # promise of precision the page then fails to keep, and it was the
        # first screen of the site making it.
        anchor = f'cert-{slugify(record["issuer"])}'
        links.append(
            f'<a href="career.html#{anchor}">{record["issuer"]}{suffix}</a>'
        )
    return (
        '<div class="hero-facts__row">\n'
        f'  <dt>{tr("facts.certified", "Certified")}</dt>\n'
        f'  <dd>{" &middot; ".join(links)}</dd>\n'
        "</div>"
    )


def proof_link(item: dict) -> str:
    """One language-proof link. The label translates by value, the href does not.

    `evidence` on a language record is a structure of addresses, not prose, so
    it is not routed through the record overlay: translating a block of links
    wholesale is how an href gets edited by someone editing a sentence. The
    visible half is translated on its own, by value, the way the tag vocabulary
    is: one entry does every record that says the same thing.
    """
    label = tr(f"proof.{item['text']}", item["text"])
    return f'<a href="{item["href"]}">{label}</a>'


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
                proof_link(item) for item in record["evidence"]
            )
            proof = f'\n    <span class="hero-facts__proof">{links}</span>'
        rows.append(
            '  <div class="hero-facts__lang">\n'
            f'    <dt>{t(record, "name")}</dt>\n'
            f'    <dd>{t(record, "level")}{proof}</dd>\n'
            "  </div>"
        )
    body = "\n".join(rows)
    return (
        '<div class="hero-facts__row">\n'
        f'  <dt>{tr("facts.languages", "Languages")}</dt>\n'
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

    end = month_year(record["end"]) if record.get("end") else tr("date.present", ONGOING_EN)
    period = (f'{month_year(record["start"])} - {end}'
              f' ({tenure(record["start"], record.get("end"))})')

    title_parts = []
    if record.get("role"):
        title_parts.append(f'<span class="entry__role">{record["role"]}</span>')
    title_parts.append(f'<span class="entry__company">{company}</span>')

    dateline = []
    if t(record, "location"):
        dateline.append(f'<span class="entry__location">{t(record, "location")}</span>')
    dateline.append(period)

    parts = [
        f'<h3 class="entry__title">\n  {" &middot; ".join(title_parts)}\n</h3>',
        f'<p class="entry__period">{" &middot; ".join(dateline)}</p>',
        render_meta(record, "experience"),
    ]
    if t(record, "home_summary"):
        parts.append(f'<p class="entry__summary">{t(record, "home_summary")}</p>')

    body = "\n".join(indent(part, 2) for part in parts if part)
    return f'<li class="entry">\n{body}\n</li>'


def cite_index(sources: dict[str, list[dict]]) -> dict[str, dict]:
    """Every bullet that carries an `id`, with the record and page it lives on.

    Built so Home's Selected Impact can *cite* a bullet rather than paraphrase
    it. The block used to hold a hand-written sentence beside a hand-written
    figure, both restating a bullet that already existed in `experience.json`,
    which is two copies of one fact kept in agreement by a person. home.md
    records the two occasions that failed.

    An id is added to a bullet only when Home cites it, so the index is a
    handful of entries rather than every bullet on the site: an anchor nothing
    points at is a URL promise the author did not mean to make.

    **`sources` maps a page to the records on it, and this used to be the
    single argument `experience`.** The docstring above says "the page it lives
    on" and there was only ever one: the index walked `experience.json` alone
    and `render_impact` hardcoded `career.html`. A bullet on Projects, Teaching
    or Research could not be cited at all, which is why the open-source result
    needed a second code path (`upstream_prs`) with a hand-written `evidence`
    string, and why it renders a status where its four neighbours render a
    company. One page's worth of citation machinery produced an exception that
    looked like a design decision.
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
        walk(t(record, "points", []) or [], owner)
        for group in t(record, "groups", []) or []:
            walk(group["points"], owner)

    for page, records in sources.items():
        for record in records:
            scan(record, {**record, "page": page})
            for role in t(record, "roles", []) or []:
                # A sub-role inherits its company from the record above it, and
                # keeps its own dates: OEM's two roles ran in different summers.
                scan(role, {**record, **role, "page": page})
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
    needle = t(record, "figure")["value"].lower()
    if not any(needle in source.lower() for source in sources):
        raise ValueError(
            f'{t(record, "title")}: figure "{t(record, "figure")["value"]}" does not '
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
    figure = t(record, "figure")
    lead = f'<b>{figure["value"]}</b> {figure["unit"]}'

    if record.get("cite"):
        if t(record, "evidence") or record.get("source"):
            raise ValueError(
                f'{t(record, "title")}: `cite` derives the sentence and the source, '
                "so writing `evidence` or `source` beside it invites the two to "
                "disagree, which is the whole reason `cite` exists."
            )
        citation = citations[record["cite"]]
        point, owner = citation["point"], citation["owner"]
        sentence = point.get("impact") or point["point"]
        check_figure(record, point["point"], point.get("impact", ""))
        # The page comes from wherever cite_index found the id, never from a
        # constant here. It was `career.html`, hardcoded twice, which is what
        # confined the whole mechanism to one page.
        page = owner["page"]
        context = owner.get("company") or owner.get("host") or owner["title"]
        href = f'{page}#{record["cite"]}'
        label = page_labels[page]
    else:
        if not record.get("upstream_prs"):
            raise ValueError(
                f'{t(record, "title")}: an impact record cites a bullet with `cite`, '
                "or aggregates project records with `upstream_prs`. There is no "
                "third kind."
            )
        sentence = t(record, "evidence")
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


def volunteering_sort_key(record: dict) -> str:
    """Newest first; a record with no year yet sorts last.

    The same rule publication_sort_key uses, for the same reason: nothing is
    invented to make a record sortable. The Red Crescent record is undated
    because nobody has supplied the months, not because it is oldest, and
    guessing a year to place it correctly would be guessing.
    """
    return str(record.get("year") or "")


def render_volunteering(record: dict) -> str:
    """One volunteering record as the site-wide .entry component.

    **No metadata model.** A chip row reading "Crisis relief" over pandemic aid
    distribution reads as credential-farming, which is the one register this
    block cannot afford. career.md section 8 carries the argument. Two records
    were the stated condition for reopening the question; the pair arrived, the
    question was asked, and the answer held.

    **`initiative` is what the pair actually revealed.** Both records happened
    under a named programme, "COVID-19 response" and "Orientini", and there was
    nowhere to put it: the first record had been keeping its programme name in
    `period`, which is why that field held a topic instead of a date. It
    renders on the dateline joined to the year with a middot, the same shape
    render_experience uses for `Location &middot; Period`, so it needs no
    component and no new rule in main.css.

    **One record per edition**, which is how Awards already holds TCPC 22 and
    TCPC 23, and Hello World v2.0 through v4.0. A single record spanning two
    editions would not sort and would say less about either.

    A record with neither `year` nor `start` renders no dateline at all rather
    than an empty one: awards.md rule 5, missing data is omitted.
    """
    organisation = t(record, "organisation")
    if record.get("url"):
        organisation = (
            f'<a class="link-external" href="{record["url"]}" target="_blank"'
            f' rel="noopener">{organisation}</a>'
        )
    title = organisation
    if record.get("branch"):
        title += f' <span class="entry__role">&middot; {t(record, "branch")}</span>'

    dateline = []
    if t(record, "location"):
        dateline.append(f'<span class="entry__location">{t(record, "location")}</span>')
    if record.get("initiative"):
        dateline.append(t(record, "initiative"))
    if record.get("start"):
        start_str = month_year(record["start"])
        if record.get("end"):
            if record["start"] == record["end"]:
                range_str = start_str
            else:
                range_str = f'{start_str} - {month_year(record["end"])}'
        else:
            range_str = f'{start_str} - {tr("date.present", ONGOING_EN)}'
        dateline.append(f'{range_str} ({tenure(record["start"], record.get("end"))})')
    elif record.get("year"):
        year = record["year"]
        dateline.append(f'<time datetime="{year}">{year}</time>')

    parts = [f'<h3 class="entry__title">{title}</h3>']
    if dateline:
        parts.append(f'<p class="entry__period">{" &middot; ".join(dateline)}</p>')
    if t(record, "summary"):
        parts.append(f'<p class="entry__summary">{t(record, "summary")}</p>')
    if t(record, "points"):
        parts.append(render_points(t(record, "points")))

    body = "\n".join(indent(part, 2) for part in parts)
    return entry_li(record, record["id"], body)


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
        for kind, label in ((k, tr(f"proof_key.{k}", v)) for k, v in PROOF_KEY.items())
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

    # Standing reads the English evidence, the chips read the locale's. The
    # split is deliberate: `standing()` answers *which kinds of proof exist*,
    # which is a fact about the career and identical in every language, while
    # the chip is prose naming the record a reader will land on. Computing the
    # standing from the overlay would let a translator who dropped a chip
    # silently demote the row.
    #
    # The chips went through `record["evidence"]` until this comment existed,
    # which is the failure CLAUDE.md section 9 lists as build-refused: a field
    # a renderer reads directly instead of through `t()` is never reported
    # missing, so all 39 chips rendered English on the French page while the
    # coverage figure counted them as fine. Every user-visible string here
    # routes through `t()` now, and an untranslated `evidence` shows up in the
    # build's missing list like everything else.
    localised = t(record, "evidence") or evidence

    tools = "\n".join(
        f'  <li class="tag tag--stack">{tool}</li>' for tool in record["tools"]
    )
    chips = []
    for kind in PROOF:
        for item in localised.get(kind, []):
            chips.append(
                f'  <li><a class="tag tag--{kind}" href="{item["href"]}">'
                f'{item["text"]}</a></li>'
            )

    head = (
        '<div class="skill__head">\n'
        f'  <h3 class="skill__name">{t(record, "name")}</h3>\n'
        f'  <p class="skill__standing">{tr(f"standing.{standing(evidence)}", standing(evidence))}</p>\n'
        "</div>"
    )
    proof = (
        '<div class="skill__proof">\n'
        f'  <ul class="tag-list skill__tools" aria-label="{tr("label.tools", TOOLS_LABEL_EN)}">\n'
        + "\n".join("  " + line for line in tools.splitlines())
        + "\n  </ul>\n"
        f'  <ul class="tag-list" aria-label="{tr("label.evidence", PROOF_LABEL_EN)}">\n'
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


def render_contact_channels(site: dict) -> str:
    """The addresses, and where the author is, from src/site.json.

    Typed into the fragment until now, while `site.json` held its own copies
    for the JSON-LD. Two sources, no guard, and they had already drifted: the
    data said `Email` / `University` / `Phone` and the page said `Primary
    email` / `Academic email` / `Phone / WhatsApp`. The structured data a search
    engine reads and the text a person reads came from different places, which
    is the shape of every other bug this build has guards for, sitting on the
    one page with no model document.

    The `Based in` row joins two owned strings and edits neither.
    [`CLAUDE.md`](CLAUDE.md) §4 forbids paraphrasing a residence status, so the
    joining is punctuation: `location`, a full stop, `availability` verbatim,
    exactly as Home's hero renders it.
    """
    rows = []
    for entry in site["contact"]:
        label = tr(f"contact.{slugify(entry['label'])}", entry["label"])
        rows.append(
            '<li class="contact-list__item">\n'
            f'  <a class="contact-list__link" href="{entry["href"]}">\n'
            f'    <span class="contact-list__label">{label}</span>\n'
            f'    <span class="contact-list__value">{entry["text"]}</span>\n'
            "  </a>\n"
            "</li>"
        )
    return "\n".join(rows)


def render_contact_facts(site: dict) -> str:
    """Availability and location, in Contact's page header.

    **They are page-level facts and they were sitting in a channel list.**
    `Contact Details` answers *how do I reach you*, and neither of these is a
    way of reaching anyone: one is a residence status and the other is a city.
    A reader scanning a list of addresses met a sentence about EU work
    authorisation in the middle of it.

    They have now been three arrangements, and the history is the argument for
    this one. First two rows with `Location` above `Availability`, which handed
    a recruiter the disqualifying half first: the silent filter CLAUDE.md
    section 4 exists to prevent, produced by the page meant to prevent it. Then
    one merged row, which fixed the ordering and cost the sentence its own
    line, where it read as a tail on a city. Then two rows again, reordered,
    which fixed both and left them in the wrong section.

    The header is where a fact about the page rather than about a row belongs.
    DESIGN.md section 9 already permits a `.page-header` to carry a title and a
    summary grid, which is the slot Awards fills, and this is the same idea one
    component along.

    `.hero-facts` is reused rather than reinvented. It is the label column Home
    renders this exact sentence in, so a reader who saw it there meets the same
    shape here, and DESIGN.md section 11 asks a fifth label-column case to use
    the idiom rather than invent a sixth. Nothing in its stylesheet was ever
    coupled to the hero: only the section header claimed so, and that comment
    is corrected.

    Both strings render verbatim from `src/site.json`. Section 4 forbids
    paraphrasing a residence status, and the reason the site once carried three
    wordings is that three places each held a copy.
    """
    rows = []
    for key, label, value in (
        ("contact.availability", "Availability", site["availability"]),
        ("contact.based-in", "Based in", site["location"]),
    ):
        rows.append(
            '<div class="hero-facts__row">\n'
            f'  <dt>{tr(key, label)}</dt>\n'
            f'  <dd>{value}</dd>\n'
            "</div>"
        )
    body = "\n".join(indent(row, 2) for row in rows)
    return '<dl class="hero-facts">\n' + body + '\n</dl>' 


def render_contact_socials(site: dict) -> str:
    """The same list the JSON-LD `sameAs` is built from, rendered for a human."""
    rows = []
    for entry in site["socials"]:
        rows.append(
            '<li class="contact-list__item">\n'
            f'  <a class="contact-list__link" href="{entry["href"]}"'
            ' target="_blank" rel="noopener">\n'
            f'    <span class="contact-list__label">{entry["name"]}</span>\n'
            f'    <span class="contact-list__value">{entry["handle"]}</span>\n'
            "  </a>\n"
            "</li>"
        )
    return "\n".join(rows)


def image_size(path: Path) -> tuple[int, int]:
    """The intrinsic pixel size of a JPEG or PNG, read from the file itself.

    For `og:image:width` and `og:image:height`. A crawler that is given them
    can lay the card out on its first pass instead of deferring until it has
    fetched and decoded the image, and several never come back for the second
    pass. Without them the portrait card renders inconsistently across LinkedIn,
    Slack and X.

    Measured rather than declared. Two integers typed into `site.json` would be
    a hand-copied fact about a file sitting next to the file, which is the
    drift surface this build removes everywhere else: crop the portrait and the
    numbers would quietly start lying, with nothing to catch it.
    """
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        index = 2
        while index < len(data) - 9:
            if data[index] != 0xFF:
                break
            marker = data[index + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3):
                height, width = struct.unpack(">HH", data[index + 5:index + 9])
                return width, height
            index += 2 + struct.unpack(">H", data[index + 2:index + 4])[0]
    raise ValueError(f"{path}: could not read intrinsic size")


# --- architecture diagrams ---------------------------------------------------

# One layered diagram, drawn at build time as inline SVG.
#
# CLAUDE.md M1 asks for at least one real architecture diagram and says, in
# those words, do not auto-generate this content. So this is the container and
# never the content: the author writes nodes and edges as facts, and the build
# does arithmetic. Nothing here infers what connects to what.
#
# Inline SVG rather than a library, for the reasons DESIGN.md Principle 1 gives.
# Mermaid would need roughly 100KB of JavaScript on every page carrying a
# diagram, would render nothing where scripts are blocked, and would print as an
# empty box, on a site whose whole argument is that the page is a document. The
# cost of drawing it here is one layout function.
#
# Every measurement is in user units and the whole thing scales through the
# viewBox, so there is one geometry and no breakpoints.
NODE_W, NODE_H = 148, 52       # a box
GAP_X, GAP_Y = 64, 22          # between columns, between boxes in a column
PAD = 12                       # around the drawing
LANE_H = 22                    # the layer label strip above the boxes
CHAR_W = 6.6                   # 11px Noto Sans, measured on the widest lowercase
LINE_H = 13


def wrap_label(text: str, width: int) -> list[str]:
    """Break a node label into lines that fit NODE_W.

    SVG text does not wrap, so a label either fits or runs out of its box. The
    break is on words and never mid-word: a diagram that hyphenates a service
    name has made the name harder to recognise than the overflow would have.
    """
    words, lines, line = text.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) * CHAR_W <= width - 16 or not line:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines[:3]


def render_diagram(spec: dict) -> str:
    """One architecture diagram as inline, script-free, theme-aware SVG.

    Layered left to right: every layer is a column, every node a box in it,
    every edge a line from one box's right edge to another's left. The author
    declares the layers and the edges; the positions are computed here.

    **Theme-aware without a second palette.** Strokes and text use
    `currentColor`, so the diagram inherits whatever the page's colour is in
    light, dark and print alike. There is no fill on a node except the surface
    token, and the print stylesheet turns the ink black the same way it does
    for everything else. A diagram that needed its own dark palette would be a
    second design system.

    **Readable without seeing it.** `role="img"` with a `<title>` and a `<desc>`
    the author writes, so a screen reader gets the architecture as a sentence
    rather than as a list of disconnected box labels. The `<desc>` is required:
    a diagram nobody can read is decoration, and DESIGN.md Principle 1 does not
    admit decoration.
    """
    # Every user-visible string here goes through `t()`. A diagram is drawn
    # once per locale (page_blocks is re-rendered per language), so reading
    # `spec["title"]` directly would put English lane labels and English box
    # text inside a French page and report nothing missing, which is the
    # failure CLAUDE.md section 9 lists and which render_skill had shipped.
    # `edges` never translates: those are node ids, not prose.
    layers = t(spec, "layers")
    rows = max(len(layer["nodes"]) for layer in layers)
    width = PAD * 2 + len(layers) * NODE_W + (len(layers) - 1) * GAP_X
    height = PAD * 2 + LANE_H + rows * NODE_H + (rows - 1) * GAP_Y

    place, boxes, labels = {}, [], []
    for column, layer in enumerate(layers):
        x = PAD + column * (NODE_W + GAP_X)
        labels.append(
            f'<text class="diagram__lane" x="{x + NODE_W / 2:.0f}" y="{PAD + 10}"'
            f' text-anchor="middle">{layer["label"]}</text>')
        # A short column is centred against the tallest, so a three-box lane
        # beside a one-box lane reads as one flow rather than as a ragged edge.
        offset = (rows - len(layer["nodes"])) * (NODE_H + GAP_Y) / 2
        for row, node in enumerate(layer["nodes"]):
            y = PAD + LANE_H + offset + row * (NODE_H + GAP_Y)
            place[node["id"]] = (x, y)
            lines = wrap_label(node["label"], NODE_W)
            start = y + NODE_H / 2 - (len(lines) - 1) * LINE_H / 2 + 4
            spans = "".join(
                f'<tspan x="{x + NODE_W / 2:.0f}" y="{start + i * LINE_H:.0f}">{line}</tspan>'
                for i, line in enumerate(lines))
            boxes.append(
                f'<g class="diagram__node">'
                f'<rect x="{x}" y="{y:.0f}" width="{NODE_W}" height="{NODE_H}" rx="4"/>'
                f'<text text-anchor="middle">{spans}</text></g>')

    edges = []
    for source, target in spec["edges"]:
        if source not in place or target not in place:
            raise ValueError(
                f'{spec["id"]}: edge {source} -> {target} names a node the '
                "diagram does not declare.")
        x1, y1 = place[source]
        x2, y2 = place[target]
        sx, sy = x1 + NODE_W, y1 + NODE_H / 2
        tx, ty = x2, y2 + NODE_H / 2
        mid = (sx + tx) / 2
        edges.append(
            f'<path class="diagram__edge" d="M{sx:.0f} {sy:.0f} '
            f'C{mid:.0f} {sy:.0f} {mid:.0f} {ty:.0f} {tx:.0f} {ty:.0f}"/>')

    title_id, desc_id = f'{spec["id"]}-title', f'{spec["id"]}-desc'
    body = "\n".join(
        indent(part, 4) for part in
        [f'<title id="{title_id}">{t(spec, "title")}</title>',
         f'<desc id="{desc_id}">{t(spec, "desc")}</desc>'] + labels + edges + boxes)
    return (
        f'<figure class="diagram" id="{spec["id"]}">\n'
        f'  <svg class="diagram__svg" viewBox="0 0 {width} {height:.0f}"'
        f' role="img" aria-labelledby="{title_id} {desc_id}">\n'
        f'{body}\n'
        "  </svg>\n"
        f'  <figcaption class="diagram__caption">{t(spec, "caption")}</figcaption>\n'
        "</figure>")


def json_ld(site: dict, meta: dict, canonical: str,
            title: str, description: str, employer: dict | None = None) -> str:
    """The structured data for one page, in one locale.

    `title` and `description` are passed in, never re-read from `meta`. The
    fragment's comment header is the English source; the locale's rendering
    of it lives in the overlay, and the head meta already resolves it through
    `tr()`. Reading `meta` here a second time is what shipped seven French
    pages whose head said one thing in French and whose Schema.org block said
    another in English, with nothing failing the build. One resolved string,
    handed to both, is the guard: they cannot disagree because there is only
    one of them.
    """
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
    # The current post, read off the top of experience.json rather than typed.
    # A role that ends, or a company that changes, moves the record and the
    # Person node follows it; a hand-written employer here would be a second
    # copy of a fact Career already owns, free to disagree with it.
    if employer:
        person["worksFor"] = {
            "@type": "Organization",
            "name": employer["company"],
            **({"url": employer["url"]} if employer.get("url") else {}),
        }
    page = {
        "@context": "https://schema.org",
        "@type": meta.get("schema_type", "WebPage"),
        "name": title,
        "url": canonical,
        "description": description,
        "isPartOf": {"@type": "WebSite", "name": site["name"], "url": site["base_url"] + "/"},
        "author": {"@type": "Person", "name": site["name"], "url": site["base_url"] + "/"},
    }
    payload = person if meta.get("nav") == "home" else page
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def fragment_for(locale: Locale, name: str) -> Path:
    """The page fragment to render for this locale.

    Prose is translated as a whole fragment (src/i18n/<code>/pages/<name>),
    not as keyed strings. A heading and a block__intro are sentences with
    markup threaded through them, and keying those by id produces an overlay
    nobody can read and a translator cannot work in.

    The fragment is the one thing here that is genuinely duplicated, so it is
    the one thing guarded: check_fragment_parity refuses a translation that
    does not carry the same anchors and the same generated blocks.
    """
    candidate = I18N / locale.code / "pages" / name
    return candidate if candidate.exists() else PAGES / name


def check_fragment_parity(locale: Locale, name: str) -> list[str]:
    """Every id and every {{ block }} must survive translation.

    An id is an anchor that impact.json, skills.json and the page context rail
    all address; a missing {{ build.x }} silently drops a whole block of
    records. Both are invisible in a language the author does not read, which
    is exactly why the build checks rather than trusting.
    """
    translated = I18N / locale.code / "pages" / name
    if not translated.exists():
        return []
    english = (PAGES / name).read_text(encoding="utf-8")
    other = translated.read_text(encoding="utf-8")
    locale.witness(f"pages/{name}", english)
    problems = []
    for label, pattern in (("anchor", r'id="([^"]+)"'), ("block", r"\{\{\s*([\w.]+)\s*\}\}")):
        want = set(re.findall(pattern, english))
        got = set(re.findall(pattern, other))
        for item in sorted(want - got):
            problems.append(f"{locale.code}/pages/{name}: {label} {item!r} is missing")
        for item in sorted(got - want):
            problems.append(f"{locale.code}/pages/{name}: {label} {item!r} is not in the English source")
    return problems


# How much of a page has to be in the locale's own language before the site
# will publish it there.
#
# Below this, the page is built, measured and thrown away, and neither the
# hreflang cluster nor the language switch mentions it. That sounds harsh for a
# translation in progress and it is the lenient option: the alternative, which
# is what shipped, was eight URLs announcing `lang="fr"` over English prose.
#
# Everything downstream of that attribute then acts on it. A screen reader
# pronounces English words with French phonemes. A search engine is told these
# are the same page in two languages and finds two copies of one. A French
# recruiter, the first market CLAUDE.md section 4 names, clicks `Francais` and
# lands on English, which is worse than finding no French at all because it
# spends trust rather than merely lacking it.
#
# CLAUDE.md section 10 already holds the principle: a stale translation is
# worse than a missing one, because a missing string falls back and is
# reported while a stale one reads fluent, confident and wrong. An untranslated
# *page* is that failure at page scale, and the fallback that makes a missing
# string survivable is exactly what makes the page unsurvivable. The gap was
# that the rule was enforced on strings and not on what they added up to.
#
# 0.50 is set where it is because a real translation still shares proper nouns,
# tool names, companies and certificate titles with its source, so demanding
# near-total divergence would fail pages that are genuinely done. Half is well
# above what an untranslated page can reach by accident and well below what a
# finished one scores. Awards, the pilot, measures 0.62.
MIN_TRANSLATED = 0.50


def translated_fraction(source: str, target: str) -> float:
    """How much of a rendered page differs from the English it was built from.

    Compared on the visible words of the page body rather than on the markup,
    which is identical by construction and would report every page as fully
    translated.
    """
    def words(markup: str) -> list[str]:
        body = re.sub(r"<!--.*?-->", " ", markup, flags=re.DOTALL)
        return re.sub(r"<[^>]+>", " ", body).split()

    english, other = words(source), words(target)
    if not other:
        return 0.0
    shared = sum(block.size for block in
                 difflib.SequenceMatcher(None, english, other).get_matching_blocks())
    return 1.0 - min(shared, len(other)) / len(other)


def render_alternates(site: dict, locales: list[Locale], output_name: str) -> str:
    """hreflang for every rendering of this page, including x-default.

    Search engines need to be told these are the same page in two languages
    rather than two pages competing for the same words, and a reader arriving
    from a French search should land on the French one.
    """
    # One rendering is not a cluster. A lone self-referential hreflang tells a
    # crawler nothing it did not have from the canonical tag.
    if len(locales) < 2:
        return ""
    leaf = "" if output_name == "index.html" else output_name
    lines = []
    for other in locales:
        href = f"{site['base_url']}/{other.dir}{leaf}"
        lines.append(f'<link rel="alternate" hreflang="{other.lang}" href="{href}">')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{site["base_url"]}/{leaf}">')
    return "\n".join(lines)


def render_lang_switch(locales: list[Locale], active: Locale, output_name: str) -> str:
    """The language control, beside the theme switch in the brand bar.

    Links, not buttons: each one is a real page at a real URL, so this is
    navigation and not state, and it needs no script. The active language is
    marked with aria-current and rendered as plain text rather than a link,
    because a link to the page you are on is a small lie.
    """
    if len(locales) < 2:
        return ""
    leaf = "" if output_name == "index.html" else output_name
    items = []
    for other in locales:
        if other.code == active.code:
            items.append(
                f'<span class="lang-switch__current" aria-current="true">{other.label}</span>'
            )
        else:
            href = f"{active.up}{other.dir}{leaf}" or f"{active.up}index.html"
            items.append(
                f'<a class="lang-switch__option" href="{href}" lang="{other.lang}"'
                f' hreflang="{other.lang}">{other.label}</a>'
            )
    body = f' <span class="lang-switch__sep" aria-hidden="true">&middot;</span> '.join(items)
    label = tr("chrome.language", "Language:")
    return (f'<div class="lang-switch">\n'
            f'  <span class="lang-switch__label">{label}</span>\n'
            f'  {body}\n'
            f'</div>')


def chrome_context() -> dict:
    """The layout's own words, in the active locale."""
    return {
        "chrome.skip": tr("chrome.skip", "Skip to content"),
        "chrome.cv": tr("chrome.cv", "CV (PDF)"),
        "chrome.primary_nav": tr("chrome.primary_nav", "Primary"),
        "chrome.theme": tr("chrome.theme", "Theme:"),
        "chrome.theme_system": tr("chrome.theme_system", "System"),
        "chrome.theme_light": tr("chrome.theme_light", "Light"),
        "chrome.theme_dark": tr("chrome.theme_dark", "Dark"),
        "chrome.theme_group": tr("chrome.theme_group", "Colour theme"),
        "chrome.last_update": tr("chrome.last_update", "Last update"),
        "chrome.hosted": tr("chrome.hosted", "Hosted on GitHub Pages"),
    }


def lock_path(locale: Locale) -> Path:
    return I18N / f"{locale.code}.lock.json"


def check_translations(locales: list[Locale], sync: bool) -> list[str]:
    """Fail when a translated string's English original has since changed.

    The fallback in `t` covers a string that was never translated. Nothing
    covered the opposite and worse case: a string translated once, then edited
    in English, where the French keeps saying the old thing with no gap for
    anyone to notice. Two pages then disagree about a figure or a date, in a
    language the author does not proofread, which is the exact drift every
    other guard in this build exists to prevent.

    The lock records the English each translation was made from. A mismatch is
    fatal rather than a warning, because a stale translation is not less
    complete than a missing one, it is wrong. `--sync` re-stamps the lock and
    is how you say "I have updated the French to match".

    A locale with no lock yet is bootstrapped rather than failed: the first
    build after adding a language has nothing to have drifted from.
    """
    problems: list[str] = []
    for locale in locales:
        if locale.code == "en":
            continue
        path = lock_path(locale)
        previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

        if previous is not None and not sync:
            for key, digest in sorted(locale.seen.items()):
                was = previous.get(key)
                if was is not None and was != digest:
                    problems.append(
                        f"{locale.code}: {key} was translated from an English "
                        f"source that has since changed. Update the translation, "
                        f"then re-stamp with: python3 tools/build.py --sync"
                    )

        if sync or previous is None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                json.dumps(locale.seen, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
    return problems


def report_missing(locales: list[Locale]) -> None:
    """Say what is still English, per locale, on every build.

    A missing string falls back rather than failing, because a half-translated
    page is readable and an empty one is not. That leniency only works if the
    gap is visible, so it is counted here and never silently absorbed.
    """
    for locale in locales:
        if locale.code == "en" or not locale.missing:
            continue
        keys = sorted(locale.missing)
        head = ", ".join(keys[:6])
        more = f", and {len(keys) - 6} more" if len(keys) > 6 else ""
        print(f"  {locale.code}: {len(keys)} untranslated: {head}{more}")


def report_withheld(withheld: list[tuple[str, str, float]]) -> None:
    """Name every page a locale is not publishing, and how far off it is.

    Withholding has to be louder than shipping, or it becomes a quiet way to
    have no French at all. Each line is the page, the language, what it
    measures and what it needs, so the next translation pass has a worklist
    rather than a verdict.
    """
    if not withheld:
        return
    for code in sorted({c for c, _, _ in withheld}):
        rows = [(name, share) for c, name, share in withheld if c == code]
        print(f"  {code}: {len(rows)} page(s) withheld, under "
              f"{MIN_TRANSLATED:.0%} translated:")
        for name, share in sorted(rows, key=lambda row: -row[1]):
            print(f"      {name:16} {share:.0%}")


def page_blocks(site: dict) -> dict:
    """Every data-driven region of every page, rendered for ACTIVE.

    Called once per locale. The records are re-read and re-rendered each
    time rather than rendered once and patched, because a translation is
    not a string substitution over finished markup: an ordinal, a month, a
    duration and a tag are all generated, and each is generated
    differently per language.
    """
    # Data-driven sections. A page fragment holds the section's heading and
    # prose; the records themselves come from src/data/, rendered through the
    # shared metadata rules so the tag order and colours are identical
    # everywhere. Indented to sit inside the <ul class="entries"> that the
    # fragment opens.
    # Ids are stamped before anything renders or sorts: see with_ids.
    awards = with_ids(json.loads((DATA / "awards.json").read_text(encoding="utf-8")), "award")
    competitions = [a for a in awards if a.get("type") == "Competitive Programming"]
    hackathons = [a for a in awards if a.get("type") == "Hackathon"]
    # The Workshops split is a filter on `block`, following Projects rather
    # than Awards: `block` is not a metadata category and never renders, so no
    # record carries a chip restating the heading it sits under. The two
    # blocks are the descent the page lede already claims, hardware down to
    # algorithms, which reverse chronology happens to render: see workshops.md.
    workshops = with_ids(json.loads((DATA / "workshops.json").read_text(encoding="utf-8")), "ws")
    for workshop in workshops:
        check_workshop_block(workshop)
    hardware_workshops = [w for w in workshops if w["block"] == "hardware"]
    algorithm_workshops = [w for w in workshops if w["block"] == "algorithms"]
    courses = sorted(
        with_ids(json.loads((DATA / "teaching.json").read_text(encoding="utf-8")), "course"),
        key=course_sort_key,
        reverse=True,
    )
    publications = sorted(
        with_ids(json.loads((DATA / "research.json").read_text(encoding="utf-8")), "pub"),
        key=publication_sort_key,
        reverse=True,
    )
    articles = sorted(
        with_ids(json.loads((DATA / "writing.json").read_text(encoding="utf-8")), "art"),
        key=publication_sort_key,
        reverse=True,
    )
    # The Projects split is a filter on `block`, exactly as Awards filters on
    # `type`. It differs in one respect, deliberately: `block` is not a
    # metadata category and never renders, so no record carries a tag
    # restating the heading it already sits under: the tension awards.md
    # records, resolved research.md's way.
    projects = sorted(
        with_ids(json.loads((DATA / "projects.json").read_text(encoding="utf-8")), "proj"),
        key=project_sort_key,
        reverse=True,
    )
    articles_by_id = {a["id"]: a for a in articles}
    # Career. Experience and Education sort newest-first on their start date;
    # credentials keep the order they are written in, because an issuer group
    # has no date to sort on and grouping by issuer is the ordering.
    experience = sorted(
        with_ids(json.loads((DATA / "experience.json").read_text(encoding="utf-8")), "exp"),
        key=tenure_sort_key,
        reverse=True,
    )
    education = sorted(
        with_ids(json.loads((DATA / "education.json").read_text(encoding="utf-8")), "edu"),
        key=lambda record: record["start"],
        reverse=True,
    )
    # Author-written architecture. CLAUDE.md M1: do not auto-generate this.
    diagrams = json.loads((DATA / "diagrams.json").read_text(encoding="utf-8"))
    certifications = with_ids(json.loads((DATA / "certifications.json").read_text(encoding="utf-8")), "cert")
    languages = with_ids(json.loads((DATA / "languages.json").read_text(encoding="utf-8")), "lang")
    online_courses = with_ids(json.loads((DATA / "courses.json").read_text(encoding="utf-8")), "learn")
    # Home. An impact line cites the page that evidences it, and the link text
    # comes from the navigation rather than from the record, so a citation
    # cannot name one page and point at another.
    page_labels = {entry["href"]: entry["label"] for entry in site["nav"]}
    impact = with_ids(json.loads((DATA / "impact.json").read_text(encoding="utf-8")), "impact")
    volunteering = sorted(
        with_ids(json.loads((DATA / "volunteering.json").read_text(encoding="utf-8")), "vol"),
        key=volunteering_sort_key,
        reverse=True,
    )
    # Every page that carries citable bullets. Adding one here is all it takes
    # for a bullet on that page to become citable from Home.
    citations = cite_index({
        "career.html": experience,
        "projects.html": projects,
        "research.html": publications,
        "teaching.html": courses,
        "workshops.html": workshops,
    })
    skills = sorted(
        with_ids(json.loads((DATA / "skills.json").read_text(encoding="utf-8")), "skill"),
        key=skill_sort_key,
    )
    open_source = [p for p in projects if p.get("block") == "open-source"]
    ml_projects = [p for p in projects if p.get("block") == "machine-learning"]
    blocks = {
        "build.credential_row": indent(render_credential_row(certifications), 8),
        "build.language_row": indent(render_language_row(languages), 8),
        "build.awards_summary": indent(render_awards_summary(awards), 4),
        "build.awards": indent("\n".join(render_award(a) for a in awards), 4),
        "build.competitions": indent("\n".join(render_award(a) for a in competitions), 4),
        "build.hackathons": indent("\n".join(render_award(a) for a in hackathons), 4),
        "build.workshops_hardware": indent(
            "\n".join(render_workshop(w) for w in hardware_workshops), 4),
        "build.workshops_algorithms": indent(
            "\n".join(render_workshop(w) for w in algorithm_workshops), 4),
        "build.courses": indent("\n".join(render_course(c) for c in courses), 4),
        "build.publications": indent("\n".join(render_publication(p, site) for p in publications), 4),
        "build.articles": indent("\n".join(render_article(a) for a in articles), 4),
        "build.reach_note": indent(reach_note(articles), 2),
        "build.contact_channels": indent(render_contact_channels(site), 4),
        "build.contact_facts": indent(render_contact_facts(site), 2),
        "build.contact_socials": indent(render_contact_socials(site), 4),
        # One key per diagram, so a fragment places it by name where it belongs
        # rather than the build guessing which page a diagram is about. The id
        # uses underscores because PLACEHOLDER does not admit a dash.
        **{f'build.diagram.{spec["id"]}': indent(render_diagram(spec), 2)
           for spec in diagrams},
        "build.open_source": indent(
            "\n".join(render_project(p, articles_by_id) for p in open_source), 4),
        "build.ml_projects": indent(
            "\n".join(render_project(p, articles_by_id) for p in ml_projects), 4),
        "build.experience": indent(
            "\n".join(render_experience(e) for e in experience), 4),
        "build.education": indent(
            "\n".join(render_education(e) for e in education), 4),
        "build.certifications": indent(
            "\n".join(render_credentials(c, "issuer", "cert") for c in certifications), 4),
        "build.online_courses": indent(
            "\n".join(render_credentials(c, "platform", "learn") for c in online_courses), 4),
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
    return blocks


def build(check_only: bool = False, sync: bool = False) -> int:
    site = json.loads((SRC / "site.json").read_text(encoding="utf-8"))
    layout = (SRC / "layout.html").read_text(encoding="utf-8")

    # Cache-bust CSS and JS off their actual contents, so a redeploy never
    # serves a stale stylesheet and an unchanged one is never re-downloaded.
    fingerprint = hashlib.sha256()
    for asset in ("assets/css/main.css",):
        fingerprint.update((ROOT / asset).read_bytes())
    asset_version = fingerprint.hexdigest()[:12]

    site_context = {f"site.{k}": v for k, v in site.items() if isinstance(v, (str, int))}

    # The current post, for the Person node's worksFor. Same file and same
    # ordering Career renders from, so the employer named in structured data
    # is the one at the top of the page and cannot be separately edited.
    current_post = max(
        with_ids(json.loads((DATA / "experience.json").read_text(encoding="utf-8")), "exp"),
        key=tenure_sort_key,
        default=None,
    )

    global ACTIVE

    locales = load_locales()
    problems: list[str] = []
    stale: list[str] = []
    written: list[str] = []
    removed: list[str] = []
    withheld: list[tuple[str, str, float]] = []

    # --- pass 1: render every page body in every locale, and measure it -----
    #
    # Two passes, because a page cannot be assembled until it is known which
    # languages publish it: the hreflang cluster and the language switch both
    # name the other renderings, and naming one that is being withheld is the
    # same broken promise in a different element.
    bodies: dict[tuple[str, str], dict] = {}

    for locale in locales:
        ACTIVE = locale

        # Re-rendered per locale rather than substituted into finished markup:
        # ordinals, months, durations and tags are all generated, and each is
        # generated differently per language.
        # The locale's own site values, before the blocks are rendered. Passing
        # the raw `site` here meant every renderer reading it directly
        # (render_contact_facts, render_contact_channels) emitted English on a
        # French page: `availability` and `location` are overlaid on `site`, not
        # on a record, so `t()` never saw them.
        locale_site = {**site, **locale.overrides}
        blocks = page_blocks(locale_site)
        locale_context = {f"site.{k}": v for k, v in locale_site.items()
                          if isinstance(v, (str, int))}
        # <html lang> and og:locale are the locale's own, not the site's.
        # Missing this shipped a French page announcing itself as English,
        # which is the one metadata error a translation cannot survive: it
        # tells a screen reader which voice to use and a search engine which
        # audience to serve.
        locale_context["site.lang"] = locale.lang
        locale_context["site.locale"] = locale.og_locale

        for nav_entry in site["nav"]:
            source = fragment_for(locale, nav_entry["href"])
            problems += check_fragment_parity(locale, nav_entry["href"])
            meta, content = parse_front_matter(source.read_text(encoding="utf-8"))
            content = render(content.strip(),
                             {**locale_context, **blocks, "page.root": locale.up})
            bodies[(locale.code, nav_entry["href"])] = {
                "source": source,
                "meta": meta,
                "content": content,
                "locale_site": locale_site,
                "locale_context": locale_context,
            }

    # --- which locales publish which page -----------------------------------
    source_locale = locales[0]
    publishes: dict[str, list[Locale]] = {}
    for nav_entry in site["nav"]:
        name = nav_entry["href"]
        english = bodies[(source_locale.code, name)]["content"]
        allowed = []
        for locale in locales:
            if locale.code == source_locale.code:
                allowed.append(locale)
                continue
            share = translated_fraction(english, bodies[(locale.code, name)]["content"])
            if share >= MIN_TRANSLATED:
                allowed.append(locale)
            else:
                withheld.append((locale.code, name, share))
        publishes[name] = allowed

    # --- validate before anything is written or deleted ---------------------
    #
    # This ran after pass 2 and cost a file. A stale-translation failure
    # returned 1 with seven withheld pages already unlinked from disk, so a
    # build that reported doing nothing had in fact deleted seven pages. Every
    # check that can fail the build now runs while the tree is untouched.
    ACTIVE = source_locale
    problems += check_translations(locales, sync)
    if problems:
        for problem in sorted(set(problems)):
            print(f"translation: {problem}", file=sys.stderr)
        return 1

    # --- pass 2: assemble and write -----------------------------------------
    for locale in locales:
        ACTIVE = locale
        for nav_entry in site["nav"]:
            output_name = nav_entry["href"]
            path = f"{locale.dir}{'' if output_name == 'index.html' else output_name}"
            target = ROOT / path if path.endswith(".html") else ROOT / locale.dir / "index.html"
            allowed = publishes[output_name]

            if locale not in allowed:
                # Withheld. Any copy left from a previous build is deleted
                # rather than left to rot: a stale file on disk is still served
                # by GitHub Pages, and the whole point of withholding it is
                # that nobody should reach it.
                if target.exists():
                    if check_only:
                        stale.append(str(target.relative_to(ROOT)))
                    else:
                        target.unlink()
                        removed.append(str(target.relative_to(ROOT)))
                continue

            body = bodies[(locale.code, output_name)]
            source, meta = body["source"], body["meta"]
            content, locale_site = body["content"], body["locale_site"]
            page_context = render_page_context(content, source)

            canonical = f"{site['base_url']}/{path}"
            page_title = tr(f"page.{nav_entry['id']}.title", meta["title"])
            # The brand a social card prints. It is home's title verbatim, so
            # the name-plus-role join is written in one place and punctuated by
            # the locale that owns it: a colon in English, a spaced colon in
            # French. Never assembled here from `name` and `role`, which would
            # be a second rendering free to drift from the first.
            site_name = tr("page.home.title",
                           bodies[(source_locale.code, "index.html")]["meta"]["title"])
            page_description = tr(f"page.{nav_entry['id']}.description",
                                  meta["description"])
            title_tag = (page_title if meta.get("nav") == "home"
                         else f"{page_title} &middot; {locale_site['name']}")

            # A page withheld in this locale is still reachable, in the
            # source language, at the source language's URL.
            #
            # This is the fallback `t` has always used for a missing string,
            # applied to a missing page, and it is not the failure the
            # threshold exists to stop. That failure was a French URL
            # declaring `lang="fr"` over English prose: the declaration was
            # the lie, never the English. Sending a reader to /career.html,
            # which says it is English and is, tells the truth. The link
            # carries `lang` and `hreflang` so a screen reader switches voice
            # and a crawler knows it has left the locale.
            nav_items = []
            for item in site["nav"]:
                target_locales = publishes[item["href"]]
                here = locale in target_locales
                destination = locale if here else source_locale
                leaf = "" if item["href"] == "index.html" else item["href"]
                # A sibling in this locale is addressed by its bare name. Only
                # a page being served from the other locale needs climbing out
                # of this directory first.
                href = (leaf or "index.html") if here else f"{locale.up}{destination.dir}{leaf}"
                nav_items.append({
                    **item,
                    "href": href,
                    "label": tr(f"nav.{item['id']}", item["label"]),
                    "lang": "" if here else
                            f' lang="{source_locale.lang}" hreflang="{source_locale.lang}"',
                    "aria_current": ' aria-current="page"' if item["id"] == nav_entry["id"] else "",
                })

            portrait_w, portrait_h = image_size(ROOT / site["portrait"])
            context = {
                **body["locale_context"],
                "site.portrait_width": portrait_w,
                "site.portrait_height": portrait_h,
                "page.title_tag": title_tag,
                "page.description": page_description,
                "site.site_name": site_name,
                "page.canonical": canonical,
                "page.og_type": "profile" if meta.get("nav") == "home" else "website",
                "page.content": indent(content, 8),
                "page.root": locale.up,
                # The brand bar goes home, and home is this locale's home only
                # where this locale publishes one. It was the literal string
                # "index.html", which resolved inside /fr/ to a page that the
                # translation threshold may be withholding.
                "page.home": next(item["href"] for item in nav_items
                                  if item["id"] == "home"),
                "build.page_context": indent(page_context, 8),
                "build.asset_version": asset_version,
                "build.json_ld": json_ld(locale_site, meta, canonical,
                                         page_title, page_description,
                                         current_post),
                "build.nav": render_items("nav-item.html", nav_items),
                "build.alternates": indent(render_alternates(site, allowed, output_name), 2),
                "build.lang_switch": indent(render_lang_switch(allowed, locale, output_name), 10),
                "build.chrome": "",
                **chrome_context(),
            }

            page_html = (BANNER.format(source=source.name)
                         + strip_comments(render(layout, context)))

            if check_only:
                current = target.read_text(encoding="utf-8") if target.exists() else ""
                if current != page_html:
                    stale.append(str(target.relative_to(ROOT)))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(page_html, encoding="utf-8")
                written.append(str(target.relative_to(ROOT)))

    ACTIVE = source_locale
    report_missing(locales)
    report_withheld(withheld)

    if check_only:
        if stale:
            print("stale (run: python3 tools/build.py): " + ", ".join(stale), file=sys.stderr)
            return 1
        print("up to date")
        return 0

    if removed:
        print("withdrawn (below the translation threshold): " + ", ".join(removed))

    if sync:
        print("translation locks re-stamped")
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
    parser.add_argument("--sync", action="store_true",
                        help="re-stamp the translation locks: use after updating a translation "
                             "to match an edited English source")
    args = parser.parse_args()
    if args.watch:
        sys.exit(watch())
    sys.exit(build(check_only=args.check, sync=args.sync))
