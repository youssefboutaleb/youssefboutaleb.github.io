#!/usr/bin/env python3
"""Verify the built site: assets resolve, markup is sound, CSS and HTML agree.

    python3 tools/check.py

There is no test framework here because there is no application code — the
things that actually break on a static portfolio are dead links, a class name
that exists in the markup but not the stylesheet, a stray inline style, and an
image with no alt text. This checks exactly those, plus that the committed
pages match their sources.
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
        self.in_script_or_style = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        line = self.getpos()[0]

        if tag in ("script", "style"):
            self.in_script_or_style = True

        if "style" in attrs:
            fail(self.page, f"line {line}: inline style on <{tag}> — belongs in main.css")
        for name in attrs:
            if name.startswith("on"):
                fail(self.page, f"line {line}: inline event handler {name}= on <{tag}>")

        if attrs.get("class"):
            self.classes.update(attrs["class"].split())
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in attrs:
            fail(self.page, f"line {line}: <img src={attrs.get('src')!r}> has no alt attribute")
        if tag == "a" and attrs.get("target") == "_blank":
            rel = attrs.get("rel", "")
            if "noopener" not in rel:
                fail(self.page, f"line {line}: target=_blank without rel=noopener")

        for attribute in ("href", "src"):
            if attribute in attrs:
                self.refs.append((attrs[attribute], line))

        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_endtag(self, tag):
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


def main() -> int:
    pages = sorted(p for p in ROOT.glob("*.html"))
    if not pages:
        print("no pages found", file=sys.stderr)
        return 1

    known_classes = css_selectors()
    css_variable_audit()

    for page in pages:
        audit = PageAudit(page.name)
        audit.feed(page.read_text(encoding="utf-8"))

        for tag, line in audit.stack:
            fail(page.name, f"<{tag}> opened at line {line} is never closed")

        if audit.h1_count != 1:
            fail(page.name, f"expected exactly one <h1>, found {audit.h1_count}")

        duplicates = {i for i in audit.ids if audit.ids.count(i) > 1}
        if duplicates:
            fail(page.name, f"duplicate id attributes: {', '.join(sorted(duplicates))}")

        for name in sorted(audit.classes - known_classes):
            fail(page.name, f"class '{name}' is used in markup but has no rule in main.css")

        for ref, line in audit.refs:
            parsed = urlparse(ref)
            if parsed.scheme or parsed.netloc or ref.startswith(("#", "mailto:", "tel:", "data:")):
                continue
            target = ROOT / unquote(parsed.path)
            if not target.exists():
                fail(page.name, f"line {line}: broken local reference '{parsed.path}'")

            if parsed.fragment and target.suffix == ".html" and target.exists():
                if f'id="{parsed.fragment}"' not in target.read_text(encoding="utf-8"):
                    fail(page.name, f"line {line}: '{ref}' points at a missing anchor")

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
