# Workshops: metadata model

The declaration for the Workshops page: which categories a workshop record
states about itself, in what order, and what a value in each looks like.

It applies the general rules in [`awards.md`](awards.md) and binds to the
treatments in [`DESIGN.md`](DESIGN.md) §7.1. Neither of those is restated here.

---

## The page: two blocks, and the climb between them

The page carried one section, headed *Workshops Delivered*, which restated the
`h1` three lines above it and told the reader nothing. It is two now:

| Block | Holds | Says |
|---|---|---|
| **Hardware & Execution** | CS Fundamentals (2026), Assembly (2023) | What the machine does with the code |
| **Algorithms & Language** | Competitive Programming (2023), Python (2022) | What the code should say in the first place |

**The order was already right and was invisible.** The page lede claims a
traversal of the stack, *from cache lines and instruction pipelines up to the
algorithms that keep them fed*, and reverse chronology happens to render
exactly that: hardware, assembly, algorithms, language. Nothing told the reader
the order meant anything, so four sessions read as four unrelated events. The
blocks name the two halves of the climb, and newest-first survives inside each
of them.

**It used to say *down to*, and the page it describes goes up.** This paragraph
called the order a descent for as long as the lede did, which is how a wrong
direction word survives: the model document quotes the page rather than
checking it. Hardware is the bottom of the stack and the algorithms sit on top
of it, so the reading order climbs, and the two `block__intro` lines were
already saying so (*from the first line of Python up*). Idiomatic *down to*, as
in *down to the last detail*, is defensible anywhere except on a page whose
whole subject is a stack with a real up and a real down.

**The split is a filter on `block`, and `block` never renders.** That is the
Projects convention rather than the Awards one, and the reason is recorded in
`MODELS` in `tools/build.py`: Awards filtered on `type`, which was also a tag,
so every record carried a chip repeating the heading three lines above it.
`block` is not a metadata category, has no `.tag--block` rule, and appears in
no vocabulary table here. A new value is a new section in the fragment, and a
subject that fits neither block is a question about the page, not a field.

**Each block gets one `block__intro`**, which is the pitch rank
[`DESIGN.md`](DESIGN.md) §11.1 owns, and the page keeps its `.page-lede` above
both. The two ranks now say different things: the lede states the climb, and
each intro pitches one half of it.

---

## The page header: who asked for these sessions, and how big they were

One thing stands above the first heading, and it is not written: three cards
derived from `src/data/workshops.json`, one per organisation that invited him.

**Why the page needed a summary.** Every record states its own attendance and
its own duration, in grey chips at positions five and three of six, and nothing
stated the page. A recruiter asking *how much of this is there, and who asked
for it* had to add four chips up and read four hosts off four records.

**The card is Awards' scope card, reused whole** ([`DESIGN.md`](DESIGN.md)
§9.4): the same grid, the same `.entry`, the same four lines in the same ranks.

| Line | Class | Holds |
|---|---|---|
| Label | `.result__scope` | the host |
| Figure | `.result__figure` | the head count across that host's sessions |
| Qualifier | `.result__scale` | how many sessions, and how many hours |
| Provenance | `.result__source` | the sessions themselves, as anchors |

```
OLIVESOFT              Securinets ENIS         IEEE Student Branch ENIS
30 participants        60 participants         52 participants
1 session &middot; 2 h            1 session &middot; 4 h            2 sessions &middot; 6 h
Introduction to CS     Assembly Programming    Introduction to Competitive
Fundamentals           Workshop                Programming
(Hardware)                                     Introduction to Python
```

**A host that ran more than one session lists them one to a line**, on
`.result__source--stacked`, and not joined with `&middot;`. The middot is the
peer separator for *short* peers ([`CLAUDE.md`](CLAUDE.md) §6), and two
forty-character workshop titles in a 271px track are not that: joined, the pair
wrapped mid-title. The line break separates them and no punctuation has to,
which is the call [`DESIGN.md`](DESIGN.md) §10.2 already makes for
`.hero-facts`. Awards' cards keep the middot, because `TCPC 23 &middot; TCPC 22`
is exactly the case it is for.

**Nothing in a card is written.** The head count sums `scale.count`, the hours
sum `duration`, the session count is the group size, the label is `host` and
the links are the records' own ids and titles. A card cannot say *60* while the
record below says something else, and `check.py` fails the build on a card
pointing at a record that is not there.

**Why the grouping is the host and not the total.** This was the choice, and
the argument against a row of totals is the one [`CLAUDE.md`](CLAUDE.md) §10
already made when it deleted the Domains block: **a card carries a citation or
it is a keyword.** `142 participants` cannot point at one record; *60
participants at Securinets ENIS* points at exactly one. The totals are still
there for anyone adding three cards up, and the grouping answers the question
the chips never did, which is that one of the three hosts is a company.

