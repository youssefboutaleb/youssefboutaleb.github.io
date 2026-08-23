# Projects: metadata model

The declaration for the Projects page: which categories a project states about
itself, in what order, and what a value in each looks like.

It applies the general rules in [`awards.md`](awards.md) and binds to the
treatments in [`DESIGN.md`](DESIGN.md) §7.1. Neither of those is restated here.
[`workshops.md`](workshops.md), [`teaching.md`](teaching.md),
[`research.md`](research.md) and [`writing.md`](writing.md) are the sibling
models.

---

## The model

```
Model:  projects
Order:  upstream → kind → stack

  upstream  whether anyone else took it   "Submitted upstream · PR #586"
  kind      what the deliverable is       "Kanboard Plugin", "Notebook"
  stack     what it is built with         "Python · YOLOv8 · FastAPI · Gradio"
```

The order is defined once, in `MODELS["projects"]` in `tools/build.py`.

### Why these three, in this order

A project list is read to answer three questions in sequence: *did this go
anywhere beyond your own machine, what sort of thing is it, and what is it
built with.*

**`upstream` first.** It is the altitude of the record, as `status` is on a
paper and `placement` is on a contest. A plugin that has been submitted to the
project it extends is a different claim from one that has not, and every line
beneath is read in that light. Only a record that has actually been submitted
carries it; per [`awards.md`](awards.md) rule 5 the others render one tag fewer
rather than an invented one.

**`kind` second.** It is the substance: it says what the reader will find on
the other end of the repository link, which the title usually does not. *Model
& Service* and *Notebook* are the difference between something deployed and
something that runs when you open it: the single most useful fact about an
applied ML project, and invisible from a title.

**`stack` last, and quiet.** Regular-weight grey and the terminal position,
exactly as `scale` on Awards, `host` on Workshops, `publisher` on Research and
`platform` on Writing. A stack is context for the record, not a claim it makes:
*PHP · JavaScript* tells you what you would be reading, and takes the treatment
that says so.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `upstream` | `{ "repo": "kanboard/website", "pr": 586, "state": "open" }`: label and URL both derived |
| `kind` | `Kanboard Plugin` · `Model &amp; Service` · `Notebook` |
| `stack` | A list of at most four tool names, rendered as one tag |

`kind` names the deliverable, not the field. *Computer Vision* is a discipline
and belongs in the summary; *Notebook* is what the repository actually contains.
Where the two ML records differ is exactly what this category exists to say, and
a value that applied equally to both would be worth deleting.

**A notebook is called a notebook.** It is the least flattering value in the
table and it stays, because a reader who is told *Service*, follows the link and
finds four `.ipynb` directories has been given a reason to disbelieve every
other tag on the page. [`awards.md`](awards.md) rule 6: prefer the plain fact
over the claim.

---

## `upstream` states the state, and the colour grades nothing

`state` is stored raw and the wording comes from `UPSTREAM_STATES` in
`tools/build.py`: [`awards.md`](awards.md) rule 7, the same mechanism that
turns `1` into `1st Place`:

| `state` | Renders as |
|---|---|
| `open` | `Submitted upstream · PR #586` |
| `merged` | `Accepted upstream · PR #586` |

The tag says this on sight, which is why the block intro no longer explains it.
Mechanics live in this document; the intro is one line and it is a pitch
([`DESIGN.md`](DESIGN.md) §11.1).

Both take the **same amber**, because the treatment says *this tag is an
upstream status* and never *this status is the good one*. This is the rule
`status` proves on Research, applied to the page where it is easiest to break.

> **What this replaced.** The hand-written version of this page rendered the
> pull request as `Official Plugin PR #585` in the utility **success green**:
> the colour `DESIGN.md` reserves for *verified / published / shipped*. Neither
> pull request has been merged. The styling made a claim the work had not yet
> earned, and it made it in a colour rather than in words, which is precisely
> what rule 4 forbids. The tag now says which of the two states it is in, and
> links to the pull request so the reader can check.

Storing `state` by hand has the ordinary cost: nothing re-reads GitHub, so a
merge upstream will not update this page. Flip `state` to `merged` in the same
change that notices it. The failure mode is a record that undersells itself,
which is the right direction for this particular field to fail in.

### The link on the tag

