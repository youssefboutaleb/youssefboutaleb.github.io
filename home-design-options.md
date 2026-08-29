# Home: the page that was almost aligned

The record of the design pass that gave Home one vertical edge, took its
section headings out of a 208px box, and split the hairline into two weights.

The author asked for design directions that raised the page without changing
its content or breaking the language the rest of the site is written in. Five
were put; **Directions 1, 2 and 3 were chosen and built together**, which was
the recommendation, on the argument that the three of them close defects rather
than add features and that they leave the two ambitious options open.

---

## Part 1: the finding

**Home read as *almost* aligned, and that is the worst of the three states a
page can be in.** Aligned is a system. Unaligned is a texture. Almost aligned
is neither, and a reader cannot tell which of the page's other regularities are
intended.

Four label tracks ran down one page, none of them agreeing:

| | Track | Gap | Flowing column began at |
|---|---|---|---|
| Hero portrait | 180px | `--space-5` | **x = 200** |
| Block heading (`.block--casebook`) | 13rem | `--space-6` | **x = 240** |
| `.result__figure` | 13rem | `--space-5` | **x = 228** |
| `.skill__head` | 15rem | `--space-5` | **x = 260** |

Four gutters inside 60px of each other. Nothing was off by enough to look
deliberate; everything was off by enough to see.

### 1.1 Two of three section headings did not fit their own column

`.block--casebook` put the `h2` in a 13rem (208px) side head. Measured from the
shipped Noto Sans at 32px with `-0.02em`:

| Heading | Width | In a 208px column |
|---|---|---|
| `Currently` | 135px | fits |
| `Skills & Evidence` | 237px | **wraps** |
| `Impact in Numbers` | 279px | **wraps** |
| `En ce moment` | 209px | **wraps** |
| `L'impact en chiffres` | 284px | **wraps** |
| `Compétences et preuves` | 358px | **wraps** |

So five of six headings across the two languages set as two lines, at every
width from 768px up, and that was not a decision anyone took. The component
asked a 32px display rank to live in a 208px box.

### 1.2 One hairline weight was doing three jobs

`--color-border` drew the block boundary, the rule between two results, and the
rule between two skills. Three sections and fifteen ruled rows, at one value:
sixteen equal divisions on a document with three parts. `.hero-facts__row` had
been using `--color-border-soft` for its rows the whole time, so the page was
already disagreeing with its own header.

### 1.3 The fact strip left the page's alignment on the widest screen

Above 1280px a `min-width` query turned the hero into three tracks and moved
`.hero-facts` into a 14rem right-hand column with a left rule: the only
right-aligned element on the site, placed outside the alignment on the one
viewport wide enough for the alignment to be visible.

### 1.4 `.block--casebook` was documented nowhere

`grep` for it across `DESIGN.md`, `home.md`, `CLAUDE.md` and every model
document returns nothing. It is the third component to arrive without its
document, after `hero-header__headline` and Contact's eight private classes,
and it is the third one to be found wrong on measurements. The pattern is now
firm enough to state: **a component nobody wrote down is a component nobody
re-measured.**

---

## Part 2: what was built

| | Before | After |
|---|---|---|
| Spine token | none, four literals | `--spine: 13rem`, gutter `--space-6`, flowing column at **x = 240** everywhere |
| Hero portrait | 180 x 220 (0.818) | **208 x 260** (a true 4:5), filling the spine |
| Hero fact strip | `grid-column: 2`; a third column above 1280px | full width, labels on the spine, **the 1280px query deleted** |
| `.hero-facts__row` on Home | 10rem label | `--spine`, scoped to `.hero-header__content > .hero-facts`, in a `min-width: 601px` query |
| `.hero-facts__row` on Contact | 10rem label | **unchanged** |
| Section headings | in a 13rem side head, five of six wrapping | full width, `h2` then pitch then records |
| `.block--casebook` | two-column grid + boundary rule | **`.block--ruled`**: the boundary rule only |
| `.result` | 13rem / `--space-5` / `--color-border` | `--spine` / `--space-6` / **`--color-border-soft`** |
| `.skill` | 15rem / `--space-5` / `--color-border` | `--spine` / `--space-6` / **`--color-border-soft`** |
| Portrait at ≤480px | 140 x 170 | 144 x 180, matching the 4:5 above it |
| Print | no rule for the boundary | `.block--ruled` border suppressed: print takes the heading's underline back instead |

### The arithmetic that fixed 13rem

It is not a preference and it is not the average of the four it replaced:

- The widest `.result__figure`, *150+ jobs under alerting*, is **194px**. A
  narrower spine wraps the figures the block exists to show.
- The flowing column left at the widest container is **668px** against a
  **652px** `--measure`. A wider spine eats the reading line.

That leaves 13rem as the only track that satisfies both, with 16px of slack.

### The 32px the skill column gave up buys nothing back

The case for keeping `.skill` at 15rem was unwrapped capability names. Measured
against the shipped bold face at 17px, they wrap either way:

