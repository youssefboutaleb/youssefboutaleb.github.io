# Home: Selected Impact

The block that answers *what changed because I shipped*, in the position and
the shape that make it hardest to read.

---

## Part 1: findings

### 1.1 It closes the page, behind the longest block on it

Measured from the built page:

| Block | Markup | Records |
|---|---|---|
| Currently | 1,657 bytes | 1 entry, 9 tags |
| Skills & Evidence | **12,673 bytes** | 10 skill rows, 83 tags |
| Selected Impact | 3,780 bytes | 5 entries, 15 tags |

Skills & Evidence is **3.4 times** the markup of Selected Impact and sits
directly above it. On a desktop column the impact block starts somewhere around
1,800 to 2,000px down: past two full screens.

[`home.md`](home.md) already made exactly this argument once, and stopped one
block short:

> **Currently sits above Skills & Evidence** because it is the only block that
> answers *what is this person doing now*, and a hiring manager who reads three
> blocks and leaves should have read it.

A hiring manager who reads three blocks and leaves today reads the opening,
Currently and Skills & Evidence. They never reach the block that says what
changed.

The reader sequence bounces, too. From `home.md`'s own table:

| Position | Block | Reader |
|---|---|---|
| 1 | The opening | Recruiter |
| 2 | Currently | Hiring manager |
| 3 | Skills & Evidence | Hiring manager, then **engineer** |
| 4 | Selected Impact | **Hiring manager** |

It hands off to the engineer and then comes back.

### 1.2 The hierarchy is inverted

The block is called Selected Impact. In every record, the largest and boldest
line is a **topic**, and the result is a chip:

| Element | Holds | Treatment |
|---|---|---|
| `.entry__title` | *Azure cost control* | `--text-lg` (17px), bold, heading ink |
| `.tag--figure` | *€1,400 per month* | `--text-xs` (12px), grey |

A reader scanning titles gets *Azure cost control, Pipeline observability,
Integration resilience, Signal preprocessing, Open source*: five categories, no
outcomes. The numbers are the smallest text in the record.

[`DESIGN.md`](DESIGN.md) already states the opposite principle, for `.specs`:

> The weighting is inverted from the old `.deflist` on purpose. There the label
> was the bold thing you scanned for; here the reader is scanning the
> **figures**, so the label recedes and the value carries the weight.

That is written about a teaching spec strip. It is far more true of a block
whose entire subject is results.

### 1.3 "Aug 2024 - Present" renders three times on Home

Five of the six `.entry__period` lines on the page are inside this block:

```
Paris, France · Aug 2024 - Present (2 years)     ← Currently
JACQUEMUS · Aug 2024 - Present                   ← Impact
JACQUEMUS · Aug 2024 - Present                   ← Impact
OLIVESOFT · Feb 2024 - Jul 2024                  ← Impact
OEM ENGINEERING S.A.R.L · Jun 2022 - Aug 2022    ← Impact
2026                                             ← Impact
```

The dateline is generated, so it cannot go stale. It is still the same fact
three times on one page, and the two adjacent JACQUEMUS rows read as a
repetition rather than as two results.

### 1.4 The `source` tag says "Career" four times

Four of five rows end in an identical grey chip reading *Career*. It links, and
that matters, but the label carries nothing: the period line above it already
names the company. One column of the tag row is noise in 80% of rows.

### 1.5 The intro hard-codes a count nothing checks

```html
<p class="block__intro">Five results, each one quoting the record that earned it.</p>
```

The count is typed in the fragment; the records are whatever carries
`"home": true` in [`src/data/impact.json`](src/data/impact.json). Add a sixth
and the intro is silently wrong. Every comparable count on this site is either
generated or guarded.

The second half is worse: *each one quoting the record that earned it* is
**mechanics**, and [`CLAUDE.md`](CLAUDE.md) §6 puts mechanics in the model
documents and never on the page. A `block__intro` is a pitch.

