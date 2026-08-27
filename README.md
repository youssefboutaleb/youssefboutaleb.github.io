# youssefboutaleb.github.io

Personal engineering portfolio: a static site with no runtime dependencies,
served directly by GitHub Pages.

## Architecture

The eight published pages share an identical head, brand bar, navigation and
footer. Those are written **once** and rendered into the pages by a build step,
so the site cannot drift out of sync with itself again.

```
src/
  site.json          identity, availability, contact details, socials, navigation
  layout.html        the page shell: head, brand bar, nav, footer
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
*.html               BUILD OUTPUT: generated, do not edit by hand
```

Deployment stays build-free: the generated `*.html` files are committed and
GitHub Pages serves them as-is. `.nojekyll` disables Jekyll processing.

**Comment `src/` freely; none of it ships.** `strip_comments` drops every HTML
comment on the way out, so a fragment can carry the argument for why a block is
shaped the way it is without spending it on the reader. Only the generated-file
banner survives, because it is the one comment addressed to somebody reading
the built file. `index.html` was 14.8% comment bytes before this, and one of
them opened *"INTERIM, awaiting the author's sentence"*.

**There is a little JavaScript, and it is all in `src/layout.html`.** Two short
inline blocks run the theme switch: one in the head that reads the stored
preference before first paint, and one at the end of the body that records a
click. Nothing else on the site scripts anything, no file is fetched, and with
scripting off the switch is not rendered and the page still follows the
reader's system scheme. Keep it that way: `DESIGN.md` §2 and `CLAUDE.md` §7
carry why a control exists here at all.

**Two things on every page are indexes of the rest, and neither is written by
hand.** The page context rail in the left margin is built by parsing each page
after it renders, so a record added to `src/data/` gains a rail entry with no
second edit. Home's *Currently* and *Impact in Numbers* blocks are projections of
records held elsewhere in the same way. If you find yourself typing a heading
into the rail, or a sentence into Home that also exists on Career, stop: the
site has a mechanism for that, and `home.md` explains it.

## Translations

**English is the source. A translation is an overlay, never a second copy.**
`src/data/*.json` holds the records in English and is not touched by
translation work; `src/i18n/<code>.json` maps strings onto them.

```
src/i18n/
  fr.json              chrome, tag vocabulary, and record overlays
  fr/pages/*.html      translated page fragments (optional, per page)
```

A locale file has five parts:

| Key | Holds |
|---|---|
| `lang`, `og_locale`, `label` | what goes in `<html lang>`, `og:locale`, and the language switch |
| `site` | overrides for `src/site.json`: role, description, last_updated |
| `strings` | chrome, navigation, months, units, tag vocabulary, page titles |
| `records` | `"<record id>.<field>": "..."`, the record prose |
| `keep`, `ordinal`, `group` | what stays in English, how ordinals are formed, the thousands separator |

**Record ids are the addresses, and they never change.** `award-tcpc-23` is
built from the English title by `with_ids`, and `impact.json`, `skills.json`,
the page context rail and every overlay key all address records by it.
Translating an id would break all four at once and silently.

**A missing string falls back to English**, and every build prints how many are
still missing and which. That leniency is the point: a half-translated page is
readable and an empty one is not. Add `"keep": ["*.title", "*.company"]` for
strings that are deliberately staying English, so the report stays worth
reading.

**Page prose is a whole fragment, not keyed strings.** A heading and a
`block__intro` are sentences with markup threaded through them. Drop a
translated copy at `src/i18n/fr/pages/awards.html` and it is used instead of
`src/pages/awards.html`. **The build fails** if it does not carry the same
anchors and the same `{{ build.* }}` blocks, because a dropped anchor breaks a
citation and a dropped block silently deletes every record under it.

**Anything generated is generated per language.** Ordinals (`1st Place` /
`1re place`), months, durations (`2 years 3 months` / `2 ans 3 mois`),
thousands separators (`7,094` / `7 094`) and the metadata tags all come from
the locale, never from a stored string. `1re` and `643e` follow one rule in
`ordinal`, so no locale enumerates placements.

### The two languages move together

**A translated string whose English original later changes fails the build.**
`src/i18n/<code>.lock.json` records the English each translation was made from;
`build.py` compares and refuses when they have diverged. So the workflow for
editing anything already translated is:

