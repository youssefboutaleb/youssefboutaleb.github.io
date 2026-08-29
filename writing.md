# Writing: metadata model

The declaration for the Technical Articles block on the Research & Writing page:
which categories a self-published article states about itself, in what order,
and what a value in each looks like.

It applies the general rules in [`awards.md`](awards.md) and binds to the
treatments in [`DESIGN.md`](DESIGN.md) §7.1. Neither of those is restated here.
[`research.md`](research.md) is the sibling model it shares a page with;
[`workshops.md`](workshops.md) and [`teaching.md`](teaching.md) are the others.

---

## Why this is a second model and not two more rows in `research`

The Research page carries two blocks that share the `.entry` component and
nothing else. A peer-reviewed paper and a Medium post are both *writing that is
published*, and that is exactly where the similarity stops, so the honest
structure is one page, two blocks, two models.

Merging them fails on all three of the paper model's categories:

- **`status`** would put `Published` on an Elsevier article and `Published` on
  a Medium post. The word is identical and the claim is not: one says *this
  cleared peer review*, the other says *I pressed the button*. Per the rule in
  `MODELS` in `tools/build.py`, two models may share a category name only if
  they mean the same thing by it, and this is the textbook case of not.
- **`authorship`** says nothing on a sole-authored post. `First Author` on a
  piece with one author is a tag that looks like information and carries none.
- **`publisher`** is ruled out by `research.md`'s own vocabulary table: *the
  publishing house, not the platform*. Medium is the platform.

Putting the two lists under one heading fails for a further reason that is
about the reader rather than the data. A merged list forces the type into a tag
on every record, and `research.md` already refuses that: *Journal Article* is
what the block heading says, and a fact true of every record in a block belongs
to the block. Two blocks state the distinction once each, in the two places a
reader actually looks.

---

## The model

```
Model:  writing
Order:  format → reach → platform

  format    what shape of write-up it is   "Walkthrough", "Configuration Guide"
  reach     how far it actually travelled  "3K views · 1.5K reads"
  platform  where it lives                 "Medium"
```

The order is defined once, in `MODELS["writing"]` in `tools/build.py`.

### Why these three, in this order

An article list is read to answer three questions in sequence: *what kind of
thing is this, did anyone actually read it, and where does it live.* The title
carries the subject and the bullets carry the substance, so the model adds
nothing further.

**`format` first.** It is the altitude of the record, as `status` is on a paper
and `level` is on a course. A Configuration Guide and a Walkthrough are read
differently (one is followed at a keyboard, the other is read through) and
that framing belongs before anything else.

**`reach` second.** It is the substance, in the slot `authorship` occupies on a
paper: the reader's real question about a self-published piece is whether it
found an audience, and that is invisible from the title. It takes the violet
the tag family already spends on reach (`scope` says how far an award
travelled, `mode` how far a room did) so the colour was not chosen for this
category so much as already the answer to the question it asks.

**The two figures travel as one value.** Views counts everyone who opened the
tab; reads counts everyone who reached the bottom; and it is the *gap between
them* that says whether the piece held up. Either number alone misleads (views
inflates, reads hides the ratio it should be judged against) so they render as
a single tag, the way `workload` renders a total and its breakdown together.

**`platform` last, and quiet.** Per [`awards.md`](awards.md) it takes the
regular-weight grey and the terminal position, exactly as `publisher` does one
block above, `host` does on Workshops and `scale` does on Awards.

That parallel with `publisher` is deliberate and is the point of the whole
arrangement. Both blocks end their tag list with a grey tag answering *who
stands behind this*, so a reader scanning down the page reads **Elsevier** on
one and **Medium** on the other, in the same position, in the same colour. The
distinction the page has to make honestly gets made by the layout, in a word,
without a sentence of disclaimer anywhere near a record.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `format` | `Walkthrough` · `Configuration Guide` |
| `reach` | `{ "views": 3000, "reads": 1500 }`: two raw integers, never a typed string |
| `platform` | Where the article is hosted: `Medium` |

`format` is the *same* category Workshops declares, reusing its rule rather
than coining a synonym: on both pages it names the shape the deliverable takes
(a Hands-on Lab, a Configuration Guide) so it keeps one name, one meaning and
one colour. This is [`teaching.md`](teaching.md)'s reuse rule applied a second
time, and per [`DESIGN.md`](DESIGN.md) it cost two lines where a synonym would
have cost a colour.

A `Walkthrough` builds one thing end to end and the reader follows along. A
`Configuration Guide` changes the setup of something that already exists. Where
a piece is genuinely neither, add the value to this table in the same change
that adds the record: do not stretch one of these two over it.

