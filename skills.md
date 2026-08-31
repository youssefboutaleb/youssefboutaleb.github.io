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

In production, and verified outside it                       ← the band, once
Data pipeline engineering   [Azure Data Factory & Fabric at JACQUEMUS]
                            [API-led integration at OLIVESOFT]
                            [Talend Data Integration] [MuleSoft L1]
                            [Astronomer ×2] [Data Engineering 1 & 2] ← citations
                            (Talend) (MuleSoft) (Apache Airflow)     ← tools
────────────────────────────────────────────────────────────────────
Data warehousing & analytics [Azure data platform] [DP-300] [DP-700]
                            [Data Warehousing] [Analytics & Reporting]
                            (Azure SQL) (SQL Server) (PostgreSQL)

Verified, not yet in production                              ← the next band
Workflow orchestration          [Airflow 3 Fundamentals] [DAG Authoring]
                                [Packaging & Delivery]
                                (Apache Airflow 3)
```

Four parts, and each answers a different question:

| Part | Answers | Source |
|---|---|---|
| **Capability** | What can you do? | `name` |
| **Evidence** | How would I know? | `evidence`, keyed by kind |
| **Tools** | What do you do it with? | `tools` |
| **Standing** | How strongly is it proven? | *derived*, and printed **once per run**, see below |

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

**They sit on their own list and are never merged into the evidence.** The
colour-run reading argued below is a claim about the colour of a row's *first*
chip, and an outlined tool chip inside the run would destroy the one thing
giving up positional reading bought. Outlined against filled is also the
distinction [`projects.md`](projects.md) already draws: a filled chip is a
dimension of the record, an outlined one is an item inside a dimension.

**That list sits below the evidence, and it used to sit above.** Which made
this section's own heading false. Every `.skill__proof` opened with the tools,
so 38 outlined grey chips stood at the top of every proof column and *"a row
that starts green ran in production"* was not what the markup rendered: every
row started grey, and the coloured run began a line down, at an offset that
varied with how many tools a capability happens to have. The argument above is
about **merging** the two lists, and it was never an argument about their
order. Below is what makes the sentence it did argue for true.

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

### A citation names the bullet, not the job

**Eight of the block's 41 chips used to land somewhere their label did not
describe.** Four of them, in four different rows, resolved to
`career.html#exp-jacquemus`: *Azure Data Factory & Fabric at JACQUEMUS*,
*Azure data platform*, *Enterprise systems at JACQUEMUS* and *Azure Data Lake
& SQL integration*. A reader checking four capabilities arrived at the top of
the same record four times, three of them having been promised something the
record head does not name. `check.py` had been reporting it as a note on every
run since the fan-in audit was written.

The rule now: **a `production` citation points at a bullet id.** A
certification or a course is a whole record and cites one; a production claim
is a thing that was done, and the site has had an id mechanism for that since
Impact in Numbers needed one. Three bullets gained ids to make it true
(`jq-pipelines`, `jq-api-services`, `olivesoft-api-led`, `oem-classifier`),
which is exactly the condition [`README.md`](README.md) sets for adding one:
somewhere on the site cites it.

`check_citations` in [`tools/build.py`](tools/build.py) fails the build on any
production citation that lands on a record head. The last declared exception,
the medallion lakehouse behind *Data warehousing & analytics*, landed as the
`jq-lakehouse` bullet in the same pass that retired the `PENDING_CITATIONS`
mechanism.

**Two chips may share a destination, and that is not the defect.** *PowerShell
automation* and *€1,400/month saved* both cite `jq-finops`, because that bullet
genuinely proves a scripting claim and a cloud-operations claim, and it names
both. What was wrong was never duplication; it was imprecision.

### Every tool is a fact some record carries

The evidence chips cite. **The tools line does not, and that was read as
harmless because tools were assumed to summarise what the linked records
already say.** Twelve of thirty-six did not: `ActiveMQ`, `SFTP`, `IAM`,
`Application Gateway`, `SQL Server`, `Microsoft Fabric`, *APM & distributed
tracing*, *log management*, `Jira`, `Confluence`, `Postman` and `Agile/Scrum`
appeared nowhere else on the site.

So Home was **originating** twelve facts about the work, in a hand-written
array, on the one page whose model document
([`home.md`](home.md)) exists because facts originating on Home is how it
drifted twice.

`home_tools_audit` in [`tools/check.py`](tools/check.py) now fails when a tool
named here appears on no other built page. It is checked against the built
pages and not against `stack` arrays, deliberately: seventeen legitimate tools
are named in a bullet, a syllabus module or a project body rather than in a
stack, and a rule demanding a stack entry would be demanding the wrong shape.