```bash
# 1. edit the English in src/data/ or src/pages/
python3 tools/build.py            # fails, naming every key that drifted
# 2. update the French in src/i18n/fr.json or src/i18n/fr/pages/
python3 tools/build.py --sync     # re-stamp: the translation has caught up
```

The lock is committed. Do not hand-edit it, and do not reach for `--sync` to
make an error go away: it asserts that you have updated the translation, and
using it without doing so is how the site ends up saying two different numbers
in two languages.

**Missing and stale are deliberately different.** A missing string falls back
to English and is counted on every build. A stale one is fatal, because it
reads as fluent, confident and wrong, in a language nobody proofreads.

To add a language: write `src/i18n/<code>.json` with at least `lang`,
`og_locale` and `label`, then rebuild. It appears at `/<code>/`, gains
`hreflang` pairs and a language switch entry, and falls back to English until
you fill it in.

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

`tools/check.py` also fails on a skipped heading level, on the same word spelled
two ways across the built pages, and on a CSS class no markup uses unless it is
declared in `STAGED_CSS` with the reason it is waiting. It notes, without
failing, any group of more than three differently-labelled links that all land
on one destination: honest when several capabilities cite one record, and the
symptom when a block of citations has nowhere precise to point.

Every run prints two lists for each non-English locale: the strings still
untranslated, and the **pages being withheld** because they are under
`MIN_TRANSLATED` different from their English source, with the percentage each
one currently measures. A withheld page is not written, is deleted if a
previous build left a copy, and is named by no `hreflang`, no language switch
and no navigation link: its nav entry points at the English URL instead. This
is what stops `/fr/career.html` shipping English prose under `lang="fr"`.

### Adding an award

Awards are data, not markup. Append a record to `src/data/awards.json` and
rebuild: the page never lists entries by hand:

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
`venue`, `placement`, `scale` and `points` are all optional: a field with no
data is left out rather than filled in.

**`short` is optional too, and every record type accepts it.** It is the label
this record shows in the page context rail, for a title too long to sit in a
240px track: `"IEEEXtreme Programming Competition 17.0"` carries
`"short": "IEEEXtreme 17.0"`. Leave it out and the rail uses the record's own
heading, which is right nearly always. It exists as data because the rail's
parser used to hold the abbreviations itself, as literal string replacements
naming two specific awards, so renaming either one here silently stopped
shortening it. The four metadata tags always render in
the order `placement → type → scope → scale`, defined once as
`MODELS["awards"]` in `tools/build.py`; see [DESIGN.md §7](DESIGN.md) for the
colour rules.

**The cards at the top of the page follow on their own.** They show the best
result in each scope, derived from these same fields by
`render_awards_summary`, so adding a record that beats the current best in its
scope moves its card with it and adding one that does not leaves it alone.
There is nothing to edit by hand, and a scope no record reaches renders no
card. A new `scope` value has to be added to `SCOPE_ORDER` in `tools/build.py`
to appear at all, which is deliberate: the reading order is a decision, not a
sort. The rule that picks each card's wording is in
[awards.md](awards.md#the-scope-summary); the grid itself is
[DESIGN.md §9.4](DESIGN.md).

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
tags (they render as the period line (`Fall 2025-2026`)) and position in the
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
never rendered: unlike Awards, which filters on `type` and then tags it, no
record here repeats the heading it sits under. `upstream` was the first of the
site's two categories whose value carries a link (`accreditation` on Education
is the other): `meta_url` builds the pull request
address from the stored repo and number, and the tag *is* the link, keeping its
category's amber. That amber is deliberate: `state` is stored raw and
`UPSTREAM_STATES` turns `open` into `Submitted upstream` and `merged` into
`Accepted upstream`, both in the same colour, because the treatment says *this
is an upstream status* and never *this one is the good one*. `stack` is a list rendered as
**one outlined chip per tool**, capped at four names. It is the site's one
category that renders a chip per value, and it is admissible because `stack` is
always the *last* category in its model, so a run whose length varies shifts
nothing before it and every earlier category still reads down its column. Full
rationale, including what the old hand-written chip runs actually got wrong, in
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
by `author_position`, which produces `Second Author`, so correcting an author
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
blocks *do* share is position: `platform` takes the quiet grey terminal slot
that `publisher` takes above it, so the reader scanning the page finds
**Elsevier** and **Medium** in the same place, in the same colour, and the
distinction is made by the layout instead of by a disclaimer. `format` is the
same category Workshops declares, reused rather than renamed.

