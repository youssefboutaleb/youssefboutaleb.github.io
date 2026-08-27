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

5. ~~**The in-progress paper has no date.**~~ **Closed.** See phase 3 below.
6. ~~**`Opportunities & Services` offers consulting.**~~ **Closed by the
   author, against the audit:** the row stands. See the correction in phase 3.
7. **Nothing links to Contact but the navigation.** A closing line on Home was
   offered and not chosen, so the invitation renders on Contact alone.

## Not done, and why

- **`.entry__context` reads before `.entry__summary` still.** Only the
  typography sorts them. Reversing the order was available and not taken:
  a reader who does want the employer should still meet it first.
- ~~**Unit formatting**~~ **Closed.** See phase 3 below.
- **`medal--bronze`** remains the one staged CSS rule, declared in
  `STAGED_CSS`. It is reachable code awaiting a third place, not dead.

---

# Phase 3: closing the author-led items

Five items that needed a fact only the author had. Four are now closed.

| Item | Resolution |
|---|---|
| `Opportunities & Services` offered consulting | **Raised, deleted, and restored by the author.** The row stands and the block keeps its name. The §3 argument was put and answered; see the correction below. `contact.md` §5 |
| The in-progress paper had no date | **Dateline derived from `site.last_updated`.** Every record on the site now carries one. `report_undated` was deleted with it: `render_publication` emits a dateline on both branches, so the condition it reported is unreachable |
| `In progress` rendered twice on that record | **Status moved to `Under Review`; the dateline keeps the time alone.** `as of August 2026`, then `[Under Review]` |
| Unit formatting drifted | **`duration` is stored as an integer and spaced once in `meta_label`.** `2h` and `48h` became `2 h` and `48 h` |
| `PowerShell automation` cited nothing | **The `jq-finops` bullet now names the tool, and the chip points at it.** See below |

## The two that needed care

**`In progress` twice.** The first fix put `In progress (as of August 2026)` in
the dateline while the `status` chip 40px below still read `In Progress`: one
fact in two slots, in two capitalisations. The slots have different jobs and
the fix is to let each do its own. `MODELS["research"]` declares `status` as a
tag, so the chip owns the status; the dateline owns the time, which is what it
holds on every other record on the site (a published paper's dateline is
`2025`). The record now reads: title, `as of August 2026`, authors and venue,
then `[Under Review] [Second Author]`.

**PowerShell.** The chip claimed production PowerShell and nothing in
`experience.json` mentioned it, so there was no bullet to point at and no
agent could write one: what the work was is a fact only the author has. Put to
the author, the answer was that the evidence had been there all along and did
not name its tool. The `jq-finops` bullet already described *automating
development-environment shutdowns*, and `Automation Accounts` was already a
listed tool on the Cloud platform operations row.

So the bullet now reads *"by automating development-environment shutdowns with
**PowerShell** runbooks in Azure Automation Accounts"*, and the chip points at
`career.html#jq-finops` instead of the top of the Experience block.

**This is the C7 finding paying off twice.** The chip was unverifiable *and*
its claim was true; the block-level anchor hid both facts equally. A citation
that has to name a record is a citation somebody has to check, and checking it
is what surfaced a tool the record had simply forgotten to mention.

## Still open

1. **`Architecture & recovery docs`** points at `career.html#summary`, which is
   prose rather than a record. A green production chip is asserting more than a
   paragraph carries. Needs a bullet on a role record, or the chip retired.
2. **The French translation**, roughly 5,000 words. Seven of eight pages are
   withheld and the build prints the worklist on every run.
3. **The two French `block__intro` lines** on Awards are literal drafts.
4. **Nothing links to Contact but the navigation.**
5. **The `Under Review` paper names a venue it has not been accepted to.**
   `venue: Computers & Industrial Engineering` renders in the slot the
   published paper's accepted venue occupies, so the layout does not
   distinguish *under review at X* from *published in X*. Raised, not acted on:
   it is a claim, and it is the author's.

## Correction to phase 3

**The consulting row was restored by the author, and the Based in row was
split.** Both reverse decisions recorded above, and the record is corrected
rather than quietly overwritten.

`Opportunities & Services` keeps its name and its two rows. The audit argued
the consulting row against [`CLAUDE.md`](CLAUDE.md) §3; the row was deleted on
that reading and the author put it back. **That closes it.** §3 governs how the
role is claimed, which happens on Home's `h1`, the hero lede and the ordering
of Skills & Evidence. What work is accepted is a different question, and it is
the author's. `contact.md` §5 now says so, with an instruction not to re-delete
the row on §3's authority: the argument has been made and answered, and making
it again would be an agent overruling a positioning call that §10 reserves
absolutely.

`Availability` and `Based in` moved out of the channel list entirely and into
Contact's page header, which is the fourth arrangement and the one that names
what they are. `Contact Details` answers *how do I reach you*, and a residence
status and a city answer neither: a reader scanning addresses was meeting a
sentence about EU work authorisation in the middle of them. They render as
`.hero-facts`, the label column Home already puts the same sentence in, in the
`.page-header` slot DESIGN.md §9 permits and Awards fills.

The three arrangements before it, in order: two rows with `Location` on top, which handed a recruiter the disqualifying
half first; one merged row, which fixed the ordering and cost the sentence its
own line; two rows with availability leading, which fixed both and left them in
the wrong section. Neither string was edited at any point, and both still come
from `src/site.json`. `contact.md` §6 carries the table.

**Two audit findings, two author reversals, and both were right.** Worth
recording plainly: an audit can be correct that something is a tension and
wrong that deleting it is the resolution.
