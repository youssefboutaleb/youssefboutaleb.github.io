# Career: experience and credential models

The declaration for the Career page. It carries **three** record types, not
one: a job, a qualification, and a credential. The first two answer metadata
models; the third deliberately answers none, and the reason is the more useful
half of this document.

It applies the general rules in [`awards.md`](awards.md) and binds to the
treatments in [`DESIGN.md`](DESIGN.md) §7.1. Neither of those is restated here.
[`workshops.md`](workshops.md), [`teaching.md`](teaching.md),
[`research.md`](research.md), [`writing.md`](writing.md) and
[`projects.md`](projects.md) are the sibling models.

---

## 1. The experience model

```
Model:  experience
Order:  domain → engagement → mode → scale → stack

  domain      what the data was about       "Luxury E-commerce & Retail"
  engagement  what kind of contract it was  "Permanent", "Summer Internship"
  mode        where it was delivered from   "Remote", "On-site"
  scale       the size of what was run      "150+ pipelines"
  stack       what the work was built with  "Azure Data Factory · Apache Spark"
```

The order is defined once, in `MODELS["experience"]` in `tools/build.py`.

### Why five categories, and why these five

The hand-written version of this page carried a loose run of chips: one
`.tag--accent` for the headline tool and three or four `.tag--neutral` for the
rest:

```html
<li class="tag tag--accent">Talend</li>
<li class="tag tag--neutral">Azure</li>
<li class="tag tag--neutral">Datadog</li>
<li class="tag tag--neutral">REST APIs</li>
<li class="tag tag--neutral">Salesforce</li>
```

Three things were wrong with it, and they are the three this model exists to
fix.

**The run had no fixed length**, so no column existed and the three jobs could
not be compared down one. Five chips on the first record, three on the second,
three on the third: [`teaching.md`](teaching.md)'s rule: *a category holds one
value.*

**The accent on `Talend` graded a value.** Amber-blue said *this is the
important one*, which is a claim about the tool rather than a statement of a
category, exactly what [`awards.md`](awards.md) rule 4 forbids. The stack now
renders as one grey tag and names its tools in the order they mattered, which
says the same thing without spending a colour on it.

**`REST APIs` was not a tool.** It is an interface style, and it was in the
first bullet already. It is gone from the tag and stayed in the bullet.

What replaced them is a fixed model, and it grew to five when the facts it was
waiting on arrived. Each category answers a question one of the three readers
in [`CLAUDE.md`](CLAUDE.md) §2 asks in the order they ask it, and none of them
can be answered by the record's own title:

**`domain` first, and blue.** It is the substance of the record: the slot
`type` takes on an award and `kind` takes on a project. It answers the question
a job title does not: *what was the data about.* Three of the five roles here
are titled some variant of *Data Engineer*, and the title alone cannot say that
one moved luxury retail orders and another moved industrial sensor frames.

**A repeated `domain` is the point, not a collision.** The four employers pair
off into two: JACQUEMUS and OLIVESOFT both read *Luxury E-commerce & Retail*,
and REGIM and OEM share the stem *Time-Series Sensor Data*. Read down the blue
column, the page says **two sectors, two records each**, where four distinct
values said four unrelated jobs. That is the scattered-profile problem in §3 of
[`CLAUDE.md`](CLAUDE.md) answered by the data rather than by a paragraph
asking the reader to see a thread.

OLIVESOFT previously read *Customer Feedback Integration*, which broke the
category's own rule below: it named the system that was built rather than the
business the data belonged to. What it said is not lost, it is the second
sentence of the summary and both bullets, which is where a system belongs.

**A paired value carries its context in parentheses**, so pairing costs no
specificity: *Time-Series Sensor Data (Energy Research)* and *(Industrial
Sorting)* say what the older *Energy Telemetry Research* and *Industrial
Material Sorting* said, and say in addition that the two are the same kind of
work in two settings. The stem goes first because that is the half being read
down a column; the parenthesis is the aside, which is the punctuation
[`CLAUDE.md`](CLAUDE.md) §6 assigns to exactly that job.

**The stem is chosen for the trunk it feeds.** *Sensor Signal Processing* was
the more literal description of both records and was rejected for it: it names
a discipline standing beside data engineering rather than feeding it, and §3
is that a change making the target role harder to name in one word is the
wrong change. *Time-Series Sensor Data* is true of both records (30-minute
interval telemetry across 300 households; roughly 2,000 spectral frames per
second inline) and is a data noun, so the two earliest jobs read as
high-frequency data work rather than as a second career in DSP. The signal
processing itself is not hidden by this: it is the OEM role title, the `stack`
tag, and every bullet under it.

**Pairing is not a licence to round two records into one word.** A stem is
earned when the two records are genuinely the same kind of work, and the test
is whether both sets of bullets still read as evidence for it. If a third
record needs a third value, it gets one: three pairs of two is a structure,
and one bucket holding everything is a category that has stopped saying
anything.

**`stack` last, and quiet.** Reused from [`projects.md`](projects.md), same
name, same meaning, same rule, capped at four names and rendered as one
outlined chip per tool. [`awards.md`](awards.md) rule 3: when a page needs a
category another model already defines, it takes that category rather than
coining a synonym.

**`engagement` second, and amber.** Whether a role was permanent, part-time or
an internship is the recruiter's first question, and the page used to leave it
to be inferred from a job title, which fails outright on OEM: the company
record carries no title at all, only two nested ones. It is amber because it is
the standing of the record, the slot `placement` holds on an award and `level`
holds on a course.

