# Skills: the evidence model

The Home page block that answers the only question a hiring manager is really
asking: *can this person do the job, and how would I know?*

Every other block on this site describes something that happened. This one
makes a **claim about capability**, which is the one kind of statement a
portfolio cannot be trusted on. So it never stands alone: each capability
carries links to the records elsewhere on the site that prove it, and its
standing is computed from what those links are, never typed, never chosen.

---

## The shape of a skill

Two columns. The left is fixed and says what the capability **is**; the right
flows and holds the **proof**.

```
[Run in production] [Certified] [Taught] [Published] [Applied]   ← the key, once

Data pipeline engineering   (Talend) (MuleSoft) (Apache Airflow)     ← tools
Production-proven ← derived [Azure Data Factory & Fabric at JACQUEMUS]
                            [API-led integration at OLIVESOFT]
                            [Talend Data Integration] [MuleSoft L1]
                            [Astronomer ×2] [Data Engineering 1 & 2] ← citations
────────────────────────────────────────────────────────────────────
Distributed processing      (Apache Spark)
Verified: not yet in prod.  [Processing at Volume]
```

Four parts, and each answers a different question:

| Part | Answers | Source |
|---|---|---|
| **Capability** | What can you do? | `name` |
| **Tools** | What do you do it with? | `tools` |
| **Evidence** | How would I know? | `evidence`, keyed by kind |
| **Standing** | How strongly is it proven? | *derived*, see below |

### Why two columns

The block used to be one run per skill: capability, tools and its citations all
flowing from the same left edge. With ten capabilities and forty chips that read
as a wall, and it hid the one thing the block computes for itself. **The order
is an argument** (standing first, then thread, then how much evidence), and
nothing lined up well enough for that order to be visible. A fixed label column
gives the eye something to run down. It is the same device `.contact-list` uses
for a channel and its address.

Three forms were on the table and two were rejected on evidence:

- **A true evidence matrix**, rows by the five proof kinds, is what this
  document has always called the block. It does not fit. The widest citation is
  45 characters and five columns of that need roughly 1500px against a content
  column of about 1050px, so the chips would have to shrink to about fifteen
  characters, which breaks rule 3 below: the specificity **is** the reason to
  click. And 23 of the 50 cells are empty, which reads as honest variation in a
  list and as a page of blanks in a table.
- **A card grid**, matching Certifications, was rejected twice over. A grid
  reads left to right and down, so the first row stops looking like the first
  row and the computed ranking is thrown away. And [`DESIGN.md`](DESIGN.md) §9
  says entries are never boxed.

### The tools line is the `stack` treatment, and it never leads

Tools render as outlined chips, one per tool, exactly as Career and Projects
render a `stack`: one vocabulary for *a thing this was built with*, everywhere
on the site.

**They sit on their own list above the evidence and are never merged into it.**
The colour-run reading argued below is a claim about the colour of a row's
*first* chip, and an outlined tool chip in front of the run would destroy the
one thing giving up positional reading bought. Outlined against filled is also
the distinction [`projects.md`](projects.md) already draws: a filled chip is a
dimension of the record, an outlined one is an item inside a dimension.

### The key

Five specimen chips above the block, naming what each colour means.

The code was documented here and shown to nobody: a visitor worked out that
green meant production somewhere around the fourth row, if at all. Chips rather
than a worded legend, because the thing being explained is a chip and a
sentence would make the reader hold a translation in their head.

It is the only tag list on the site whose chips cite nothing, which is why they
are `<li>` and not links: a key is a specimen, and giving five specimens an
`href` would put five destinations on the page that prove nothing. It is also
the only tag list that does not print, because the print stylesheet forces every
colour it explains to black.

Admissible under [`CLAUDE.md`](CLAUDE.md) §7's test, the one written for the
depth dial: it is a **reading aid, not a control**. No state, no navigation, no
content that exists in one mode and not another. It makes a code the page was
already using legible on the first row instead of the fourth.

### A tool is not a skill

`Talend` is not a capability; **building pipelines** is, and Talend is one of
the things it is built with. This is why tools sit in a muted line *under* the
capability rather than being the row heading. A list of tool names is what a
keyword filter reads; a list of capabilities is what a person reads.