`upstream` was the first of the two categories on the site whose value carries
a URL: [`career.md`](career.md)'s `accreditation` is the other, and follows
this reasoning. The pull request *is* the evidence for the claim the tag makes,
so the tag is the link; `meta_url` in `tools/build.py` builds the address from
the stored repo and number, for the reason [`research.md`](research.md) builds
a DOI link: the identifier is the durable fact and the URL is derived from it.

A linked tag keeps its category's colour. The link is a route to the evidence,
not a different kind of tag.

---

## Why `stack` is one tag and not four

[`teaching.md`](teaching.md) removed a `stack` category that rendered one chip
per tool, and the rule it broke governs here too:

> **A category holds one value.** A run of tags whose length changes from
> record to record destroys the positional reading that the fixed order exists
> to provide.

The hand-written version of this page had it both ways and neither well: the
plugins carried a category tag and a PR link, while the ML projects carried
four loose `.tag--neutral` technology chips. Two records could not be compared
down a column because no column existed.

Projects nonetheless *needs* the category ([`awards.md`](awards.md) rule 3
names `stack` among the things a reader may genuinely need) so it is kept and
rendered as **one tag**, joined by `·`, the way `workload` renders a total with
its breakdown and `reach` renders a pair. One value, one position, one colour.

**Four tools is the cap.** A `.tag` is `white-space: nowrap`, so a long value
cannot wrap and will push past a narrow viewport. A stack that will not fit in
four names is a sign the record should name the rest in its summary, which is
what the YOLOv8 entry does with Docker and Vercel.

---

## One model, two blocks

The page splits into **Open Source & Plugins** and **Machine Learning & Applied
AI**. The split is a filter on `block` in `build()`, not a second model:

```python
open_source = [p for p in projects if p.get("block") == "open-source"]
ml_projects = [p for p in projects if p.get("block") == "machine-learning"]
```

`block` is **not a metadata category and never renders.** This is the one place
Projects deliberately departs from Awards, which filters on `type` and then
tags `type` on every record, restating the heading it already sits under:
the tension [`awards.md`](awards.md) records against itself. Projects resolves
it [`research.md`](research.md)'s way: a fact true of every record in a block
belongs to the block.

Both blocks render through `render_project` and the one `MODELS["projects"]`
order, so a reader who learns the tag positions in the first block reads the
second without relearning them.

---

## Editorial rules for the summary

The tags carry metadata; the prose carries substance. On this page, substance
means **what the thing does for whoever uses it**, not the technique, which
`stack` already names.

1. **One sentence, and it says what the software does.** "Reads the digits off
   a utility meter photograph" is the record; "designed and implemented a deep
   learning model" is a description of having done work.
2. **Never restate a tag.** *YOLOv8*, *FastAPI* and *Gradio* are in `stack` one
   row up. The summary's job is the part no tag carries, where the weights are
   actually served from.
3. **Name what the reader would otherwise have to clone the repo to learn.**
   Four successive versions in one notebook; a containerised API on Vercel and
   a Gradio Space beside it.
4. **Claim only what the repository supports**: [`research.md`](research.md)
   rule 4. A summary written from the title alone invents the parts it does not
   know.
5. **`points` are for a project that needs enumerating.** Most do not; an entry
   that would repeat its summary uses only the summary.

---

## The article cross-link

Where a project has a write-up on the Research page, the project record carries
`"article": "<id>"` and `render_project` resolves it against
`src/data/writing.json`. The URL is not repeated here: one address, one file,
and a project can no longer point at something the Research page has changed.

The article renders as a utility tag after the model's three, because it is an
artefact of the work rather than a dimension of it: the same standing a slide
deck has on a workshop. See [`writing.md`](writing.md) for why the link runs in
this direction and not the other.

---

## Adding a project

1. Append a record to `src/data/projects.json`: position in the file does not
   matter for ordering across years, `project_sort_key` sorts newest first, and
   records sharing a year keep their file order. Give it a `title`, `block`,
   `year`, `repo`, `kind`, `stack` and a `summary`.
2. Add `upstream` only if it has actually been submitted somewhere, with the
   real `state`. Add `article` only if a record in `writing.json` covers it,
   by that record's `id`.
3. Use a value from the vocabulary table above, or add the new value to that
   table in the same change.
4. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `projects.html`; it is build output.
