#!/usr/bin/env python3
"""Verify the built site: assets resolve, markup is sound, CSS and HTML agree.

    python3 tools/check.py

There is no test framework here because there is no application code: the
things that actually break on a static portfolio are dead links, a class name
that exists in the markup but not the stylesheet, a stray inline style, and an
image with no alt text. This checks exactly those, plus that the committed
pages match their sources, plus CLAUDE.md's dash ban across the whole
repository rather than only the built pages.
"""

from __future__ import annotations

import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "assets" / "css" / "main.css"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

# CLAUDE.md's dash ban. The glyphs are written as escapes and the entities are
# assembled from a fragment so that this file does not trip the audit it
# defines: the same trap that made the rule's own paragraph in CLAUDE.md the
# one permanent false positive of a repository-wide search.
DASH_MARKS = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "&" + "mdash;": "em dash entity",
    "&" + "ndash;": "en dash entity",
}
# The ban covers every file, so this walks sources rather than built pages.
DASH_SUFFIXES = {".html", ".css", ".json", ".md", ".py", ".txt", ".yml", ".yaml"}
DASH_SKIP_DIRS = {".git", "__pycache__", "node_modules"}

failures: list[str] = []
notes: list[str] = []


def fail(page: str, message: str) -> None:
    failures.append(f"{page}: {message}")


