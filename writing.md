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
carries the subject and the summary carries the substance, so the model adds
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
  block, so it is stated once in the `block__note` beneath the records and
  never as a tag. A per-record disclaimer would be both repetition and a
  strange kind of apology; the block says it plainly once, below the work
  rather than in front of it, and then lets the work stand.
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

   **This rule was written here, styled as `.block__note`, and built by
   neither, for as long as the page existed.** Two hand-copied figures shipped
   undated, one of them quoted on Home as a skill citation, on a site whose
   third reader checks. `.block__note` sat in `main.css` with no user and was
   reported as dead CSS on every run while [`CLAUDE.md`](CLAUDE.md) §6 named it
   as the site's provenance mechanism. A rule nothing enforces is a rule the
   repository has only promised.

   Update `reach` on every record in one change, or update neither. A fresh date over stale numbers is worse than the stale numbers
   alone, because it converts an ageing fact into a false claim. The date sits
   in the note and not in the intro because provenance is a footnote: the intro
   is one line and it is a pitch ([`DESIGN.md`](DESIGN.md) §11.1), while a
   hand-copied figure has to say when it was copied, and the two jobs do not
   fit in one sentence.
2. **Precision follows the source.** Medium reports large figures already
   rounded (*3K*, *1.5K*) so store the rounded expansion (`3000`) rather than
   an exact count nobody measured, and let `abbreviate` in `tools/build.py`
   print it back in the form it arrived in. Storing the integer keeps the value
   comparable; rendering it abbreviated keeps the page from claiming three
   digits of accuracy it was never given.

The date lives in the block intro rather than on each record because it is
true of every record in the block: [`awards.md`](awards.md) rule 1, the same
reason *not peer reviewed* is stated once in the block note instead of tagged four
times down here.

---

## Editorial rules for the summary

The tags carry metadata; the prose carries substance. On this block, substance
means **the mechanism the article actually shows**: the decision or the wiring
a reader would otherwise have to reconstruct from the code.

1. **One sentence, and it is not the standfirst.** Say what the piece builds or
   configures, and the choice that makes it worth reading.
2. **Name the mechanism, not the topic.** "An introduction to observability" is
   a category. "A Log4j2 HTTP appender POSTs straight to the Send Logs API,
   with no agent installed" is what the article shows.
3. **Never restate the title.** The title is one row above and already carries
   the subject and the stack.
4. **Claim only what the article supports**: [`research.md`](research.md)
   rule 4, and for the same reason: an entry written from the title alone
   invents the parts it does not know.

---

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
   (the published title, verbatim), `year`, `format`, `platform`, `url` and a
   `summary`. Add `reach` once the piece has figures worth reporting, as both
   integers or not at all; a new article has none and simply omits it.
2. Use a value from the vocabulary table above, or add the new value to that
   table in the same change.
3. If it documents a project that has a Projects entry, add the link tag there
   too, per the section above.
4. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `research.html`; it is build output.
