# Portfolio design system

The reference for every visual and structural decision on this site.
The implementation lives in [`assets/css/main.css`](assets/css/main.css); this
document explains the reasoning so the system can be extended without drifting.

Its companion is [`awards.md`](awards.md), which owns the *information* model:
what a record states about itself and in what order (with
[`workshops.md`](workshops.md) and [`teaching.md`](teaching.md) declaring the
models built on it). This document owns how any of that looks. The two meet at one point — a metadata category name binds to a
`.tag--<category>` rule — and neither restates the other.

---

## The brief

Classic, restrained, academic. This site descends from the orderedlist
**Minimal** theme by way of [elyesmanai.github.io](https://elyesmanai.github.io/),
and that lineage is the design — a sticky identity rail on the left, a plain
document on the right, one typeface, one blue for links, hairlines for
structure.

**What this system changes is discipline, not style.** The original look was
hand-tuned page by page, which is why it had drifted: three different contact
blocks, one section rule that existed only on the Projects page, icons squashed
by percentage widths. Everything below reproduces that look from tokens and
named components, so it stays consistent as the site grows.

### Explicitly out of scope

These were considered and rejected as wrong for the register:

- Uppercase letterspaced eyebrow labels
- Large display numerals for metrics
- A second (serif or display) typeface
- Filled or outlined buttons in the content flow
- Cards, tinted panels, drop shadows on content
- Hover animations, scroll effects, entrance transitions

If a future addition needs one of these, the addition is probably wrong.

---

## Principles

1. **A document, not an interface.** Structure comes from headings, bullets,
   hairlines and whitespace. A reader should be able to print the page and lose
   nothing.
2. **Coherence over novelty.** One type scale, one spacing scale, one accent,
   one content component. A new page is assembled from parts that already exist.
3. **Credibility before persuasion.** Claims carry a number and a link to where
   the number can be checked.
4. **Timeless over current.** Nothing here should look dated in five years,
   because none of it looks current now.
5. **Restraint in motion.** Interaction is acknowledged with colour and an
   underline, never performed.
6. **Single source of truth.** Every literal is a token; every shared region of
   markup is generated from one template. Duplication is a defect.

---

## 1. Typography

**One family: Noto Sans**, self-hosted (woff2 / woff / ttf), in **two weights
only — 400 and 700**. The family ships no others, so any 500 or 600 would be a
synthesised fake. Emphasis comes from weight, colour and size.

A second typeface was the single biggest thing that tipped an earlier draft out
of register: a serif for titles reads as *magazine*, not as *academic page*.

| Token | Size | Use |
|---|---|---|
| `--text-xs` | 11px | Tags |
| `--text-sm` | 12px | Dates, "last update", footer |
| `--text-md` | 13px | Navigation, sidebar, contact |
| `--text-base` | 15px | Body copy |
| `--text-lg` | 16px | Page lede, entry titles, sidebar headings |
| `--text-xl` | 18px | Section headings (`h3`) |
| `--text-2xl` | 24px | Page title (`h1`) |
| `--text-3xl` | 28px | The name in the sidebar |

These are the original theme's proportions with **one change: body copy moved
from 14px to 15px.** That step is the whole accessibility argument and costs
nothing visually.

Line height: 1.2 for headings, 1.45 for short-measure text, 1.6 for prose.
Prose is capped at `--measure` (74ch).

### Heading ramp

The theme's signature is a *stepped* grey ramp — each heading level one notch
lighter than the one above:

| Level | Colour | Role |
|---|---|---|
| `h1` / the name / `strong` | `#222222` | Strongest |
| `h2` / page title | `#393939` | Page-level |
| `h3` / section headings | `#494949` | Section-level |
| Body | `#373737` | — |

Note that body text is *darker* than `h3`. That is not a mistake; it is the
original ramp and it is why the page reads calm rather than shouty.

## 2. Colour

One grey ramp and one blue. Nothing else may be introduced.

- **Links** — `--blue-600` `#267cb9`, the theme's blue (4.6:1 on white, AA).
  Hover is `--blue-800` `#006699`.
- **Rules** — `--rule` `#e5e5e5` for structural hairlines, `--rule-soft`
  `#eaeaea` for the lighter underline beneath section headings.
- **Muted text** — the theme's `#777` was darkened to `#6b6b6b`, the smallest
  change that clears AA at 12px.

**Semantic layer.** Components address `--color-text`, `--color-heading`,
`--color-link`, `--color-border` and so on — never a primitive. Re-theming
means editing one block. `tools/check.py` fails on an undefined token and
reports any token nothing consumes.

**Status colours** exist for tags alone — see §7.

Light-only, and it prints cleanly. Dark mode is deliberately deferred: the
brand logos in `images/icons/` are fixed-colour SVGs that would each need a
treatment, and half-solving it is worse than not solving it.

## 3. Spacing

Built around the theme's **20px block rhythm** rather than a generic 8pt grid,
so the vertical texture of the original page survives:

`--space-1` 4 · `--space-2` 8 · `--space-3` 12 · `--space-4` 16 ·
**`--space-5` 20** · `--space-6` 32 · `--space-7` 40 · `--space-8` 60

`--space-5` is the default bottom margin on every block-level element.
`--space-7` is the column gap and the separation between sections.

## 4. Layout & containers

`--container-max` 1120px at `--container-fluid` 95%, holding a fixed
`--sidebar-width` 280px rail and a fluid content column, `--column-gap` apart.

The rail is sticky and scrolls independently, so identity, credentials, the CV
link and contact details stay reachable from anywhere in a long document —
the most useful thing a portfolio can do for someone reading it in order to
get in touch.

## 5. Borders, radius & elevation

`--radius-sm` 3px (tags), `--radius-md` 5px (code blocks), `--radius-full`
(portrait only).

**The system is flat.** There is exactly one shadow token,
`--shadow-portrait`, applied to exactly one element. Content is never lifted.
Separation is a 1px hairline.

## 6. Iconography

Brand logos arrive in wildly different aspect ratios — square, 2500×1184
wordmarks, 412×800 portraits. **Every icon renders inside a fixed square box
with `object-fit: contain`** via `.icon` plus a size modifier (`--xs` 12,
`--sm` 15, `--md` 18, `--lg` 32). This is the rule that keeps logos
undistorted and optically aligned. Icons are never sized inline; the original
sized social marks with `width="15%"`, which is why they never lined up.

Decorative icons take `alt=""`; an icon that is the only content of a link
carries that link's accessible name in its `alt`.

## 7. Tags

The one addition to the classic vocabulary, and the one piece of colour on the
page. Tags **classify**; they never decorate. There are two families.

### 7.1 Metadata tags — one treatment per category

A record describes itself through a fixed, declared set of metadata categories
rendered in a fixed order. **That model — which categories exist, what they
mean, what order they take — is defined in the model documents
([`awards.md`](awards.md), [`workshops.md`](workshops.md),
[`teaching.md`](teaching.md), [`research.md`](research.md),
[`writing.md`](writing.md), [`projects.md`](projects.md),
[`career.md`](career.md)), not here.** What belongs here is the single
visual rule that makes it work:

> **The treatment belongs to the category, never to the value.** Amber does not
> mean "good", it means *this tag is a placement*. That is what lets a tag list
> be read positionally after the first record instead of word by word — and it
> is why a value may never be given styling of its own.

Every declared category therefore binds to exactly one `.tag--<category>` rule.
There is one model per record type. The eight in use today:

**Awards** — declared in [`awards.md`](awards.md)

| Variant | Colour |
|---|---|
| `.tag--placement` | Amber (+ medal disc, below) |
| `.tag--type` | Blue |
| `.tag--scope` | Violet |
| `.tag--scale` | Grey, regular weight |

**Workshops** — declared in [`workshops.md`](workshops.md)

| Variant | Colour |
|---|---|
| `.tag--format` | Blue |
| `.tag--mode` | Violet |
| `.tag--audience` | Amber |
| `.tag--host` | Grey, regular weight |

**Teaching** — declared in [`teaching.md`](teaching.md)

| Variant | Colour |
|---|---|
| `.tag--level` | Amber |
| `.tag--workload` | Blue |
| `.tag--scale` | Grey, regular weight — *the same rule as Awards* |

**Research** — declared in [`research.md`](research.md)

| Variant | Colour |
|---|---|
| `.tag--status` | Amber |
| `.tag--authorship` | Blue |
| `.tag--publisher` | Grey, regular weight |

**Writing** — declared in [`writing.md`](writing.md)

| Variant | Colour |
|---|---|
| `.tag--format` | Blue — *the same rule as Workshops* |
| `.tag--reach` | Violet — *the same hue as Awards' `scope`* |
| `.tag--platform` | Grey, regular weight |

**Projects** — declared in [`projects.md`](projects.md)

| Variant | Colour |
|---|---|
| `.tag--upstream` | Amber, and carries a link to the pull request |
| `.tag--kind` | Blue |
| `.tag--stack` | Grey, regular weight |

**Experience** — declared in [`career.md`](career.md)

| Variant | Colour |
|---|---|
| `.tag--domain` | Blue |
| `.tag--stack` | Grey, regular weight — *the same rule as Projects* |

**Education** — declared in [`career.md`](career.md)

| Variant | Colour |
|---|---|
| `.tag--accreditation` | Grey, regular weight, and carries a link to the accrediting body |

`status` is the sharpest illustration of the rule above. *Published* and *In
Progress* take the **same** amber, because the treatment says *this tag is a
status* and never *this status is the good one*. The hand-written version of
the Research page gave *Published* a green and *In Progress* an amber, which
read as a verdict on the record rather than as a category — and would have made
the tag unreadable positionally the moment a third status appeared.

`scale` is borrowed rather than added: it means the size of the group a record
involved wherever it appears — `86 teams`, `12 students` — so it keeps one
name, one meaning and one rule across the models that use it. A shared name
that meant two different things would be the defect; a shared name that means
one thing is the system working. `format` is borrowed on the same terms: on
Workshops and on Writing alike it names the shape the deliverable takes — a
`Hands-on Lab`, a `Configuration Guide` — so it too keeps one rule.

`reach` is the reverse case done right: a **new name** on a **reused hue**.
Violet is what this system already spends on how far something travelled —
`scope` for an award, `mode` for a room, `reach` for an article — so a reader
who has learned the mapping anywhere reads it here without being taught again.
The hue was not picked for the category; it was already the answer to the
question the category asks. Reuse the *treatment* whenever the question is the
same; reuse the *name* only when the answer means the same thing.

`publisher` and `platform` are the reverse test, and the reason the Research
page's two blocks do not share a model. Both sit last, both are grey, and both
answer *who stands behind this* — but *Elsevier* peer-reviewed the work and
*Medium* hosted it, which are not the same claim, so they take separate names.
The shared treatment is what lets a reader scan the page and find the answer in
the same position both times; the separate names are what stops the second
block borrowing the first block's authority. Reuse a category when the meaning
is identical, never when only the position is.

**No two categories in one model may share a treatment.** Two *different*
models may reuse a hue, because they are never read side by side — a reader
learns the mapping per page, from the first record. What breaks the system is
ambiguity within a single tag list, not across the site. Adding a category
means adding one row here and one rule in `main.css` — never a colour decision
inside a page.

`.tag--scale`, `.tag--host`, `.tag--publisher`, `.tag--platform`,
`.tag--stack` and `.tag--accreditation` are the metadata tags at regular
weight: a field size, a cohort size, the organisation that ran the room, the
house that published the paper, the site that hosts the article, the tools a
project is built from, the body that accredits the degree. All are context for
the record rather than claims of their own, so the eye lands on the categories
before them first.

`accreditation` is the newest member and the one that had to be *moved* into
the family. The hand-written Career page gave it `.tag--success` — the green
below, reserved for *verified / published / shipped* — which graded the value
instead of naming the category, and borrowed a utility treatment for a
dimension of a record. It answers the same question `publisher`, `host` and
`platform` answer, so it takes their treatment and keeps its own name.

**A metadata tag may carry a link without changing colour.** Two categories do:
`upstream` points at the pull request and `accreditation` at the accrediting
body, and in both cases the destination is the evidence for the claim the tag
makes, so the tag is the route to it. One is amber and one is grey, which is
the rule working — the link is a destination, not a kind, so it changes
nothing about the treatment the category already had.
Utility tags such as `.tag--critical` on a slide deck link for the different
reason that the artefact *is* the tag.

**A category holds one value.** An earlier draft of the Teaching model gave
`stack` a list of tool names, rendering one tag per tool. It was removed: a run
of tags whose length changes per record destroys the positional reading the
fixed order exists to provide, and a tool name means more beside the thing it
was used for than it does in a row. Technologies are now named inside the
syllabus module that teaches them.

The hand-written Career page was the last place that rule was broken, and it
broke it twice in one tag list: three to five loose technology chips per job,
with the headline tool given `.tag--accent` and the rest `.tag--neutral`. The
varying length meant no column existed to read down, and the accent graded a
*value* — *Talend is the important one* — which is the thing rule 4 forbids.
Both are gone; the tools render as one `stack` tag, in the order they mattered.

**Medals.** First, second and third place carry a small struck-metal disc
(`.medal--gold` / `--silver` / `--bronze`) before the label. It exists so the
top results are recognised *before* the text is read, and it is what makes
wording like "Winner", "Champion" or "Runner-up" unnecessary — the label stays
factual and the medal does the signalling. The disc is drawn in CSS, sized in
`em` so it tracks the type, `aria-hidden` because the text beside it already
says "1st Place", and forced through to the printer because greyscale would
lose the one thing it encodes.

### 7.2 Utility tags — single facts

For the things that are not dimensions of a record. Written by hand where they
apply; no ordering rule, because they do not form a sequence.

| Variant | Meaning | Example | In use |
|---|---|---|---|
| `.tag--neutral` | Factual context | `Azure`, `Graduate Level` | — |
| `.tag--accent` | Role or category | `Instructor` | — |
| `.tag--success` | Verified, published, shipped | `Article on Medium` | Projects |
| `.tag--honor` | Distinction or pending status | `In Progress` | — |
| `.tag--critical` | Downloadable artefact | `Slides (.pptx)` | Workshops |

Violet is the only hue this system added, and it was added for scope alone: it
had to be unmistakable beside the blue that a record's type carries, without
borrowing the green that means *verified* or the red that means *download*.

**Three of the five currently have no markup using them**, and `check.py`
reports that as a note rather than a failure. It is the expected end state, not
neglect: `.tag--neutral`, `.tag--accent` and `.tag--honor` were what the
hand-written pages reached for whenever a record had a fact and no category to
put it in — `Azure` on a job, `Instructor` on a course, `In Progress` on a
paper. Every one of those facts is now a declared category on a model, which is
the point of §7.1. The rules stay because a genuine one-off will appear again;
what may not happen is a page reaching for one *instead of* declaring the
category it needs.

## 8. Interactive states

Every interactive element defines rest, hover and `:focus-visible` (2px blue
outline, 2px offset).

Links get colour plus an underline on hover — **never a weight change**. The
original's `a:hover { font-weight: bold }` reflowed the sentence under the
cursor.

There are no buttons in the content flow. The CV is a plain link under a
"Downloadables" heading, as it was.

## 9. Content records

One component, `.entry`, is used for every record on the site: a job, a
project, a paper, a course, a workshop, an award. It is a **bulleted list
item**, exactly as the original CV pages were written by hand:

```
• Title — Role                    .entry__title / .entry__role
  Aug 2024 – Present              .entry__period   (italic, muted)
  [tags]                          .tag-list        (§7, fixed order)
  – point                         .points
  – point
```

The tags carry the record's *metadata*; the bullets carry its *substance*. A
fact stated by a tag is not repeated in a bullet — "1st Place" and "86 teams"
are the tag list's job, so the bullets are free to say what was actually done.

**Records are stored as data, not markup — whether or not they carry a
metadata model.** Every file in `src/data/` holds records; the matching
fragment in `src/pages/` holds only the section heading and its intro, and
interpolates the rendered block. This is what makes the ordering and colour
rules structurally true rather than a convention someone has to remember.
[`awards.md`](awards.md) states the rules a new page follows to do the same;
[`workshops.md`](workshops.md), [`teaching.md`](teaching.md),
[`research.md`](research.md), [`writing.md`](writing.md),
[`projects.md`](projects.md) and [`career.md`](career.md) are the worked
models.

Certifications, Online Courses and Volunteering are the case that shows the two
halves are separable: they are data (`src/data/certifications.json`,
`src/data/courses.json`, `src/data/volunteering.json`) and they carry **no**
metadata model. Who issued a
credential is its only dimension a reader needs, and that is already the
`.issuer` heading the group sits under — so a tag would restate the heading on
every row. [`career.md`](career.md) §3 has the reasoning. Volunteering is a
single record and still comes from data, because one hand-written `.entry` is
how the second one gets hand-written too. §10 draws the matching line for
`.deflist` content, which does *not* all become data.

Optional `.entry__group` subdivides a long record (Data Integration / Cloud &
Security / Observability) and is emitted by one helper, `render_group`, shared
by a job's disciplines and a course's syllabus modules. `.issuer` heads a
credential group with its brand mark.

Entries are **never boxed**. A CV is a document, not a feed of cards.

## 10. Definition lists

`.deflist` handles all "category: values" content — skills, languages, impact.
The original wrote these as `<li><b>Label:</b> values</li>`: correct on screen,
but the pairing lived only in the punctuation.

`.deflist` renders **identically** — bullet, bold label, colon, values, all on
one line — while being a real `<dl>`. The `.deflist__item` wrapper `<div>` is
valid inside a `<dl>` and is what lets a `dt`/`dd` pair share one list marker.

### When a list is data and when it is markup

§9 settles it for `.entry`: those are records and always come from `src/data/`.
A `.deflist` is the case that needed a rule of its own, because Skills,
Languages and Selected Impact are the same component doing two different jobs.

> **A list stays in its page fragment when that page is the only place its
> facts live. It becomes data when it restates facts held elsewhere on the
> site.**

Skills and Languages are the sole source of truth for what they say. Nothing
else on the site claims a proficiency level, and moving eight `dt`/`dd` pairs
into JSON would buy a build step and no guarantee.

Selected Impact is the opposite and the reason the rule exists. Every line in
it is a second telling of a record on another page — a saving from a job, a
placement from a contest, a pull request from a project — so it is the one
block that can quietly contradict the site it sits on. It did: the front page
read *2 plugins accepted upstream, both listed in the official directory* while
`projects.json` had both pull requests still `open`, and the promotional
version was the one a visitor read first. The records now live in
`src/data/impact.json` beside what they summarise, each with a mandatory
`source` page whose link text is read from the navigation in `site.json`, so a
citation cannot name one page and point at another.

The figure itself is still written by hand, and deliberately: deriving
"€1,400 per month" would mean parsing a prose bullet, and a parser that guesses
is a worse liar than a person who checks. That half is an editorial rule, and
it is stated in the fragment directly above the block.

## 11. Page structure

Every page is the same stack:

```
page-header   h1 + optional lede
block         h3 (underlined) + optional intro + entries or deflist
              + optional note                                        ← repeated
```

Each page has exactly one `<h1>` — its own title. The site name in the rail is
a link styled to the old `h1`'s size, not a heading, so every page gets a
unique document outline. Enforced by `tools/check.py`.

### 11.1 Section intros — one line, and it is the pitch

**A `block__intro` is a single punchy line.** One sentence, no second sentence,
no conversational run-up, no explanation of how the block works.

The intro is the one place on the site that is allowed to *sell*. The people
who read this page are a hiring manager, a recruiter and an engineer, in that
order, and each of them decides in a second whether the block below is worth
their attention. An intro that opens with mechanics — where a link points, what
a tag means, which records were filtered in — spends that second on plumbing
nobody asked about, and the block loses the reader before its first record.

So the intro says **why this work exists and what it shows about the person who
did it**; the records below it carry the evidence. The reference pair is
Awards:

> Competitions — *Engineering background plus competitive programming edge.*
>
> Hackathons — *Rapid prototyping, product design, and fast technical delivery.*

This does not soften Principle 3, *credibility before persuasion*. The intro
persuades **once**, in one line, and every claim underneath it still carries a
number and a link to where the number can be checked. A pitch that the records
cannot back is a defect, not a stronger pitch.

Rules:

1. **One sentence.** If it needs a semicolon it is probably still one line; if
   it needs a full stop and a second clause, cut the second clause.
2. **No mechanics.** *"Each entry links to the issuer's own record"*, *"a pull
   request tag says whether it was merged"*, *"author names link to Scholar"* —
   all true, all obvious on sight, none of it earns the first line of a block.
   Mechanics that genuinely need stating go in the model document for the page.
3. **No per-record facts.** A fact true of one record is a tag or a bullet on
   that record (§7, §9). The intro speaks for the whole block or it does not
   belong there.
4. **Dated or hedged facts go in a `block__note`**, below the records — see
   §11.2. They are provenance, and provenance is a footnote.
5. **Write it as a person, not as a résumé.** Curiosity, effort and intent are
   the point; "leveraged", "demonstrated" and "consistent track record of" are
   the register this whole site exists to avoid.

**The one exception** is Teaching, whose intro is a `ul.points.block__intro` of
four labelled facts (appointment, workload, language, assessment) rather than
prose. Those are constants true of every course on the page, and a reader
scans them positionally exactly as they scan the tags on the records below —
the same argument §9 makes for tags. [`teaching.md`](teaching.md) owns the
reasoning. A second such exception needs the same argument made in writing
first; prose intros get no exceptions at all.

### 11.2 `block__note` — the dated footnote

Some figures come from a source that does not refresh them. A note in
`--text-sm` muted ink, placed **after** the records, carries their provenance
and an explicit *as of* date, so the intro is not forced to hold a disclaimer.
Research → Technical Articles is the only user today: Medium's view and read
counts are hand-copied, and the counts and that date move in one change or
neither does ([`writing.md`](writing.md)).

A note is for provenance and dating. It is not an overflow bin for the
sentences the intro rule removed.

## 12. Navigation

The original rendered this as a `<table>` row, which meant the site's real
tables inherited its styling and **no page could show which one you were on**.
`.nav` keeps the look — evenly distributed links over a hairline — as a list,
with `aria-current="page"` rendered as bold ink.

## 13. Responsive behaviour

| Breakpoint | Change |
|---|---|
| >960px | Two columns, sticky rail |
| ≤960px | One column; the rail becomes a centred band above the document (the theme's own breakpoint) |
| ≤720px | Padding tightens; nav items shrink-wrap |
| ≤480px | Navigation scrolls horizontally, bleeding to the viewport edges so the affordance is visible; type steps down |

## 14. Motion

A single `--duration` of 150ms, on colour and opacity only. Fully disabled
under `prefers-reduced-motion: reduce`.

## 15. Accessibility

- Skip link to `<main>`.
- Landmarks: rail `<header>`, `<nav aria-label="Primary">`, `<main>`.
- One `<h1>` per page; every block labelled with `aria-labelledby`.
- `:focus-visible` outline on every interactive element.
- Every `<img>` has an `alt` (empty when decorative).
- Every `target="_blank"` carries `rel="noopener"`.
- Body text 15px; 11px is used only for tags, which always repeat information
  present in the surrounding prose.
- Pinch-zoom is not disabled. The removed `scale.fix.js` set
  `user-scalable=no` on iOS, violating WCAG 1.4.4.
- `prefers-contrast: more` darkens the secondary and muted ramps.

## 16. Content hierarchy

The site answers hiring questions in order:

| Question | Where |
|---|---|
| Who is this engineer? | Rail identity + Home page title |
| How do they work? | Home → Profile |
| What technologies do they actually use? | Home → Skills |
| What impact did they create? | Home → Selected Impact |
| What problems have they solved? | Career → Experience |
| What can they build? | Projects |
| How technically deep are they? | Research, Workshops, Teaching |
| Can I trust their engineering practices? | Career → Certifications (all verifiable) |
| Where can I verify their work? | Every entry links to source, badge or DOI |
| How do I reach them? | The rail, on every page |

## 17. Extending the system

1. Reach for an existing component first. `.entry` and `.deflist` cover almost
   everything on the site.
2. If a new component is genuinely needed, build it from tokens only. A literal
   in a component rule is a bug.
3. Check it against **Explicitly out of scope** at the top of this document.
4. Add it here and to `assets/css/main.css` under a numbered section.
5. Run `python3 tools/check.py` — it fails on classes used in markup but absent
   from the stylesheet, undefined tokens, inline styles and broken links, and
   reports any CSS rule or token nothing uses.

A new **metadata category** is not a new component. Declare it in the model
document for its page ([`awards.md`](awards.md), [`workshops.md`](workshops.md),
[`teaching.md`](teaching.md)), order it in `MODELS` in `tools/build.py`, give it
one `.tag--<category>` rule in `main.css`, and add its row to §7.1. Never decide
ordering or colour inside a page. Before adding one, check whether an existing
category already means what you need — reusing `format` and `scale` cost two
lines; a synonym would have cost a colour.