`reach` is stored as two raw integers and rendered as one violet tag
(`723 views · 424 reads`) because the pair is the unit: views alone inflates,
reads alone hides the ratio it should be judged against. `abbreviate` prints
large figures the way Medium reports them (`3000` → `3K`), so the page never
claims more precision than its source gave it. The counts are hand-copied and
nothing refreshes them, so a `block__note` beneath the records carries an
explicit *as of* date; the figures and that date must move in the same change
or neither. A record
carries both numbers or omits `reach` entirely. Full rationale in
[writing.md](writing.md).

Where an article documents a project that has its own Projects entry, the link
goes on the *project* record as a utility tag: the article stays declared once
here and rendered once on Research.

### Adding a job

`src/data/experience.json`, rendering
`domain → engagement → mode → scale → stack`:

```json
{
  "company": "JACQUEMUS",
  "url": "https://www.linkedin.com/company/jacquemus/posts/?feedView=all",
  "role": "Data Engineer",
  "start": "2024-08",
  "location": "Paris, France",
  "domain": "Luxury E-commerce &amp; Retail",
  "engagement": "Permanent",
  "mode": "Remote",
  "scale": { "count": 150, "unit": "pipelines", "minimum": true },
  "stack": ["Azure Data Factory", "Azure Fabric", "Apache Spark", "Datadog"],
  "summary": "JACQUEMUS is a French luxury fashion house selling …",
  "home_summary": "Order, customer, product and pricing data into a medallion lakehouse …",
  "groups": [
    { "title": "Monitoring &amp; Observability", "points": [
      { "point": "Instrumented ingestion workloads with Datadog APM …",
        "impact": "Alert coverage across the 150+ job estate, so a silent failure …" }
    ] }
  ]
}
```

**A bullet gains an `id` only when Home's Impact in Numbers cites it.** The id
becomes the anchor the citation lands on, and `check.py` validates it. Four
bullets carry one today. See *Adding a Impact in Numbers line* below.

**`home_summary` exists for the newest record only, and only Home reads it.**
Home's *Currently* block is a projection of `experience[0]` after
`tenure_sort_key`: it prints the same title, dateline and tags Career prints,
then this one sentence instead of Career's eighty-word `summary` and its groups
of bullets. A record without a `home_summary` renders no sentence there rather
than falling back to `summary`, because a company description is not a Home
sentence and a silent fallback is how it would become one. Write it on the
record it summarises, never on Home. [home.md](home.md) has the rule.

Five categories, one per question the three readers actually arrive with.
`domain` is the blue substance slot: what the *data* was about, which the job
title does not say. **Values are chosen to pair**, not to be unique: JACQUEMUS
and OLIVESOFT both read `Luxury E-commerce &amp; Retail`, and REGIM and OEM
share the `Time-Series Sensor Data` stem with their setting in parentheses, so
the blue column reads as two sectors of two rather than four unrelated jobs. A
title states the role and never the contract, because `engagement` states the
contract one line below it. `engagement` is amber and is the recruiter's first
question, the one the page used to leave to be inferred from a title, which
fails on OEM because its company record has no title at all. `mode` is reused
from `workshops.json` unchanged, because *where was this delivered from* is the
same question on both pages, and it is on a CV written for remote hiring.
`scale` is reused from Awards and Teaching: the size of the thing that was run,
which used to sit mid-paragraph in the company summary where nobody scanning
reached it. `stack` is reused from `projects.json`, capped at four names and
rendered as one outlined chip per tool: the one category on the site that does,
because it is always last, so a varying length shifts nothing before it. What
the hand-written page did wrong was grading the headline tool with
`.tag--accent` and rendering chips instead of categories, and neither of those
is back.

`scale` stores one figure and an optional shape: `"minimum": true` renders
`150+ pipelines`, `"approx": true` renders `~2,000 frames/second`, and neither
renders the bare number. The two are different claims and are not
interchangeable.

