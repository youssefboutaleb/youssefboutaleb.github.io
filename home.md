# Home: the page that restates

The model for `src/pages/index.html`. Every other page on this site owns its
facts. **Home owns almost none of them**, and that single property is what
makes it the most dangerous page in the repository and the reason it needed a
document of its own.

A record on Career is true because it is the record. A figure on Home is true
only for as long as it still agrees with the record it came from. Twice now it
has stopped agreeing, in both directions:

- Impact in Numbers once read *"2 plugins accepted upstream, both listed in the
  official directory"* while `projects.json` had both pull requests `open`.
- After they merged, the same block read *"submitted upstream, both open"*
  while Projects rendered *Accepted upstream*, so the front page was
  **understating** work the site could prove.

The first was caught. The second sat in the build. **Both had the same cause:
a sentence about a record, hand-written somewhere the record could not reach.**

The block no longer writes sentences. It quotes them, from the bullet that
earned them, through an id. Everything below follows from that.

---

## The one rule

> **Home may restate a fact only if the restatement is generated from the same
> data the original renders from, or is a link to it.**

Three ways a block satisfies it:

| Mechanism | Used by | Guarantee |
|---|---|---|
| **Projection**: rendered from another page's records | Currently | Cannot drift. There is one copy |
| **Citation**: a chip that links to the record | Skills & Evidence | `check.py` fails the build on a dead anchor |
| **Quotation**: the record's own sentence, rendered here | Impact in Numbers | Cannot drift. There is one copy, and it lives on the record |

**There used to be a fourth, and it is gone.** Impact in Numbers held a
hand-written sentence beside a hand-written figure, both restating a bullet that
already existed in `experience.json`. Two copies of one fact, kept in agreement
by a person, on the block this document opens by calling the most dangerous on
the site. It now quotes instead: a record names a bullet with `cite`, and the
bullet's own words render. The only claim still typed on Home is the `figure`,
and `check_figure` asserts its value appears verbatim in the text it cites.

That last one is a **lint, not a parser**. Deriving *100x faster* from prose
means guessing; asserting that the string `100&times;` appears in the bullet the
record cites costs nothing and catches the failure that actually happens, which
is a bullet edited without its figure.

**Nothing else on Home may restate anything.** A fourth block wanting to
summarise another page is the signal that the summary belongs on that page.

---

## Block order

```
The opening       identity, claim, availability, credentials
Currently         the job I am doing right now                 ← projection
Impact in Numbers what changed because I shipped               ← restatement
Skills & Evidence what I can do, and what proves it            ← citations
The closing       the invitation, and where to take it         ← projection
```

**The closing is a projection, which is the only reason it is allowed.** It is
the fifth block and the one exception to the shape of the other four: no
heading, no records, one line and a link. The line is not written on Home. It
is `contact_invitation` in `src/site.json`, which already renders as Contact's
own intro, so the two pages share a sentence rather than keeping two in
agreement, which is the same mechanism Impact in Numbers uses and the same
reason `availability` has one owner ([`CLAUDE.md`](CLAUDE.md) §4).

It takes `data-toc-skip` and is absent from the rail on purpose. The rail is a
contents page, and *Get in touch* is not a section of the document: it is the
document ending. Listing it would also print, two inches under the nav bar, a
link to the page the nav bar already links to.

**The order is the reader sequence, not block strength.** Recruiter, hiring
manager, hiring manager, engineer, and it no longer hands off to the engineer
and asks the hiring manager to come back. The blocks also lengthen as the page
descends, so the longest and most detailed one is aimed at the reader who has
already decided to keep going.

Impact in Numbers used to be last, behind a block 3.4 times its size, roughly two
screens down. A hiring manager who read three blocks and left never reached the
one that says what changed.

That order is the three readers of [`CLAUDE.md`](CLAUDE.md) §2 arriving in
sequence, and each block is aimed at one of them:

| Block | Reader | Answers |
|---|---|---|
| The opening | Recruiter, in seconds | Right shape of candidate, what is certified, and can they be hired |
| Currently | Hiring manager | Scale and ownership, today, not three years ago |
| Impact in Numbers | Hiring manager | What actually changed |
| Skills & Evidence | Hiring manager, then engineer | Capability, with the proof attached |

**Currently sits above Skills & Evidence** because it is the only block that
answers *what is this person doing now*, and a hiring manager who reads three
blocks and leaves should have read it. Skills & Evidence is the stronger block
and it survives being fourth: it is also by far the longest, and putting it
higher buries everything underneath it.

