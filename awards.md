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
Label  figure   Label  figure  measurements, side by side
- point                        what was actually done
- point
```

The tags carry **metadata**; the bullets carry **substance**. A fact stated by
a tag is never repeated in a bullet. That split is what makes an entry
skimmable in a few seconds and readable in full if the reader chooses.

**The third layer is newer and is the one this page needed.** A tag files a
record under a category and a bullet says what was done, and a *measurement* is
neither: `8 / 8` is not a filing category and it is not a sentence. Awards is
the only user today, through `.perf` (see the performance spec, below).

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
Order:  placement → distinction → scope → scale → duration → track → stack

  placement    where the entry finished          1, 2, 13, "Quarter-finalist"
  distinction  notable stage or honor            "National Finalist"
  scope        how far the field reached         "Regional", "National",
                                                 "African", "International"
  scale        how large the field was           "7,094 teams", "86 teams", "200 teams"
  duration     how long the event lasted         4, 5, 24, 48  (integer hours)
  track        event focus / topic area          "GenAI for Healthcare"
  stack        what the record was built with    ["FastAPI", "Pydantic", "Jinja2"]

Appended after the model's tags, as a utility tag:

  dataset          the data the work ran on      a URL
  dataset_label    what that data is called      "Stroke Prediction"

Beside the tags, not among them:

  summary      one or two framing sentences    "Clinical records are written
                                                for clinicians. ..."

  performance  the score and the team size       {"solved": 8, "problems": 8, "team": 2}
```

The order is defined once, in `MODELS["awards"]` in `tools/build.py`.

**`placement` first**, because it is the primary ranking metric. **`distinction`
second**, highlighting stage honors like *National Finalist*. **`scope` third**,
as the qualifier on how far that result reaches. **`scale` fourth, and quiet**:
field size legibility. **`duration` and `track`** provide situational context
for hackathons. **`stack` last, and it has to be**: it renders one chip per
tool, so it is the one category whose length varies, and `render_meta` states
the condition plainly, that a run of variable length sits after every category
read positionally.

