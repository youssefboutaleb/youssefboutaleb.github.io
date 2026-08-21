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

### Adding a project

`src/data/projects.json`, rendering `upstream → kind → stack`:

```json
{
  "title": "Kanboard Plugin: Draw.io Integration",
  "block": "open-source",
  "year": 2026,
  "repo": "https://github.com/youssefboutaleb/kanboard-plugin-drawio",
  "upstream": { "repo": "kanboard/website", "pr": 586, "state": "open" },
  "kind": "Kanboard Plugin",
  "stack": ["PHP", "JavaScript"],
  "summary": "Embeds diagrams.net into Kanboard tasks and projects …"
}
```

`block` selects which of the page's two sections the record lands in and is
never rendered — unlike Awards, which filters on `type` and then tags it, no
record here repeats the heading it sits under. `upstream` was the first of the
site's two categories whose value carries a link (`accreditation` on Education
is the other): `meta_url` builds the pull request
address from the stored repo and number, and the tag *is* the link, keeping its
category's amber. That amber is deliberate — `state` is stored raw and
`UPSTREAM_STATES` turns `open` into `Submitted upstream` and `merged` into
`Accepted upstream`, both in the same colour, because the treatment says *this
is an upstream status* and never *this one is the good one*. `stack` is a list
rendered as a **single** tag, capped at four names: `teaching.md` deleted an
earlier `stack` category that rendered a chip per tool, because a run whose
length varies per record destroys positional reading. Full rationale in
[projects.md](projects.md).

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

### Adding a technical article

Self-published writing is a *second block* on the same page, on its own model.
`src/data/writing.json`, rendering `format → reach → platform`:

```json
{
  "title": "Simplify Your Log Management: Configuring DataDog Integration with Log4j2 In Mulesoft",
  "year": 2024,
  "format": "Configuration Guide",
  "reach": { "views": 723, "reads": 424 },
  "platform": "Medium",
  "url": "https://medium.com/@youssefboutaleb.info/simplify-your-log-management-…",
  "summary": "Ships logs without installing the DataDog agent: a Log4j2 HTTP appender …"
}
```

It does not borrow the paper model, because all three of that model's
categories degrade on a Medium post: `status` would put the same word
*Published* on peer-reviewed and self-published work while meaning two
different things, `authorship` says nothing about a sole author, and
`publisher` is defined as the house rather than the platform. What the two
blocks *do* share is position — `platform` takes the quiet grey terminal slot
that `publisher` takes above it, so the reader scanning the page finds
**Elsevier** and **Medium** in the same place, in the same colour, and the
distinction is made by the layout instead of by a disclaimer. `format` is the
same category Workshops declares, reused rather than renamed.

`reach` is stored as two raw integers and rendered as one violet tag —
`723 views · 424 reads` — because the pair is the unit: views alone inflates,
reads alone hides the ratio it should be judged against. `abbreviate` prints
large figures the way Medium reports them (`3000` → `3K`), so the page never
claims more precision than its source gave it. The counts are hand-copied and
nothing refreshes them, so the block intro carries an explicit *as of* date;
the figures and that date must move in the same change or neither. A record
carries both numbers or omits `reach` entirely. Full rationale in
[writing.md](writing.md).

Where an article documents a project that has its own Projects entry, the link
goes on the *project* record as a utility tag — the article stays declared once
here and rendered once on Research.

### Adding a job

`src/data/experience.json`, rendering `domain → stack`:

```json
{
  "company": "JACQUEMUS",
  "url": "https://www.linkedin.com/company/jacquemus/posts/?feedView=all",
  "role": "Data Integration Engineer &amp; Operations Engineer",
  "start": "2024-08",
  "domain": "E-commerce &amp; Retail",
  "stack": ["Talend", "Azure", "Datadog", "Salesforce"],
  "groups": [
    { "title": "Observability", "points": ["Deployed a real-time Datadog monitoring solution …"] }
  ]
}
```