That argument was written for Currently and stopped one block short. It is more
true of Impact in Numbers than of any other block on the page, which is why
Impact in Numbers is now third.

---

## The blocks

### The opening

**Home has one opening block, and it is the `.hero-header`.** Portrait, title,
lede, availability, credentials. The one page with a face on it, kept
deliberately ([`CLAUDE.md`](CLAUDE.md) §5), and not repeated elsewhere: eight
portraits is decoration, one is a person.

#### Why there is only one

There were two: this hero, and a Profile block beneath it carrying an intro, a
paragraph and the credentials. Both introduced the same person, and two blocks
with the same job find the same things to say. They did:

> **Lede.** *I build and operate enterprise-scale data platforms on Microsoft
> Azure: ETL/ELT pipelines, API-led integrations between business-critical
> systems, and the observability that keeps them dependable in production.*

> **Profile.** *I have been building on Microsoft Azure since 2024, and working
> in engineering roles since 2022: end-to-end ETL/ELT pipelines with Talend and
> MuleSoft, and the Datadog instrumentation that says when one of them stops.*

Azure, ETL/ELT, integration, observability: both, in that order. About 45 words
spent twice, before the reader reached one piece of evidence.

**That was the one restatement on Home that neither generated nor cited
anything.** The rule at the top of this document exists because Impact in Numbers
drifted twice, and the guard built for it (`cite`, quotation through an id)
cannot see two hand-written paragraphs agreeing with each other by hand. The
fix was not to reword one of them. It was to remove the second block, because
a duplicate is a symptom and two openings was the cause.

Nothing linked to `#profile`, so the anchor cost nothing to retire.

**Do not add a second introduction back.** A block that wants to say who this
person is, above Currently, is this block.

#### What is generated, and what is not

| | Source |
|---|---|
| Portrait, alt text | `portrait`, `portrait_alt` in [`src/site.json`](src/site.json) |
| Availability | `availability` in [`src/site.json`](src/site.json) |
| Credentials | `build.credential_row`, from [`src/data/certifications.json`](src/data/certifications.json) |
| Languages | `build.language_row`, from [`src/data/languages.json`](src/data/languages.json) |
| Title, lede | Written in [`src/pages/index.html`](src/pages/index.html) |

**There is no third line, and there was.** A `hero-header__headline` sat
between the `h1` and the lede reading *Data Engineer &middot; University
Instructor at IHEC &middot; Competitive Programmer &middot; Open Source
Contributor*. The lede below it re-verbed three of those four, IHEC was named
twice in consecutive lines, and *Data Engineer* appeared three times in the
first forty words once the `h1` and the brand bar are counted.

The table above is why it went rather than the lede: **this document listed
"Title, lede" and had never heard of the headline.** It is the element that
arrived without the document, and the one restating. The lede survives because
it carries Azure, which the headline did not, and because the cloud qualifier
lives in its first clause (below). Do not add a third line here: this section
already says the fix for two blocks with the same job is to remove one, and
that applies inside a block as much as between two.

**The availability sentence is never typed into a fragment.**
[`CLAUDE.md`](CLAUDE.md) §4 forbids paraphrasing a residence status, and the
way three different paraphrases appeared was that three places each held their
own copy.

**The credential strip is never typed either, and this is new.** It was four
strings in `site.json` summarising the ten records in `certifications.json`:
*MuleSoft & Talend Certified*, *Datadog Certified in Fundamentals, APM & Log
Management*, and so on. The four agreed with the ten. Nothing made them stay in
agreement, and a stale certification list in the first screen of a site built
on checkable claims is the cheapest possible way to lose the third reader.

It now renders one link per issuer, in the order `certifications.json` writes
them, with `&times;N` where an issuer granted more than one:

> **Certified:** Microsoft ×3 · Astronomer ×2 · MuleSoft · Talend · Datadog ×3

The count is the point: three Datadog certificates and one MuleSoft are not the
same claim, and a bare list of issuer names flattens them into one. The order is
the authored order and not the counts, because sorting here would put the strip
and the block it links to in two different orders.

Every issuer links, because this is the only capability claim on Home that
Skills & Evidence does not govern, and an unlinked credential on a site built
around checkable claims is the one row a reader cannot check.

#### The title is one word

`<h1>Data Engineer</h1>`.