An earlier version of this document declined the category on the grounds that
the fact was *not recorded* anywhere: neither the CV nor the LinkedIn entries
state it, and rule 5 forbids a plausible-looking placeholder. That was right,
and it was a note to go and ask rather than a permanent ruling. The author
supplied all five values, so the category is now stated. **The values are the
author's and are not to be inferred from a date range or a job title.**

**`mode` third, and violet.** Reused from [`workshops.md`](workshops.md), same
name, same treatment: on both pages it answers *where was this delivered from*.
It is on the page because the site is written for remote international hiring
([`CLAUDE.md`](CLAUDE.md) §4), and a recruiter filling a remote role wants
evidence that remote work has actually been done rather than a line in the rail
saying it is acceptable.

`Remote delivery` is the one value that is not a plain work arrangement. It
describes the OLIVESOFT engagement precisely: on-site at a Tunisian delivery
centre, shipping to a Paris consultancy's LVMH account. *On-site* would state
only where the desk was and throw away the fact a reader is looking for.

**`scale` fourth, and grey.** Reused from Awards, Workshops and Teaching
unchanged: the size of the thing the record involved. This is the hiring
manager's question, and before the category existed the answer was buried
mid-paragraph in a company summary, where a reader giving the page seconds
never reached it.

Two shapes of imprecision are stored, and they are different claims:
`"minimum": true` renders `150+ pipelines` (at least this many), `"approx":
true` renders `~2,000 frames/second` (about this many). A record carrying
neither prints the bare figure. Rendering a floor as an estimate, or the
reverse, misstates a number the bullets below state exactly.

`scale` may repeat a figure that also appears in a bullet, and the JACQUEMUS
record does: the tag says `150+ pipelines` and the first bullet says *20+ of a
150+ pipeline estate*. That is not the restatement rule 2 of §6 forbids. The
tag states the size of the platform, which is context; the bullet states the
share of it that is this author's, which is the claim. Dropping either one
leaves a reader with the wrong picture, in opposite directions.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `domain` | `Luxury E-commerce &amp; Retail` · `Time-Series Sensor Data (Energy Research)` · `Time-Series Sensor Data (Industrial Sorting)` |
| `engagement` | `Permanent` · `Fixed-term` · `Part-time` · `End-of-studies Internship` · `Summer Internship` |
| `mode` | `On-site` · `Hybrid` · `Remote` · `Remote delivery` |
| `scale` | `{"count": n, "unit": "...", "minimum"\|"approx": true}`, the flag optional |
| `stack` | A list of at most four tool names, one outlined chip each |

`domain` names what the data was, not the discipline the engineer practised.
*Data Engineering* is the discipline and is the job title; the parenthesis in
*Time-Series Sensor Data (Industrial Sorting)* is where the infrared frames
come from. Each value is derived from what the record's own bullets describe,
and a role whose domain cannot be read off its bullets should get the fact
added to a bullet rather than a tag invented for it.

**A job title states the role and never the contract**, because `engagement`
states the contract one line below it. The records used to read *Data Engineer
Intern* and *Machine Learning Engineer Intern*, which said the same thing
twice, and [`awards.md`](awards.md) rule 1 is that a fact carried by a declared
category is not restated in the record. The titles are now *Data Engineer* and
*Machine Learning Engineer*, with the amber tag beneath each saying exactly
which kind of internship it was: more specific than the word it replaced, not
less. The PDF CV and the LinkedIn entries have to be moved in the same
direction, or §1 of [`CLAUDE.md`](CLAUDE.md) is broken: the two renderings of
one career may not disagree about a title.

`engagement` names the contract, not the seniority. *Data Engineer* and
*Machine Learning Engineer Intern* are titles and already sit at the top of
their records; whether the second was a summer placement or an end-of-studies
one is the fact the title cannot carry. The two internship values are kept
apart rather than collapsed into `Internship` because six weeks over a summer
and a six-month final-year engagement are different propositions, and a French
or EU recruiter reads *End-of-studies Internship* as the PFE it was.

`mode` is the arrangement the role actually ran on, not the employer's policy
and not what the location line says. A record's dateline gives the city; `mode`
says whether the work happened there.

`stack` renders **one outlined chip per tool**, not one chip holding all of
them, and it is the only category on the site that does. The argument is
[`projects.md`](projects.md)'s and is not repeated here; the short version is
that `stack` is always the last category, so a run whose length varies shifts
nothing before it, and that a joined stack ran to 58 characters in a chip that
cannot wrap. What the old hand-written page did wrong was never the *number* of
chips: it was grading one of them with `.tag--accent`, and rendering chips
**instead of** categories rather than after them.

`stack` names tools, not techniques. The OEM role reads `C++` alone: a
Savitzky-Golay filter and a Random Forest classifier are things that were
*built*, and they are named in the bullets that describe building them. A
one-name stack is the honest rendering of a role that used one language.

### A company with more than one role

OEM is the page's only employer with two positions, and the record states the
company, its summary and its `domain` once, then nests both roles beneath. The
alternative is two flat records repeating the same three facts, which reads as
two unrelated jobs and throws away the one thing worth showing: an internship
that turned into an engineering role at the same company inside three months.
That is trajectory, and trajectory is what the hiring manager is reading for
(§2 of [`CLAUDE.md`](CLAUDE.md)).

**The roles sit in one `.entry__roles` wrapper carrying a single left rule**,
the same `border-left` [`teaching.md`](teaching.md)'s assignments use. The
direction of the rule is the whole argument:

| Rule | Says | Correct for |
|---|---|---|
| Left, unbroken | *these belong to the record above* | A progression inside one company |
| Horizontal | *a division starts here* | Nothing on this record |