**`reach` is all or nothing.** A record carries both figures or omits the
category entirely; `render_meta` drops an absent field cleanly, so an article
with nothing worth reporting simply shows two tags. Publishing views while
suppressing reads is the one arrangement this model must never render: it is
the shape of a number chosen to flatter, and a reader who works out what is
missing discounts every other figure on the page. If the pair would embarrass
the record, leave `reach` off it and let the writing stand on its own.

---

## What is deliberately not in the model

- **The type.** *Technical Article* is what the block heading says.
- **Peer-review status.** *Not peer reviewed* is true of every record in this
  block, so it is never a tag. A per-record disclaimer would be both repetition
  and a strange kind of apology.

  **This paragraph used to say the block stated it once in a `block__note`, and
  the block never did.** No such note has ever been rendered on this page: the
  sentence described a mechanism, the mechanism was not built, and the document
  was the only place the claim existed. What actually states the distinction is
  the layout, and that is the better answer anyway: the grey terminal chip says
  *Medium* here and *Elsevier* one block above, in the same slot and the same
  colour, and a reader who has read both blocks has been told which is which
  without a line of disclaimer anywhere near a record.
- **The stack.** *YOLOv8*, *FastAPI*, *Log4j2* are already in the titles. A tag
  repeating the title is noise: [`awards.md`](awards.md) rule 1.
- **Claps.** Not tracked. They measure approval rather than reading, and
  nothing on this site tracks approval. (Views and reads *are* tracked, see
  the section below for why the same objection does not sink them.)

---

## Why views and reads are tracked when citations are not

The first version of this document ruled these out alongside claps, borrowing
the reason [`research.md`](research.md) gives for citation counts: *a number
that is stale the week after it is written is worse than no number.* The
objection was right and the conclusion did not follow, because the two numbers
are not doing the same job.

A citation count is **redundant**. Scholar publishes it, keeps it current, and
a reader who wants it has a canonical source one click away; restating it here
adds a maintenance burden and no information. A read count is **not**
redundant. It is the only external evidence a self-published article has: it
stands where peer review stands in the block above, and no third party
publishes it on this author's behalf. Declining to state it does not make the
page more honest, only quieter about the one thing this block can prove.

What the objection does earn is the mitigation, which is the dating rule below.
A stale number that says when it was read stays honest as it ages. A stale
number that says nothing starts lying the moment it drifts.

### Refreshing the figures

The counts are read by hand from Medium's stats page, and nothing keeps them
current. Two rules make that safe:

1. **The figures and the date move together, and the build now enforces it.**
   `reach` carries `as_of` alongside `views` and `reads`, in the same object,
   so the figure and its date cannot be edited apart. `check_reach` in
   `tools/build.py` refuses a `reach` without one.

   Update `reach` on every record in one change, or update neither. A fresh
   date over stale numbers is worse than the stale numbers alone, because it
   converts an ageing fact into a false claim.

   **The date is not printed on the page, and this paragraph used to say it
   was.** A `block__note` reading *Reach figures read from Medium, August 2026*
   was built for exactly this and then withdrawn on the author's call: a
   footnote dating two chips is a maintenance promise made in front of the
   reader, and the block is two records that a recruiter scans in four seconds.
   `as_of` stays required and `check_reach` stays fatal, so the discipline is
   unchanged where it does the work, which is in the data: a figure cannot be
   refreshed without its date, or dated without being refreshed, because both
   live in the same object. What changed is that the date is now evidence for
   whoever edits the record rather than a line on the page.

   `.block__note` is back in `STAGED_CSS` with that as its reason. It is still
   the site's provenance component ([`DESIGN.md`](DESIGN.md) §11.2) and it
   still has no user.
2. **Precision follows the source.** Medium reports large figures already
   rounded (*3K*, *1.5K*) so store the rounded expansion (`3000`) rather than
   an exact count nobody measured, and let `abbreviate` in `tools/build.py`
   print it back in the form it arrived in. Storing the integer keeps the value
   comparable; rendering it abbreviated keeps the page from claiming three
   digits of accuracy it was never given.

`as_of` sits on each record and not in one place for the block, which looks
like a violation of [`awards.md`](awards.md) rule 1 and is not: the rule is
about what a *record states to a reader*, and `as_of` states nothing to a
reader. It is the field that makes the figure beside it uneditable on its own.

---

## Editorial rules for the bullets

The tags carry metadata; the prose carries substance. On this block, substance
means **the mechanism the article actually shows**: the decision or the wiring
a reader would otherwise have to reconstruct from the code.

