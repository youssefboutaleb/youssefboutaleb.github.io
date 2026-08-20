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

BANNER = (
    "<!-- GENERATED FILE — do not edit.\n"
    "     Source: src/layout.html + src/pages/{source} (content), src/site.json (data).\n"
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

    stale: list[str] = []
    written: list[str] = []

    for nav_entry in site["nav"]:
        source = PAGES / nav_entry["href"]   # content fragment mirrors its output name
        meta, content = parse_front_matter(source.read_text(encoding="utf-8"))

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
            "page.content": indent(content.strip(), 8),
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify output is current")
    sys.exit(build(check_only=parser.parse_args().check))