An earlier version put a `border-top` on each role group, which produced two
horizontal bars inside one entry: the first cutting the company summary away
from the roles it exists to introduce, the second dividing a promotion into two
halves. Two stacked rules also begin assembling, out of parts, the card that
[`DESIGN.md`](DESIGN.md) §9 forbids. One wrapper and one left rule replaced
both, and add no vocabulary the site did not already have.

**A category sits on the company record when it is true of both roles, and on
the role when it is not.** OEM carries `domain` and `mode` at company level:
the business and the site are the same for both positions. `engagement`,
`scale` and `stack` sit on the roles, because a part-time engineering contract
and a summer internship are not the same engagement and did not run the same
stack. Stating either one twice would be the repetition the nesting exists to
remove; stating a role-level fact once at the top would make it wrong for one
of the two roles.

The fixed order holds whichever level a category renders at, so the company
line reads `domain, mode` and each role line reads `engagement, scale, stack`,
and neither is a reordering of the other.

**The company period is the union of its roles** (`Jun 2022 - May 2023` over
`Sep 2022 - May 2023` and `Jun 2022 - Aug 2022`). It is stored, not computed,
for the reason §4 gives about periods generally, and it stays because a year at
one employer is the fact a recruiter weighs first; the nested dates then say
how that year was spent.

---

## 2. The education model

```
Model:  education
Order:  programme → focus → accreditation

  programme      what kind of programme it was   "National Preparatory Programme"
  focus          what it was about               "Data Engineering & Distributed Systems"
  accreditation  who vouches for it              "EUR-ACE® Accredited"
```

Three categories, and **no record renders more than two**. That is not an
oversight, it is the model's governing rule:

> **A category renders only where its answer is not already in the record's
> own title.**

This is [`awards.md`](awards.md) rule 1 applied per record rather than per
model, and it is what keeps a three-category model off the padding that rule 3
warns about. Worked through both records:

| | Degree | Preparatory programme |
|---|---|---|
| Title says | *Computer Science Engineer's Degree* | *Bachelor of Engineering (Mathematics and Physics)* |
| `programme` | omitted: *Engineering Degree* is the title | **National Preparatory Programme**: the title does not say this, and it is the fact the record turns on |
| `focus` | **Data Engineering & Distributed Systems**: the title says computer science and nothing narrower | omitted: *(Mathematics and Physics)* is in the title |
| `accreditation` | **EUR-ACE® Accredited** | omitted: the programme holds none this site can point at |

Two records, two tags then one. The model went from one category to three in
one change, and the two additions each answer a defect rather than filling a
slot.

### `focus`, and why the specialization left the prose

The summary used to carry *specializing in Data Engineering, Distributed
Systems, Cloud Architectures, and Applied AI* mid-sentence. That clause is the
most direct link on the page between the education and the claim in §3 of
[`CLAUDE.md`](CLAUDE.md), and a reader scanning the block never reached it.

`focus` holds two of the four, not all four: a category holds one value, and
*Cloud Architectures* and *Applied AI* stay in the summary and in the **Data &
Systems Specialization** group below. The relationship is the one `scale` has
with its bullet on a job record: the tag is the scan version and the prose is
the full one, and neither is a restatement of the other because they do not
carry the same amount.

It is blue, the substance slot `domain` holds on a job and `kind` holds on a
project.

### `programme`, and the reader it exists for

*Bachelor of Engineering (Mathematics and Physics)*, dated 2019-2021, reads to
a French or Gulf recruiter as a two-year BEng, which sounds truncated. It is
the Tunisian national engineering preparatory programme: competitive entry,
and a competitive national ranking on the way out. Nothing on the record said
so above the summary.

It is amber, the standing slot `placement` holds on an award and `engagement`
holds on a job, because a national preparatory programme is an institution
with a bar to clear rather than a subject.

**The summary was fixed in the same change, and the tag did not do that work.**
[`CLAUDE.md`](CLAUDE.md) §4 is that Tunisian context is made legible rather
than glossed, and a four-word chip cannot explain a national admission system.
The summary now leads with what the programme is and states how admission is
decided; the tag is the scan line, the sentence is the explanation, and a
reader who needs neither has already moved on.

### Why the two additions do not reopen `field` and `level`

They were rejected below and stay rejected. The test is the same one the table
above applies: `field` would print *Computer Science* under a title reading
*Computer Science Engineer's Degree*, and `level` would print *Engineer's
Degree* under the same. Both fail on both records. `focus` and `programme`
pass on the record that carries them and are omitted on the record that would
fail, which is the difference between a category and a slot to fill.

Everything else an education record carries is already on the record and would
be a restatement if tagged. The degree is the title. The institution trails it
in `entry__role`, written out in full rather than abbreviated. Location and
period share the line beneath, in the dateline shape Experience already uses,
so a qualification and a job state where and when the same way. A `field` category would say
*Computer Science* underneath a title reading *Computer Science Engineer's
Degree*, and a `level` category would say *Engineer's Degree* underneath the
same. [`awards.md`](awards.md) rule 1: a fact that does not belong to a declared
category belongs in the record, and a fact already in the record does not get a
category invented for it.

That leaves exactly one thing a reader cannot get from the title: whether the
programme is accredited, and by whom. So the model is one category, and the
second record renders zero tags because the Mahdia bachelor carries no
accreditation this site can point at.

### `accreditation` is grey, and it used to be green

The hand-written page rendered it as a utility tag:

```html
<li><a class="tag tag--success link-external" href="…">EUR-ACE® Accredited</a></li>
```

`.tag--success` is the green [`DESIGN.md`](DESIGN.md) §7.2 reserves for
*verified / published / shipped*. Read as a category it is wrong twice over: it
grades the value (*the accreditation is the good news*) where the category
itself is the information, and it borrows a utility treatment for a dimension
of the record.

