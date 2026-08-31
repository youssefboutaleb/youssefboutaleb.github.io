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
Order:  kind → upstream → stack

  kind      what the deliverable is       "Kanboard Plugin", "Notebook"
  upstream  how it was received           "Accepted upstream · PR #586"
  stack     what it is built with         "Python" "YOLOv8" "FastAPI" "Gradio"
```

The order is defined once, in `MODELS["projects"]` in `tools/build.py`.

### Why these three, in this order

A project scan line answers three questions: *what sort of thing is it, how was
it received, and what is it built with?* The separate proof footer answers the
fourth: *where can I go and look?* It holds the repository first, then a live
demo, article, or slide deck when those artefacts exist.

**`kind` first.** It is the substance: it says what the reader will find on
the other end of the repository link, which the title usually does not. *Model
& Service* and *Notebook* are the difference between something deployed and
something that runs when you open it: the single most useful fact about an
applied ML project, and invisible from a title.

**`upstream` second, and it was in the footer until this pass.** The reversal
is argued in full below, under *Why `upstream` is a category and not an
artefact*. It sits after `kind` rather than before it, which is where
[`research.md`](research.md) puts the equivalent `status`, for one reason:
`kind` is carried by every project and `upstream` by two of four, and a
category some records omit reads better after the one they all carry.
[`awards.md`](awards.md) rule 5 governs the omission, exactly as it does for a
contest that never published a rank.

**`stack` last, and quiet.** Terminal in the order, exactly as `scale` on
Awards, `host` on Workshops, `publisher` on Research and `platform` on Writing.
A stack is context for the record, not a claim it makes: *PHP*, *JavaScript*
tells you what you would be reading, and takes the treatment that says so. It
is the one of them drawn as an outline rather than a fill, and the one that
renders a chip per value; both are argued below.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `kind` | `Kanboard Plugin` · `Model &amp; Service` · `Notebook` |
| `upstream` | `{ repo, pr, state }`, `state` being `open` or `merged`. The chip is the link to the pull request |
| `stack` | A list of at most four tool names, one outlined chip each |
| proof | Repository required; optional `demo`, `article`, and `slides` links in the dossier footer |

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

## The proof footer

Every project ends with a footer, separated from the technical detail by a
hairline. It holds **artefacts, and only artefacts**: places a reader can go
and look. The repository is required and comes first; optional links follow in
a fixed order: live demo, article, slides.

The word *artefact* is doing the work, and it is what the section below turns
on. A repository, a Hugging Face space and a slide deck are destinations. An
upstream acceptance is not a destination, it is a fact about how the work was
received, and it used to render in this row as a peer of the repository link.
It does not any more.

### It carries no visible label

The footer opened with a muted `Project proof` line until this pass. It
rendered identically on all four records, spending roughly 25px of vertical
each (a 17px line and an 8px margin, about 100px across the page) to name the
rank the hairline directly above it already draws. Compare `What was built`
one group up, which earns its line by naming what the bullets are.

**A name survives as the list's `aria-label` and nowhere else.** Every tag list
on the site carries one, so deleting the name outright would have left an
unnamed list; what was deleted is the `<p>` a sighted reader did not need and
the `.entry__proof-label` rule that styled it.

**And the name changed with the row.** It is `Project links` now (French:
*Liens du projet*), under the key `label.project_links`. `Project proof` was
accurate while the row mixed an upstream acceptance with a repository; once
`upstream` moved to the scan line, what is left is four kinds of destination,
and calling them *proof* named the wrong half. That is the same rule the
visible label failed: say something about the record, or say nothing.

---

## Why `upstream` is a category and not an artefact

This reverses a documented decision, so both sides are kept.

**The argument that put it in the footer**, recorded verbatim in
`MODELS["projects"]` before this pass:

> Upstream acceptance is proof of a project's adoption, not a dimension of the
> deliverable. Projects therefore place it with the repository, demo and
> write-up in their proof footer; the scan line answers only what the
> deliverable is and what it is built with.

**Why it lost.** `status` on [`research.md`](research.md) is not a dimension of
the deliverable either. *Published* says nothing about what a paper **is**, only
about how the outside world received it, and it sits at position 1 of that
model rather than in a footer. By the line the paragraph above draws,
`MODELS["research"]` would be `("authorship", "publisher")`.

The stylesheet had already settled it, in its own words, above `.tag--upstream`
in `main.css`:

> `upstream` is amber because it is a status, and amber is what a status looks
> like here: the same rule that puts Published and In Progress in one colour on
> Research.

Both categories resolve to the identical `--status-honor` triple. So the site
had decided this tag belonged to the status family and left it filed with the
artefacts, which is the contradiction the reader met on the page: the page's
strongest fact, and the only external validation these four records carry, set
at 12px below the bullets, under a chrome label, behind a link every record has.

**Two documents never stopped describing it as a category.**
[`README.md`](README.md) declared the model as `upstream → kind → stack` and
[`DESIGN.md`](DESIGN.md) §7.1 listed `.tag--upstream` above `.tag--kind`, both
throughout the period the tag rendered in the footer. Neither was propagated
when it moved. They are aligned to the order actually built now, which puts
`upstream` second.

### `state` states the state, and the colour grades nothing

`state` is stored raw and the wording comes from `UPSTREAM_STATES` in
`tools/build.py`: [`awards.md`](awards.md) rule 7, the same mechanism that
turns `1` into `1st Place`:

| `state` | Renders as |
|---|---|
| `open` | `Submitted upstream · PR #586` |
| `merged` | `Accepted upstream · PR #586` |