| | 15rem (240px) | 13rem (208px) |
|---|---|---|
| English names wrapping | 3 of 10 | 7 of 10 |
| French names wrapping | 6 of 10 | 9 of 10 |

The widest, *Apprentissage automatique et vision par ordinateur*, is 444px and
wraps at any width the column can afford. The extra 32px was buying a longer
first line on three rows and the one track that agreed with nothing else.

---

## Part 3: corrections to my own earlier claims

Recorded plainly, because the next agent reads this file and not the transcript.

1. **"Four left columns" was wrong, or at least imprecise.** Every left edge
   was already at x = 0 and always had been. What was ragged was the *second*
   edge, where the flowing column starts. The fix is the same; the diagnosis
   in the first option list was not, and it would have sent someone looking at
   the wrong side of the grid.

2. **`DESIGN.md` §1's hero measurement was wrong before I touched it, and I
   repeated it.** It stated `Ingénieur Data` at **453px**; measured with
   `fontTools` against `assets/fonts/`, it is **435px** at 64px. I quoted 453
   in the option list as a live constraint and used it to reason about which
   spine widths were affordable. Both the old figure and the new one clear the
   narrowest bio track (452px at a 1024px viewport), so no decision turned on
   it, but the reasoning was resting on an unverified number for one round.
   §1 now carries the correction and the instruction to re-derive rather than
   scale it.

3. **`DESIGN.md` §13's responsive table had four wrong numbers**, none of them
   mine: the ≤720px type steps were given as 32px and 22px and the ≤480px steps
   as 28px and 20px, against a stylesheet that has said 48/28 and 40/24 since
   the display pair was rebuilt. The `≥1024px` row, the breakpoint that
   introduces the rail and widens the container, was missing from the table
   entirely. Corrected in the same pass because leaving known-false rows beside
   newly-true ones is worse than the original drift.

---

## Part 4: the collision, and how it was resolved

**Answers 2 and 3 contradicted each other and the contradiction was visible in
the previews.** Answer 2 chose the site's ordinary heading grammar, which
deletes `.block--casebook`. Answer 3 chose a two-step rule ramp whose strong
step is *the block boundary*, which is a rule that existed only inside
`.block--casebook`. Building both as literally chosen would have deleted the
strong step of the ramp the author had just selected.

Resolved in the open rather than by picking: **the class survives, reduced to
the one job answer 3 needs.** It keeps `border-top` and `padding-top` and loses
the grid, and it is renamed `.block--ruled`, because a modifier called
`casebook` describing a border is how a stylesheet starts documenting a page
that is not there.

---

## Part 5: decided against, and not built

- **Direction 4, density as cadence.** Setting each block at its own vertical
  rhythm and reducing the chip weight in Skills & Evidence. Independent of what
  shipped and still available. Its cost is that it spends deliberately from
  Principle 2's one spacing scale, and it touches `.tag--stack`, which is
  site-wide.
- **Direction 5, the margin carries the index.** The strongest page-level idea
  and the most expensive. Two things block it and both are real: moving
  `.result__source` into the margin contradicts `DESIGN.md` §9.3, which put
  provenance under the sentence because *Career* said nothing as a chip and
  said it four times in five rows (in a margin it would say it five times in a
  column, the same failure rotated); and giving `Currently` a two-column form
  means either taking the dateline out of `.entry` or inventing a Home-only
  variant of it. **The spine that shipped is the half of Direction 5 that had
  no such cost**, so the ground is prepared if it is ever wanted.

---

## Part 6: still open, and author-led

1. **`--icon-sm` is now an orphan token, and it is not from this pass.**
   `.icon--sm { width: var(--icon-sm); height: var(--icon-sm); }` is present in
   `HEAD`'s stylesheet and absent from the working tree, removed by an edit
   that is not mine and that I did not undo. Nothing in the repository
   references `.icon--sm`, so its removal was correct and the unused-class
   check would have failed otherwise. What is left behind is the token, which
   `check.py` now reports, and `DESIGN.md` §17, which still lists `--icon-sm`
   (15) as one of the icon sizes. Deleting a token in a component this pass did
   not touch is the author's call.

2. **The checker's output changed mid-pass in a way I could not attribute.**
   The first run after the CSS work reported *161 css classes* with no token
   note; the next, after I had edited only Markdown, reported *159* with the
   `--icon-sm` note. Three consecutive runs since are identical and every check
   passes, so the current state is sound, and the transition is recorded here
   rather than explained, because I could not explain it honestly.

3. **Verification limit, stated rather than implied.** There is no headless
   browser here. Every width in this document is computed from the shipped
   `woff2`/`ttf` faces with `fontTools`, ignoring kerning and hinting, so the
   figures are accurate to a few pixels and the *fits / wraps* calls near a
   boundary carry that tolerance. `Ingénieur Data` at 435px against a 452px
   track at a 1024px viewport is the tightest of them and is the one worth
   looking at on a real screen.

4. **The first screen is taller above 1280px**, because the fact strip no
   longer sits beside the bio. That was named as the cost when the option was
   put and accepted with it, and it is the one change here a reader who knew
   the old page would notice immediately.