It read `Data Engineer | Cloud & Integration`, and **this document used to
defend that**: the pipe was doing *role, then qualifier*, which is a rank, where
`&middot;` joins peers, and the entry said not to "fix" it. That argument was
wrong on the thing that mattered. `|` is not a separator this repository owns,
it appeared nowhere else in it, and whatever a pipe was meant to signal, what a
reader sees is two things side by side. [`CLAUDE.md`](CLAUDE.md) §3: *if a
change makes the target role harder to name in one word, the change is wrong*,
and the `h1` is where that is tested.

The qualifier did not disappear. It is the first clause of the lede
(*enterprise-scale data platforms on Microsoft Azure*, *API-led integrations*)
where it modifies the role instead of standing beside it, and it is rows 3 and
4 of Skills & Evidence with their proof attached. This is roadmap M5 landing on
the one line where it was most visible.

**Do not put a separator back in the `h1`**, of any kind. A second noun there
is the change §3 forbids.

#### The fact strip

Availability, Certified and Languages sit beneath the lede as `.hero-facts`, a
label column ([`DESIGN.md`](DESIGN.md) §10.2). They are one kind of fact, and
it is the kind the first reader of [`CLAUDE.md`](CLAUDE.md) §2 filters on.
Nothing else belongs in it. A fact a recruiter does not filter on is a record,
and records go in blocks with a citation.

**Two of the three arrived here, for the same reason stated twice.**

Availability used to render a step smaller than everything around it, which
told the reader *footnote* while its position in the hero told them *read this
first*. One of the two was wrong. Its position was right, so the size moved.

Languages used to be the last block on the page. This document already argued
that it belongs on Home rather than Contact because *a filter a recruiter has
to open a second page for is a filter that gets applied by guessing*, and then
put it in the last place on the page a recruiter reaches. Same argument, one
step further: it is a fact line now, next to the other two facts it is read
alongside.

**Levels are the author's, and are not converted.** The wording is LinkedIn's
scale, kept deliberately after CEFR was considered and declined. Do not
"modernise" it to C1/C2, and do not restate a level twice: *bilingual
proficiency (native)* said one thing in two ways, and it now says *Native*.

**Languages is data, and became data by the rule rather than by preference.**
It is [`src/data/languages.json`](src/data/languages.json), because French and
English each cite `teaching.html#courses-taught`, and
[`DESIGN.md`](DESIGN.md) §10 says a list becomes data the moment it restates
facts held elsewhere on the site.

That citation was available all along and was missed. The block's old intro
claimed *"three, and I have taught in two of them"* and was retired as
unverifiable, on the grounds that no language field exists anywhere in
`src/data/`. True, and beside the point: `src/pages/teaching.html` has been
stating **Instruction: French & English** in its spec strip the whole time.
The claim was sound, it was the citation that was missing, and the row now
carries it.

**Arabic cites nothing, and that stays visible.** Inventing a link for
symmetry would be the failure [`CLAUDE.md`](CLAUDE.md) §5 exists to prevent, in
the block that sits highest on the page.

### Currently

**Generated from `experience[0]` in [`src/data/experience.json`](src/data/experience.json).
Never hand-written, and never given content of its own.**

It renders the current role in the site's standard `.entry` grammar: title
line, dateline with tenure, the full `experience` tag row, and one summary
sentence.

```
Data Engineer · JACQUEMUS          Paris, France · Aug 2024 - Present (2 years)
[Luxury E-commerce & Retail] [Permanent] [Remote] [150+ pipelines]
[Azure Data Factory] [Azure Fabric] [Apache Spark] [Datadog]
Order, customer, product and pricing data into a medallion lakehouse, on
flows carrying roughly 800,000 events and records a day and order peaks
near 5,000 an hour at sale events.
```

Three rules:

1. **The record is `experience[0]` after `tenure_sort_key`.** It is not chosen
   by a flag and not named in the fragment. When a new job starts, the block
   follows, because the sort follows.
2. **The bullets do not come along.** Career's job record carries three groups
   of bullets with `Impact:` lines beneath them. Home takes the title, the
   dateline, the tags and one sentence. A reader who wants the bullets has a
   link to them, and duplicating them would make Home a second Career page that
   can disagree with the first.
3. **The one sentence is `home_summary` on the record**, a field that exists
   only for this block. It is hand-written, it lives *inside* the record it
   summarises rather than on Home, and it is the shortest true version of the
   `summary` field above it. If a record has no `home_summary`, the block
   renders without a sentence rather than falling back to `summary`: an
   eighty-word company description is not a Home sentence.

