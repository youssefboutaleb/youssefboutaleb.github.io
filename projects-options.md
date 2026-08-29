# Projects: the record foot pass

What was found on the Projects page, what was decided, what was built, and what
is still the author's. The next agent reads this file, not the transcript.

The brief was *take the page design to the next level without changing the
content unnecessarily*. Five directions went to the author; one was chosen. **No
content changed.** No record was rewritten, no bullet reworded, no tag value
altered, no project added or removed.

---

## Before and after

| | Before | After |
|---|---|---|
| `MODELS["projects"]` | `kind → stack` | `kind → upstream → stack` |
| The upstream standing | A chip in the proof footer, second in the row | A chip in the scan line, second in the row |
| Where a plugin states it cleared review | Below the bullets, at 12px, after the repository link | Line three of the record, where every other record states its standing |
| The proof footer holds | Repository, upstream PR, demo, article, slides | Repository, demo, article, slides. Artefacts only |
| The footer's visible label | `Project proof`, on all four records, ~25px each | Deleted. A name survives as the list's `aria-label` and nothing else |
| That accessible name | `label.project_proof`, *Preuves du projet* | `label.project_links`, `Project links` / *Liens du projet* |
| `.entry__proof-label` | A rule in `main.css` | Deleted, with the markup that used it |
| A plugin's footer | Two chips | One chip, the repository |
| `render_project`'s docstring | Described a footer holding the upstream review | Describes artefacts, and points at `MODELS` for the reversal |
| `README.md` | Declared `upstream → kind → stack` (stale, never built) | Declares what is built |
| `DESIGN.md` §7.1 | Listed `.tag--upstream` above `.tag--kind` (stale) | Lists them in model order, with the reason for the amber |

Unchanged, deliberately: every title, every summary, all twelve bullets, every
tag *value*, both block headings, both `block__intro` lines, the page lede, the
`stack` treatment, the footer's hairline, and the order of the artefact links
inside it.

## The finding, and it was one finding

The foot held two kinds of statement as visual peers, and the repository
already knew they were different kinds:

- `MODELS` in `tools/build.py` said upstream was *"proof of a project's
  adoption, not a dimension of the deliverable"*, so it belonged with the
  artefacts.
- `main.css`, above `.tag--upstream`, said it was amber *"because it is a
  status, and amber is what a status looks like here: the same rule that puts
  Published and In Progress in one colour on Research."*

`.tag--upstream` and `.tag--status` resolve to the identical `--status-honor`
triple. The stylesheet had filed the tag with Research's `status` family; the
model had filed it with the repository links. Research puts that family at
position 1 of its scan line. This page put it at the bottom of the record.

Three symptoms followed from that one cause, and all three closed with it:

1. The row led with its most routine item. `render_project` appended the
   repository first, and all four records carry one; the standing, carried by
   two of four, came second.
2. `Project proof` rendered identically on all four records, spending ~25px of
   vertical each to name the rank the hairline above it already draws.
3. The page's only external validation sat at 12px, below the bullets, behind a
   link every record has.

**Lesson 31 fired** (a model document that contradicts itself means the page is
already broken), and so did **lesson 32** (grep for the argument before writing
it: the CSS comment made the case better than a fresh argument would have).

## What was decided, and by whom

Two questions went to the author. Both were answered before anything was built.

| Question | Decision |
|---|---|
| Where the upstream standing sits | The scan line, as a metadata category |
| The footer's visible label | Deleted |

**The five directions, and what happened to the four not taken.** Recorded so
they are not re-proposed as new:

| Direction | Outcome |
|---|---|
| A. Rank the open-source block (`--text-xl` titles, `--space-6` rhythm), on §9.5's precedent | **Not chosen, still open.** It buys the plugins credibility by visibly demoting the ML block, which is positioning and the author's call |
| B. A header card grid, as Awards and Workshops have | **Not chosen.** Four records make a per-project card a 1:1 projection, which §9.4 names as the page saying everything twice. Only admissible if it aggregates over verification standing |
| C. Rebuild the record's foot | **Chosen and built** |
| D. A diagram of the YOLOv8 serving path | **Refused by the author.** No diagrams on this page |
| E. Two-column ledger geometry, borrowing `.skill`'s grid | **Not chosen.** It breaks §9's fixed part order to buy a preference, not to correct a false statement, which is the bar §9.5 sets |