`accreditation` now joins `scale`, `host`, `publisher` and `platform` in the
regular-weight grey family, because it answers the identical question
those categories answer: **who stands behind this.** *Elsevier* peer-reviewed
the paper, *IEEE Student Branch ENIS* ran the room, *ENAEE* accredits the
degree. [`DESIGN.md`](DESIGN.md) §7.1: reuse the *treatment* whenever the
question is the same; reuse the *name* only when the answer means the same
thing, so the treatment is shared and the name is not.

### The link, and why it is on the tag

`accreditation` is the second category on the site whose value carries a URL,
after `upstream`. The reasoning is [`projects.md`](projects.md)'s exactly: the
ENAEE page **is** the evidence for the claim the tag makes, and a reader who
wants to check what EUR-ACE® means should not have to go looking. The tag keeps
its category's grey: a link is a route to evidence, not a different kind of
tag.

It is stored as a pair so the two cannot separate:

```json
"accreditation": {
  "name": "EUR-ACE&reg; Accredited",
  "url": "https://www.enaee.eu/eur-ace-system/"
}
```

### The three groups on the engineering degree

The record carries `groups`, not a flat list of bullets, because a degree is
three different kinds of thing and a reader scanning for one of them should not
have to read the other two:

| Group | Answers |
|---|---|
| Graduation Thesis | What was studied in depth, and what it concluded |
| Data & Systems Specialization | What was taught |
| Student Clubs & Training | What was done with the rest of the time |

Two constraints hold this together, and both are easy to break by accident.

**The thesis group states the study, not the build.** The same work is an
Experience record (the OLIVESOFT internship), and the engineering detail (the
tools, the retry policy, the dead-letter handling) belongs there. Education
says what the report argued and that it was defended. Written the other way, a
reader meets one integration twice on a single screen and learns nothing the
second time.

**The clubs group states roles, never events.** Every session this author
personally delivered is already a record on Workshops, with its host, audience
and attendance. What Workshops cannot show is the standing responsibility
behind them: a training track that ran to a schedule, and the work of finding
people to teach the parts the club could not. That is what the group is for. A
line here that names a single session is a duplicate, and the fix is to delete
it, not to reword it.

The same test applies to anything added later: if a fact would be checked on
Awards, Projects or Workshops, it does not get restated here.

---

## 3. Credentials carry no model, and that is the point

Certifications and Online Courses render through one function,
`render_credentials`, into the `.issuer` component rather than into a tag list.
No metadata model, no categories, no order to declare.

**The grouping is the metadata.** Who granted a certificate is the only
dimension of it a reader needs, and it is already the group heading with the
issuer's brand mark beside it. A `.tag--issuer` on every credential inside a
block headed *Datadog* would restate the heading on every row: the tension
[`awards.md`](awards.md) records against its own page, resolved
[`research.md`](research.md)'s way: **a fact true of every record in a block
belongs to the block.**

A credential is therefore two fields:

```json
{
  "issuer": "Datadog",
  "icon": "datadog.svg",
  "credentials": [
    { "name": "Datadog Certified: Fundamentals", "url": "https://www.credly.com/badges/…" }
  ]
}
```

`icon` is a bare filename; `render_credentials` builds `images/icons/<icon>`.
The directory is stated once in the renderer rather than seven times in the
data: [`awards.md`](awards.md) rule 7 applied to a path.

### `issuer` and `platform` are two words on purpose

`certifications.json` keys its groups on `issuer`; `courses.json` keys them on
`platform`. One renderer reads both, taking the field name as an argument.

This is [`writing.md`](writing.md)'s distinction, in the place it matters most.
An **issuer** examined the holder and stands behind the result; a **platform**
hosted lessons the holder watched. Both name who is behind the entry, both sit
in the same position, and collapsing them into one word would let the second
borrow the first's authority: a Udemy course sitting under the same noun as a
MuleSoft certification. The two blocks are also separated by heading, so a
reader who reads no further than *Certifications* and *Online Courses* has
already been told the difference.

That is also why neither block intro spells the distinction out any more. An
earlier pair of intros explained the link policy and defined *course work
rather than examined credentials* in the first line of each block: mechanics
this document already owns (see below), stated where the reader had not yet
been given a reason to care. Both are now one line and both are a pitch, per
[`DESIGN.md`](DESIGN.md) §11.1: *Vendor-certified across every layer of the
stack I ship on*, and *The habit behind the certifications: continuous,
self-directed learning*. The second is deliberately written so the block reads
as the engine behind the one above it rather than as a lesser version of it.

### Every credential row carries the external marker

`render_credentials` puts `.link-external` on all of them, so the arrow means
one thing here: **this row opens away from the page.** That is true of every
credential, since they share one `target="_blank"`, and it holds whether the
link is the issuer's own record or a copy of the certificate this site serves.

An earlier version derived the marker from the URL scheme, so a Credly badge
got the arrow and `data/DP-300.png` did not. The distinction it drew was real
(*the issuer, not me, is showing you this*) but the two Microsoft rows were the
only names in the block with nothing after them, which reads as *not a link*
before it reads as *not third-party verified*, and losing the click is the
worse of the two failures. The provenance is still legible: the row says
*Microsoft Certified*, and what opens is visibly a scan.

Add a Microsoft Learn credential URL the day one is to hand, and the row
becomes checkable at the source without any change to how it renders.

### The rule for adding a credential

**Link the issuer's record of it, or don't add the row.** A course's own
catalogue page is not evidence that anyone completed it; a certificate URL with
a verification id is. Where the platform issues an accomplishment URL, that URL
is the one that goes in.