class PageAudit(HTMLParser):
    """Collects everything we assert on in a single pass over the document."""

    def __init__(self, page: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page = page
        self.stack: list[tuple[str, int]] = []
        self.classes: set[str] = set()
        self.refs: list[tuple[str, int]] = []
        self.ids: list[str] = []
        self.h1_count = 0
        self.headings: list[tuple[int, int]] = []
        self.links: list[tuple[str, str]] = []
        self._link_href: str | None = None
        self._link_text: list[str] = []
        self.in_script_or_style = False

    def handle_data(self, data):
        if self._link_href is not None:
            self._link_text.append(data)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        line = self.getpos()[0]

        if tag in ("script", "style"):
            self.in_script_or_style = True

        if "style" in attrs:
            fail(self.page, f"line {line}: inline style on <{tag}>: belongs in main.css")
        for name in attrs:
            if name.startswith("on"):
                fail(self.page, f"line {line}: inline event handler {name}= on <{tag}>")

        if attrs.get("class"):
            self.classes.update(attrs["class"].split())
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append((int(tag[1]), line))
        if tag == "img" and "alt" not in attrs:
            fail(self.page, f"line {line}: <img src={attrs.get('src')!r}> has no alt attribute")
        if tag == "a" and attrs.get("target") == "_blank":
            rel = attrs.get("rel", "")
            if "noopener" not in rel:
                fail(self.page, f"line {line}: target=_blank without rel=noopener")

        for attribute in ("href", "src"):
            if attribute in attrs:
                self.refs.append((attrs[attribute], line))

        if tag == "a" and "href" in attrs:
            self._link_href = attrs["href"]
            self._link_text = []

        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_endtag(self, tag):
        if tag == "a" and self._link_href is not None:
            text = " ".join("".join(self._link_text).split())
            if text:
                self.links.append((text, self._link_href))
            self._link_href = None
        if tag in VOID:
            return
        if tag in ("script", "style"):
            self.in_script_or_style = False
        if not self.stack:
            fail(self.page, f"line {self.getpos()[0]}: stray </{tag}>")
            return
        if self.stack[-1][0] != tag:
            open_tag, open_line = self.stack[-1]
            fail(self.page, f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> opened at line {open_line}")
            # Recover so one mistake does not cascade into noise.
            for index in range(len(self.stack) - 1, -1, -1):
                if self.stack[index][0] == tag:
                    del self.stack[index:]
                    return
            return
        self.stack.pop()


def css_selectors() -> set[str]:
    """Every class name the stylesheet defines a rule for."""
    css = CSS.read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    # Quoted strings hold font paths like "…/Noto-Sans.woff2", whose extensions
    # would otherwise be read as class selectors.
    css = re.sub(r"'[^']*'|\"[^\"]*\"", "''", css)
    return set(re.findall(r"\.(-?[_a-zA-Z][\w-]*)", css))


def css_variable_audit() -> None:
    css = re.sub(r"/\*.*?\*/", "", CSS.read_text(encoding="utf-8"), flags=re.DOTALL)
    defined = set(re.findall(r"^\s*(--[\w-]+)\s*:", css, flags=re.MULTILINE))
    used = set(re.findall(r"var\(\s*(--[\w-]+)", css))
    for name in sorted(used - defined):
        failures.append(f"main.css: var({name}) is used but never defined")
    unused = sorted(defined - used)
    if unused:
        notes.append(f"tokens defined but not consumed by any rule: {', '.join(unused)}")


# Rules that exist in main.css with nothing using them yet, and why each is
# allowed to. Anything not on this list is a failure: dead CSS is a maintenance
# tax, and five rules rotted here long enough for one of them, .block__note, to
# be cited by CLAUDE.md as an implemented mechanism while rendering nowhere.
STAGED_CSS = {
    # The six diagram* names lived here while src/data/diagrams.json was empty.
    # Career carries the JACQUEMUS order path and Research the Ausgrid pipeline
    # now, so the rules are reached by markup and this list would be lying
    # about them. See diagrams.md.
    # MEDALS in build.py emits medal--bronze for any third place. The rule is
    # reachable; the data has no third place yet.
    "medal--bronze",
}

# Words this repository spells two ways. British and American forms are both
# fine; using both is not, and the pair colorisation/colorization appeared in
# one page's <meta> and its own record title. Listed as the -ise form; the
# audit reports whichever spelling is in the minority across the built pages.
SPELLING_PAIRS = [
    "colorise", "colorisation", "optimise", "optimisation", "normalise",
    "normalisation", "organise", "organisation", "containerise",
    "containerisation", "visualise", "visualisation", "specialise",
    "specialisation", "summarise", "neutralise", "synchronise",
    "synchronisation", "vectorise", "vectorisation", "generalise",
    "generalisation", "decentralise", "serialise", "serialisation",
]


def heading_audit(page: str, headings: list[tuple[int, int]]) -> None:
    """No level may be skipped on the way down.

    Seven of eight pages ran h1 straight to h3 and had no h2 at all, while
    Contact was the only page with an h2 and used it for the same visual rank
    the others got from an h3. Nothing caught either, because the only heading
    assertion here counted h1s. A screen reader user navigating by heading gets
    the document's shape from these numbers and from nothing else.
    """
    previous = 0
    for level, line in headings:
        if previous and level > previous + 1:
            fail(page, f"line {line}: <h{level}> follows <h{previous}>, "
                       f"skipping <h{previous + 1}>")
        previous = level


def spelling_audit(pages: list[Path]) -> None:
    """Fail when the same word is spelled both ways across the built site.

    Not a preference between British and American English: the repository may
    have either. What it may not have is `colorisation` in a page description
    and `Colorization` in the title of the record that description describes,
    which is what shipped. The dash ban is enforced to the codepoint and this
    was not enforced at all.
    """
    # English pages only. A locale directory is a different language, and
    # comparing across them reported the correct French "vectorisation"
    # against the correct English "vectorization" as a repository that
    # could not spell.
    english = [p for p in pages if p.parent == ROOT]
    text = " ".join(p.read_text(encoding="utf-8") for p in english).lower()
    for ise in SPELLING_PAIRS:
        ize = ise.replace("ise", "ize").replace("isation", "ization")
        counts = {}
        for form in (ise, ize):
            # Match the stem so one entry covers -ed, -es, -ing, -ation.
            counts[form] = len(re.findall(rf"\b{form}", text))
        if counts[ise] and counts[ize]:
            minority = min(counts, key=counts.get)
            failures.append(
                f"spelling: '{ise}' ({counts[ise]}) and '{ize}' ({counts[ize]}) "
                f"both appear across the built pages. Pick one and change the "
                f"{counts[minority]} instance(s) of '{minority}' in src/."
            )


def link_fanin_audit(page: str, links: list[tuple[str, str]]) -> None:
    """Report distinct link texts that all land on the same destination.

    Home's evidence chips promised a claim could be checked in one click and
    sent 45 differently-labelled links to 9 addresses, because certifications
    carried no ids and the linker fell back to the block heading. Reported, not
    fatal: several chips honestly citing one record is normal, and only the
    author can say which case a given group is.
    """
    by_target: dict[str, set[str]] = {}
    for text, href in links:
        if href.startswith("#") or "#" not in href:
            continue
        by_target.setdefault(href, set()).add(text)
    worst = [(href, labels) for href, labels in by_target.items() if len(labels) > 3]
    for href, labels in sorted(worst, key=lambda row: -len(row[1])):
        notes.append(f"{page}: {len(labels)} differently-labelled links all go "
                     f"to '{href}'")


def dash_audit() -> None:
    """Fail on an em dash or en dash anywhere in the repository's sources.

    CLAUDE.md bans both because the em dash is the loudest tell that a passage
    was machine-written, and the site's whole argument is that a person wrote
    it. The rule was enforced by hand until it was not: one survivor in a
    paragraph undoes the rest, and nothing was looking.
    """
    for path in sorted(ROOT.rglob("*")):
        if path.suffix not in DASH_SUFFIXES or not path.is_file():
            continue
        if DASH_SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), 1):
            hit = next((n for m, n in DASH_MARKS.items() if m in line), None)
            if hit:
                fail(str(path.relative_to(ROOT)), f"line {number}: {hit}")


