# Awards: the performance spec

The record of the pass that turned `Solved 8 / 8 problems in 4h (Team of 2)`
into fields, and gave the page a lede.

---

## The finding

The request was to remove a sentence. The cause was that **`awards.md`
contradicted itself**, and the page had been paying for it in both languages.

| | |
|---|---|
| **Rule 7** | *"Store the raw fact and let the renderer produce the label. Hand-written labels are how `1st Place`, `1st place` and `First` end up on the same page."* |
| **Bullet rule 1** | *"State the score, duration, and team size. `Solved 8 / 8 problems in 4h (Team of 2)` is the whole bullet."* |

One document, two rules, pointing opposite ways. What it produced:

- **Four facts welded into prose** in seven records: solved, total, hours, team.
- **Seven more hand-written strings in French**, translating the same sentence.
- **Two spellings of one unit on one page.** The bullets printed `4h`, `5h`,
  `24h`; the hackathon's `duration` tag printed `48 h`.
- **The two languages disagreeing about the format of a figure.** The French
  overlay had quietly corrected it to `4 h`, so English was the one that was
  wrong by its own renderer.

**The argument was already in the codebase.** `tools/build.py`, on `duration`
in `meta_label`:

> *"Stored as a number, spaced here, so `2h` and `20 h` cannot coexist. They
> did... A value formatted at the call site is a value that drifts from every
> other call site."*

The awards bullets were that call site, still drifting, on a model whose
`MODELS["awards"]` tuple had carried a `duration` field the whole time.

## What shipped

| | Before | After |
|---|---|---|
| The four facts | one prose sentence per record | `"duration": 4` and `"performance": {"solved": 8, "problems": 8, "team": 2}` |
| Hours | `4h` in bullets, `48 h` in a tag | `4 h` everywhere, through `meta_label` |
| Rendering | `.points` bullet | `duration` tag + a `.perf` label column |
| French | 7 hand-translated sentences | 3 chrome strings, and the locale's own number format |
| Hackathon bullet | *"Delivered an MVP in 48h..."* beside its own `48 h` tag | duration removed from the sentence, kept in the tag |
| Awards lede | none | *Where the algorithmic reflex was built, and put under a clock.* |

**A new guard.** `check_award_shape` fails the build on a record carrying both
`performance` and `points`, because that is a record stating one thing twice,
which is how the sentence got there. Added to [`CLAUDE.md`](CLAUDE.md) §9's
table.

**Not chips, and that was the design decision.** The score could have been two
more tag categories and was not: a tag says *this record is filed under X*,
which a solve count is not, and `awards.md` rule 3 picks categories for the
reader rather than for symmetry. Seven chips on a row is the wall
[`skills.md`](skills.md) rejected. `.perf` is the fifth user of the
label-column idiom and the first to live *inside* a record, so it takes the
idiom at its smallest: a 7rem label, `--text-md`, and no hairline between rows,
because a rule inside a bulleted record draws a table inside a bullet.

## The three ledes

Written with the author, not promoted, because all three pages carry
block-specific pitches that nothing could be lifted from.

| Page | Lede | Derived from |
|---|---|---|
| Projects | *The same debugging instinct, applied to someone else's codebase and to whole pipelines of my own.* | [`CLAUDE.md`](CLAUDE.md) §3 on open source, plus the half it does not cover |
| Research | *What pipelines have to feed, and what bad data costs downstream.* | [`CLAUDE.md`](CLAUDE.md) §3, near verbatim |
| Awards | *Where the algorithmic reflex was built, and put under a clock.* | [`CLAUDE.md`](CLAUDE.md) §3 on competitions; the second clause reaches Hackathons |

All eight pages now have a lede except Career, which keeps its Summary as its
only opening by the decision recorded in
[`career-experience-options.md`](career-experience-options.md).

## Decided against

- **A solve-rate meter.** A hairline bar showing 8/8 against 11/26 would spare
  the reader the division, and it was put to the author beside the chosen
  option. It costs a second drawn element on a site that rations them to one
  ([`DESIGN.md`](DESIGN.md) §1.1), and it needs the written argument the
  diagram and the theme switch each got. Not built. Still the most interesting
  thing left on this page.
- **Score and team as tags.** See above.
- **Giving the hackathon a `performance` block.** Its team size is inferable
  from *"collaborated with teammate Mohamed Brahim"*, and inferring a figure is
  not the same as being told one. `render_performance` requires the full block
  and will raise rather than half-render, which is the loud failure the site
  prefers.

## Still open

- **The scope summary mixes two components.** `render_awards_summary` puts
  `.result__figure` and `.result__source` inside `.entry` cards in an
  `.entries--grid`. It works and it is documented in `awards.md`, but it is one
  component wearing another's classes, which is the shape that produced every
  other finding in this file. Not touched in this pass.
- **Nothing has been seen rendered.** The markup, the data and the build output
  are verified; how the `.perf` strip sits under a five-chip tag row is
  reasoned from the CSS.