> **Outstanding.** The Coursera *Machine Learning Specialization* entry
> currently links to the specialization's catalogue page rather than to an
> accomplishment record, which is the one link on this page that does not meet
> the rule above. The sibling *Nand to Tetris* entry shows the right shape:
> `coursera.org/account/accomplishments/verify/<id>`. Replace the URL with the
> accomplishment one, or remove the entry.

### The Microsoft group is named for the issuer, not the product

It reads **Microsoft**, not *Microsoft Fabric*. DP-300 is *Azure Database
Administrator Associate* and has nothing to do with Fabric; the issuer of both
certificates is Microsoft, and grouping is by issuer. The brand mark beside it
is still `microsoft-fabric.svg`, which is now a mismatch: a generic Microsoft
mark would be the correct icon.

---

## 4. Periods are derived

An experience record stores two raw dates and no prose:

```json
"start": "2024-02", "end": "2024-05"
```

`month_year` in `tools/build.py` renders `Feb 2024 - May 2024`, so `Aug 2024`
and `August 2024` cannot appear on the same page. A record with **no** `end` is the
role being held now and renders `Present`: the word comes from `ONGOING` in
the renderer and is never stored, because *Present* is not a date and a record
that stores it keeps claiming the job after it ends.

The period is plain text rather than a `<time>` element: it is a range, and
`datetime` takes one instant. Teaching renders its academic terms the same way
for the same reason.

### The duration is derived too, and it is not a tag

The dateline closes with the length of the role in parentheses:
`Feb 2024 - Jul 2024 (6 months)`, `Aug 2024 - Present (2 years)`. `tenure` in
`tools/build.py` computes it from the same two stored dates, so a duration
cannot disagree with the range printed beside it.

**It is in the dateline and not in the tag list**, and there were three reasons
to keep it out. The model is five categories wide already, which is as wide as
Workshops. A tag list reads as the *categories* of a record and a dateline
reads as *when*, and a duration is a "when" fact: putting it among the tags
asks the reader to change register mid-scan. And unlike every other category on
this page it is **derivable from a line already on the record**, which
[`awards.md`](awards.md) rule 1 rules out: a fact already in the record does not
get a category invented for it. Sitting it beside the dates it comes from also
stops it reading as an independent claim.

**A finished role counts inclusively and a current one does not.** Feb 2024 to
Jul 2024 is six months because both endpoint months were worked; Aug 2024 to a
Present falling in Aug 2026 is twenty-four and not twenty-five, because the
month in progress is not finished. Where the two conventions disagree the
shorter number wins: this is a claim about how long somebody has been employed,
made to readers who will check it.

Two consequences worth knowing about:

- **A current role's duration changes without the data changing.** It is
  computed at build time against today's date, so a rebuild refreshes it and a
  site left unbuilt for six months understates by six months. That is the safe
  direction, and the rail already carries a `last_updated` stamp.
- **Nested roles and their company record must agree.** OEM renders
  `1 year` on the company and `9 months` plus `3 months` on the roles beneath,
  which sums exactly. It sums because the company period is the union of its
  roles (above); if a company record ever carried a period wider than its
  roles, the durations would print the discrepancy in plain sight.

**The per-role durations do not add up to the years claimed in the Summary,
and are not meant to.** The Summary says three years, which counts the paid
roles and not the two internships. A reader who sums
every duration on the page gets a larger number, and gets it from records that
say `Summer Internship` and `End-of-studies Internship` in amber. The two
figures answer different questions and neither is doing the other's job.

`tenure_sort_key` sorts newest-first on `start`, not on `end`. Sorting on the
end date would need a sentinel that outranks every real date just to keep the
current role (the one record with no end date) at the top.

Education stores plain integer years and sorts the same way.

---

## 5. The company summary

Every job record carries a `summary`, and it is **two sentences with two
different jobs**. The bullets below it report what the work achieved; the
summary answers the question no bullet can: *what is this place, and what did I
own inside it?*

**It sits beneath the tag list, not above it**, which is the order every record
on the site uses ([`DESIGN.md`](DESIGN.md) §9). Experience used to be the
exception, printing sixty words between the dateline and the chips. That put
the page's densest paragraph in front of its fastest layer, on the page a
recruiter opens first and reads for seconds, and it meant Experience and
Education disagreed about record anatomy two blocks apart.

### Sentence one: the company, and the size of its data

It starts with the company's own name, never with a bare noun phrase:
*"JACQUEMUS is a French luxury fashion house..."*, not *"Paris-based
luxury-fashion retailer."* A reader who has not heard of an employer cannot
weigh anything below it, and three of the four employers on this page are
unknown outside their market (§4 of [`CLAUDE.md`](CLAUDE.md): the scale is
stated, never left to be guessed).

It answers four questions, in this order and only where the fact is real:

| | Says | Example |
|---|---|---|
| **What it is** | The market, in the words that market uses | *a French luxury fashion house* |
| **What it sells** | The products or services, concretely | *ready-to-wear, leather goods, and accessories* |
| **Where it stands** | Its position or reach in that market | *mostly for luxury retail clients* |
| **How big the data is** | The volume, traffic or throughput the business generates | *order flows peaking at around 5,000 per hour* |

**The fourth is the one this page was missing, and it is the one the engineer
reads for.** A reader weighing a data engineer wants the size of the problem,
not the age of the company. Between *"founded in 2009"* and *"around 5,000
orders per hour at peak"*, only the second changes how the bullets underneath
are read.

**A fact that answers none of the four comes out, however true it is.** Three
that were cut from this page:

