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
