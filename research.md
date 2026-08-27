# Research: metadata model

The declaration for the Journal Articles block on the Research & Writing page:
which categories a paper states about itself, in what order, and what a value
in each looks like.

It applies the general rules in [`awards.md`](awards.md) and binds to the
treatments in [`DESIGN.md`](DESIGN.md) §7.1. Neither of those is restated here.
[`workshops.md`](workshops.md) and [`teaching.md`](teaching.md) are the sibling
models.

This model governs the **Journal Articles** block only. The page carries a
second block, *Technical Articles*, on its own model: declared in
[`writing.md`](writing.md), which also gives the reason the two are not merged.

---

## The model

```
Model:  research
Order:  status → authorship → publisher

  status       whether the work is out yet     "Published", "In Progress"
  authorship   which author the site owner was "Second Author"
  publisher    who published it                "Elsevier"
```

The order is defined once, in `MODELS["research"]` in `tools/build.py`.

### Why these three, in this order

A publication list is read to answer three questions in sequence: *is this
real work or work in flight, what was this person's part in it, and who stands
behind it.* The title and the citation line answer everything else.

**`status` first.** It is the altitude of the record, exactly as `level` is on
Teaching. A submitted manuscript and a published article are different claims,
and every bullet beneath is read in that light. Reading it second would mean
re-reading the entry once the status finally arrives.

**`authorship` second.** It is the substance: on a four-author paper, the
reader's actual question is which author this is, and the answer is invisible
from the title. It sits directly under `status` because together they answer
*what state is this in, and what was your part in it.*

**`publisher` last, and quiet.** It is attribution rather than a claim about
the work, which is why it takes the regular-weight grey and the terminal
position, exactly as `host` does on Workshops and `scale` on Awards.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `status` | `Published` · `Under Review` · `In Progress` |
| `authorship` | Derived, never written. See below. |
| `publisher` | The publishing house, not the platform: `Elsevier`, not `ScienceDirect` |

`In Progress` covers a manuscript still being written; `Under Review` covers
one sitting with reviewers. Where the stage is known, prefer the precise value.

**`status` also decides the verb in the citation line.** `PENDING_STATUS` in
[`tools/build.py`](tools/build.py) lists the two values above, and a record
carrying either prints its `venue` as *Submitted to* rather than in the bare
citation slot. Derived, never typed, for the same reason `authorship` is: a
second field saying *this one is only a target* is a field that can disagree
with the status chip 40px below it.

### `authorship` is derived, not typed

Per [`awards.md`](awards.md) rule 7, the raw fact is stored and the label is
produced by the renderer. The data marks one entry of `authors` with
`"self": true`; `author_position` in `tools/build.py` reads its index and
produces `First Author`, `Second Author`, and so on.

A hand-typed `"Second Author"` survives an author list being corrected and then
quietly says the wrong thing. Deriving it makes the two impossible to disagree.

Positions past the fifth fall back to the ordinal (`6th Author`), which is the
honest way to say *well down a long author list*. The word form is used for the
first five because a paper is not a leaderboard: `Second Author` is a role in a
collaboration, where `2nd` would read as a placing.

---

## The citation line

A paper carries more identity than any other record on the site, and it is
distributed across three components rather than pushed into tags:

```
Secure and transparent energy management using …      .entry__title  (linked)
2025                                                  .entry__period
N. Moumni, Y. Boutaleb, F. Chaabane, and F. Drira     .entry__meta:
  Computers & Industrial Engineering
[ Published ] [ Second Author ] [ Elsevier ]          .tag-list
```

**The title is the `entry__title`, not the author list.** Academic convention
opens a citation with the authors, but every record on this site opens with
what the record *is*, and [`DESIGN.md`](DESIGN.md) §9 names a paper as one of
the things `.entry` covers. A reader scanning this page is looking for the
work; the authors are the line beneath it.

### Author formatting

1. **Every author is named, in publication order.** No *et al.*: the list is
   short enough to print, and truncating it hides the position that
   `authorship` then has to assert.
2. **The site's owner is bolded.** It is the ordinary convention on a
   publication list and the thing that makes the page scannable for the reason
   it exists. This is prose, not a tag: [`awards.md`](awards.md) rule 4
   forbids styling a *value*, and says nothing about a citation line.