`duration` stores a number of hours as an integer and `meta_label` adds the
unit, so `2h` and `20 h` cannot both exist. They did, in one document.

Add `"of"` when the figure is a share of something larger, and the chip states
both: `{"count": 20, "of": 150, "unit": "pipelines", "minimum": true}` renders
`20+ of 150+ pipelines`. The shape applies to both numbers. Use it whenever the
scope owned sits inside a system whose size is the context, because a bare
`150+ pipelines` on a record where 20+ were owned is read as the scope.

A job record carries **`context` and `summary`, not one paragraph.** `context`
is what the employer is; `summary` is what was owned inside it. They render as
`.entry__context` (muted, small) and `.entry__summary` (body copy) in that
order, so a reader scanning for the work crosses the company description rather
than reading it. Put the company in `context` and keep `summary` in the first
person.

**`engagement`, `mode` and `scale` come from the author, never from
inference.** A date range does not tell you a contract type, a location line
does not tell you a work arrangement, and rule 5 still holds: a record with no
figure to give renders one tag fewer, which is why the OLIVESOFT entry carries
no `scale`. Where an employer nests roles, a category sits on the company
record only if it is true of both: OEM states `domain` and `mode` once, and
each role states its own `engagement`, `scale` and `stack`.

Dates are stored raw as `"YYYY-MM"` and labelled by `month_year`, so `Aug 2024`
and `August 2024` cannot both appear. Omitting `end` renders `Present`: the
word lives in the renderer, because *Present* is not a date and a record that
stores one keeps claiming the job after it ends. The dateline then closes with
the length of the role in parentheses, `Feb 2024 - Jul 2024 (6 months)`,
computed by `tenure` from those same two dates so it cannot contradict them.
Never store a duration, and never add one as a tag: [career.md](career.md) §4
has both reasons. `tenure_sort_key` sorts
newest-first on `start`, not `end`, so the one record without an end date needs
no sentinel to stay on top. A role that did several separable things carries
`groups`; a short one carries a flat `points`. Full rationale in
[career.md](career.md).

A point is **either a string or a `{point, impact}` pair**. The pair renders
the consequence of the work on its own muted line beneath the bullet, labelled
`Impact:`, so what was built and what changed because it shipped are not
crammed into one sentence. Not every bullet gets one: the consequence has to be
owned by the work, name who it affects, and be answerable in an interview.
[career.md](career.md) §6 has the three tests and the worked cases where a
bullet deliberately renders bare.

### Adding a qualification

`src/data/education.json`, rendering `programme → focus → accreditation`:

```json
{
  "degree": "Computer Science Engineer&rsquo;s Degree",
  "institution": "National Engineering School of Sfax",
  "url": "https://enis.rnu.tn/",
  "location": "Sfax, Tunisia",
  "start": 2021,
  "end": 2024,
  "focus": "Data Engineering &amp; Distributed Systems",
  "accreditation": {
    "name": "EUR-ACE&reg; Accredited",
    "url": "https://www.enaee.eu/eur-ace-system/"
  }
}
```

Three categories, and **no record renders more than two**, because the model's
rule is that *a category renders only where its answer is not already in the
record's own title*. The degree renders `focus` and `accreditation`, and omits
`programme` because *Engineering Degree* is the title. The preparatory
programme renders `programme` alone, because *(Mathematics and Physics)* is
already its title and it holds no accreditation this site can point at. A
record showing one tag is the model working, not a gap to fill.

That rule is also why `field` and `level` are not categories: both would
restate the title on both records. The dateline carries location, years and
the length of the programme in parentheses, in the same shape a job uses.

`accreditation` is the site's second linked metadata tag after `upstream`, and
it is **grey**, not the success-green the hand-written page gave it. It answers
the same question `publisher`, `host` and `platform` answer (who stands behind
this) so it takes their treatment; the green was grading the
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
it: a tag would restate the heading on every row. `icon` is a bare filename;
the renderer builds `images/icons/<icon>`.

**Check a new logo's fills before you add it.** If the SVG is a single-colour
black mark, or a coloured mark carrying black ink, add it to `ICON_TREATMENT`
in [`tools/build.py`](tools/build.py) as `mono` or `plate`. Everything else
needs no entry. Nothing fails the build if you skip this: the logo simply
disappears against the dark rendering's ground, which nobody reading in light
mode will ever see. `DESIGN.md` §6 has the reasoning.