**Newest host first**, which is the order the records are already in. A summary
that re-sorted its source would be a second reading order to keep in agreement
with the first.

**Two guards, both of them the [`DESIGN.md`](DESIGN.md) §9.4 lesson applied.**
That is where a summary box summed every field size on the Awards page into one
number 96% carried by two bad placements:

1. **A record missing `scale.count`, `duration` or `host` stops the build**,
   because a sum that silently skips a record is invented precision, not the
   honest omission [`awards.md`](awards.md) rule 5 permits.
2. **So does a page stating two different `scale` units**, since one figure
   cannot carry both.

**A three-column `.specs` strip stood here for one revision**, stating the
page's constants (142 participants, 12 h, 4 sessions, 3 hosts) in Teaching's
component. It was replaced on the author's call, and the reason is the one
above: a spec row states a figure and cannot carry the link that makes it
checkable.

**A diagram stood beneath it too, and was deleted.** It drew the five layers
this page teaches as a downward stack, and the author's verdict was that it did
not earn 380px at the top of the page. [`diagrams.md`](diagrams.md) §8 keeps
the reasoning, because the shape will look tempting again.

---

## The model

```
Model:  workshops
Order:  format → mode → duration → audience → scale → host

  format     what kind of session it was      "Workshop", "Workshop Series",
                                              "Hands-on Lab"
  mode       how it was delivered             "On-site", "Online"
  duration   session duration                 "4h"
  audience   who was in the room              "Engineering Students",
                                              "Engineers & Executives"
  scale      how many attended                60 students, 30 participants
  host       who ran it                       "OLIVESOFT", "Securinets ENIS",
                                              "IEEE Student Branch ENIS"
```

The order is defined once, in `MODELS["workshops"]` in `tools/build.py`. No
record, page or template chooses its own.

### Why these six, in this order

The page answers, in one glance, the question a hiring manager actually has
about a teaching record: *what was it, how real was it, how long was it, who was it pitched at, how many were in the room, and who vouched for it.*

**`format` first**, because it sets the reader's expectation for everything
after it. A *Hands-on Lab* and a *Workshop* are not the same claim: one implies
participants wrote and ran code, the other that they were taught. Reading it
first means the bullets below are read in the right register.

**`mode` second**, because it is the strongest qualifier on `format`. Running a
hands-on lab in a room and running one over Teams are different jobs, and the
distinction is invisible from the title alone.

**`duration` third.** It establishes commitment and depth (e.g. `4h`).

**`audience` fourth.** It is the calibration: the same title in front of second-
year students and in front of a company's engineers is two different sessions.

**`scale` fifth.** It states the attendee count/capacity reached (`60 students`).

**`host` last**, and at regular weight, because it is attribution rather than
substance. It is what the reader checks *after* deciding the record is
interesting, which is exactly where the eye should land last.

### Vocabulary

One phrasing per concept, fixed here so it cannot drift between records:

| Category | Permitted values |
|---|---|
| `format` | `Workshop` · `Workshop Series` (more than one session) · `Hands-on Lab` (participants write and run code) · `Webinar` (remote, presentation-only, no exercises) |
| `mode` | `On-site` · `Online` · `Hybrid` |
| `duration` | Formatted string (e.g. `4h`) |
| `audience` | `Engineering Students` · `Professionals` · `Engineers & Executives` · `Mixed` |
| `scale` | Structure `{ "count": N, "unit": "students" }` (or `participants`, `engineers`) |
| `host` | The organisation's name, plus the institution when the organisation is a chapter of one: `Securinets ENIS`, not `Securinets Club` |

A value outside these tables is added to this table first. That is what stops
`Hands-on`, `Hands-On Lab` and `Practical Workshop` from ending up on one page.

`Webinar` and `Hybrid` are declared but currently unused: they exist so the
next record does not invent a synonym under time pressure.

### What is *not* in the model

- **Role.** Every record on this page was designed and delivered by the site's
  author, so an `Instructor` tag on all four discriminates nothing. The opening
  sentence carries it (*Teaching how data moves through a machine...*), which
  is as much as a fact true of every record on a personal portfolio needs.

  **That sentence is a `.page-lede`, not a `block__intro`**, and this
  paragraph quoted a wording it had already stopped using. It moved up because
  it speaks for every record on the page, which is what a lede does.
  [`DESIGN.md`](DESIGN.md) §11.1 owns the rule that separates the two ranks.

  The reasoning recorded here was *Workshops has one block, so its pitch was
  always the page's pitch sitting one heading too low*. The promotion was right
  and that argument for it is now spent: the page has two blocks, each with a
  pitch of its own, and the lede outranks both because the climb it states is
  true of all four records and of neither block alone.