### 1.6 It reads as a second Career page

Ordered JACQUEMUS, JACQUEMUS, OLIVESOFT, OEM, 2026: reverse chronological, with
company datelines and a paragraph each. That is Career's shape, rendered again,
one page earlier.

The order is the order of the file. Not by size of result, not by recency of
the work, not by what a hiring manager would want first.

### 1.7 Five paragraphs

Summaries run 111, 160, 133, 185 and 125 characters. The block is five
paragraphs of prose after 10 skill rows of chips, at the very bottom of a long
page.

### 1.8 One row is a different shape

*Open source* has no company, its period is a bare `2026`, it cites Projects
rather than Career, and its sentence is hand-written `evidence` rather than a
quotation through an id. It is the only non-job record, and the `.entry` shape
has nowhere to put that difference except an empty-looking dateline.

---

## Part 2: the cause

**The block borrowed `.entry`, and `.entry` is the component for a dated record
that lives on its own page.**

A job, a project, an award: each has a title of its own, a period of its own,
and a body of its own. A Selected Impact record has none of those. It is a
**pointer to a result**: a number, its consequence, and the bullet it came from.

Forcing that into `.entry` produced every symptom above:

| `.entry` requires | So the block invented | Finding |
|---|---|---|
| A title | A topic label, in the most prominent slot | 1.2 |
| A period | A company dateline, repeated from Currently | 1.3, 1.6 |
| Metadata tags | The figure demoted to a 12px chip | 1.2 |
| A uniform shape | An empty-looking `2026` on the one row that is not a job | 1.8 |
| Nothing that links | A fourth chip reading *Career*, four times | 1.4 |

Fixing 1.2 by swapping two font sizes leaves the component that caused it.

---

## Part 3: options

### Shape

**A. Repair in place.** Keep `.entry`. Promote the figure into the title slot,
drop the period line, drop the `source` tag and link the title instead.

- Costs: an hour. No new component.
- Gains: 1.2, 1.3, 1.4.
- Weakens: `.entry` now means two different things on the site, one of which has
  no period and a number for a title. 1.6 and 1.8 survive.

**B. A figure-led results list.** A new component on the label-column pattern
the site now uses three times (`.skill`, `.contact-list__row`, `.hero-facts`):
the figure in the fixed left column, the consequence in the flowing right
column, the source linked at the end of it.

```
€1,400 per month     A recurring monthly saving on the platform budget, taken
                     with no SLA impact on the morning reporting pipelines.
                     JACQUEMUS · Career

150+ jobs alerting   Alert coverage across the 150+ job estate, so a silent job
                     or API failure surfaces before the business-hours
                     reporting window rather than through a user report.
                     JACQUEMUS · Career
```

- Costs: one component, one renderer rewrite, a `DESIGN.md` section.
- Gains: all eight. The figure leads, the dateline stops repeating, the source
  becomes part of the provenance line instead of a chip, and the non-job row
  needs no special case.
- Weakens: a fourth user of the label-column idiom. If that pattern is wrong,
  it is now wrong in four places.

**C. A compact figure strip.** Five figures side by side on `.specs`, no
sentences.

```
€1,400/month    150+ jobs      Zero data lost    100× faster    2 plugins
Azure cost      Alert          Integration       Signal         Accepted
control         coverage       resilience        preprocessing  upstream
```

- Costs: least markup, existing component.
- Gains: maximum scannability, shortest block.
- Weakens: **deletes the consequence sentences**, which are the substance. It
  would turn the one block that explains *why the number matters* into a row of
  numbers, which is the failure [`CLAUDE.md`](CLAUDE.md) §5 warns about when it
  says a matrix where everything looks maximally proven is one nobody believes.

### Position

**P1. Third**, after Currently, before Skills & Evidence.
Reader sequence becomes Recruiter, Hiring manager, Hiring manager, Engineer:
monotonic. Blocks also grow as the page descends, so the longest is last.

