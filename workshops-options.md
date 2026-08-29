# Workshops: the two-blocks pass

What was found on the Workshops page, what was decided, what was built, and
what is still the author's. The next agent reads this file, not the transcript.

---

## Before and after

| | Before | After |
|---|---|---|
| Blocks | One, headed *Workshops Delivered* | Two: *Hardware & Execution*, *Algorithms & Language* |
| That heading | Restated the `h1` three lines above it | Names one half of the descent the lede claims |
| Pitch lines | None on the page | One `block__intro` per block, plus the existing `.page-lede` |
| Context rail | One node, four children | Two nodes, two children each |
| The descent | Rendered by reverse chronology, invisible | Named, with newest-first surviving inside each block |
| The series | Three bullets numbering themselves in their own text | Two `.entry__group` parts, `render_group` |
| `<b>` in those bullets | Two spans and two colons in one bullet | One span, the bullet's topic, which is its only job |
| Rank between records | None: four records of identical shape | The two-part series is visibly the largest |
| A record with no section | Would render nowhere, silently | `check_workshop_block` fails the build |
| Headings | h1, h2, h3 | h1, h2, h3, h4 (the group titles) |

Unchanged, deliberately: every tag, every metric, all four titles, the page
lede, the summaries, and the wording of eleven of the fourteen bullets.

## What was decided, and by whom

Four questions went to the author. All four were answered before anything was
built.

| Question | Decision |
|---|---|
| The split | Two blocks, plain names, 2+2, chronology preserved inside each |
| The pitch lines | Mechanism-led pair, so neither opens with *Teaching* as the lede already does |
| The parts | Titled: *Part 1: Efficient execution and parallel compute*, *Part 2: Circuit-level computation* |
| The series duration | 2 h total, as it stood. The chip was already correct |

**Considered and not offered: splitting by audience** (OLIVESOFT alone, then
the three student sessions). `audience` is already a chip on every record, so a
heading restating it repeats the failure the `MODELS` comment in
`tools/build.py` records for Awards' `type`.

**Considered and not built:** a `.specs` reach panel stating the page's
constants (4 sessions, 142 participants, 12 h, 3 hosts), an Awards-style
summary card grid by host, and a fixed artefact slot on every record. The first
is the live one if the page ever needs to answer the recruiter's *how much of
this is there* in one glance; the honest argument against it is in
[`DESIGN.md`](DESIGN.md) §9.4, which records how the last aggregate on this
site went wrong.

## How it is wired

- `block` on each record in `src/data/workshops.json`, values `hardware` and
  `algorithms`. It is a filter and **never renders**: the Projects convention,
  not the Awards one, so no record carries a chip repeating its own heading.
- Two template keys, `build.workshops_hardware` and
  `build.workshops_algorithms`, placed by the fragment. The single
  `build.workshops` key is gone.
- The series' `points` became `groups`, the `[{"title", "points"}]` shape
  `cite_index` and `render_group` already understood. No new component, no new
  CSS: `.entry__group` gained a third user.
- `check_workshop_block` raises on a record whose `block` names neither
  section, which is the one failure the change introduced and the only one
  nothing downstream would have reported.

## Corrections made to my own earlier claims

- I reported the page as carrying **25 metadata chips**, counting the slide
  deck. It is 24 model chips plus one utility tag, which is a different thing:
  `.tag--artifact` sits outside the model by design, and
  [`workshops.md`](workshops.md) says so.
- I proposed the group field as `parts`. It is `groups`, because `cite_index`
  in `tools/build.py` already walks `record["groups"]` and a second name would
  have made the series' bullets uncitable from Home. Checking the consumer
  before naming the field is what changed the answer.
- My option list said direction A costs "two new pitch lines" and nothing else.
  It also cost a data field, two template keys, a build guard, and a French
  translation of four strings. The prose was right about the visible change and
  understated the wiring.

## Found on the way, not fixed here

