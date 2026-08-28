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
  reasoned from the CSS. The strip took two corrective passes after the author
  looked at it on a screen, which is the argument for doing that earlier: it
  shipped stacked, went to two columns on request, and then needed the track,
  the gaps, the inset and the ink all re-derived, because a component turned
  sideways keeps solving the problem it had before. Both faults were visible at
  a glance and invisible in the markup.

## Corrections to this file's own pass

- **`.perf` shipped with a 22px indent that lined up with nothing.**
  `padding-left: 1.4em` was copied from `.points`, which earns it by being a
  `<ul>` drawing bullet markers into that gutter. A `<dl>` draws none, so the
  strip sat inset from the title, the dateline and the tag row above it.
- **It shipped with a third ink recipe.** A muted label against a heading-ink
  value containing a `<b>` that was also heading ink, so a figure and its unit
  differed by weight alone. `.spec__row` already had the right answer and its
  own comment already said why. It uses that now, and the `<b>` is gone from
  `render_performance`.
- **The 7rem label track survived the rotation to two columns**, where it was
  pure air: `Team` used 37px of it and its figure sat 75px away, further than
  the 20px separating the two pairs.

---

# Awards: the Hackathons block

A second pass, on the block below the one above. The request was to elevate the
Hackathons section's design without touching its content or the site's
language. The finding was that **its content had already been upgraded to
Projects grade and it was still being rendered by the Awards model**, which was
built for records that are entirely metadata and carry no prose at all.

## The findings

| # | Finding | Evidence |
|---|---|---|
| 1 | The block was the page's densest content and its flattest | 740 characters, **11 wrapped lines** against the 630px available inside `.points`. Every competition record above it is about five lines and carries no prose |
| 2 | Bold meant two different things on one page | Projects writes `<b>Security &amp; CSP hardening:</b>` for a bullet's *topic*; this record used `<b>` on four *tool names*. `b` is `--color-heading` at 700, so the tools competed with the record title for the darkest ink in the block |
| 3 | The stack was prose, and everywhere else on the site it is chips | [`CLAUDE.md`](CLAUDE.md) §6: tools are outlined chips on Career, Projects and Home, "one vocabulary for a thing this was built with". This was the one build record on the site with no stack row |
| 4 | One bullet ended in a consequence with nowhere to go | *"...so unvalidated model output never reached a patient-facing page."* [`DESIGN.md`](DESIGN.md) §9.2 defines `.point__impact` for precisely that trailing clause |
| 5 | Six chips, one of which repeated the `h2` | Measured run 566px against 460px for a competition. `Hackathon` 84px, `Competitive Programming` 181px and the widest chip on the page |
| 6 | `dataset` and `dataset_label` were dead data | No renderer read them. The Kaggle set was a hand-written `<a>` inside the first bullet, without the `link-external` marker the teammate link two bullets down did carry: one record, two inline links, two treatments |
| 7 | Nothing on the site cites this record | `skills.json` cites `awards.html#competitions`. No row cites `#hackathons`. The one Awards record that is a *built artefact* is the one the evidence graph never reaches |

Findings 2 to 6 are one cause, which is why they are one change.

## What was decided, and built

| | Before | After |
|---|---|---|
| Model order | `placement → distinction → type → scope → scale → duration → track` | `placement → distinction → scope → scale → duration → track → stack` |
| `type` | A chip on all eight records, repeating its block heading | Field only. `build()` still filters on it; the chip, the `.tag--type` rule and the two `tag.type.*` French strings are gone |
| Tools | Four `<b>` spans inside the prose | Five `.tag--stack` chips, 438px, the treatment Career and Projects use |
| Dataset | A raw `<a>` mid-sentence, `dataset` fields unread | A `.tag--artifact` link, 175px, label from the `tag.dataset` chrome string so the French says *Jeu de données* |
| Bullets | Three sentences opening on verbs | Three topics in bold, then a colon: *The contract*, *Validation and fallback*, *Ownership* |
| The consequence | A trailing clause on bullet two | Its own `.point__impact` line |
| Prose shape | 11 lines in one undifferentiated run | 9 lines in three labelled runs plus a 1 line impact |

