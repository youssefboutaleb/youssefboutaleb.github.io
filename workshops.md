# Workshops: metadata model

The declaration for the Workshops page: which categories a workshop record
states about itself, in what order, and what a value in each looks like.

It applies the general rules in [`awards.md`](awards.md) and binds to the
treatments in [`DESIGN.md`](DESIGN.md) §7.1. Neither of those is restated here.

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
  sentence carries it (*Teaching how data moves through hardware...*), which is
  as much as a fact true of every record on a personal portfolio needs.

  **That sentence is a `.page-lede` now, not a `block__intro`**, and this
  paragraph quoted a wording it had already stopped using. Workshops has one
  block, so its pitch was always the page's pitch sitting one heading too low;
  it moved into the page header and the block opens straight onto its records.
  [`DESIGN.md`](DESIGN.md) §11.1 owns the rule that separates the two ranks.
- **Subject.** *Assembly*, *Python*, *Competitive Programming* are already in
  the entry titles. A tag repeating the title is noise; per
  [`awards.md`](awards.md) rule 1, technical depth is substance and belongs in
  the bullets.

---

## Outside the model

Two things a workshop carries that are not dimensions of it, and so are not
sequenced among the tags:

- **A repository link** renders as an `.icon-link` inside `.entry__title`,
  because it points at the thing the title names.
- **A slide deck** renders as a `.tag--critical` utility tag appended *after*
  the model's four. It is an artefact, not a property of the session; appending
  it keeps the four metadata positions readable positionally.

Both come from the data (`repo`, `slides`), never from hand-written markup.

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
   renderer sequences them. Omit a category you have no real value for.
2. Use a value from the vocabulary table above, or add the new value to that
   table in the same change.
3. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `workshops.html`; it is build output.

Adding a *category* is a larger change: declare it here, add it to
`MODELS["workshops"]` in `tools/build.py`, give it one `.tag--<category>` rule
in `main.css`, and add its row to `DESIGN.md` §7.1. It must not share a
treatment with the other four.