Both take the **same amber**, because the treatment says *this tag is an
upstream status* and never *this status is the good one*. This is the rule
`status` proves on Research, applied to the page where it is easiest to break.

> **What this replaced.** The hand-written version of this page rendered the
> pull request as `Official Plugin PR #585` in the utility **success green**:
> the colour `DESIGN.md` reserves for *verified / published / shipped*. Neither
> pull request had been merged at the time. The styling made a claim the work
> had not yet earned, and it made it in a colour rather than in words, which is
> precisely what rule 4 forbids. The tag says which of the two states it is in,
> and links to the pull request so the reader can check. Both have since
> merged, and the wording moved with the data because nothing about it was
> hand-typed.

Storing `state` by hand has the ordinary cost: nothing re-reads GitHub, so a
merge upstream will not update this page. Flip `state` to `merged` in the same
change that notices it. The failure mode is a record that undersells itself,
which is the right direction for this particular field to fail in.

### The upstream link

The pull request *is* the evidence for the claim the tag makes, so the tag is
the link; `meta_url` in `tools/build.py` builds the address from the stored repo
and number, for the reason [`research.md`](research.md) builds a DOI link: the
identifier is the durable fact and the URL is derived from it.

A linked tag keeps its category's colour. The link is a route to the evidence,
not a different kind of tag. Moving the tag into the scan line changed nothing
about that: `render_meta` derives the external marker from the address itself,
so the chip still opens away from the site and still says so.

**One thing this costs, stated plainly.** The two clickable pieces of evidence
on a plugin record now sit apart: the pull request in the scan line, the
repository about 200px below it in the footer. That is the price of the split,
and it is paid because the two are different kinds of claim. A reader looking
for *where do I check this* finds both; a reader scanning for seconds now
reaches the one that matters without reading the bullets first.

---

## Why `stack` is one chip per tool

It was one joined tag until it was not, and both versions were right about
something. The argument is worth keeping in full, because the rule it appears
to break is a real rule.

### What the joined tag got right

[`teaching.md`](teaching.md) removed a `stack` category that rendered one chip
per tool, and the rule it invoked governs here too:

> **A category holds one value.** A run of tags whose length changes from
> record to record destroys the positional reading that the fixed order exists
> to provide.

That rule is sound and nothing below repeals it. The hand-written version of
this page broke it badly: the plugins carried a category tag and a PR link
while the ML projects carried four loose `.tag--neutral` technology chips, so
no two records could be compared down a column because no column existed.

### What it got wrong

**The rule does not reach the last position.** `stack` is the terminal
category in every model that declares it. A run whose length varies at the
*end* of a list shifts nothing before it: positions one through four render in
their fixed places on every record, and a reader comparing `kind` down a column
finds it exactly where it was. The positional reading the rule protects is
never at risk here. It would be at risk the moment `stack` stopped being last,
which is the boundary and the reason this is a rule about *position* rather
than a licence to split any category.

**And the joined tag did not fit.** The version of this document that argued
for one tag already saw the failure coming, and capped the stack at four names
because *a `.tag` is `white-space: nowrap`, so a long value cannot wrap and
will push past a narrow viewport.* The cap was not enough. Four names is still
58 characters on the longest Career record, about 393px of unbreakable chip in
a content column of roughly 308px at a 360px viewport. Separate chips wrap
because `.tag-list` is a flex container; one long chip cannot wrap at all.

So the choice was never *one value per category* against *several*. It was a
correct positional rule applied one position too far, against a value that
overflowed the page.

### What was actually wrong with the old chips

Not their number. Two other things, and both still hold:

| The old run | Why it failed | Still forbidden |
|---|---|---|
| `.tag--accent` on the headline tool, `.tag--neutral` on the rest | Graded a value: *Talend is the important one* | Yes: [`awards.md`](awards.md) rule 4 |
| Loose chips **instead of** categories | Nothing to read positionally, because nothing held a position | Yes: the five categories render first, in fixed order |

