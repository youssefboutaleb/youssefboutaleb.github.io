# youssefboutaleb.github.io

Personal engineering portfolio — a static site with no runtime dependencies,
served directly by GitHub Pages.

## Architecture

The seven published pages share an identical head, sidebar, navigation and
footer. Those are written **once** and rendered into the pages by a build step,
so the site cannot drift out of sync with itself again.

```
src/
  site.json          identity, contact details, social profiles, navigation
  layout.html        the page shell — head, sidebar, nav, footer
  partials/          item templates for the repeated lists in the shell
  pages/*.html       page content only, one file per page
  data/*.json        records rendered from structured fields (see below)
assets/
  css/main.css       the entire design system (see DESIGN.md)
  fonts/             self-hosted Noto Sans (woff2 / woff / ttf)
images/, data/       portrait, brand icons, CV, workshop slides
tools/
  build.py           renders src/ → the *.html files in the repository root
  check.py           verifies the built site
*.html               BUILD OUTPUT — generated, do not edit by hand
```

Deployment stays build-free: the generated `*.html` files are committed and
GitHub Pages serves them as-is. `.nojekyll` disables Jekyll processing.

## Working on the site

Edit content in `src/pages/`, shared chrome in `src/layout.html`, and identity
or navigation in `src/site.json`. Then:

```bash
python3 tools/build.py          # regenerate the root *.html files
python3 tools/build.py --watch  # auto-rebuild on changes while developing
python3 tools/check.py          # verify before committing
```

Preview by opening `index.html` in a browser, or:

```bash
python3 -m http.server 8000
```

`tools/build.py --check` exits non-zero if the committed pages are stale, which
makes it usable as a pre-commit or CI gate.

### Adding an award

Awards are data, not markup. Append a record to `src/data/awards.json` and
rebuild — the page never lists entries by hand:

```json
{
  "title": "Hello World v4.0",
  "venue": "Sfax",
  "year": "2024",
  "placement": 1,
  "type": "Competitive Programming",
  "scope": "Regional",
  "scale": { "count": 86, "unit": "teams" },
  "points": ["Solved 8 problems"]
}
```

`placement` is a plain integer where there is a rank (`1` renders as `1st Place`
with a gold medal; `2` silver, `3` bronze) or a string otherwise (`"Finalist"`).
`venue`, `placement`, `scale` and `points` are all optional — a field with no
data is left out rather than filled in. The four metadata tags always render in
the order `placement → type → scope → scale`, defined once as
`MODELS["awards"]` in `tools/build.py`; see [DESIGN.md §7](DESIGN.md) for the
colour rules.

### Adding a workshop

Same shape, a different model. Append a record to `src/data/workshops.json`:

```json
{
  "title": "Introduction to Competitive Programming",
  "year": "2023",
  "format": "Workshop",
  "mode": "On-site",
  "audience": "Engineering Students",
  "host": "IEEE Student Branch ENIS",
  "summary": "An entry point into contest-style problem solving …",
  "points": ["Complexity analysis first: reading a problem's constraints …"]
}
```

The four tags render in the order `format → mode → audience → host`, from
`MODELS["workshops"]`. Optional `repo` adds a GitHub icon-link to the title and
`slides` appends a download tag after the metadata. The permitted value for
each category, and the editorial rules for the bullets, are in
[workshops.md](workshops.md).

### Adding a course

`src/data/teaching.json`, rendering `level → workload → scale`:

```json
{
  "title": "Data Engineering 2",
  "term": "Fall",
  "year": 2025,
  "level": 2,
  "workload": { "lecture": 20, "lab": 8, "project": 4 },
  "scale": { "count": 12, "unit": "students" },
  "summary": "The second-year sequel …",
  "syllabus": [
    { "title": "Resilient Pipeline Design", "points": ["Retry management …", "<b>Lab:</b> …"] }
  ],
  "capstone": { "title": "Fault-Tolerant Ingestion Pipeline", "points": ["…"] }
}
```