| Cut | Why |
|---|---|
| *founded in 2009 and based in Paris* | A founding year weighs nothing, and the country is already in *French* |
| *delivery hubs in Tunis, Sfax, and Dubai, a Salesforce ecosystem partner, a Qlik and Talend integration partner, and a Datadog advanced partner* | A partner-badge list is the consultancy's own marketing, and it says nothing about the work |
| *founded in 1997 and organised around four research axes in vision, signal, text, and social-media data science* | Answers none of the four, and pushes the sentence that says what the work was off the reader's first screen |

**Scale is stated only where it can be checked, and never as a figure that
will drift.** A throughput the author measured, a channel mix, a client
segment: stable, and answerable if asked. A headcount, a revenue figure or a
valuation is a snapshot from a data broker, and the dating rule in
[`writing.md`](writing.md) applies to it: it does not go on the page without
the author, and it does not go on the page without moving in the same change
as its *as of* date. Where no such fact is to hand, the sentence carries the
qualitative shape of the business and stops. Rule 5 of
[`awards.md`](awards.md), applied to an employer.

### Sentence two: what the data was, not who received it

In the first person and in the tense the dates imply: *I work* on the current
role, *I worked* on every past one. It names, where each is real:

- the team or the account,
- the **internal data domains** owned (orders, customers, products),
- the **external systems** integrated (exchange rates, emailing, shipping,
  refunds),
- the **architecture** the data lands in (a medallion lakehouse).

It does not name the achievement: that is what the bullets are for. And it
does not list the teams that consume the output. An earlier version read
*"preparing order, inventory, product, pricing, and exchange-rate data for the
analytics, logistics, e-commerce reporting, and inventory-management teams"*,
which tells the reader who was served and nothing about what was engineered:
it reads as a support function handing files to departments, where the same
work described as owned domains, integrated systems and a modelled
architecture reads as a platform. The consumer teams are not lost, they move to
the impact line of the bullet they actually explain (§6), which is where a
consequence belongs.

---

## 6. Editorial rules for the bullets

The tags carry metadata; the bullets carry substance. On this page substance
means **what changed because the work happened**.

1. **State the outcome and its measure.** "saving €1,400 per month", "a 100×
   speedup": a figure a reader can weigh. A bullet that ends at "designed and
   implemented" describes having been employed.
2. **Never restate a tag.** *Talend*, *Azure*, *Datadog* and *Salesforce* are
   in `stack` one row up. A bullet names a tool only where it says what the
   tool was made to do.
3. **Name the systems by name.** *ORLI*, *Diduenjoy*, *Salesforce Service
   Cloud*. An integration is defined by its two ends, and "multiple enterprise
   systems" is the phrasing that hides them.
4. **`groups` when a role did several separable things; `points` when it did
   one.** Nothing forces a four-month role into three headed groups of one
   bullet each. `render_group` emits the same `.entry__group` component the
   Teaching syllabus uses.

   The OEM engineer role is the declared exception: two groups of **one**
   bullet each, *Real-Time Classification* and *Model R&D*. It earns them
   because the division is itself the claim. One model runs inline at
   production speed and one was built, measured at 94.7% and deliberately kept
   out of production for being too slow; run together under a single heading,
   the second reads as something that shipped. A heading that separates what
   was deployed from what was investigated is worth a group with one bullet in
   it. A heading that only labels a bullet is not.
5. **A group title names a discipline, not a project.** *Data Integration*,
   *Cloud & Security Operations*, *Observability*: three of them, and a reader
   scanning for whether this person has run anything in production finds the
   third without reading the first two.

### The impact line, and which bullets earn one

A bullet says what was built. `.point__impact` says what changed because it
shipped, on its own line beneath, labelled `Impact:`. The component and its
treatment are [`DESIGN.md`](DESIGN.md) §9.2; **which bullets get one is this
document's rule**, and it is the half that is easy to get wrong.

The CV model this split is borrowed from puts a business-impact line under
every bullet. That is the wrong half to copy, for two reasons. Fifteen
identical lines teach the reader to skip the shape, and filling fifteen of them
forces the writer into consequences nobody owns: *protected brand credibility*,
*reduced engineer burnout risk*. Those are inferences about a company dressed
as achievements of a person, and they are exactly what the third reader is
checking for.

**A bullet earns an impact line when the consequence is owned, specific and
answerable in an interview.** Three tests, all of which have to pass:

| Test | Fails when |
|---|---|
| **Owned** | The outcome belongs to the company, not to the work. A conversion rate is not a data engineer's number. |
| **Specific** | It names who is affected, or what stops happening. *Improved trust* names neither. |
| **Answerable** | The author can be asked *how do you know* and have an answer. Not necessarily a public link: a cost report, a ticket, a named consumer team. |

A bullet that fails any of them renders the technical line alone, and the gap
is the point: it is the same argument as showing an unmerged pull request.
Two worked cases from this page:

- **REGIM Lab carries no impact lines at all.** It was a research prototype on
  a public dataset. There is no business outcome to claim, and inventing a
  plausible one there would put the least defensible sentence on the page next
  to the one record that openly says it was not a deployment.
- **The OEM XGBoost bullet carries none either.** The model reached 94.7% and
  was kept out of production because it was too slow. The judgement is the
  achievement, and it is already in the sentence; an impact line under it
  could only restate it.

Two further constraints:

**One consequence, once.** Where two bullets share an outcome, the impact line
goes on the bullet that states the outcome, not on the one that enabled it.
The 100&times; preprocessing speedup made the ~2,000 fps inline path possible,
so the impact line sits on the frames-per-second bullet and the speedup bullet
runs bare. Otherwise the reader meets the same consequence twice and discounts
both.

**It is a consequence, not a restatement.** *Held through peak sales events*
under a bullet that already says *peaking at approximately 5,000 orders per
hour* adds a line and no information. That bullet is one of the ones that stays
bare.

---

## 7. The page above the records