- **`workshops.md` described a tag that does not exist.** *Outside the model*
  said the slide deck renders as `.tag--critical` and appends after "the
  model's four". Crimson was retired (the comment above the rule in `main.css`
  gives the reason) and the model has carried six categories since `duration`
  and `scale` joined it. Corrected in place, in the same paragraph, with the
  correction stated.
- **`README.md` documented four tags in the order
  `format → mode → audience → host`.** `MODELS["workshops"]` has had six since
  `duration` and `scale` were added. Corrected, along with the sample record,
  which was missing both.
- **[`DESIGN.md`](DESIGN.md) §9 still says *Entries are never boxed*, flatly.**
  §9.3 in the same document records that this sentence was never true, because
  `.entries--grid` boxes Career's credential cards, and lesson 11 in the rework
  skill is the pass that discovered it. One of the two paragraphs is wrong and
  it is not this pass's to settle.
- **The translation lock was stamped before this pass began.**
  `src/i18n/fr.lock.json` was written at 17:16, ahead of every edit here, and
  already carried a `ws-introduction-to-cs-fundamentals-hardware.groups` key
  and the current fragment hash, for an English this tree does not contain.
  The build then reported exactly two stale keys, both of them things this pass
  changed in both languages, so `--sync` blessed nothing else. If a second
  session was working this page at the same time, that is where to look.

## Still open, and author-led

- **The two `block__intro` lines are approved, not authored.** *What a NumPy
  call becomes by the time it reaches the hardware* and *Turning brute force
  into the right complexity, from the first line of Python up* were drafted
  here and chosen from a pair. They assert something about the author, so they
  are his to rewrite at will.
- **The same holds for their French**, and one step more so: *Ce qu'un appel
  NumPy devient une fois arrivé au matériel* and *Passer de la force brute à la
  bonne complexité, dès la première ligne de Python* are readable French, not
  approved French, which is the state [`CLAUDE.md`](CLAUDE.md) M4 already
  records for every pitch line on the site.
- **The block names themselves.** *Hardware & Execution* and *Algorithms &
  Language* match the site's noun-phrase heading style. A voiced pair (*The
  Machine* / *The Program*) was offered and declined; it remains available.
- **A fifth workshop needs a block**, and the build now says so out loud. A
  subject that fits neither is a question about the page, not a new field.

---

# Workshops: the page header pass

Three things were built above the first heading and **one is on the page**: a
grid of host cards. A stack diagram and a spec strip were built first and both
were replaced on the author's verdict. All three are recorded, because the two
that went are the more useful half.

## Before and after

| | Before | After |
|---|---|---|
| Page header | `h1` and a lede | `h1`, the lede, three host cards |
| The page's scale | 24 chips, four of which held the numbers | `30`, `60`, `52` participants, per host, each linking to its sessions |
| Who invited him | Readable off four records, one chip at a time | Three cards, one per organisation |
| A workshop missing `scale`, `duration` or `host` | Rendered a record with a gap | Fails the build: a figure would have silently shrunk |
| A page mixing two `scale` units | Two units, two chips, no total | Fails the build: one figure cannot carry both |

Unchanged, deliberately: every record, every tag, every bullet, both block
headings, both intros and the lede. Nothing in `src/data/workshops.json` moved.

## What is on the page

The card is Awards' scope card reused whole, which is the finding worth
keeping: it needed **no new component, no new class and no new CSS**.

```
OLIVESOFT              Securinets ENIS         IEEE Student Branch ENIS
30 participants        60 participants         52 participants
1 session &middot; 2 h            1 session &middot; 4 h            2 sessions &middot; 6 h
Introduction to CS     Assembly Programming    Introduction to Competitive
Fundamentals           Workshop                Programming
(Hardware)                                     Introduction to Python
```