Two of the twelve were not tools at all. *APM & distributed tracing* and *log
management* are practices, and the row already cites `Datadog ×3`, whose
certificates are Fundamentals, APM and Log Management. They were deleted rather
than rehomed.

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

That sentence is now literally true of the rendered row, which for as long as
the block existed it was not: the tools ran in front of it. See the section
above.

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
row from the top standing. The split is in the renderer and is deliberate, and
`.skill__kinds` reads the same English for the same reason.

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
| **Production-deployed & externally verified** | Run in production **and** certified, taught, or published |
| **Production-deployed** | Shipped, but nothing outside the job confirms it |
| **Externally verified (Pre-production)** | Certified and/or taught, no production record |
| **Applied & academic projects** | A project or coursework only |

**Three of those four were renamed, and the reason was on the page rather than
in the model.** They read *Production-proven*, *Run in production* and
*Verified: not yet in production*. The top two were near-synonyms whose order a
reader could not derive from the words, and the second was **verbatim** the
first chip of the key printed directly above the bands, so four identical words
named a kind of proof in one place and, a line later, a standing weaker than
the band over it. French repeated it: *En production* in the key, against
*Éprouvé en production* and *Exploité en production*.

The labels are the two booleans `standing()` reads, so they now rank by
inclusion: the second band is visibly the first minus a clause, and neither is
a phrase the key uses.

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
the top standing, so citation count decided the front page and put computer
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

### The standing is printed once per run, and it used to be printed per row

`.skills__band`: a `<p>` above each run of rows that share a standing, and the
`<ul>` under it is labelled by it.

**It was a caption under every capability name, and this document defended
that:** *"it stays a caption rather than becoming a sub-heading that groups the
rows. The block already sorts on standing first, so the grouping is there to be
seen without a second heading level inside a block."* That argument lost on two
measurements.

**Seven of ten rows derive the top standing.** So the fixed column, which
exists to give the eye something to run down, printed one string seven times
running: 70% of it saying the same thing on every line it said it on, and the
boundary between the first standing and the second looking exactly like the
boundary between rows three and four. The sort does group the rows. Nothing
rendered the grouping.

**And it was the second rendering of a fact the row already carried.** The
evidence runs in `PROOF` order, so the leading chip is green for exactly those
seven rows, blue for the eighth and violet for the last two: the same three
bands, in the same order, one column to the right. Two columns, one fact, ten
times.

**The heading-level half of the old argument was answered, not overruled.** The
band is a `<p>`, so the block still runs `h2` then `h3`, and the page context
rail (which indexes `li.entry` and `div.entry__group`, never a paragraph) does
not gain ten entries with nothing to say. The French band also stops being
squeezed: *Vérifié : pas encore en production* is 206.2px and the caption's
track was 208px, which is 1.8px of clearance; a band spans the block.

What the band does **not** do is render the second and third sort keys. `thread`
and evidence count still decide the order inside a run and are still invisible,
so a reader who counts chips finds machine learning (six) below rows with four.
**A presence gutter was built to close it and was deleted**, and what it
taught is worth keeping. Five discs between the capability and its evidence,
one per kind of proof, filled where the row had that kind. It was accurate and
cheap (82px, three extra French chip lines) and it still did not earn the
space: it summarised in marks what the row states in words one column to the
right, and the reader who wants to know whether something ran in production is
already looking at a green chip. **Accuracy is not the test for adding an
element. Earning the space is**, which is the verdict
[`CLAUDE.md`](CLAUDE.md) §8 records against the third diagram.

Anything proposed for this column next has to beat that: it must say something
the chip run does not already say.

### Standing carries no colour

The band is muted grey text and nothing else. Colouring it would
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

One row on the page today carries no green chip:

- **Workflow orchestration**: Airflow 3, certified twice by Astronomer and
  taught as a graduate module, but never run in production.

(Distributed processing previously sat here before being linked to production PySpark lakehouse operations at JACQUEMUS and DP-700 certification).

It sits under a band that says *Verified: not yet in production* in as
many words, once, above it. That is the argument stated rather than
left to be inferred from the absence of a green chip.

Leaving this out would make the block shorter and stronger-looking, and would
destroy it. A matrix where everything is maximally proven is a matrix nobody
believes; the unproven row is what makes the proven ones credible, and
is the same argument [`CLAUDE.md`](CLAUDE.md) §5 makes for showing
unmerged pull requests. It also states something true and useful: this is an
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
   runbooks, the recovery procedures and the pipelines they cover, and the chip
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