**One block sits before Experience**, and it holds the only things a run of
dated records cannot say for themselves. Everything else that used to sit here
has been deleted, and what was deleted is the more useful half of this section.

### Summary: the layer the records cannot supply

**Career has no `page-lede`.** It used to, and it is the only page of eight
that ever did. The `Summary` block below it said the same thing at greater
length, which meant two blocks were competing to introduce one career: the
lede spent 28 words on *sensor work first, luxury retail now*, and the first
paragraph of the block then spent 66 words on *sensor work first, luxury
retail now*. That is the surface Home's opening was merged to remove
(`home-opening-options.md`), reproduced one page across, and rewording either
half would have left it standing. The page now opens on `h1` and the block,
like every other page on the site.

The block is **one paragraph of prose and nothing else**: no capability list,
no figures, no tags. Three sentences, in this order, and the order is the
argument:

| Sentence | Says | Why no record can |
|---|---|---|
| **The claim** | Data Engineer, three years in, who builds pipelines and runs them | The `h1` on this page is *Career*, not a role. Nothing else above the records names the job being wanted ([`CLAUDE.md`](CLAUDE.md) §3). |
| **The thread** | Sensor data taught it, luxury retail runs it | It is a statement about four records at once. Each record can only speak for itself. |
| **The doctrine** | Error handling, alerting, recovery and written architecture are the deliverable | It is a claim about how the author works, not about a job that was held. |

The doctrine sentence moved here from Home's `Profile`, where it was the best
prose on the site sitting on the wrong page: it is about how a person behaves
inside a job, and this is the page about jobs. Home's opening is now the one
paragraph Home alone can say, and neither page repeats the other.

**It names no company.** An earlier version opened on JACQUEMUS, OLIVESOFT,
Kenzo Paris and LVMH, every one of which is named again within one screen, in
the `summary` field of the record that owns it (§5). A summary that previews
the next four hundred pixels is not a summary, it is a table of contents, and
it delays the sentences only this block can carry.

**It carries no figures**, for the reason the `.specs` strip was deleted
below: a number belongs on the record that earned it. The three quantified
lines a conventional CV summary ends on are already on this page as
`.point__impact` lines, and on Home as *Impact in Numbers*, which quotes those
same bullets by id rather than restating them.

**The block carries no capability rows.** It used to carry three `.deflist`
rows headed *Cloud & FinOps*, *Enterprise API & Data Engineering* and
*Monitoring & Observability*, each followed by a list of tools. That was
Home's Skills & Evidence with the evidence removed: the same shape (capability
heading, then tools), three rows against ten, and not one citation.
[`skills.md`](skills.md) built a whole component so that a capability claim
can never appear without the record that proves it, and this block quietly
reintroduced the thing that component exists to prevent, one page away.

An earlier version of this document defended the rows on the grounds that they
were *not a second Skills block* but answered the narrower question *what does
the career below consist of*. The markup did not support the defence. Two
further defects settled it: the third row filed *C++ low-latency signal
filtering* under **Monitoring & Observability**, a category error caused by
OEM having nowhere else to sit, and every tool named in the rows restated a
`stack` tag a few hundred pixels below, which §6 rule 2 forbids by name.

**A capability claim belongs on Home, cited. A tool belongs in a `stack` tag.
Neither belongs in a summary.**

### Verified impact was deleted, and the tags are why

A `.specs` strip used to sit between Summary and Experience, rendering every
`impact.json` record whose `source` was this page: four columns, each a figure
with a label and a sentence of evidence.

It was defensible when it was written. A recruiter reading for seconds may
never scroll into the bullets, and the strip lifted four numbers to the top of
the page where they would be seen. Adding `scale` to the experience model (§1)
took that argument away, because a `scale` tag does the same job better: it
sits **on the record that earned the figure** instead of four hundred pixels
above it, and it cannot be read as belonging to some other job.

What was left was repetition. Every figure in the strip was already in a
bullet, two of the four were now also `scale` tags, and two of the four were
also on Home:

| Figure | Strip | `scale` tag | Bullet | Home |
|---|---|---|---|---|
| 150+ pipelines | yes | yes | yes | |
| ~2,000 fps | yes | yes | yes | |
| &euro;1,400 per month | yes | | yes | yes |
| 100&times; | yes | | yes | yes |

The 150 printed three times on one page. That is the failure `render_impact`
was written to prevent, arrived at from the other direction: not two pages
disagreeing, but one page agreeing with itself three times and teaching the
reader that the numbers are decoration.

**Home's Impact in Numbers stays, and the asymmetry is the point.** Home's block
spans three pages (Career, Projects, Awards), so it is a site-wide selection
and no single page can render it. Career's could only ever be a subset of the
page it sat on, which is a table of contents for the screen below it. A block
that summarises what is already visible is not a summary.

`render_impact_spec` and the `build.career_impact` placeholder are gone with
it. `.specs` itself stays: Teaching is still its user ([`DESIGN.md`](DESIGN.md)
§10.1).

**Two `impact.json` records went with the strip**, *Pipeline ownership* and
*Inline classification*, which were the two that carried no `home` flag and so
had nowhere left to render. Both figures survive where they are load-bearing:
as the `scale` tag and the bullet on the record that earned each one. Every
record in `impact.json` now renders, which is the state a data file should be
in.

---

---

## 8. Volunteering, and the model it deliberately does not have

The block sits last on the page, after the three credential blocks, so
Education, Certifications and Online Courses stay one unbroken run. It came
from Home, where it closed the front page: [`home.md`](home.md) has that
argument.

### Why it carries no tags