It also fixes a problem the old Skills list had: *Talend* appeared once, under
*Data Integration & APIs*, and the reader had no way to learn that it was
certified, run in production at two companies, and taught at graduate level.

---

## The proof model

Five kinds of evidence, in one fixed order, declared as `PROOF` in
[`tools/build.py`](tools/build.py):

```
production → certification → taught → published → applied
```

| Kind | Means | Colour | Links to |
|---|---|---|---|
| `production` | Shipped and run in a paying job | Green | Career → Experience |
| `certification` | A third party examined it | Blue | Career → Certifications |
| `taught` | Taught to graduate students, or delivered as a workshop | Violet | Teaching, Workshops |
| `published` | Written up publicly: peer-reviewed or self-published | Amber | Research |
| `applied` | Built in a project, or contested | Grey | Projects, Awards |

The order is **strongest proof first**, and it never varies. That is what makes
the leading colour of a row readable as a fact: **a row that starts green ran
in production; a row that starts blue did not.** The gradient is not a separate
device layered on top: it falls out of the ordering.

Green is the site's *verified/shipped* hue and keeps that meaning here
([`DESIGN.md`](DESIGN.md) §7.2). Grey is the quiet terminal slot every model on
this site ends on (`scale`, `host`, `publisher`, `platform`) and
`applied` joins it because a side project is real evidence and the weakest kind
of it.

---

## The two rules this model breaks, and why

### 1. A category may hold more than one value

Almost every category on the site holds one value, and
[`teaching.md`](teaching.md) is emphatic about it: a `stack` category that
rendered one chip per tool was removed there, because *a run whose length
changes per record destroys the positional reading the fixed order exists to
give.*

There is now one other category that repeats, and the two exceptions are
unalike in a way worth keeping straight. `stack` renders a chip per tool on
Projects and Career because it is the **terminal** category in those models, so
a run of varying length shifts no earlier position and the fixed order survives
untouched ([`projects.md`](projects.md)). It gives up nothing. Skills gives up
positional reading altogether, and the paragraphs below are the argument for
why that trade is worth making here and nowhere else.

**Here the varying length is itself the information.** The other models tag a record
with its *dimensions*: an award has one scope, one placement, one scale, and a
second value in any of them would be a contradiction. This model does not tag
dimensions. It lists **citations**, and citations accumulate: three Datadog
certifications are three separate artifacts a reader can open separately, not
one dimension holding three values.

So the rule is not broken so much as inapplicable. What replaces positional
reading is **colour-run reading**: the categories still appear in a fixed
order, so a reader who wants "was this ever run in production" looks at the
front of the row, and one who wants "is any of this written up" looks for
amber. That is a weaker guarantee than the one-value models get, and it is
bought deliberately: a reader comparing capabilities needs to see *how much*
proof each has, and a model that renders one chip per category cannot show it.

### 2. The block is data, and it restates facts held elsewhere

[`DESIGN.md`](DESIGN.md) §10 draws the line: *a list stays in its page fragment
when that page is the only place its facts live; it becomes data when it
restates facts held elsewhere on the site.* Under that rule, the old Skills
list was correctly markup: nothing else on the site claimed a proficiency.

Adding evidence flipped it. Every chip now points at a record on another page,
which makes this block the second one (after Impact in Numbers) that can
quietly contradict the site it sits on. It is therefore data, for exactly the
reason Impact in Numbers is: the failure mode is a link that names one thing and
points at another, and `check.py` can only catch that if the link is generated.

**Consequence: `check.py` validates every one of these citations.** A chip
pointing at a page that does not exist, or an anchor that does not exist, fails
the build. A skill cannot cite proof the site does not carry.

**And the chip text is translated, which it was not for as long as the French
existed.** `render_skill` read `item["text"]` off the English record directly
instead of through `t()`, so all thirty-nine chips rendered English on
`fr/index.html` while the coverage figure counted them as fine: a field that
never passes through `t()` is a field the build never reports missing
([`CLAUDE.md`](CLAUDE.md) §9). The overlay key is `<skill-id>.evidence` and it
mirrors the whole structure, `href` included, exactly as `groups` does on an
experience record.