**A new certification also updates Home**, with no second edit. The
`Certified` row of Home's fact strip is `render_credential_row`, generated
from this same file: one link per issuer, in the order the file writes them,
with `&times;N` where an issuer granted more than one. That line used to be
four hand-written strings in `src/site.json` summarising these records, which
agreed with them only for as long as somebody remembered.

The two files key their groups differently, on `issuer` and on `platform`, and
one renderer takes the field name as an argument. An issuer examined the holder;
a platform hosted the lessons. One noun for both would let a Udemy course borrow
a MuleSoft certification's authority: the same distinction `publisher` and
`platform` make on Research.

Every credential row gets `.link-external`, so the arrow means *this opens away
from the page*: true of a Credly badge and of `data/DP-300.png` alike, since
both share one `target="_blank"`. The rule for adding a row is that the link must be the issuer's record of the credential: a
course's catalogue page is not evidence anyone completed it. Full rationale in
[career.md](career.md).

### Adding a skill

`src/data/skills.json`. A capability, the tools it uses, and links to the
records on this site that prove it:

```json
{
  "name": "Workflow orchestration",
  "thread": "trunk",
  "tools": ["Apache Airflow 3"],
  "evidence": {
    "certification": [
      { "text": "Airflow 3 Fundamentals", "href": "career.html#certifications" },
      { "text": "DAG Authoring", "href": "career.html#certifications" }
    ],
    "taught": [
      { "text": "Packaging & Delivery module", "href": "teaching.html#courses-taught" }
    ]
  }
}
```

Evidence kinds, rendered in this fixed order: `production` (green) →
`certification` (blue) → `taught` (violet) → `published` (amber) → `applied`
(grey). **Every entry needs an `href` to a record that already exists on the
site**: `check.py` fails the build on a citation pointing at a missing page or
anchor. The five colours are named once by the key above the block, rendered
from `PROOF_KEY` in `tools/build.py`; adding a kind means adding a row there
too, or the key stops describing the block.

The record renders in two columns: capability and standing on the left, tools
then evidence on the right. `tools` take the outlined `stack` treatment Career
and Projects use, on their own line **above** the evidence: putting them in the
same run would leave every row starting on an outlined chip and destroy the
colour-run reading. [DESIGN.md §9.1](DESIGN.md) has the layout.

`thread` is the one field set by hand, and it is a **positioning** call rather
than a rating: `"trunk"` if the capability supports the Data Engineering claim
directly, `"branch"` if it is real, proven, and supporting evidence for the
trunk rather than the claim itself. It cannot move a skill across a standing
boundary, so it never ranks a capability above the evidence it has.

Do not write a standing or a position. Both are derived: `standing()` reads
which kinds of evidence exist, and `skill_sort_key` orders the block by
standing, then `thread`, then how much evidence each skill carries. Adding a
certification is the only way to move a row up. Full rationale, including why
this is the one model whose categories may repeat and how `thread` stays out of
self-assessment, in [skills.md](skills.md).

### Adding a Impact in Numbers line

`src/data/impact.json`. This is the only block on the site that restates facts
held on other pages, so it is the only one that can contradict them. **It no
longer writes the sentence; it quotes it.** The model and the rules are in
[home.md](home.md):

```json
{
  "title": "Azure cost control",
  "cite": "jq-finops",
  "result": "Recurring saving",
  "figure": { "value": "&euro;1,400", "unit": "per month" },
  "home": true
}
```

`cite` names a bullet in `experience.json` that carries a matching `id`:

```json
{
  "id": "jq-finops",
  "point":  "Reduced <b>Azure infrastructure spend by &euro;1,400 per month</b> by …",
  "impact": "A recurring monthly saving on the platform budget, taken with …"
}
```