**P2. Second**, immediately after the opening, before Currently.
Leads with the strongest evidence on the page. Costs Currently the position
`home.md` argued it into.

**P3. Last**, unchanged.

---

## Part 4: recommendation

**B, at position P1.**

B because the shape problems are one problem: a pointer to a result was written
as a dated record. Repairing the symptoms (A) keeps the component that will
regenerate them the next time a row is added, and C solves the scanning
problem by deleting the content.

P1 because [`home.md`](home.md) has already written the argument and applied it
to Currently and not to this block. *A hiring manager who reads three blocks and
leaves should have read it* is more true of the block that says what changed
than of any other block on the page. It also stops the page handing off to the
engineer and then asking the hiring manager to come back.

**The counter, answered.** [`home.md`](home.md) says Skills & Evidence *"is the
stronger block and it survives being third"*. Strength is not the ordering
principle on this page; reader sequence is, and that sentence was written when
the alternative was burying Currently. Skills & Evidence survives being fourth
for the same reason it survived being third, and it gains something: it is the
longest and most detailed block, aimed at the reader who has already decided to
keep reading.

---

## Part 5: what needs the author

1. **The intro.** It has to stop counting and stop describing mechanics. A
   pitch line for this block is one sentence about the work, and it is a claim,
   so it is yours.
2. **Order of the five records.** Currently the file order, which renders as
   reverse chronological. Options: leave it, order by size of result, or put
   the two JACQUEMUS rows apart so the block stops reading as a career list.
3. **The topic labels.** If the figure leads, *Azure cost control* and the
   other four either become a small kicker above the sentence or disappear.
   They are the only hand-written text in the records that is not a quotation.

---

## Part 6: what was decided and built

| Question | Answer |
|---|---|
| Shape | **B**, a figure-led list on the new `.result` component |
| Position | **P1**, third: after Currently, before Skills & Evidence |
| Intro | Author's to write. An interim line ships, marked in the fragment |

| | Before | After |
|---|---|---|
| Component | `.entry` | `.result` (`DESIGN.md` §9.3) |
| Most prominent line | topic, 17px bold | **the figure**, 17px bold |
| The figure | 12px grey chip | the figure column |
| Position | 4th, ~2 screens down | 3rd |
| `entry__period` lines on Home | 6 | 1 |
| Identical *Career* chips | 4 | 0 |
| Metadata models in `build.py` | 9 | 8 |

### Removed, because the change made them dead

- The `impact` entry in `MODELS` and `MODEL_LABELS`.
- `.tag--result`, `.tag--figure`, `.tag--source`, and the `figure` and `source`
  branches of `meta_label` and `meta_url`.
- The `result` field on all five records in `impact.json`. The aggregate row's
  standing is still derived from `projects.json` through `UPSTREAM_STATES`; it
  renders in the provenance line (*Accepted upstream · Projects*) instead of a
  chip, so the guard that once caught *submitted* against *accepted* is intact.

### Kept, deliberately

- **Every guard.** `check_figure`, the `cite`/`evidence` exclusivity error, the
  duplicate-id check and the phantom-PR check all still run.
- **`title` on every record**, no longer rendered. It is the handle a build
  error names and the label a person editing `impact.json` navigates by.

### Still open

1. **The intro.** Ships as *"What changed because the work shipped."*, which is
   the block's own definition from [`home.md`](home.md) and asserts nothing new
   about the author. It is marked `INTERIM` in
   [`src/pages/index.html`](src/pages/index.html) and is waiting for a sentence
   from you.
2. **Record order**, unchanged: still the file order, which renders reverse
   chronological with the two JACQUEMUS rows adjacent. Ordering by size of
   result was raised in Part 5 and not decided.
3. **Verification limit.** No headless browser here, so the 13rem figure column
   against a 74ch consequence column is reasoned from the tokens, not seen.