**`standing()` still reads the English.** Which kinds of proof a capability has
is a fact about the career and is the same in every language, so deriving it
from the overlay would let a translator who dropped a chip silently demote a
row from *Production-proven*. The split is in the renderer and is deliberate.

Two things stay in English inside the French chips, because the records they
land on do: **certifications**, which are awarded titles rather than
descriptions (*Talend Data Integration*, *DP-700*), and **course titles**,
which `fr/teaching.html` prints in English today. Module names do not: the
syllabus is translated, so *Logging & Monitoring module* becomes *Module
Journalisation et supervision* and the chip says what the heading under it
says. **A chip that names a record in a different language from the record is
the same failure as a chip pointing at the wrong anchor**, and neither
`check.py` nor the build can see it.

---

## Standing is derived, never typed

`standing()` in [`tools/build.py`](tools/build.py) computes one of four labels
from which kinds of evidence a skill actually has:

| Standing | Condition |
|---|---|
| **Production-proven** | Run in production **and** verified outside it (certified, taught, or published) |
| **Run in production** | Shipped, but nothing outside the job confirms it |
| **Verified, not yet in production** | Certified and/or taught, no production record |
| **Applied & studied** | A project or coursework only |

Nothing in `src/data/skills.json` says how good anyone is at anything. That is
the point. **A self-rated level is an opinion; "run in production and certified
twice" is a pair of facts with links on them.** Percentages, five-star ratings
and progress bars are all the same claim wearing a chart, and this site does
not make it.

The block **orders itself** by standing, then by `thread`, then by how much
evidence a skill carries: `skill_sort_key` in the same file. Hand-ordering would
drift the moment a certification is added, and the one thing this block must
never do is rank a skill above the evidence it now has.

### `thread`: the one hand-set field, and it is not a level

`thread` is `"trunk"` or `"branch"`, and it answers **which claim a capability
serves**, never how good anyone is at it:

- `trunk`: supports the Data Engineering claim directly.
- `branch`: real, proven, and supporting evidence for the trunk rather than the
  claim itself. [`CLAUDE.md`](CLAUDE.md) §3's metaphor, in the data.

It exists because the sort had only two keys and four skills tied at
*Production-proven*, so citation count decided the front page and put computer
vision second on a site whose whole argument is that Data Engineering is the
role. It **cannot reorder anything across a standing boundary**: a branch skill
still outranks every trunk skill proven less well than it is, which is what
keeps it from becoming the ranking this model refuses.

Machine learning and computer vision is the only `branch` today. It carries six
citations and the top standing the model awards, and it renders seventh. The
field did not demote it; it filed it. Writing `"thread": "branch"` on a skill to
push it down the page, rather than because it genuinely serves the trunk, is the
one way to misuse this field, and it is the reason it is documented here rather
than left to look obvious.

### Standing carries no colour

The standing label is muted grey text and nothing else. Colouring it would
break [`DESIGN.md`](DESIGN.md) §7.1 (*the treatment belongs to the category,
never to the value*) and would repeat the mistake [`projects.md`](projects.md)
records against an earlier version of this site, where an unmerged pull request
was styled success-green and asserted in colour what the work had not earned.

Green on a chip means *this is a production citation*. Green on a standing
would mean *this skill is good*. The first is a fact; the second is the
self-assessment this whole model exists to avoid.

---

## What is deliberately not evidence

- **Online courses.** They are on the Career page and they are honest there,
  but a completed course proves attendance, not capability
  ([`career.md`](career.md) §3 draws the same line between an *issuer* who
  examined you and a *platform* that hosted lessons). A skill whose only
  support is a course belongs in **Applied & studied**, on its coursework.
- **Years of experience.** A duration is not proof of anything; two years of
  shipping beats five years of watching. The dates are on the Career page for a
  reader who wants them.
- **Self-assessment of any kind.** No levels, no ratings, no bars. See above.
- **A tool with no capability above it.** If a tool cannot be filed under
  something a person *does*, it is a keyword, and this block does not carry
  keywords for their own sake.

---

## The honest rows are the point

Two rows on the page today carry no green chip:

- **Workflow orchestration**: Airflow 3, certified twice by Astronomer and
  taught as a graduate module, but never run in production.
