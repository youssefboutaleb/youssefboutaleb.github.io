# Entry metadata convention

A reusable rule set for describing records on this site, generalised from the
validated Awards implementation.

This document defines an **information model**: what an entry states about
itself, how those statements are named, and in what order they appear. It says
nothing about how any of it looks. [`DESIGN.md`](DESIGN.md) owns that, and the
two must not be merged, see [Relationship to `DESIGN.md`](#relationship-to-designmd).

The rules here are general. [`workshops.md`](workshops.md),
[`teaching.md`](teaching.md) and [`research.md`](research.md) apply them to a
page each, and are the shorter things to read if you are adding one. The Awards
model itself is declared below, because this file is where it lives.

---

## The shape of an entry

Every record on the site (a job, a project, a paper, a course, a workshop, an
award) is the same component:

```
Title: Qualifier              identity
Period                         when
[ metadata tags ]              the facts, in a fixed order   ← this document
- point                        what was actually done
- point
```

The tags carry **metadata**; the bullets carry **substance**. A fact stated by
a tag is never repeated in a bullet. That split is what makes an entry
skimmable in a few seconds and readable in full if the reader chooses.

---

## Rules

### 1. A page declares a metadata model, up front

A metadata model is an **ordered list of named categories**. It is declared
once, for the page or record type that uses it, and every entry on that page
answers it. Categories are never invented per entry: if a fact does not belong
to a declared category, either the model is missing a category or the fact
belongs in a bullet.

### 2. Order is centralized, never per entry

The display order lives in exactly one place (the model definition) and the
renderer emits tags in that sequence. Entries are stored as data with their
fields in whatever order is convenient; no entry, page or template chooses an
order of its own.

This is the rule that stops drift. Reordering a category means editing one
line, and every entry that uses the model follows.

### 3. Categories are chosen for the reader, not for symmetry

Pick the categories a recruiter or hiring manager actually needs in order to
judge the record in a glance: typically some subset of *context, significance,
scope, scale, role, status, stack*. A page includes a category only if it
carries real information there, and it can define categories no other page has.

**Forcing every page onto one universal set is the failure mode**, not the
goal. Two pages sharing a category name should mean the same thing by it; two
pages needing different categories should have different models.

The corollary is worth stating, because it is the half that gets forgotten:
**when a page genuinely needs a category another model already defines, it
takes that category (name, meaning and treatment) rather than coining a
synonym.** Teaching reuses `format` from Workshops and `scale` from Awards for
exactly this reason. A model built only from new categories is as much a smell
as one that forces a fact into a category that does not fit.

### 4. One category, one visual treatment

Every tag in a category looks identical, and no two categories in the same
model look alike. The treatment belongs to the **category**, not to the value:
it says *"this tag is a status"*, never *"this value is good"*. A value is
therefore never given styling of its own.

Once a reader has parsed one entry, they read the rest positionally instead of
word by word, which only works if the mapping never varies.

### 5. Missing data is omitted, never invented

An entry that has nothing to say in a category renders one tag fewer. A
plausible-looking placeholder is worse than a visible gap, because a reader
cannot tell it apart from a real value.

### 6. Terminology is factual, concise and fixed

One phrasing per concept, and the phrasing lives in the renderer rather than in
the data, so it cannot drift between entries. Prefer the plain fact over the
claim: state the rank, the count, the status. Avoid promotional wording
(*Winner*, *Elite*, *Award-winning*) and anything the reader cannot verify.

Where the plain wording is genuinely weak, add a **visual signal beside it**
rather than inflating the words. (The Awards page marks its top three
placements with a small medal disc for exactly this reason; the label stays
`1st Place`.)

### 7. Values may be derived from data, not written by hand

Store the raw fact (an integer, a count, a date) and let the renderer produce
the label. `1` becomes `1st Place`; `{ "count": 86, "unit": "teams" }` becomes
`86 teams`. Hand-written labels are how `1st Place`, `1st place` and `First`
end up on the same page.

---

## The Awards model

The page these rules were generalised from, declared in the same form as the
other three so it can be read the same way.

```
Model:  awards
Order:  placement → distinction → type → scope → scale → duration → track

  placement    where the entry finished          1, 2, 13, "Quarter-finalist"
  distinction  notable stage or honor            "National Finalist"
  type         what kind of event it was         "Competitive Programming", "Hackathon"
  scope        how far the field reached         "Regional", "National",
                                                 "African", "International"
  scale        how large the field was           "7,094 teams", "86 teams", "200 teams"
  duration     how long the event lasted         "48h"
  track        event focus / topic area          "GenAI for Healthcare"
```

The order is defined once, in `MODELS["awards"]` in `tools/build.py`.

**`placement` first**, because it is the primary ranking metric. **`distinction` second**, highlighting stage honors like *National Finalist*. **`type` third**, distinguishing programming contests from hackathons. **`scope` fourth**, as the qualifier on how far that result reaches. **`scale` fifth, and quiet**: field size legibility. **`duration` and `track`** provide situational context for hackathons.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `placement` | Integer, or a string for a stage rather than a rank. The renderer turns `1` into `1st Place` and `1432` into `1,432nd Place`; `"Quarter-finalist"` passes through |
| `type` | `Competitive Programming` · `Hackathon` |
| `scope` | `Regional` · `National` · `African` · `International` |
| `scale` | `{"count": 7094, "unit": "teams"}` → `7,094 teams` |
| `duration` | `"48h"` |
| `track` | `"GenAI for Healthcare"` |

`venue` is not a category. It renders as the `.entry__role` qualifier after the
title (*TCPC 23) Tunisian Collegiate Programming Contest*, because it
expands what the title names rather than classifying the record.

### One model, two blocks

The page splits into **Competitions** and **Hackathons**. The split is a filter
on `type` in `build()`, not a second model:

```python
competitions = [a for a in awards if a.get("type") == "Competitive Programming"]
hackathons   = [a for a in awards if a.get("type") == "Hackathon"]
```

Both blocks render through `render_award` and the one `MODELS["awards"]` order,
so a reader who has learned the tag positions in the first block reads the
second without relearning them. Each block carries a one-line `block__intro`
naming what that kind of result actually shows about the person who earned it
(*Engineering background plus competitive programming edge* versus *Rapid
prototyping, product design, and fast technical delivery*), which is the fact
the two blocks exist to separate. These two lines are the reference examples
for the site-wide intro rule; see below and [`DESIGN.md`](DESIGN.md) §11.1.

> **Known tension.** Because the split is on `type`, every record inside a
> block now carries a `type` tag that repeats its heading. By the test in
> [`teaching.md`](teaching.md) (*does this distinguish this record from its
> neighbours?*) it no longer does, and [`research.md`](research.md) resolves
> the same situation the other way, keeping the type in the block heading and
> out of the model. Awards keeps the tag for now; if it goes, it goes from
> `MODELS["awards"]` and nowhere else.

### The scope summary

The page opens on a card per scope, on the grid that carries Career's
certifications ([`DESIGN.md`](DESIGN.md) §9.4), and it is **derived, never
written**. Each card leads with the result, and carries the scope and the
record that earned it on a quiet provenance line beneath.
`render_awards_summary` takes the best record in each scope and applies one
rule:

| The best record | The row says |
|---|---|
| carries a `distinction` | that distinction, counted when more than one record in the scope earned it |
| does not | its `placement` and its `scale` |

Which is why National reads *2&times; National Finalist* rather than *13th
Place*: two national finals is the fact, and the two placements are on the two
records the card lists. Every string comes out of `meta_label`, the function
that renders the tags below, so a card cannot come to disagree with the entry
it links to, and it translates with the tag vocabulary rather than with chrome
strings of its own.

**The card used to be a certifications card and it read as the page saying
everything twice.** A scope in the title slot, the winning record's own tag
chips beneath it, and a `.points` list of the records. So the Regional card
printed a gold disc, `1st Place` and `86 teams`, and the record 300px below
printed a gold disc, `1st Place`, `Competitive Programming`, `Regional` and
`86 teams`: three of the card's four facts, in the same chips, in the same
colours, inside one screen. **A projection styled identically to its source
does not read as a summary.**

The fix is the one [`DESIGN.md`](DESIGN.md) §9.3 made for Impact in Numbers,
for the same reason: *put the figure in the slot the title had.* The scope was
never the interesting half of a scope card, because a reader looking at four
cards can see they are scopes; the result is. So `.result__figure` carries the
result at title weight, `.result__source` carries the scope and its records as
provenance, and the chips are gone. Those two classes are borrowed rather than
reinvented: they mean *the figure* and *where this came from*, which is what
these two lines are, and only `.result`'s two-column grid belongs to Home.

**The medal disc is deliberately absent here** and stays on the record. Rule 4
keeps it because it is recognised before the label is read, which is worth a
disc once and is a double-take twice.

Three consequences, all of them rule 5 and rule 7 doing their job:

- **A scope with no record renders no card.** Nothing is invented to square
  the 2&times;2 shape.
- **`SCOPE_ORDER` in `tools/build.py` fixes the reading order**, weakest reach
  first. A new scope value is placed there deliberately, not wherever a sort
  puts it.
- **The International card says *643rd Place* and *7,094 teams*** and is
  meant to. [`CLAUDE.md`](CLAUDE.md) §5: a summary where every figure is
  maximally flattering is a summary nobody believes, and the honest placement
  is the one that makes the 1st above it worth reading.

The cards replaced `.awards-stats`, a bordered box that hand-formatted its own
labels; the full list of what that cost is in [`DESIGN.md`](DESIGN.md) §9.4.

### The records

Eight results, newest first, in `src/data/awards.json`:

| Result | Year | Placement | Scope | Field |
|---|---|---|---|---|
| Hello World v4.0: Sfax | 2024 | 1st | Regional | 86 teams |
| Hello World v3.0: Sfax | 2023 | 2nd | Regional | 52 teams |
| TCPC 23: Tunisian Collegiate Programming Contest | 2023 | 13th | National | 90 teams |
| IEEEXtreme Programming Competition 17.0 | 2023 | 643rd | International | 7,094 teams |
| A2SV GenAI Hackathon | 2023 | Quarter-finalist | African | 200 teams |
| TCPC 22: Tunisian Collegiate Programming Contest | 2022 | 21st | National | 80 teams |
| IEEEXtreme Programming Competition 16.0 | 2022 | 1,432nd | International | 6,376 teams |
| Hello World v2.0: Sfax | 2022 | 7th | Regional | 21 teams |

### Editorial rules for the bullets

A contest result is almost entirely metadata, so the bullets are thin by
design and there is exactly one thing worth saying in them.

1. **State the score, duration, and team size.** `Solved 8 / 8 problems in 4h (Team of 2)` is the whole
   bullet. It carries the score context, total problems, time constraint, and team size.
2. **A hackathon is the exception, and says what was built.** There is no
   problem count to state, so the bullets carry the artefact, architecture ownership,
   and model details (*Team of 2, built an MVP in 48h...*), which is the substance a
   placement leaves unexplained.
3. **Never restate a tag.** The field size, the scope and the rank are already
   on screen. A bullet reading "competed against 86 teams nationally" is a
   third copy of two facts.

---

## Defining a model for a new page

Three steps, in this order.

**1. Declare the model.** Name each category, fix the sequence, and write down
what the category means and what a value looks like:

```
Model:  <page or record type>
Order:  <category-a> → <category-b> → <category-c>

  category-a   what it tells the reader        e.g. "…", "…"
  category-b   what it tells the reader        e.g. "…"
  category-c   what it tells the reader        e.g. "…"
```

**2. Implement the order once.** The sequence goes in `tools/build.py`; the
records go in `src/data/<page>.json`, keyed by category name. The page fragment
in `src/pages/` holds the section heading and prose only, and interpolates the
rendered block. A page that hand-writes tag markup has already broken the
convention.

> Current state: `MODELS` in `tools/build.py` maps a model name to its ordered
> categories: `awards`, `workshops`, `teaching` and `research` today. A fifth
> page adds a fifth entry; it never merges its categories into an existing
> tuple, because a model that has to answer another page's questions is two
> models wearing one name. Reusing an individual *category* across models is
> the opposite and is encouraged, see rule 3 and the note below. `scale` is
> shared by Awards and Teaching for exactly that reason.

**3. Bind each category to a treatment.** Add one `.tag--<category>` rule in
`main.css` and record it in `DESIGN.md` §7. Nothing else in the markup or the
data refers to colour.

### And write the block intro as one line

The prose the fragment holds is **one sentence per block**, and it is a pitch,
not a manual. The reader is a hiring manager, a recruiter or an engineer
deciding in about a second whether to read the records below; an intro that
opens on mechanics (where a link points, what a tag means, which records were
filtered in) spends that second on plumbing. Say why the work exists and what
it shows about the person who did it, and let the records carry the evidence.

Mechanics still get written down; they get written down **here**, in the model
document, which is where someone adding a record goes looking for them. That
split is why this file can be long and every intro on the site is short.

[`DESIGN.md`](DESIGN.md) §11.1 states the full rule, the exception Teaching
earns, and what belongs in a `block__note` instead.

### Worked example

The Workshops page is the second model built this way, and the shortest
end-to-end illustration of the three steps above:

```
Model:  workshops
Order:  format → mode → audience → host

  format     what kind of session it was      "Workshop", "Hands-on Lab"
  mode       how it was delivered             "On-site", "Online"
  audience   who was in the room              "Engineering Students"
  host       who ran it                       "Securinets ENIS"
```

```json
{
  "title": "Introduction to Competitive Programming",
  "year": "2023",
  "format": "Workshop",
  "mode": "On-site",
  "audience": "Engineering Students",
  "host": "IEEE Student Branch ENIS",
  "points": ["Complexity analysis first: reading a problem's constraints …"]
}
```

A record with nothing to say in a category renders one tag fewer, in the
declared order, and nothing is invented to fill the gap. A further page needing
different categories declares its own model; it does not borrow this one
wholesale, though it may reuse individual categories from it.
[`workshops.md`](workshops.md), [`teaching.md`](teaching.md) and
[`research.md`](research.md) carry the full declarations and the editorial
rules that go with them.

---

## Relationship to `DESIGN.md`

Two documents, one boundary: **meaning versus appearance.**

| | [`DESIGN.md`](DESIGN.md) | `awards.md` (this file), [`workshops.md`](workshops.md), [`teaching.md`](teaching.md), [`research.md`](research.md), [`skills.md`](skills.md) |
|---|---|---|
| Owns | The visual and structural system | The information model |
| Answers | *What does a tag look like?* | *What does an entry state, and in what order?* |
| Contains | Type scale, colour, spacing, components, `.tag--*` treatments, accessibility | Category declaration, ordering, terminology, data-vs-markup rules |

They meet at exactly one point: a category name binds to a `.tag--<category>`
rule. This document names the categories; `DESIGN.md` styles them.

Read `DESIGN.md` before adding a component. Read this before adding a page of
records.