`render_workshops_hosts` in `tools/build.py`, one template key
(`build.workshops_hosts`), placed inside an `.entries--grid--compact` list in
both fragments' `page-header`. Every value is computed: the head count sums
`scale.count`, the hours sum `duration`, the label is `host`, and the links are
the records' own ids and titles, so `check.py` fails on a card pointing at a
record that is not there. Two French chrome strings (`unit.session`,
`unit.sessions`); the host names do not translate and the audience keys the
strip needed are gone.

**Measured, not eyeballed:** at a 908px column the three tracks give each card
271px of text. Every line fits on one except two record titles, which wrap to a
second line, and that is the same latitude Awards' cards take. That measurement
is also the argument for stacking the links rather than joining them: the pair
runs 407px against a 271px track, so a middot between them put the break
mid-title.

## The two that went, and why

**The stack diagram.** Five layers read downward, each with the session that
taught it beside it. It cost a second orientation in the renderer, a `note`
field, a CSS rule and about 380px at the top of the page. It was accurate, it
printed and it was translated; the author's verdict was that it was not good
enough to look at and not useful enough to keep. Everything it added is gone,
not staged: the record, both placements, the French overlay, `stack_diagram`,
`diagram_figure`, four geometry constants and `.diagram__note`.
`render_diagram` is byte-identical to what it was, and so is the output of the
other two diagrams, which was checked.

**The spec strip.** Three columns stating the page's constants (142
participants, 12 h, 4 sessions, 3 hosts) on Teaching's component. Correct, and
replaced, and the argument that replaced it is the reusable one: **a card
carries a citation and a spec row cannot.** `142 participants` points at no
record; *60 participants at Securinets ENIS* points at exactly one. That is
[`CLAUDE.md`](CLAUDE.md) §10's Domains argument arriving at a different
component.

**One change from those two passes was kept**, because it is a fix rather than
a feature: `wrap_label` counted an HTML entity as its characters, so `&amp;`
measured five glyphs wide and broke a label early. It measures the rendered
glyph now, and no existing diagram's output changed.

**The lesson about [`diagrams.md`](diagrams.md) §1's test** is recorded there
and in [`DESIGN.md`](DESIGN.md) §1.1: a diagram that is true, prints, and
restates what the page already says in words is still decoration. Being able to
answer *could a reader learn something here the prose leaves open* in theory is
not the same as the picture being worth the space.

## Decisions, and who made them

| Decision | Made by | Note |
|---|---|---|
| Delete the diagram | Author | Explicit |
| Cards instead of the strip, Awards style | Author | Explicit |
| Group by host, not by measurement or audience | Author | Chosen from four costed options |
| Newest host first | Here | The order the records are already in |
| The head count is the figure, sessions and hours the qualifier | Here | Awards' ranks, applied to what this page measures |
| A host's sessions stack, one to a line | Author | `.result__source--stacked`, one new CSS rule. The middot stays on Awards, where the peers are short |

## Found on the way, not fixed here

- **The spelling audit cannot tell a vocabulary term from prose.** It counts
  `"@type":"Organization"` in every page's JSON-LD as an American spelling, so
  the word *organisation* is unusable anywhere on the site. The fix, when
  someone wants it, is to skip `application/ld+json` blocks in
  `tools/check.py`, not to change the word.
- **`.perf` is documented and does not exist.** [`DESIGN.md`](DESIGN.md) §9.3
  describes it in detail as the fifth user of the label-column idiom, with an
  account of turning it sideways and re-deriving its track.
  `render_performance` in `tools/build.py` is never called, `main.css` has no
  `.perf` rule, and `awards.html` renders `tag--problems` and `tag--team` chips
  instead. One of the two is wrong and it is the author's call which.

## Still open, and author-led

- **What the cards dropped.** The audience split (112 students against 30
  professionals), the span (2022-2026) and the sittings count are no longer
  stated anywhere on the page. The audience split is the one with a claim
  attached to it, and it survives as a chip on every record.