3. **Each author links to their Google Scholar profile where one exists**, from
   `authors[].scholar`. An author with no profile renders as plain text rather
   than as a dead or invented link: rule 5, applied to a person.
4. **The journal is italic, and follows a `&middot;`.** It is set in
   `.entry__meta` with the authors because it is part of the citation, not a
   dimension of the record.

These are also the two mechanics the block intro used to describe. It no longer
does: an author link and a title link announce themselves, and the intro is one
line (*Applied machine learning taken all the way to peer-reviewed
publication*) per [`DESIGN.md`](DESIGN.md) §11.1.

### The link on the title

`doi` is preferred and `url` is the fallback; the renderer builds
`https://doi.org/<doi>` when a DOI is present, because a DOI is the identifier
that survives a publisher moving its site. A ScienceDirect URL is what to store
until the DOI is to hand.

A record with neither renders an unlinked title. Nothing is invented to make
the title clickable.

---

## What is deliberately not in the model

- **The journal.** *Computers & Industrial Engineering* is already in the
  citation line one row above the tags. Per [`awards.md`](awards.md) rule 1, a
  fact carried by one part of the entry is not restated by another. This is why
  the model asks `publisher` rather than `venue`: *Elsevier* is a fact the
  citation does not give.

  **That reasoning holds only for work that is out, and for a while it was
  applied to work that was not.** The under-review paper printed
  `Authors &middot; <i>Computers & Industrial Engineering</i>`, which is the
  same slot, the same italics and the same journal as the published paper
  above it, and by academic convention that line means *published in*. The
  `Under Review` chip did not undo it: a reader who scans citation lines never
  reaches the chip. The journal still earns its place, because the target says
  something real about the work, so the fix was the verb rather than the
  deletion. See `status` above.
- **The type.** *Journal Article* is what the block heading says. When a
  conference paper is added it takes a second `.block` titled *Conference
  Papers*, exactly as Awards splits into *Competitions* and *Hackathons*: a
  fact true of every record in a block belongs to the block. *Technical
  Articles* is that rule already exercised: self-published writing sits in its
  own block rather than carrying a per-record tag saying so.
- **The subject.** *Embedded Systems*, *Blockchain* are already in the titles
  and the summaries. An earlier hand-written version of this page carried
  `Embedded Systems` as a `.tag--neutral` on one entry of two; a tag repeating
  the title is noise, and one that appears on a single record implies something
  about the other.
- **Citation counts.** Not tracked here. A number that is stale the week after
  it is written is worse than no number, and Scholar already publishes it.

---

## Editorial rules for the summary

The tags carry metadata; the prose carries substance. On this page, substance
means **the engineering problem the paper actually solves**: the thing an
abstract buries in its fourth sentence.

1. **One sentence, and it is not the abstract.** `entry__summary` says what the
   work does and what it was evaluated against. A reader who wants the abstract
   follows the title link.
2. **Name the mechanism, not the field.** "Applies machine learning to energy
   data" is a category. "Two sensing modalities have to agree before a
   detection is reported" is what was built.
3. **Never restate the title.** The title is one row above and is usually
   descriptive enough to make a paraphrase read as padding.
4. **Claim only what the paper supports.** A summary written from the title
   alone stays at the granularity the title actually gives. A thin entry is
   better than an invented one: [`workshops.md`](workshops.md) rule 4, applied
   to a paper where the cost of being wrong is higher.
5. **`points` are for a paper that needs enumerating**: a contribution list, a
   dataset, a result. Most do not; an entry that would repeat its summary uses
   only the summary.

---

## Adding a publication

1. Append a record to `src/data/research.json`: position in the file does not
   matter, `publication_sort_key` orders it newest first, and a record with no
   `year` yet sorts last. Give it a `title`, `authors`, `venue`, `status`,
   `publisher`, a `summary`, and a `year` and `doi` once it is out.
2. Use a value from the vocabulary table above, or add the new value to that
   table in the same change. A new value that means *not out yet* goes in
   `PENDING_STATUS` too, or the record will print its target journal as though
   the journal had accepted it.
3. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `research.html`; it is build output.

Adding a *category* is a larger change: declare it here, add it to
`MODELS["research"]` in `tools/build.py`, give it one `.tag--<category>` rule
in `main.css`, and add its row to `DESIGN.md` §7.1. It must not share a
treatment with the other three.