- **Subject.** *Assembly*, *Python*, *Competitive Programming* are already in
  the entry titles. A tag repeating the title is noise; per
  [`awards.md`](awards.md) rule 1, technical depth is substance and belongs in
  the bullets.

---

## Outside the model

Three things a workshop carries that are not dimensions of it, and so are not
sequenced among the tags:

- **A repository link** renders as an `.icon-link` inside `.entry__title`,
  because it points at the thing the title names.
- **A slide deck** renders as a `.tag--artifact` utility tag appended *after*
  the model's six. It is an artefact, not a property of the session; appending
  it keeps the six metadata positions readable positionally. This paragraph
  said `.tag--critical` and *four* until the blocks pass corrected it: crimson
  was retired for the reason the comment above the rule in `main.css` gives,
  and the model has carried six categories since `duration` and `scale` joined
  it.
- **Parts.** A session delivered in more than one sitting replaces `points`
  with `groups`, the `[{"title", "points"}]` shape a job's disciplines and a
  course's syllabus modules already use, and `render_group` draws it.

The first two come from the data (`repo`, `slides`), never from hand-written
markup; the third is the data's own shape.

### Why parts are a component and not a bullet convention

The series had been numbering itself inside its own prose:

```
<b>Part 1.a: Efficient data &amp; code execution:</b> CPU instruction pipelining …
<b>Part 1.b: Parallel compute &amp; Python bindings:</b> SIMD, SIMT, and MIMD …
<b>Part 2: Circuit-level computation:</b> data storage and arithmetic …
```

One bullet, two bold spans, two colons, and `<b>` doing two jobs at once: on
this site it means *this is the bullet's topic* ([`CLAUDE.md`](CLAUDE.md) §6),
and here it was also carrying the structure. The record was flat while its own
text insisted it was not. Split into two groups, the title states the part and
the bullet keeps `<b>` for its topic:

```
Part 1: Efficient execution and parallel compute
  <b>Data &amp; code execution:</b> CPU instruction pipelining …
  <b>Parallel compute &amp; Python bindings:</b> SIMD, SIMT, and MIMD …
Part 2: Circuit-level computation
  Data storage and arithmetic built up from SR/D latches …
```

**Part 2 carries no bold lead, and that is the rule, not an omission.** Its
group title already names the topic, so a `<b>` beneath it would be the same
restatement the old bullets were. A group whose title and whose single bullet
would say the same thing states it once, in the title.

**Only a record with real parts gets them.** The other three sessions ran once
and stay flat. Groups are not a way to add rank to a thin record: a single
group titled *Part 1* with nothing after it is a record pretending to be a
series.

---

## Editorial rules for the bullets

The tags carry metadata; the bullets carry substance. On this page, substance
means **the technical depth the session actually reached**: the thing a
reader is trying to judge.

1. **Never restate a tag.** The host, the format and the audience are already
   on screen. A bullet reading "organised with the IEEE Student Branch at ENIS"
   is a third copy of one fact.
2. **Name the concepts, not the adjectives.** "Explored low-level programming"
   says nothing a title does not. "Chipsets, buses, and the path an instruction
   takes to reach the CPU" is checkable and shows the level.
3. **One opening per entry, and no shared formula.** Every record on the
   previous version of this page began "Conducted a workshop on…". Repetition
   at the head of consecutive entries makes them read as one block.
4. **Claim only what the materials support.** Where a repository or deck
   exists, the bullets describe what is in it. Where nothing was published, the
   bullets stay at the granularity that is actually known: a thin entry is
   better than an invented one.
5. **`entry__summary` frames, `points` enumerate.** The summary is one sentence
   on what the session was for; the bullets are what it covered. An entry that
   would repeat itself across the two uses only one.

---

## Adding a workshop

1. Append a record to `src/data/workshops.json`. Fields in any order: the
   renderer sequences them. Omit a category you have no real value for, with
   three exceptions: `scale`, `duration` and `host` are what the host cards
   total, so a record without them stops the build rather than quietly
   shrinking a figure in the page header. A new `host` is a fourth card, with
   no other change.
1. **Set `block`**, `hardware` or `algorithms`. `check_workshop_block` in
   `tools/build.py` fails the build without it, because the page filters its
   two sections on this field and a record that reached neither would leave
   the site with nothing downstream to notice: the ids stay valid and
   `check.py` finds no dead link, since nothing links to a record that is not
   there. It is a filter, not a tag: no vocabulary table above and no
   treatment in [`DESIGN.md`](DESIGN.md) §7.1, because it never reaches the
   reader.
2. Use a value from the vocabulary table above, or add the new value to that
   table in the same change.
3. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `workshops.html`; it is build output.

Adding a *category* is a larger change: declare it here, add it to
`MODELS["workshops"]` in `tools/build.py`, give it one `.tag--<category>` rule
in `main.css`, and add its row to `DESIGN.md` §7.1. It must not share a
treatment with the other four.