Everything is stored raw and labelled by the renderer: `2` becomes
`Master's Year 2`, the workload hours are **summed** into
`32 h · 20 lecture + 8 lab + 4 project` so the total can never disagree with
its parts, and modules are numbered at render time. `term` and `year` are not
tags — they render as the period line (`Fall 2025 – 2026`) — and position in the
file does not matter, because `course_sort_key` sorts newest-first on
`(year, term)`; Fall precedes Spring inside one academic year, so sorting on the
year alone would get it wrong.

`scale` is the *same* category Awards uses, reusing its rule rather than
coining a synonym. Technologies carry no tags: they are named inside the module
that teaches them. The capstone is a sibling of `syllabus` rather than a sixth
module, so the five modules keep matching the twenty lecture hours the workload
claims. Full rationale in [teaching.md](teaching.md).

### Adding a publication

`src/data/research.json`, rendering `status → authorship → publisher`:

```json
{
  "title": "Secure and transparent energy management using blockchain …",
  "authors": [
    { "name": "N. Moumni", "scholar": "https://scholar.google.com/citations?user=…" },
    { "name": "Y. Boutaleb", "scholar": "https://scholar.google.com/citations?user=…", "self": true }
  ],
  "venue": "Computers &amp; Industrial Engineering",
  "year": 2025,
  "status": "Published",
  "publisher": "Elsevier",
  "url": "https://www.sciencedirect.com/science/article/abs/pii/S036083522500186X",
  "summary": "Blockchain used to make energy exchange records auditable …"
}
```

`authorship` is never typed: the author marked `"self": true` has its index read
by `author_position`, which produces `Second Author` — so correcting an author
list can no longer leave a stale claim behind. The journal is not a tag either,
because it is already in the citation line; the model asks `publisher`
(*Elsevier*) instead, which the citation does not give. `doi` is preferred over
`url` when it exists, and a record with no `year` is not yet out, so it renders
no period line and `publication_sort_key` sorts it last. Full rationale in
[research.md](research.md).

### What `check.py` verifies

- Every local `href`/`src` resolves to a file that exists, and every in-page
  anchor points at an id that exists
- No inline `style=` attributes and no inline event handlers
- Every `<img>` has an `alt`; every `target="_blank"` has `rel="noopener"`
- Exactly one `<h1>` per page, and no duplicate `id`s
- Every class used in the markup has a rule in `main.css`, and every rule and
  token is used by something (dead CSS is reported, not fatal)
- Every `var(--token)` is defined
- Tags are balanced and correctly nested
- The committed pages match their sources

Requires only Python 3 from the standard library. No Node, no bundler, no
package manager.

## Design system

A classic academic stylesheet in the lineage of the orderedlist **Minimal**
theme this site was forked from: a sticky identity rail, a plain document, one
typeface, one blue for links, hairlines for structure.

Typography, colour, spacing, components, responsive behaviour and accessibility
rules — plus an explicit list of what is *out of scope* — are documented in
**[DESIGN.md](DESIGN.md)**. Read it before adding a component; almost
everything on the site is already expressible with `.block`, `.entry`,
`.deflist` and `.tag`.

**[awards.md](awards.md)** is its companion, covering the other half: the
information model behind an entry — how a page declares its metadata
categories, fixes their order in one place, and keeps its terminology factual.
Read it before adding a page of records. DESIGN.md defines how a tag looks;
awards.md defines what it says.

**[workshops.md](workshops.md)**, **[teaching.md](teaching.md)** and
**[research.md](research.md)** are that convention applied to a page each: the declared categories for the record, why
they are in that order, the permitted value for each, and what deliberately
stays out of the model. `teaching.md` also covers the three rules the third
model forced into the open — when to reuse another model's category instead of
inventing one, why a category holds exactly one value, and why a fact that is
true of every record on a page belongs to the page rather than to the records.
`research.md` adds the fourth: a category whose values are a progression —
*In Progress*, then *Published* — still takes one treatment, because the colour
names the category and never grades the value.

`awards.md` doubles as the model document for its own page, since the
convention was generalised from it: the Awards declaration, the
Competitions/Hackathons split, and the editorial rule that a contest bullet
states the score and nothing else all live there.

## Credits

Originally forked from [elyesmanai.github.io](https://github.com/elyesmanai/elyesmanai.github.io);
theme lineage [orderedlist](https://github.com/orderedlist). The current design
system, markup and build are original work.