**An article carries `points` and no `summary`, and it used to be the other way
round.** One sentence held the whole record, and on both records that sentence
had become a toolchain flattened into prose: *"End-to-end computer vision data
pipeline: from Roboflow dataset annotation and Kaggle TPU x2 parallel training
(DataParallel) to containerized FastAPI inference and Hugging Face Gradio
serving"* is twenty-seven words, one colon, one parenthetical and four tools,
and it names the topic where rule 2 below asks for the mechanism. Nothing was
wrong with the facts; they were wrong with the shape. Three bullets say the
same four things and can be read in the four seconds a card gets.

1. **Two or three bullets, and one fact each.** A bullet that needs a comma
   splice is two bullets. The card is roughly 280px wide, so a bullet that runs
   past two lines there is too long wherever it is read.
2. **Name the mechanism, not the topic.** "An introduction to observability" is
   a category. "A Log4j2 HTTP appender POSTs JSONLayout events straight to
   Datadog's Send Logs API" is what the article shows.
3. **Never restate the title.** The title is one row above and already carries
   the subject and the stack.
4. **Claim only what the article supports**: [`research.md`](research.md)
   rule 4, and for the same reason: an entry written from the title alone
   invents the parts it does not know.
5. **No bold lead-in label.** Projects writes its bullets as
   `<b>Label:</b> sentence`, and that device belongs to a 74ch reading column
   where a bullet runs two lines anyway. In a 280px card the label spends the
   first line by itself and the reader gets a heading where they wanted a fact.
   One vocabulary, two measures: the site's rule is *use the device that fits
   the measure*, not *use the device the last page used*.
6. **`summary` still renders if a record carries one**, above the bullets, and
   no record does. It is there for an article that genuinely needs a hook
   before its mechanics, not as a second place to put what a bullet says.

---

## The block is a card grid, and the paper block above it is not

The two blocks share `.entry` and now differ in shape, which is the honest
rendering of what this document's first section argues: one page, two blocks,
two models, two things.

Articles render on `.entries--grid` ([`DESIGN.md`](DESIGN.md) §9.4). The test
that component sets is *a set to be counted, not a sequence to be read*, and an
article list passes it: nobody reads two posts top to bottom to see how the
second follows from the first, they scan for what is there and whether the
reach figure is worth a click.

**What it fixes is a comparison this page was making by accident.** In one
reading column, a `writing` record was a `research` record with the citation
line and the bullets missing, so a Medium post did not look like a different
kind of thing, it looked like a paper that had run out of content. §9.5 raised
the papers; this gave the articles a shape of their own rather than a smaller
share of the papers'.

**The record has bullets now, and that does not reopen the test.**
[`DESIGN.md`](DESIGN.md) §9.4 is explicit that the test is about the *list* and
not about the record: nobody reads two articles top to bottom to see how the
second follows from the first, whatever shape either one takes. The empty
`points` array was evidence for the verdict, not the reason for it, and the
verdict is unchanged. What did change is that the box is now doing something a
reading column cannot, which is holding a foot: the chips render last, pinned
to the bottom edge, so the card reads *what the piece is, what it shows, and
the evidence anybody read it*. §9.6 owns that and it is not restated here.

**Rule 5's consequence is unchanged and worth restating here.** An article with
no `reach` yet renders a card with two chips instead of three. Nothing is
invented to fill the cell, and `auto-fit` means a third article lays out as a
third card rather than as a hole.

## The cross-link from Projects

Where an article documents a project that has its own record on the Projects
page, the *project* entry carries a link to the article. It does not get a
second entry there, and the article does not get a duplicate record.

The article is declared once, in `src/data/writing.json`, and rendered once, on
this page. The Projects link is a utility tag on the project record (an
artefact of that work, in [`awards.md`](awards.md)'s sense, the same way a
slide deck is an artefact of a workshop) so it is hand-written where it
applies and carries no ordering rule.

This is the direction that matters: a reader on Projects has found the code and
may want the write-up, whereas a reader here has found the write-up and the
article itself links to its own repository.

---

## Adding an article

1. Append a record to `src/data/writing.json`: position in the file does not
   matter, `publication_sort_key` orders it newest first. Give it a `title`
   (the published title, verbatim), `year`, `format`, `platform`, `url` and two
   or three `points`. Add `reach` once the piece has figures worth reporting,
   as both integers **and** an `as_of`, or not at all; a new article has none
   and simply omits it.
2. Use a value from the vocabulary table above, or add the new value to that
   table in the same change.
3. If it documents a project that has a Projects entry, add the link tag there
   too, per the section above.
4. Translate it. `points` is a list and `t()` reports a list as missing, so the
   French gap is visible on the next build; add `<id>.points` to
   `records` in `src/i18n/fr.json` and re-stamp with
   `python3 tools/build.py --sync`.
5. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `research.html`; it is build output.