**`type` is not in the model any more.** See [One model, two blocks](#one-model-two-blocks).

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `placement` | Integer, or a string for a stage rather than a rank. The renderer turns `1` into `1st Place` and `1432` into `1,432nd Place`; `"Quarter-finalist"` passes through |
| `scope` | `Regional` · `National` · `African` · `International` |
| `scale` | `{"count": 7094, "unit": "teams"}` → `7,094 teams` |
| `duration` | Integer hours. `4` → `4 h`. **Never a string**: `"48h"` was the shape once, and `meta_label` spaces the unit so that `2h` and `20 h` cannot coexist |
| `track` | `"GenAI for Healthcare"` |
| `stack` | A list of tool names, one outlined chip each: `["FastAPI", "Pydantic", "Jinja2"]`. The site-wide `.tag--stack` treatment Career and Projects use, so *a thing this was built with* looks the same everywhere ([`CLAUDE.md`](CLAUDE.md) §6). Kept out of the overlay by `*.stack` in the `keep` list: a tool's name is its name in both languages |
| `dataset` | A URL, with `dataset_label` naming the data. Not a category and not in the model: it is an artefact of the work rather than a dimension of it, so it renders as a `.tag--artifact` appended after the model's tags, exactly as Projects appends its slides link. The noun comes from the `tag.dataset` chrome string, never stored beside the name, so the French reads *Jeu de données Prédiction AVC* with no second field to keep in agreement |
| `performance` | `{"solved": 8, "problems": 8, "team": 2}` → a `.perf` strip, not a tag |
| `summary` | One or two sentences of framing, rendered as `.entry__summary` between the tags and the bullets. A hackathon field: a competition has no bullets for it to introduce |

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

**The tension that came of that is resolved, and `type` is gone.** Because the
split is on `type`, every record inside a block carried a `type` tag that
repeated its heading three lines above it. By the test in
[`teaching.md`](teaching.md) (*does this distinguish this record from its
neighbours?*) it did not, and [`research.md`](research.md) had already resolved
the same situation the other way, keeping the type in the block heading and out
of the model. It went from `MODELS["awards"]` and nowhere else: the **field
stays in the data**, because `build()` still filters the two blocks on it, and
what went is the chip.

Measured on the shipped Noto Sans, `Competitive Programming` was 181px, the
widest chip on the page, on all seven competition records, and it said nothing
a reader had not read in the heading. The two `tag.type.*` strings left the
French overlay with it, and the `.tag--type` rule left `main.css`, because a
component nothing renders is what `check.py` fails the build on.

### The scope summary

The page opens on a card per scope, on the grid that carries Career's
certifications ([`DESIGN.md`](DESIGN.md) §9.4), and it is **derived, never
written**. Each card states one fact per line, in reading order: the scope,
the result, the field size it was won against, and the record that earned it.
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
result at title weight and the chips are gone.

**One fact per line, and the count of lines is a measurement.** The card ran
two lines until the type scale caught up with it. At a `12rem` track the text
measure inside a card is 192px, and *643rd Place of 7,094 teams* needs about
215px at 17px, so the line broke wherever it landed and left *teams* standing
on its own; *International &middot; IEEEXtreme 17.0* landed within a few
pixels of the same limit and orphaned the version number. French was already
worse, and the comment beside `.entries--grid--compact` in `main.css` had
recorded *Quart de finaliste sur 200 equipes* running 214px before this. A
card whose whole job is to state one result cannot state it in orphans, so the
sentence became four short lines that each hold one fact.

**The scope leads, and it is a label rather than a title.** It says which
reach the card is about before the reader spends attention on the figure, and
it is set at `.result__source`'s size and colour, so the result underneath
keeps all of the weight §9.3 gave it. The rejected shape was a scope in the
*title slot* with the result demoted to a chip, which is not what a quiet
label line above the figure does.

The four classes are borrowed rather than reinvented. `.result__figure` and
`.result__source` mean *the figure* and *where this came from*, which is what
those lines are; `.result__scope` and `.result__scale` extend the same
component the way `.result__consequence` already does, which is to say Home
renders some of it and this block renders the rest. Only `.result`'s
two-column grid belongs to Home.

**The medal disc is deliberately absent here** and stays on the record. Rule 4
keeps it because it is recognised before the label is read, which is worth a
disc once and is a double-take twice.

Three consequences, all of them rule 5 and rule 7 doing their job:

- **A scope with no record renders no card**, and neither does a missing
  field size: the National card carries a distinction earned by two records,
  no single `scale` belongs to both, so it renders three lines rather than
  four. Nothing is invented to square the shape.
- **`SCOPE_ORDER` in `tools/build.py` fixes the reading order**, weakest reach
  first. A new scope value is placed there deliberately, not wherever a sort
  puts it.
- **The International card says *643rd Place* and *7,094 teams*** and is
  meant to. [`CLAUDE.md`](CLAUDE.md) §5: a summary where every figure is
  maximally flattering is a summary nobody believes, and the honest placement
  is the one that makes the 1st above it worth reading.

**The four cards sit on one line, on a grid that is not counting them.** The
summary is the only user of `.entries--grid--compact`, which lowers the track
minimum from `18rem` to `9rem` and nothing else. At `18rem` only two tracks
fitted the document column, so the four scopes read as a 2x2 block of cards
stretched to twice the width their lines need. `12rem` held the row only above
1240px, which put the fourth card under the first at the width most readers
open the page at; that minimum had been sized for a card of two long lines,
and the longest line on the card is now *of 7,094 teams* at 14px. The
reasoning, including why the base grid keeps `18rem` for the certifications
card and why this is a track minimum rather than a hardcoded four, is in
[`DESIGN.md`](DESIGN.md) 9.4. Rule 5 is the reason it matters: a scope with no
record renders no card, so the row has to lay out three cards as readily as
four.

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

### The performance spec, and the sentence it replaced

A contest result is almost entirely metadata, so a competition record has **no
bullets at all**. Its four facts are fields:

```json
"duration": 4,
"performance": { "solved": 8, "problems": 8, "team": 2 }
```

`duration` becomes a tag through `meta_label` like every other duration on the
site; `performance` becomes a `.perf` label column under the tags, rendered by
`render_performance`.

**This document used to mandate the opposite, and that is the finding.** Rule 1
here read *"State the score, duration, and team size. `Solved 8 / 8 problems in
4h (Team of 2)` is the whole bullet"*, while rule 7 above says *"Store the raw
fact and let the renderer produce the label. Hand-written labels are how `1st
Place`, `1st place` and `First` end up on the same page."* One document, two
rules, pointing opposite ways, and the page paid for it:

| | |
|---|---|
| Seven records | carried four facts welded into one prose sentence |
| Seven French strings | hand-translated the same sentence again |
| The hour unit | printed `4h` in the bullets and `48 h` in the hackathon's `duration` tag, on the same page |
| The two languages | disagreed: the French overlay had quietly corrected it to `4 h` |

`tools/build.py` already carried the argument, in the comment on `duration` in
`meta_label`: *"Stored as a number, spaced here, so `2h` and `20 h` cannot
coexist... A value formatted at the call site is a value that drifts from every
other call site."* The bullets were that call site.

Deriving the strip from fields also removed seven translated strings from the
overlay: the French now comes from `perf.problems`, `perf.solved`, `perf.team`
and the locale's own number format, so a new contest is translated the moment
it is added.

**A measurement is not a tag.** These could have been two more chip categories,
and were not: a tag says *this record is filed under X*, which a solve count is
not, and rule 3 below picks categories for the reader rather than for symmetry.
A row that already carries five chips does not need seven.

### Editorial rules for the bullets

1. **A competition has none.** Its score, duration and team size are fields.
   `tools/build.py` fails the build on a record carrying both `performance` and
   `points`, because that is a record saying one thing twice, which is how the
   sentence got there in the first place.
2. **A hackathon is the exception, and says what was built.** There is no
   problem count to state, so the bullets carry the artefact, the architecture
   and who owned which half of it, which is the substance a placement leaves
   unexplained.

   **It opens with a `summary`, and that is what the bullets are allowed to
   be sharp against.** Tightening the three bullets into *the contract*,
   *validation and fallback* and *ownership* made each of them a better
   sentence and cost the record the only thing that had ever said what the
   product was or who it was for: the retired first bullet opened *"Delivered
   an MVP transforming complex clinical diagnosis and medication data into
   patient-accessible HTML summaries"*, and nothing replaced it. That is a
   rank error, not a bullet error. `.entry__summary` is the slot
   [`DESIGN.md`](DESIGN.md) §9 fixes for framing, between the scan line and
   the evidence, and `render_award` was the only one of nine record renderers
   that never emitted it. **The summary names the product and its reader; the
   bullets say how it was built.** A summary that restates a bullet has taken
   the bullet's job.

   **Each bullet opens with its topic in bold, then a colon.** That is the
   device Projects already uses (*"`<b>Security &amp; CSP hardening:</b>`"*),
   and it is what gives three dense bullets an entry point. It also frees the
   `<b>` span for the one job it should be doing: before this, four **tool
   names** were bold inside the prose, so one page had bold meaning *this is
   the bullet's topic* on Projects and *this is a tool* on Awards, and the four
   tools competed with the record title for the darkest ink in the block.

   **A bullet that ends in a consequence hands it to `.point__impact`.**
   [`DESIGN.md`](DESIGN.md) §9.2 exists for exactly the sentence shape the
   validation bullet had, a consequence arriving in a trailing clause where
   neither reader finds it.
3. **Never restate a tag.** The field size, the scope and the rank are already
   on screen. A bullet reading "competed against 86 teams nationally" is a
   third copy of two facts. The hackathon's first bullet opened *"Delivered an
   MVP in 48h"* beside its own `48 h` tag, which was this rule being broken by
   the one record still allowed to have bullets; the duration is gone from the
   sentence and stays in the tag.

   **The rule now covers the tools and the dataset too**, because they are
   tags. `FastAPI`, `Pydantic`, `Jinja2`, `Hugging Face Inference API` and
   `Falcon` are five `stack` chips, so the bullets name none of them and read
   as architecture rather than as a list of imports. The Kaggle set was a
   hand-written `<a>` in the middle of the first sentence, carrying its own
   `target` and `rel` and **not** the `link-external` marker the teammate link
   two bullets below it did carry: one record, two inline links, two
   treatments. It is a `.tag--artifact` now and the sentence is clean.

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

## The page lede

> *Where the algorithmic reflex was built, and put under a clock.*

[`CLAUDE.md`](CLAUDE.md) §3: *"Competitions are where the algorithmic reflex
was built."* The second clause reaches the Hackathons block, which is also a
clock, so the line clears the lede test in [`DESIGN.md`](DESIGN.md) §11.1: it
speaks for both blocks and repeats neither intro.

**It names no figure, deliberately.** The scope summary sits directly beneath
it and the performance spec sits on every record; a lede quoting `8 / 8` or
`86 teams` would be the third copy of a fact, which is rule 3 one rank higher
up the page.