Two categories, because two is what the records honestly support. The
hand-written page carried three to five loose technology chips per job, with
the headline tool in `.tag--accent` and the rest in `.tag--neutral`: a run whose
length changed per record, so no column existed to read down, and an accent that
graded a *value* rather than naming a category. They are now one `stack` tag,
the same category `projects.json` declares, capped at four names. `domain` is
the blue substance slot — it answers what the *data* was about, which the job
title does not: two of the three roles here are titled Data Integration
Engineer, and one moved e-commerce orders while the other moved service-desk
tickets. There is deliberately **no** `engagement` category (permanent /
contract / internship): the fact is not recorded anywhere, and rule 5 says a
gap beats an invented placeholder.

Dates are stored raw as `"YYYY-MM"` and labelled by `month_year`, so `Aug 2024`
and `August 2024` cannot both appear. Omitting `end` renders `Present` — the
word lives in the renderer, because *Present* is not a date and a record that
stores one keeps claiming the job after it ends. `tenure_sort_key` sorts
newest-first on `start`, not `end`, so the one record without an end date needs
no sentinel to stay on top. A role that did several separable things carries
`groups`; a short one carries a flat `points`. Full rationale in
[career.md](career.md).

### Adding a qualification

`src/data/education.json`, rendering `accreditation` — a **one-category
model**, and the clearest illustration that categories are chosen for the
reader rather than for symmetry:

```json
{
  "degree": "Computer Science Engineer&rsquo;s Degree",
  "institution": "ENIS",
  "institution_full": "National Engineering School of Sfax",
  "url": "https://enis.rnu.tn/",
  "location": "Sfax",
  "start": 2021,
  "end": 2024,
  "accreditation": {
    "name": "EUR-ACE&reg; Accredited",
    "url": "https://www.enaee.eu/eur-ace-system/"
  }
}
```

The degree is the title, the institution trails it, the years are the period
line — a `field` or `level` category would restate one of the three. What is
left is the single thing the title cannot say: who accredits the programme. The
second record omits `accreditation` and renders zero tags.

`accreditation` is the site's second linked metadata tag after `upstream`, and
it is **grey**, not the success-green the hand-written page gave it. It answers
the same question `publisher`, `host`, `platform` and `stack` answer — who
stands behind this — so it takes their treatment; the green was grading the
value rather than naming the category, and green is a *utility* meaning
([DESIGN.md §7](DESIGN.md)).

### Adding a certification or a course

`src/data/certifications.json` and `src/data/courses.json`, both rendered by
`render_credentials` into the `.issuer` component:

```json
{
  "issuer": "Datadog",
  "icon": "datadog.svg",
  "credentials": [
    { "name": "Datadog Certified: Fundamentals", "url": "https://www.credly.com/badges/…" }
  ]
}
```

These are the site's only records that are **data without a metadata model**,
and deliberately so: who issued a credential is its only dimension a reader
needs, and that is already the group heading with the issuer's brand mark on
it — a tag would restate the heading on every row. `icon` is a bare filename;
the renderer builds `images/icons/<icon>`.

The two files key their groups differently, on `issuer` and on `platform`, and
one renderer takes the field name as an argument. An issuer examined the holder;
a platform hosted the lessons. One noun for both would let a Udemy course borrow
a MuleSoft certification's authority — the same distinction `publisher` and
`platform` make on Research.

Whether a link is marked external is **derived from its URL**, never declared: a
Credly badge is the issuer's own record and gets `.link-external`, while
`data/DP-300.png` is a scan this site serves and renders as a plain link, so the
external marker keeps meaning *checkable at the source*. The rule for adding a
row is that the link must be the issuer's record of the credential — a
course's catalogue page is not evidence anyone completed it. Full rationale in
[career.md](career.md).

### Adding a Selected Impact line

`src/data/impact.json`. This is the only block on the site that restates facts
held on other pages, so it is the only one that can contradict them:

```json
{
  "figure": "&euro;1,400 per month saved",
  "evidence": "Azure spend removed through automated resource-scheduling scripts, with no loss of availability.",
  "source": "career.html"
}
```

`source` is required and names a real page; the link text (*Career*) is read
from `site.json`'s navigation rather than typed, so a citation cannot say
*Projects* and point at Awards, and `check.py` fails the build if the page does
not exist. The figure itself stays hand-written — deriving it would mean parsing
a prose bullet — which makes it an **editorial** rule: every figure here is
evidenced on the page it links to, and the figure and that record move in the
same change or neither does.

This block is why the rule exists. The front page read *2 plugins accepted
upstream / both listed in the official Kanboard plugin directory* while
`projects.json` had both pull requests still `open` — two pages of one site
disagreeing, with the overstated version on the page a visitor reads first. It
now reads *2 plugins authored and submitted upstream*, in the same vocabulary
`UPSTREAM_STATES` uses on Projects. A second line had drifted the same way: a
regional contest was described as *national*, where `awards.json` says
`"scope": "Regional"`.

### Adding a volunteering record

`src/data/volunteering.json`, with `organisation`, `branch`, `period` and
`summary`. No metadata model — there is nothing a reader needs that the four
lines do not say — but it is an `.entry`, and every `.entry` on the site comes
from data. One hand-written record is how the second one gets hand-written too.

**Skills and Languages stay as markup in `src/pages/index.html`**, and that is
the rule rather than an omission: a list stays in its page fragment when that
page is the only place its facts live, and becomes data when it restates facts
held elsewhere. Nothing else on the site states a proficiency level, so moving
those `dt`/`dd` pairs into JSON would buy a build step and no guarantee.
[DESIGN.md §10](DESIGN.md) has the full boundary.

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

**[workshops.md](workshops.md)**, **[teaching.md](teaching.md)**,
**[research.md](research.md)**, **[writing.md](writing.md)**,
**[projects.md](projects.md)** and **[career.md](career.md)** are that
convention applied to a block each: the declared categories for the record, why
they are in that order, the permitted value for each, and what deliberately
stays out of the model. `teaching.md` also covers the three rules the third
model forced into the open — when to reuse another model's category instead of
inventing one, why a category holds exactly one value, and why a fact that is
true of every record on a page belongs to the page rather than to the records.
`research.md` adds the fourth: a category whose values are a progression —
*In Progress*, then *Published* — still takes one treatment, because the colour
names the category and never grades the value. `writing.md` adds the fifth, the
converse of the reuse rule: two categories that occupy the same position and
share a treatment still need separate names when they make different claims,
which is why *Elsevier* and *Medium* are `publisher` and `platform` rather than
one category with two values. `projects.md` adds the sixth, which is rule 4
tested against a live temptation: a pull request that has not been merged takes
the same amber as one that has, states which it is in words, and links to
itself so the claim can be checked — the earlier hand-written page had styled
it success-green instead, asserting in colour what the work had not yet earned.
`career.md` adds the seventh and eighth. A model may hold a **single**
category — Education declares only `accreditation`, because the degree, the
institution and the years are already on the record and a category that
restates one of them is padding. And a set of records may be data with **no**
model at all: certifications and courses group by issuer, which is the only
dimension they have, so the `.issuer` heading carries it and no tag repeats it.
It also documents the last loose-chip run on the site — the Career page's
per-job technology tags — and why a varying-length run with one accented
"important" value broke both the one-value rule and rule 4.

`awards.md` doubles as the model document for its own page, since the
convention was generalised from it: the Awards declaration, the
Competitions/Hackathons split, and the editorial rule that a contest bullet
states the score and nothing else all live there.

## Credits

Originally forked from [elyesmanai.github.io](https://github.com/elyesmanai/elyesmanai.github.io);
theme lineage [orderedlist](https://github.com/orderedlist). The current design
system, markup and build are original work.