Every other dated record on this page answers a metadata model. This one
answers none, and the reason is register rather than convenience. A chip row
reading *Crisis response &middot; Regional &middot; 4 months* over aid
distribution during a pandemic reads as credential-farming, and that is the one
tone this block cannot survive: its whole value is that it is the least
self-interested thing on the site.

**The condition for reopening this was a second record**, not a change of
mind, because a model exists to make records comparable and one record compares
to nothing. **The second and third records arrived, the question was asked, and
the answer held.** Two editions of a student orientation event next to a
pandemic relief effort do not need a chip to tell them apart: the organisation,
the initiative and the bullets already do it, and the chip would only add the
one tone this block cannot afford.

What the pair did reveal was a **missing field**, which is the more useful kind
of finding. Both records happened under a named programme, *COVID-19 response*
and *Orientini*, and there was nowhere to put it. The Red Crescent record had
been keeping its programme name in `period`, which is exactly why that field
held a topic where every other record on the page holds a date.

`initiative` renders on the dateline, joined to the year with a middot, which
is the shape `render_experience` already uses for `Location &middot; Period`.
It therefore needs no component, no class and no rule in `main.css`. It is
**not** the education model's `programme`: that means an institution with a bar
to clear (§2), and `build.py`'s own rule is that two models share a category
name only when they mean the same thing by it.

### What it does carry, and why each of those is not optional

It was, until this was written, the only `.entry` on the site with no id, no
tag and no link: zero of all three, where Certifications and Online Courses
carry ten links each and Experience carries forty-one tags. Tags are a
decision, see above. The other two were not.

**The id was the expensive one.** Without it the record was absent from the
page context rail (the section heading appeared, with nothing under it), it
could not be cited by [`impact.json`](src/data/impact.json) or
[`skills.json`](src/data/skills.json), and it could not be translated, because
the overlay in `src/i18n/` addresses records by id. It was the one record on
the site that could never be synchronised between the two languages, which is
the rule `CLAUDE.md` §10 now makes non-negotiable. It is `vol-<organisation>`,
stamped by `with_ids` like every other record.

**`url` is optional and absent.** The organisation should be linked, the way
every employer and school on this page is. It is not, because nobody has
supplied a link that was checked, and a plausible-looking address for a Red
Crescent branch is exactly the kind of thing this site must not invent.
`DESIGN.md` Principle 3 and [`awards.md`](awards.md) rule 5.

**One record per edition.** The JID work ran in 2022 and 2023 and is two
records, not one spanning both, which is how Awards already holds TCPC 22 and
TCPC 23, Hello World v2.0 through v4.0, and IEEEXtreme 16.0 and 17.0. A single
record covering two editions does not sort, and it says less about either than
two records do. Because `organisation` is then not unique, the id rule for this
block is the pair `("organisation", "year")`: `ID_RULES` in `build.py` accepts a
tuple for exactly this case.

**Dates, where they exist.** `year` for a single-edition record, `start` and
`end` for a sustained one, and `render_volunteering` derives the range and the
duration from the latter the way §4 requires. **A record with neither renders
no dateline at all** rather than an empty one, which is [`awards.md`](awards.md)
rule 5. The Red Crescent record is in that state: nobody has supplied the
months, so it is **honestly undated rather than dishonestly dated**. Sorting
follows `publication_sort_key`'s rule, newest first and undated last, and
nothing is invented to make a record sortable.

### What it says

Bullets, like the job records, not a paragraph. The prose previously opened
*"Volunteered during the COVID-19 crisis"* underneath a heading reading
*Volunteering* and a period reading *COVID-19 response*, which is the same fact
three times before the first new word. The four clauses that followed are now
two bullets and say the same things.

**It carries no number, and that is the honest state.** Weeks active, shifts
worked, households supplied: any one of them would change this block, and none
of them is known. §6's rules for bullets apply here as everywhere, including
the one that matters most: a figure nobody measured does not get estimated to
make a record look better.

## 9. Adding a record

**A job.** Append to `src/data/experience.json` with `company`, `url`, `role`,
`start`, `domain`, `engagement`, `mode`, `scale`, `stack`, and either `groups`
or `points`. `engagement`, `mode` and `scale` are facts about a contract, an
arrangement and a size: take all three from the author and never infer one from
a job title, a location line or a date range. A point is either
a string, or `{"point": "...", "impact": "..."}` where the consequence passes
the three tests above. Omit `end` only if
it is the current role. Use a `domain`, an `engagement` and a `mode` from the
vocabulary table above, or add the new value to that table in the same change.

**A qualification.** Append to `src/data/education.json` with `degree`,
`institution`, `url`, `location`, `start` and `end`. Then add `programme`,
`focus` and `accreditation` **only where the answer is not already in the
`degree` title**: a record that renders one tag because the other two would
repeat its own title is the model working, not a gap to fill. Write `institution` out in
full: a reader outside Tunisia cannot expand an abbreviation, and a school
nobody can name is a credential nobody can weigh. Add `accreditation` only if
the programme actually holds one and the accrediting body has a page to point
at.

**A credential.** Append to the right group in `src/data/certifications.json`
or `src/data/courses.json`, or add a new group with its `icon` filename: the
SVG goes in `images/icons/`. The link is the issuer's record of the credential;
see the rule above.

**An impact figure.** Append to `src/data/impact.json` with `title`, `figure`,
`label`, `evidence` and a `source` page that actually evidences it. **`"home":
true` is not optional any more**: Home is the only page that renders this file,
so a record without the flag renders nowhere and is dead data. Before adding
one at all, check that the figure is not already carried by a `scale` tag or a
bullet on its own record, which is where a figure belongs first.

Then `python3 tools/build.py` and `python3 tools/check.py`. Never edit the root
`career.html`; it is build output.