The hackathon's tag run is now 1123px across eleven chips and wraps to a second
row in the 1068px document column. That is a new condition on this page and not
on the site: REGIM Lab already runs 1007px across eight chips and OLIVESOFT
915px across seven, and `.tag--stack` is outlined and regular weight, so the
run reads as one group by treatment rather than by staying on one line.

## Corrections to this pass's own claims

- **I proposed adding a `stack` category and had to check it was allowed to go
  last.** `render_meta` states the condition in its own comment: a run whose
  length varies has to sit after every category read positionally. `track`
  moved up a place for it. The option list was written before that was
  verified, which is the wrong order.
- **The dataset chip was written English-only and had to be redone.** The
  first form emitted the literal `Dataset ({name})` from a renderer with no
  `tr()` around it, which is the exact failure [`CLAUDE.md`](CLAUDE.md) §9
  lists as *a record field a renderer reads directly instead of through
  `t()`*: the French page would have carried an English `Dataset` between
  `48 h` and `Quart de finaliste`. The noun is a chrome string now.
- **`*.dataset_label` was added to the overlay's `keep` list and then removed
  again.** A dataset's published name looked like a proper noun, on the same
  reasoning that keeps `*.stack` English. The overlay already carried a
  translation for it, so declaring it kept would have been a false statement
  about a string the site does translate.

## Still open, and author-led

- **Finding 7 is not closed.** Nothing on the site cites this record, and
  `skills.json` has no capability row for the FastAPI, schema-validation and
  model-integration work it is evidence of. Adding one is a claim about
  capability, which is the author's, not a renderer's.
- **Nothing has been seen rendered**, again. The markup, the data, both
  languages and the build output are verified; the chip widths, the wrap point
  and the line counts are measured with `fontTools` against the shipped Noto
  Sans, and the layout is reasoned from those numbers rather than looked at.
  The previous pass in this file needed two corrective rounds for exactly that
  reason.
- **The page lede was deleted from both fragments** during this pass, by an
  edit that was not part of it, and replaced with an HTML comment. It has not
  been restored, because restoring it is the author's call and
  [`awards.md`](awards.md) closes with a section arguing for that line.