- **Distributed processing**: Spark, taught only.

Leaving these out would make the block shorter and stronger-looking, and would
destroy it. A matrix where everything is maximally proven is a matrix nobody
believes; the two unproven rows are what make the six proven ones credible, and
they are the same argument [`CLAUDE.md`](CLAUDE.md) §5 makes for showing
unmerged pull requests. They also state something true and useful: this is an
engineer who knows the difference between having a certificate and having run
the thing at 3 a.m.

When Airflow reaches production, the row moves up **because the data changed**,
not because anyone re-ranked it.

---

## Adding or updating a skill

`src/data/skills.json`:

```json
{
  "name": "Workflow orchestration",
  "thread": "trunk",
  "tools": ["Apache Airflow 3"],
  "evidence": {
    "certification": [
      { "text": "Airflow 3 Fundamentals", "href": "career.html#cert-airflow-fundamentals" },
      { "text": "DAG Authoring", "href": "career.html#cert-airflow-dag-authoring" }
    ],
    "taught": [
      { "text": "Packaging & Delivery module", "href": "teaching.html#data-engineering-2-m5" }
    ]
  }
}
```

1. **The capability is a thing you do**, not a thing you use. Tools go in
   `tools`.
1. **`thread` is required**, and it is a positioning call, not a rating. If the
   capability is part of doing data engineering, it is `trunk`.
2. **Every evidence entry needs an `href` to a record already on this site.**
   If the proof is not on the site, add the record first: a citation to
   nothing is the one thing this block cannot survive.

   **The `href` names the record, not the block it sits in.** A chip saying
   *Talend Data Integration* and a chip saying *MuleSoft Developer L1* both
   pointing at `#certifications` land the reader on a heading and leave them to
   find which row was meant, which is a click plus a visual search: exactly the
   cost this block exists to remove. Every record type now carries an anchor
   for the purpose (`#cert-talend-di`, `#exp-jacquemus`, `#jq-finops`,
   `#course-machine-learning`, `#data-engineering-2-m4`,
   `#ws-introduction-to-python`, `#proj-...`), so a block anchor means the chip
   is an **aggregate**: *8 contest results* and *2 upstream pull requests* have
   no single record and correctly point at `#competitions` and `#open-source`.

   A chip that is not an aggregate and cannot find a record is not a chip whose
   `href` needs relaxing, it is a claim with no evidence, and the answer is a
   record, a correction, or a deletion.

   **A heading that is not a record is the harder version of this, because it
   passes the build.** *Architecture & recovery docs* pointed at
   `career.html#summary` for as long as the block existed. That anchor
   resolves, so `check.py` was satisfied, but Career's Summary is the author's
   own doctrine paragraph, not a dated record: the chip was rendering green
   for *run in production* on the strength of a sentence saying that written
   architecture documentation is part of the deliverable. Evidence that
   restates the claim is not evidence. It resolved the way this rule says it
   should, with a record: `jq-docs` in `experience.json` now names the
   runbooks, the recovery procedures and the estate they cover, and the chip
   cites that. **Every anchor an evidence chip names should be a record or a
   declared aggregate, and a page's prose is neither.**

   *PowerShell automation* was the example, and how it resolved is worth
   keeping. It rendered green for production while no bullet in
   `experience.json` mentioned PowerShell, so it looked like an overclaim. It
   was not: the `jq-finops` bullet had described *automating
   development-environment shutdowns* all along and had simply never named the
   tool. The bullet says `PowerShell` now and the chip cites it. **A chip that
   cannot find its record is a question, not a verdict**, and only the author
   can answer which of the three it is.
3. **Chip text says what the evidence *is*,** specifically: *€1,400/month
   saved*, not *Azure work*. The chip is the reason to click.
4. **Do not set a standing or a position.** Both are computed. Adding a
   certification is the only way to move a row up, which is as it should be.
5. Run `python3 tools/build.py && python3 tools/check.py`. A broken citation
   fails the build.

A new *kind* of evidence is a change to `PROOF` in `tools/build.py`, one
`.tag--<kind>` rule in `main.css`, and a row in the table above: the same
three steps [`awards.md`](awards.md) requires for a new metadata category.
