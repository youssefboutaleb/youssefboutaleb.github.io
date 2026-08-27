# Audit, phase 2: the twelve structural refinements

Follows [`audit-phase1-options.md`](audit-phase1-options.md). Same rules: what
was found, what was decided, what shipped, and every correction made to the
audit's own claims.

`python3 tools/build.py` and `python3 tools/check.py` both pass.

---

## Before and after

| # | Finding | Before | After |
|---|---|---|---|
| S1 | Home hero said one thing three ways | h1, a headline naming 4 roles, a lede re-verbing 3 of them, IHEC twice | Headline deleted, with its CSS rule |
| S2 | Awards summary repeated its own records | Card: medal, `1st Place`, `86 teams`, title. Record 300px below: the same four | Figure-led: `1st Place of 86 teams` / `Regional · Hello World v4.0`. No chips, no medal |
| S3 | Teaching stated one workload four times | Specs panel + a `32 h · 20 lecture + 8 lab + 4 project` chip on each of 3 courses | `workload` out of `MODELS["teaching"]`; the panel owns it |
| S4 | Contact was a private vocabulary | `.contact-section*`, the only `h2` on the site, addresses typed beside `site.json`'s copies | `section.block` / `h2.block__title`, all rows generated, 2 classes deleted, `contact.md` written |
| S5 | Tag colours had stopped meaning anything | `tag--critical` (crimson) on a `.pptx`; `tag--upstream` on both a PR and a demo; 3 of 5 utility names dead | `tag--demo` / `tag--article` / `tag--artifact`, named for the fact |
| S6 | Citations could only point at Career | `render_impact` hardcoded `career.html` twice; `cite_index` walked `experience` alone | `cite_index` takes a page→records map; href and label derive from where the id was found |
| S7 | The rail lied and was 22 deep | `<details>` forced open by CSS while reporting itself collapsed; Teaching 1 link / 22 sublinks; two identical JID links | A `<nav>`. `TOC_DEPTH = 2`. Teaching 1 / 3. Siblings disambiguated by year |
| S8 | The dating rule was documented, styled, unbuilt | Two hand-copied Medium figures, undated. `.block__note` dead CSS | `as_of` in `reach`, `check_reach` fatal, `.block__note` renders |
| S9 | Employer boilerplate led every role | One `summary`, 44 to 61 words of company description before the first-person clause | `context` (muted, small) + `summary` (body copy) |
| S10 | `check.py` missed most of this audit | No heading-order, spelling, fan-in or fatal dead-CSS check | All four added; caught 3 real spelling defects on first run |
| S11 | The document outline was broken on 8 of 8 | No `h2` anywhere but Contact; every record title a `<p>` | `h1 → h2 → h3 → h4`, valid on every page |
| S12 | The one sentence that asks | `contact_invitation` referenced nowhere in the repository | Renders as Contact's `block__intro` |

## Corrections to the audit's own claims

Two more, on top of Phase 1's three.

1. **The Awards summary's "broken parallelism" was already answered.** I
   reported the mix of `1st Place`, `2× National Finalist`, `Quarter-finalist`
   and `643rd Place` as non-parallel. `render_awards_summary`'s docstring
   states the rule: the distinction if the best record carries one, else the
   placement and the field size. It is deliberate, documented, and right, and
   only the redundancy half of that finding survived to be fixed. This is the
   rework skill's lesson 13 for the second time in two passes: **read the
   thing that owns the rule before reporting the rule as missing.**

2. **`entry__summary` was not merely "a company description".** It was two
   sentences with two declared jobs, and `career.md` §5 said so. The defect
   was that one field could not give them different typography, not that the
   company sentence should not exist.

## Decisions worth recording

**Deleted the `<details>` rather than fix its `open` state.** The audit
proposed emitting `<details open>` and closing it with CSS below 1024px. That
keeps a control whose only remaining job on desktop is to be a focusable
element that does nothing. Capping the rail at two levels removed the reason
the disclosure existed, so the disclosure went. Removing state is a better
answer than making state honest, and CLAUDE.md §7's third exception is now the
only stored state on the site.

**Reused `.result__figure` and `.result__source` on the Awards cards rather
than inventing two classes.** They mean *the figure* and *where this came
from*. Only `.result`'s two-column grid is Home's, and a grid property on a
non-grid child is inert, so nothing else came with them.

**Set the heading element defaults to what the components already rendered.**
Retagging seven pages could have been a visual redesign by accident. Every size
and colour in the new ramp is what `.block__title`, `.entry__title` and
`.entry__group-title` were already producing, so the outline changed and the
rendering did not.

**`report_undated` reports rather than fails.** `check_reach` is fatal because
the data to satisfy it exists: the figures were read on a date and that date is
known. A submission date for the in-progress paper is a fact only the author
has, and a guard that fails the build over data nobody can supply is a guard
that gets deleted.

## Still open, and author-led

Carried from phase 1, unchanged:

1. **`PowerShell automation`** is still a green *production* chip citing
   nothing. No bullet in `experience.json` mentions PowerShell.
2. **`Architecture & recovery docs`** points at `career.html#summary`, which is
   prose rather than a record.
3. **The French translation**, ~5,000 words. The threshold makes the gap
   visible on every build; it does not close it.
4. **The two French `block__intro` lines** on Awards are literal drafts.

New from this pass:

5. **The in-progress paper has no date.** It is the one record on the site
   shipping without one, and `report_undated` now names it on every build. It
   needs a submission or start date, or the record needs to say why it has
   none.
6. **`Opportunities & Services` offers consulting.** [`contact.md`](contact.md)
   §5 states the tension with CLAUDE.md §3: a row offering *Consulting &
   services* beside *founding engineering positions* invites the reader to
   conclude the author is shopping rather than targeting. Either the row goes
   or §3 is revised; at the moment one of the two is wrong.
7. **Nothing links to Contact but the navigation.** A closing line on Home was
   offered and not chosen, so the invitation renders on Contact alone.

## Not done, and why

- **`.entry__context` reads before `.entry__summary` still.** Only the
  typography sorts them. Reversing the order was available and not taken:
  a reader who does want the employer should still meet it first.
- **Unit formatting** (`2h` on Workshops, `20 h` on Teaching) is unchanged and
  unguarded.
- **`medal--bronze`** remains the one staged CSS rule, declared in
  `STAGED_CSS`. It is reachable code awaiting a third place, not dead.