## Corrections to my own earlier claims

- I told the author the proof footer rendered the standing and the routine
  links **identically**. It did not: `.tag--upstream` is amber and
  `.tag--artifact` is neutral grey. The conflation was positional and
  typographic, not chromatic, which made the fix cheaper than the first
  description implied.
- I wrote that deleting the label would also delete the French string
  `label.project_proof`, and in the same option that the list would keep its
  `aria-label`. Those cannot both hold. **The string stays** and serves the
  `aria-label`; only the visible `<p>` and its CSS rule went. The collision was
  named to the author before the build rather than resolved silently.
- I proposed Direction C as *the standing carries the ink, the artefacts stay
  chips beneath it*. Investigation moved it: giving the foot its own rank would
  have bought hierarchy with a new treatment for one page, which §9.5 and §9.6
  both refuse. The built version pays for the rank out of **order** instead, by
  moving the standing to where the site already states standings.

## A stale document that this pass happened to make true

`README.md` declared the Projects model as `upstream → kind → stack` and
`DESIGN.md` §7.1 listed `.tag--upstream` above `.tag--kind`, and both said so
throughout the period the tag actually rendered in the footer. Neither was
propagated when it moved. **Both put `upstream` first; the built order puts it
second**, after `kind`, on the ground that `kind` is carried by every project
and `upstream` by two of four, and a category some records omit reads better
after the one they all carry. The documents were aligned to the decision rather
than the decision to the documents, which is recorded here because the reverse
would have looked identical in a diff.

## Measurements

Taken with `fontTools` against the shipped `Noto-Sans-700` at 12px with the
0.02em tracking `.tag` sets, plus 16px of horizontal padding per chip and the
8px `.tag-list` gap.

| | Width |
|---|---|
| `Accepted upstream · PR #586` chip | 195px |
| `Contribution acceptée en amont · PR #586` chip (FR) | 276px |
| Plugin scan line, EN (4 chips) | 468px |
| Plugin scan line, FR (4 chips) | 549px |
| YOLOv8 scan line, EN (5 chips, unchanged by this pass) | 354px |
| Plugin footer after the move (1 chip) | 138px |

The document column is 908px at full width, so both scan lines hold one line
and wrap on a phone like every other tag list. **The French chip is 276px and
`white-space: nowrap`**, against a content column of roughly 308px at a 360px
viewport. It fits, and it was already rendering at that width in the footer, so
the pass neither created nor worsened the risk. It is the widest single chip on
the page and the one to watch if the French wording ever grows.

## What could not be verified

There is no headless browser here. Layout is reasoned from the metrics above
and from reading the built markup, not seen. Specifically unverified by eye:

- How the one-chip footer on a plugin record reads under its hairline, 16px
  margin and 12px pad. The apparatus is heavier than its contents now, and it
  was flagged as a cost of the chosen option before it was built. **Worth
  looking at on a screen**, and lesson 40 says a defect deferred for lack of a
  screen is usually one deferred for lack of a measurement.
- The wrapping behaviour of the four-chip scan line between 620px and 360px.

## Still open, and author-led

1. **Direction A.** The plugins and the notebooks still render at one rank. The
   geometry no longer hides which two cleared external review, because the scan
   line now says so, but it does not rank them either. Whether it should is a
   positioning decision.
2. **The one-chip footer.** If the hairline apparatus is judged too heavy for a
   single repository link, the options are to drop the footer when it holds one
   item (conditional chrome, which is usually worse) or to leave it, which is
   what shipped.
3. ~~**`Project proof` as an `aria-label`.**~~ **Closed by the author in the
   same pass.** The key is `label.project_links`, rendering `Project links` and
   *Liens du projet*. The old key was removed from `fr.json`, and the lock
   dropped it on `--sync` without being edited by hand, because the lock is
   rewritten from the keys the build actually used.