Today's run is neither. The fixed `kind` category renders first, and the tools
follow in one treatment, none ranked above another.

### The outline is what keeps them separable

Tool chips are drawn as an outline, not a fill. A filled chip means *a
dimension of this record*; a tool is an item inside one, not a dimension of it.
The reader is meant to see two kinds of thing rather than eight things of
unequal weight, and the distinction is drawn without spending a hue, which the
one-colour-per-category rule has none left to spend anyway.

**Four tools is still the cap**, for the reason it always was, minus the
wrapping half: a stack that needs more than four names should name the rest in
the record's summary, which is what the YOLOv8 entry does with Docker and
Vercel. The cap now governs how much a reader is asked to hold, not how much
fits on a line.

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
order. Their dossiers use the same sequence: scan line, summary, `What was
built`, then proof. A reader who learns the first block reads the second
without relearning it.

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

## Dossier detail and proof links

`points` render inside the named `What was built` group. A project's
repository, demo, write-up and slide deck links render together alongside `kind`,
`upstream` and `stack` in the top metadata scan line tag list directly under the title
and period, keeping all entry tags unified at the top.

### The article cross-link

Where a project has a write-up on the Research page, the project record carries
`"article": "<id>"` and `render_project` resolves it against
`src/data/writing.json`. The URL is not repeated here: one address, one file,
and a project can no longer point at something the Research page has changed.

The article tag renders in the top metadata tag list alongside repository and demo links.
See [`writing.md`](writing.md) for why the link runs in this direction and not the
other.

---

## Adding a project

1. Append a record to `src/data/projects.json`: position in the file does not
   matter for ordering across years, `project_sort_key` sorts newest first, and
   records sharing a year keep their file order. Give it a `title`, `block`,
   `year`, `repo`, `kind`, `stack` and a `summary`.
2. Add `upstream` only if it has actually been submitted somewhere, with the
   real `state`. It renders as a chip in the scan line, not in the footer.
   Add `demo`, `article`, or `slides` only when they are genuine material a
   reader can inspect; those render in the footer, and `article` names a record
   in `writing.json`.
3. Use a value from the vocabulary table above, or add the new value to that
   table in the same change.
4. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `projects.html`; it is build output.

## The page lede

> *The engineering I do when the requirements are mine to write.*

Projects has two blocks and each carries its own pitch, so nothing could be
promoted and this line was written with the author. It says the one thing
neither intro covers: every record on this page was chosen rather than
assigned, which is why a page of side work belongs on a CV at all.

**It replaced a line derived from [`CLAUDE.md`](CLAUDE.md) §3**, *the same
debugging instinct, applied to someone else's codebase and to whole pipelines
of my own*. Two things retired it. The block intros were rewritten to carry
concrete facts (an upstream acceptance, a served model), so a lede repeating
the instinct sat above two sentences that had moved past it, and *whole
pipelines of my own* described two notebooks, one of which is served. The §3
sentence is still the source of the open source half of the argument; it is no
longer quoted at the top of the page.

**It must keep clearing the lede test** ([`DESIGN.md`](DESIGN.md) §11.1): it
speaks for both blocks, and it repeats neither intro. A third block on this
page is the moment to re-read it.

## The block intros

> *Built for an open source project, and accepted into its official plugin
> directory.*
>
> *From raw dataset to live API: custom data pipelines and containerized
> endpoints.*

Both replaced sentences that named the category instead of pitching it:
*tooling and workflow integrations built to document systems and streamline
engineering workflows*, which said *workflow* twice and reached for the
register [`CLAUDE.md`](CLAUDE.md) §6 bans, and *applied computer vision and
model serving pipelines built for automated data ingestion and inference*,
which restated `stack` and `kind` and claimed ingestion for a record that
colorizes photographs.

**Each now lands on the block's strongest checkable fact**, which is the
[`DESIGN.md`](DESIGN.md) §11.1 job: the first on the upstream acceptance both
plugin records carry, the second on the split between the model that reached a
service and the one that stayed a notebook. The second states that asymmetry
rather than averaging it, which is [`CLAUDE.md`](CLAUDE.md) §5's rule applied
to the pitch layer: a block where every record looks maximally finished is a
block nobody believes.

**The cost is that both run close to the records below them.** The upstream
acceptance is also an amber chip on both plugins, and *notebook* is the `kind`
tag on both ML records. That is admissible where a summary restating a tag is
not (rule 2 above), because the intro speaks for the block and the tag speaks
for one record: the pitch is that *both* were accepted, which no single chip
says. If a third open source record ever lands without an upstream acceptance,
this sentence is wrong and goes first.
