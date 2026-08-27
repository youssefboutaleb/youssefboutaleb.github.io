# Awards: the page header summary

The strip under *Honors & Awards* was rebuilt. This is the record of what it
was, what it is, and what was decided but not built.

---

## Before and after

| | Before (`.awards-stats`) | After (`.entries--grid`) |
|---|---|---|
| Component | Bespoke, invented for this header | The card grid Career's certifications use, [`DESIGN.md`](DESIGN.md) §9.4 |
| CSS | 25 lines, three rules, one filled surface | None. Nothing new was styled |
| Placement | Inside `.page-header`, which §11 said held an `h1` and a lede | Same place, and §11 now admits a summary grid |
| Shape | One wrapped run of middot-separated items in a bordered box | Four cards, 2×2: scope, the result as chips, the record that proves it |
| Covers | The Competitions block | Every scope on the page, hackathon included |
| Labels | Hand-formatted strings | `meta_label` output, the same function the tags below use |
| French | Three chrome strings rendering in English | Translates with the tag vocabulary |
| Widest claim | *13,999+ Teams Competed* | Gone, see below |

Rendered:

```
┌────────────────────────────┐  ┌────────────────────────────┐
│ Regional                   │  │ National                   │
│ [● 1st Place] [86 teams]   │  │ [2× National Finalist]     │
│ • Hello World v4.0         │  │ • TCPC 23                  │
└────────────────────────────┘  │ • TCPC 22                  │
┌────────────────────────────┐  └────────────────────────────┘
│ African                    │  ┌────────────────────────────┐
│ [Quarter-finalist][200 t…] │  │ International              │
│ • A2SV GenAI Hackathon     │  │ [643rd Place][7,094 teams] │
└────────────────────────────┘  │ • IEEEXtreme 17.0          │
                                └────────────────────────────┘
```

Structurally identical to a certifications card: heading, then a `.points`
list of what the cell contains. The only addition is the tag list between
them, and its chips are the record's own.

## What was wrong, and why it was one thing

Eight symptoms, one cause: **a shape was invented where §9.3 had already named
the one to reuse.** Everything else followed. The box (the only filled surface
outside `.entries--grid`), the ~415px of text floating in a ~764px bordered
element, the fused *1st Place Regional* against `awards.md` rule 4, the
`f"{gold_count}st Place Regional"` that would have printed *2st* on a second
gold, the three chrome strings nobody added to `fr.json`, the absent
hackathon, and the fact that no document on the site described any of it.
Repairing any one of them would have left the other seven. The full table is
in [`DESIGN.md`](DESIGN.md) §10.2.

## Decisions

**The African result is *Quarter-finalist*, and stays that way.** The author
was asked directly whether the A2SV stage in `awards.json` was wrong. It is
not. *African Finalist* would have been a stronger and different claim, and
[`CLAUDE.md`](CLAUDE.md) §5 makes honest placement the site's credibility
argument, so it was put to the author rather than upgraded.

**The National row says *2&times; National Finalist*, not *13th Place*.** The
rule is written down in [`awards.md`](awards.md#the-scope-summary): a row
shows the best record's `distinction` when it has one, counted if the scope
has more than one, and its `placement` and `scale` otherwise. The placements
are on the two records the row links to.

**The International row says *643rd Place &middot; 7,094 teams* deliberately.**
A summary in which every figure is maximally flattering is one nobody
believes, and it is the honest row that makes the *1st Place* above it worth
reading.

## Retired, and why

**The medal disc survived.** It is `meta_label`'s, awarded to placements 1 to
3, and it now arrives inside the Regional card's `.tag--placement` chip
automatically instead of being pasted in beside a hardcoded label.

***13,999+ Teams Competed* is gone and should not come back.** It summed every
field size on the page. 13,470 of those 13,999 were the two IEEEXtreme fields,
so the largest and boldest number on the page was 96% carried by the 643rd and
1,432nd placements. It also counted the author's own team eight times.

**`tag.placement.Quarter-finalist` was added to `fr.json`.** It was missing
before this change: the tag on the record itself had been falling through to
English on `fr/awards.html` all along. The strip only made it visible.

## Second pass: from a fact strip to cards

The first build of this used `.hero-facts`, the label-column strip from Home.
The author asked for cards like the certifications boxes instead, and they
were right. Recording the reversal rather than quietly overwriting it:

- **`.hero-facts` was the wrong reuse and the reasoning that picked it was
  half right.** §9.3 does say a fifth case of "a short fixed thing beside a
  long flowing one" takes the label-column idiom. A scope summary is not that
  case: the four scopes are a **set to be counted**, not a column of labels
  with prose beside them, and §9.4 now carries the test that separates them.
- **A card holds more with less.** The strip had to join two records with a
  middot on the National row (*TCPC 23 · TCPC 22*); the card lists them as two
  bullets, which is what `.points` is for and what the certifications cards
  already do with three Microsoft certificates.
- **The result became chips instead of running text.** `[● 1st Place]
  [86 teams]` are the record's own `.tag--placement` and `.tag--scale`, so the
  card and the entry it links to now render the identical markup from the
  identical call.
- **Still zero new CSS.** Both passes composed from existing parts; the second
  simply picked the right ones.

## Corrections to earlier claims in this pass

- **I cited DESIGN.md §9.3's *"entries are still never boxed"* against the old
  box, and that rule was already false when I quoted it.** `.entries--grid`
  has boxed Career's credential cards all along. The old strip was wrong for
  six other reasons, none of them the box. §9.3 now reads *a record in a
  reading list is never boxed* and points at §9.4 for the distinction it was
  actually reaching for: a record you **read** is a bulleted item, a record
  you **count** is a cell in a grid.
- **`.entries--grid` was undocumented**, which is why the rule above could
  stay wrong. §9.4 exists now and covers both users.
- The first pass's preview drew the record name as a third column, and
  `.hero-facts` is a two-column grid. Moot: the cards carry it as a `.points`
  bullet, which is what the approved preview showed.
- The first pass rendered the International row as *643rd Place &middot; 7,094
  teams*, not the preview's *643rd of 7,094 teams*, so that both scopes spoke
  one vocabulary. The cards keep that, as two chips.

## Still open, and author-led

- **`aria-label` on the card tag lists** reuses `MODEL_LABELS["awards"]`, so a
  screen reader hears *Achievement details* four times in the header and again
  on each of the eight records. Accurate, repetitive, and worth a look.
- **`awards.summary_label` was added to `fr.json` and then deleted** in the
  same session, when the wrapper moved into the fragment and the renderer
  stopped emitting an `aria-label` of its own. Mentioned so nobody goes
  looking for it.
- **Sixty-three untranslated French record fields** on this page and others,
  which the build reports on every run. Unchanged by this pass.
- **The two French `block__intro` lines on this page are still literal
  drafts**, flagged in the fragment itself, and need the author's voice.