def main() -> int:
    # Root pages are English; a locale directory holds one rendering each.
    # They are checked identically: a translated page has the same anchors,
    # the same classes and the same links to keep working, and it is the one
    # nobody proofreads by eye.
    pages = sorted(ROOT.glob("*.html"))
    # A locale directory is one holding built pages, not one holding a home
    # page. build.py withholds a page whose translation is under
    # MIN_TRANSLATED, and the first thing French fell below the bar on was its
    # own index, which took the whole directory out of this scan and stopped
    # the one page that *is* translated from being checked at all.
    for locale_dir in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if locale_dir.name in {"assets", "images", "data", "src", "tools"} or locale_dir.name.startswith("."):
            continue
        pages += sorted(locale_dir.glob("*.html"))
    if not pages:
        print("no pages found", file=sys.stderr)
        return 1

    known_classes = css_selectors()
    css_variable_audit()
    dash_audit()
    spelling_audit(pages)
    used_classes: set[str] = set()

    for page in pages:
        label = str(page.relative_to(ROOT))
        audit = PageAudit(label)
        audit.feed(page.read_text(encoding="utf-8"))

        for tag, line in audit.stack:
            fail(label, f"<{tag}> opened at line {line} is never closed")

        if audit.h1_count != 1:
            fail(label, f"expected exactly one <h1>, found {audit.h1_count}")

        heading_audit(label, audit.headings)
        link_fanin_audit(label, audit.links)

        duplicates = {i for i in audit.ids if audit.ids.count(i) > 1}
        if duplicates:
            fail(label, f"duplicate id attributes: {', '.join(sorted(duplicates))}")

        used_classes |= audit.classes
        for name in sorted(audit.classes - known_classes):
            fail(label, f"class '{name}' is used in markup but has no rule in main.css")

        for ref, line in audit.refs:
            parsed = urlparse(ref)
            if parsed.scheme or parsed.netloc or ref.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            # Relative to the page, not to the site root: /fr/awards.html
            # reaches the stylesheet as ../assets/... and its sibling pages
            # as bare names.
            target = (page.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                fail(label, f"line {line}: broken local reference '{parsed.path}'")

            if parsed.fragment and target.suffix == ".html" and target.exists():
                if f'id="{parsed.fragment}"' not in target.read_text(encoding="utf-8"):
                    fail(label, f"line {line}: '{ref}' points at a missing anchor")

    # Dead CSS is a maintenance tax: the next person cannot tell which rules
    # still matter. This was a note for exactly that reason, "a rule may be
    # staged for a new page", and five rules then sat dead long enough that
    # CLAUDE.md came to describe .block__note as a working mechanism while it
    # rendered nowhere on the site. Staging is now declared in STAGED_CSS with
    # a reason, and anything else fails.
    unused = sorted(known_classes - used_classes - STAGED_CSS)
    if unused:
        failures.append(
            "main.css: no markup uses " + ", ".join(f".{name}" for name in unused)
            + ". Delete the rule, or add it to STAGED_CSS in tools/check.py "
            "with the reason it is waiting."
        )
    staged_but_used = sorted(STAGED_CSS & used_classes)
    if staged_but_used:
        notes.append("now in use, drop from STAGED_CSS: "
                     + ", ".join(f".{name}" for name in staged_but_used))

    build_check = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build.py"), "--check"],
        capture_output=True, text=True,
    )
    if build_check.returncode != 0:
        failures.append("build: " + build_check.stderr.strip())

    print(f"checked {len(pages)} pages, {len(known_classes)} css classes")
    for note in notes:
        print(f"  note: {note}")

    if failures:
        print(f"\n{len(failures)} problem(s):", file=sys.stderr)
        for problem in failures:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