- **`.perf` was deleted during this pass, also by an edit that was not part of
  it**, and a contest's score and team size became two more chips,
  `.tag--problems` and `.tag--team`. That reverses a decision documented at
  length in this file and in [`awards.md`](awards.md) (*"A measurement is not
  a tag"*), and in the comment that used to sit above the rule (*"Two more
  chips on a row that already carries five is the wall `skills.md` rejected"*).
  It was left in place rather than reverted. Three consequences, none of them
  addressed here:
  - `render_performance` and `check_award_shape` are no longer called by
    `render_award`, so the guard that stopped a record carrying `performance`
    and `points` at once no longer runs.
  - The `.perf` explanatory comment survives in `main.css` above no rule, and
    the section of [`awards.md`](awards.md) headed *The performance spec* now
    describes a component the page does not render.
  - Competition records went from five chips plus a two-row figure strip to
    six chips, which spends most of the 181px that removing `type` freed.
- **`.entries--grid--compact` gained `text-overflow: ellipsis` in the same
  unrelated edit.** The scope cards now clip `.result__figure` and
  `.result__source` to one line each. That is information loss on a card whose
  provenance line names the records it was derived from, and it should be
  looked at on a screen before it ships.

---

# Awards: restoring the performance layout, and giving the hackathon its framing back

A third pass, and the first one on this page whose job was to *undo* part of
the second. The section above closes with two items listed as collateral from
an edit that was not part of that pass, left in place rather than reverted
because [`SKILL.md`](.claude/skills/rework/SKILL.md) lesson 38 says an
undiscussed reversal is not adopted by building on it and not undone by hand
either. The author has now made the call, and it is recorded here rather than
in a commit message.

## The findings

| # | Finding | Evidence |
|---|---|---|
| 1 | `.perf` was gone and its guard with it | `render_award` no longer called `render_performance`, so `check_award_shape` (a record carries `performance` or `points`, never both) had stopped running. The rules were deleted from `main.css` and their three explanatory comments were left standing above nothing |
| 2 | The score and the team size had become chips | `.tag--problems` and `.tag--team`, reversing *A measurement is not a tag* in [`awards.md`](awards.md). TCPC 23 went from **5 chips at 388px to 7 at 598px**; the six-chip records ran 532px and 538px |
| 3 | The page lede was gone from both fragments | Replaced with an HTML comment in `src/pages/awards.html` and `src/i18n/fr/pages/awards.html`. [`awards.md`](awards.md) closes with a section arguing for that line |
| 4 | The scope cards were truncating, in French, today | `.entries--grid--compact` had gained `white-space: nowrap` and `text-overflow: ellipsis` on `.result__figure` and `.result__source`. Measured on the shipped Noto Sans at the 13px the same rule imposed: `Quart de finaliste sur 200 equipes` is **214px inside 200px of card**, so `fr/awards.html` rendered it clipped |
| 5 | `render_award` was the only record renderer of nine that never emitted `.entry__summary` | `grep -n entry__summary tools/build.py` returns nine call sites and none of them is this one. [`DESIGN.md`](DESIGN.md) §9 fixes that slot between the scan line and the evidence |
| 6 | The hackathon's context had been sharpened out of existence | The three retired bullets carried it in their first clause (*"Delivered an MVP transforming complex clinical diagnosis and medication data into patient-accessible HTML summaries"*). The three that replaced them are better sentences and none of them says what the product was or who it was for |

Findings 5 and 6 are one cause, and it is the same shape as lesson 29: the
content was not wrong, it was one rank too low, and when the rank it was
squatting in got tightened it had nowhere to go.

## What was decided, and built

| | Before this pass | After |
|---|---|---|
| Contest score | `.tag--problems` and `.tag--team` chips | The `.perf` label column, restored verbatim from the commit that shipped it |
| The shape guard | Not called | `render_performance` calls `check_award_shape` again, so `performance` and `points` on one record fails the build |
| Competition tag run | 6 to 7 chips, 449px to 598px | 4 to 5 chips, 271px to 388px |
| Page lede | An HTML comment | *Where the algorithmic reflex was built, and put under a clock.*, and its French |
| Scope cards | 13px, one line, clipped with an ellipsis | The `--text-lg` figure again, allowed to wrap |
| Hackathon framing | Nothing | An `.entry__summary` naming the product and its reader, in both languages |
| `render_award` | Title, dateline, tags, bullets | Title, dateline, tags, `.perf`, summary, bullets: [`DESIGN.md`](DESIGN.md) §9's order, in full, for the first time |

**Two things from the same edit were kept, deliberately.** `.entries--grid--compact`
had also gained `gap: var(--space-3)` and a 12/12 padding on its cards, 4px
tighter on each side than `.entries--grid > .entry`. Neither loses information
and both give the figure 8px more room inside a 218px card, which is exactly
what the un-clipped text needs, so they stay and the comment above them now
says why.

## Corrections to earlier claims in this file

- **The section above says the ellipsis "should be looked at on a screen before
  it ships".** It had already shipped, and it did not need a screen: the
  measurement settles it. A 214px string in a 200px box is clipped whatever it
  looks like.
- **[`DESIGN.md`](DESIGN.md) §10.2 claimed `.perf`'s left inset is `.points`'.**
  It has none, and has not since the pass that turned it sideways removed it,
  for the reason two paragraphs above the stale sentence already gave. Fixed
  in the same pass rather than logged, because it is a document describing a
  rule the stylesheet does not contain.

## Still open, and author-led

- **Finding 7 of the previous section is still not closed.** Nothing on the
  site cites this record and `skills.json` has no capability row for the
  FastAPI, schema-validation and model-integration work it now frames.
- **The French summary is readable French, not approved French**, which is the
  standing caveat on [`CLAUDE.md`](CLAUDE.md) M4. It was written against the
  English rather than translated from it.
- **Nothing has been seen rendered**, again. Both languages, the build output
  and the checks are verified; the chip runs, the card widths and the wrap
  points are measured with `fontTools` against the shipped Noto Sans.