Three things are derived from that one id and **must not be typed**: the
sentence (the bullet's `impact` line, or its `point` text if it has none), the
period line (company and dates from the record the bullet lives on), and the
citation link (`career.html#jq-finops`, landing on the bullet rather than the
top of the page). Add an `id` to a bullet **only** when Home cites it: an anchor
nothing points at is a URL promise nobody meant to make.

**Home is the only page that renders this file**, as `.result` rows: the figure
leads, the quoted sentence follows, and a provenance line closes it.
`"home": true` is therefore required: a record without it renders nowhere.

`title` is required and **does not render**. It is the record's handle: what a
build error names, and what tells you which row you are editing.

`figure` is a pair, not a string. The value carries the bold and the unit stays
regular, the same treatment `scale` gets on four other models, and storing it
split is what stops anything having to guess where the number ends:
`&euro;1,400` and `100&times;` both defeat a leading-digit parser.

**`figure` is the only claim still typed on Home, and it is linted.**
`check_figure` fails the build unless the value string appears verbatim
(case-insensitively) in the bullet the record cites. That is a lint, not a
parser: deriving *100x faster* from prose means guessing, while asserting that
`100&times;` appears in the cited bullet costs nothing and catches the failure
that actually happens, which is a bullet edited without its figure.

**One exception, for a claim that aggregates.** The open-source line stands for
two pull requests across two project records, so no single bullet's words can
describe it. It declares `upstream_prs`, keeps a hand-written `evidence` and a
`source`, and its `result` comes from `projects.json` through the same
`UPSTREAM_STATES` table Projects renders from. The weakest state wins: a pair is
only *Accepted upstream* when both are merged.

```json
{
  "title": "Open source",
  "figure": { "value": "2", "unit": "Kanboard plugins" },
  "upstream_prs": [586, 585],
  "evidence": "Draw.io embedding and a file-attachment rework: 2 plugins now in …",
  "source": "projects.html",
  "home": true
}
```

Five things are build errors, all of them the shapes that let two copies of one
fact drift apart: a record with both `cite` and `evidence`, a record with
neither, a `cite` naming an id nothing carries, two bullets sharing an id, and a
`figure` whose value does not appear in the text it cites.

This block is why all of that exists, and it has failed in both directions. The
front page once read *2 plugins accepted upstream / both listed in the official
Kanboard plugin directory* while `projects.json` had both pull requests `open`.
After they merged, it read *submitted upstream, both open* while Projects
rendered *Accepted upstream*, so the same block spent a release
**understating** work the site could prove. A third line had drifted the same
way: a regional contest was described as *national*, where `awards.json` says
`"scope": "Regional"`.

Career used to render every record whose `source` was `career.html` as a
*Verified impact* `.specs` strip above Experience. It was deleted once the
experience model gained a `scale` tag: the tag lifts the same figure to the
same reader while sitting on the record that earned it, which left the strip
printing numbers that were already a tag and a bullet on the screen below.
[career.md](career.md) §7 has the full argument.

### Adding a volunteering record

`src/data/volunteering.json`, with `organisation`, `initiative` and `points`,
plus a date: `year` for a single edition, or `start` and `end` for a sustained
engagement, which derive the range and the duration like every other dated
record. `branch` and `url` are optional; only add a link you have actually
opened. A record with no date renders no dateline rather than an empty one.

**One record per edition.** Work that ran in two years is two records, the way
Awards holds TCPC 22 and TCPC 23. The id is built from `organisation` **and**
`year` together, because the organisation repeats and the id must not.

`initiative` is the named programme the work happened under, *Orientini* or
*COVID-19 response*. It renders on the dateline beside the year. It is not the
education model's `programme`, which means something else entirely.

**No metadata model, and that is a decision with a condition on it.** A chip
row over crisis relief reads as credential-farming, which is the one register
this block cannot survive. [career.md](career.md) §8 carries the argument and
the condition for reopening it: a second record, so there is something to
compare. Until then, do not tag the first one.

It is an `.entry` like everything else, so it is rendered from data and it
carries an id. The id is not decoration: without one a record is absent from
the page context rail, cannot be cited, and **cannot be translated**, because
the overlay addresses records by id.

It renders as the **last block on Career**, not on Home. It closed the front
page for a while, which put the least Data Engineering thing on the site in the
last position a recruiter reads; on Career it is a dated record among dated
records. [home.md](home.md) carries the move.

**Languages stays as markup in `src/pages/index.html`**, and that is the rule
rather than an omission: a list stays in its page fragment when that page is
the only place its facts live, and becomes data when it restates facts held
elsewhere. Nothing else on the site states a proficiency, so moving those
`dt`/`dd` pairs into JSON would buy a build step and no guarantee. Skills used
to be the other example and stopped being one the moment it began citing
records on other pages. [DESIGN.md §10](DESIGN.md) has the full boundary.

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
theme this site was forked from: a plain document, one typeface, one blue for
links, hairlines for structure. The theme's sticky identity rail was dropped for
a brand bar and a top navigation; [DESIGN.md](DESIGN.md) §4 records why.

Typography, colour, spacing, components, responsive behaviour and accessibility
rules (plus an explicit list of what is *out of scope*) are documented in
**[DESIGN.md](DESIGN.md)**. Read it before adding a component; almost
everything on the site is already expressible with `.block`, `.entry` and
`.tag`.

It also owns the site's one editorial rule about prose: **a `block__intro` is a
single punchy line, and it is a pitch** ([DESIGN.md](DESIGN.md) §11.1). How a
block works (where its links point, what its tags mean, which records it
filters in) belongs in the model document for that page, not in the first line
a reader sees. Figures that need an *as of* date go in a `block__note` beneath
the records instead (§11.2). Teaching is the single declared exception: its
intro states an appointment rather than making a pitch, and the specifications
that used to sit in it are a `.specs` strip beneath (§10.1).

**[awards.md](awards.md)** is its companion, covering the other half: the
information model behind an entry: how a page declares its metadata
categories, fixes their order in one place, and keeps its terminology factual.
Read it before adding a page of records. DESIGN.md defines how a tag looks;
awards.md defines what it says.

**[workshops.md](workshops.md)**, **[teaching.md](teaching.md)**,
**[research.md](research.md)**, **[writing.md](writing.md)**,
**[projects.md](projects.md)** and **[career.md](career.md)** are that
convention applied to a block each: the declared categories for the record, why
they are in that order, the permitted value for each, and what deliberately
stays out of the model. `teaching.md` also covers the three rules the third
model forced into the open, when to reuse another model's category instead of
inventing one, why a category holds exactly one value, and why a fact that is
true of every record on a page belongs to the page rather than to the records.
`research.md` adds the fourth: a category whose values are a progression
(*In Progress*, then *Published*) still takes one treatment, because the colour
names the category and never grades the value. `writing.md` adds the fifth, the
converse of the reuse rule: two categories that occupy the same position and
share a treatment still need separate names when they make different claims,
which is why *Elsevier* and *Medium* are `publisher` and `platform` rather than
one category with two values. `projects.md` adds the sixth, which is rule 4
tested against a live temptation: a pull request that has not been merged takes
the same amber as one that has, states which it is in words, and links to
itself so the claim can be checked: the earlier hand-written page had styled
it success-green instead, asserting in colour what the work had not yet earned.
`career.md` adds the seventh and eighth. A model may hold a **single**
category: Education declares only `accreditation`, because the degree, the
institution and the years are already on the record and a category that
restates one of them is padding. And a set of records may be data with **no**
model at all: certifications and courses group by issuer, which is the only
dimension they have, so the `.issuer` heading carries it and no tag repeats it.
It also documents the last loose-chip run on the site (the Career page's
per-job technology tags) and why a varying-length run with one accented
"important" value broke both the one-value rule and rule 4.

**[skills.md](skills.md)** is the ninth and the one that breaks a rule on
purpose. Its categories are *citations* rather than dimensions, so they repeat
(three certifications are three artifacts, not one dimension holding three
values) and positional reading is traded for colour-run reading, where the
fixed order makes a row's leading chip colour say whether it ever ran in
production. It is also the block that flipped sides on the data-vs-markup rule
in [DESIGN.md](DESIGN.md) §10: the moment Skills began citing records held on
other pages, the rule moved it into `src/data/`.

`awards.md` doubles as the model document for its own page, since the
convention was generalised from it: the Awards declaration, the
Competitions/Hackathons split, and the editorial rule that a contest bullet
states the score and nothing else all live there.

## Credits

Originally forked from [elyesmanai.github.io](https://github.com/elyesmanai/elyesmanai.github.io);
theme lineage [orderedlist](https://github.com/orderedlist). The current design
system, markup and build are original work.