This is the block that answers [`CLAUDE.md`](CLAUDE.md) §3. The tags say
*luxury retail, permanent, remote, 150+ pipelines, Azure and Spark and Datadog*
before a reader has scrolled, and every one of those is the same string Career
renders.

### Skills & Evidence

Owned entirely by [`skills.md`](skills.md). Nothing about its model, its
citations or its two-column layout is decided here.

One thing Home does decide is the **order within a standing**, because the
front page is where positioning is set. `skill_sort_key` sorts on standing,
then `thread`, then evidence count:

- `thread: "trunk"`: the capability supports the Data Engineering claim
  directly.
- `thread: "branch"`: real, proven, and supporting evidence for the trunk
  rather than the claim itself.

The field encodes **which claim a skill serves, never how good anyone is at
it**, which is the distinction that keeps it out of the self-assessment
[`skills.md`](skills.md) exists to refuse. Machine learning and computer vision
is `branch` while carrying six citations and the strongest standing the model
awards: the field did not demote it, it filed it.

### Impact in Numbers

The block that quotes. Records: [`src/data/impact.json`](src/data/impact.json),
rendered as `.result` ([`DESIGN.md`](DESIGN.md) §9.3).

```
€1,400 per month   A recurring monthly saving on the       result__figure
                   platform budget, taken with no SLA      result__consequence
                   impact on the morning reporting             ← quoted, not written
                   pipelines.
                   JACQUEMUS · Career                      result__source
```

Three parts, and only one of them is written by hand:

| Part | Holds | Where it comes from |
|---|---|---|
| `figure` | The number | The record. **The one hand-written claim on Home**, linted by `check_figure` |
| Consequence | What changed | Quoted from the bullet's own `impact` line, through `cite` |
| Provenance | Company (or the derived upstream state) and the page | Both derived from the same lookup as the sentence |

**The figure leads, and that is the whole shape.** This block was an `.entry`
until it was not, and the swap is worth understanding before anyone moves it
back.

`.entry` is the component for a dated record that lives on its own page: a job,
a project, an award. It requires a title, a period and a body. A Selected
Impact record has none of those. It is a pointer to a result. Forcing it into
`.entry` produced every complaint the block attracted:

| `.entry` required | So the block invented | What it cost |
|---|---|---|
| A title | A topic (*Azure cost control*) | 17px bold heading ink for a category |
| Metadata tags | A `figure` chip | 12px grey for the number the block exists to show |
| A period | A company dateline | *Aug 2024 - Present* three times on one page, twice here and once in Currently |
| A uniform shape | A bare `2026` | The one non-job record looking broken |
| Nothing that links | A `source` chip | An identical grey *Career* in four rows of five |

A reader scanning the block got five categories and no outcomes, on the block
whose entire subject is outcomes. [`DESIGN.md`](DESIGN.md) had already written
the correct principle, for the teaching spec strip: *the reader is scanning the
figures, so the label recedes and the value carries the weight.*

`.result` gives the figure the slot and the size the title had. **`title` still
exists on every record and no longer renders**: it is the record's handle, what
a build error names and what tells a person editing `impact.json` which row
they are in. `result` is gone, and with it the amber `tag--result`, the
`tag--figure` and the `tag--source`: the `impact` metadata model no longer
exists, because the block no longer has metadata.

**The provenance line replaced the tag row.** It carries the company for a
cited record and the derived upstream state (*Accepted upstream*) for the
aggregate one, then the page, linked. The link still lands on the bullet
through the `cite` id, never at the top of a long page.

### How a record quotes

A record names a bullet with `cite`. The bullet carries a matching `id` in
`experience.json`, and `cite_index` builds the lookup:

```json
// src/data/experience.json
{ "id": "jq-finops",
  "point":  "Reduced <b>Azure infrastructure spend by &euro;1,400 per month</b> by …",
  "impact": "A recurring monthly saving on the platform budget, taken with …" }

// src/data/impact.json
{ "title":  "Azure cost control",
  "cite":   "jq-finops",
  "result": "Recurring saving",
  "figure": { "value": "&euro;1,400", "unit": "per month" } }
```

Three things come out of that one id, and none of them can be typed:

1. **The sentence.** The bullet's `impact` line, which is the register
   [`DESIGN.md`](DESIGN.md) §9.2 defines for exactly this: *what changed
   because it shipped*. Impact in Numbers is that register at Home's altitude,
   which is why the two share a sentence instead of paraphrasing each other.
   A bullet with no `impact` line renders its `point` text instead: still the
   source's own words, never a summary of them.
2. **The period line.** Company and dates from the record the bullet lives on,
   so a figure cannot be dated to one job and linked to another. It also dates
   the claims honestly: *100x faster* is from 2022 and used to read as current.
3. **The link.** `career.html#jq-finops`, which lands on the bullet rather than
   at the top of a long page. A bullet carries an `id` only where Home cites
   it, because an anchor nothing points at is a URL promise nobody meant to
   make. `check.py` fails the build on one that does not resolve.

### The aggregate exception

The open-source line stands for two pull requests across two project records,
so no single bullet's words can describe it. It declares `upstream_prs`, keeps
a hand-written `evidence`, and takes its `result` from `projects.json` through
the same `UPSTREAM_STATES` table Projects renders from.

**A record carrying both `cite` and `evidence`, or neither, is a build error.**
The exception is for a claim that genuinely aggregates, and it is not a way back
to hand-writing the sentence.

Project records carry no `impact` register at all: they have `summary` and
plain points, where an experience bullet has the two-part point/impact shape.
That asymmetry is why the exception exists, and closing it would mean giving
projects an impact register, which is a Projects decision and not a Home one.

### The rules that are still editorial

1. **`figure` is the only claim typed on Home**, and `check_figure` lints it
   against the text it cites.
2. **The first three lines are data engineering.** The block is called
   *Selected*, which is an admission that it is curated; the curation is
   allowed to leave out a good result, and is not allowed to make the site look
   like it belongs to a different engineer than [`CLAUDE.md`](CLAUDE.md) §3
   describes. It once held four lines of which two were not data engineering,
   and led on a saving rather than on a pipeline.
3. **Order is the file order, and the file order is the argument.** This is the
   one block on the site that does not compute its own ordering, because there
   is nothing to compute it from: a figure is not comparable to another figure,
   and recency would bury the strongest line. Curation is the point.

---

## What Home no longer carries

Recorded so it is not re-added by someone who notices the gap.

| Block | Where it went | Why |
|---|---|---|
| **Domains** | Deleted | One `.deflist` row listing five industries: no citation, no record, nothing to check. It was the one capability-shaped claim Skills & Evidence did not govern. Career's `domain` tags say it with a dated record under each |
| **Volunteering** | Career, last block | A dated record among dated records. It closed the front page, which put the least Data Engineering thing on the site in the last position a recruiter reads. It goes after the credential blocks rather than between them, so Education, Certifications and Online Courses stay one run |
| **"Seeking a full-time role"** | Deleted | Availability in the hero says the useful half. The rest is what a site like this is for |
| **Contact details** | `contact.html` | They were in the rail on eight pages to be reachable from one. [`DESIGN.md`](DESIGN.md) §4 |
| **Languages** | The opening, as a fact line | A block heading, a pitch line and a `<dl>` were more format than three proficiency ratings can fill, and it closed the page on the one block with nothing to check. Its intro also claimed *"I have taught in two of them"*, which no record in `src/data/` supports. It took `.deflist` with it: [`DESIGN.md`](DESIGN.md) §10 |

---

## Changing something on Home

1. **Adding a figure? Ask where it already lives.** If it is in `src/data/`,
   render it. If it is not, the record it belongs to is the thing to add, and
   Home comes after.
2. **Adding a block? It must be a projection, a citation, or nothing.** The
   restatement mechanism has one user and is not accepting a second without an
   argument written into this file.
3. **Changing the availability sentence** is `site.json` and the author, never
   a fragment and never an agent ([`CLAUDE.md`](CLAUDE.md) §4).
4. **Every block gets a `block__intro`**, one line, and it is a pitch
   ([`DESIGN.md`](DESIGN.md) §11.1). Home is the page a recruiter opens first
   and was, for a while, the page with the fewest pitch lines on it.
5. **A block with no heading needs `data-toc-skip`, and the build says so.**
   A `<section class="block" aria-labelledby="x">` with no `h2` carrying `id`
   `x` raises *page context: no label found*, which is the guard doing its job:
   a rail entry with nothing to print is how a slug ships as though it were a
   title. Either give the block a real heading or declare it out of the rail,
   and the second answer needs the reason written here, as the closing has.
6. Run `python3 tools/build.py && python3 tools/check.py`.
