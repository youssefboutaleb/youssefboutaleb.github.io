# Teaching — metadata model

The declaration for the Teaching page: which categories a taught-course record
states about itself, in what order, and what a value in each looks like.

It applies the general rules in [`awards.md`](awards.md) and binds to the
treatments in [`DESIGN.md`](DESIGN.md) §7.1. Neither of those is restated here.
[`workshops.md`](workshops.md) is the sibling model for one-off sessions; this
one covers courses that run for a semester.

---

## The model

```
Model:  teaching
Order:  level → workload → scale

  level      which cohort it was taught to   "Master's Year 1", "Master's Year 2"
  workload   how much teaching it was        "32 h · 20 lecture + 8 lab + 4 project"
  scale      how large the group was         "12 students", "16 students"
```

The order is defined once, in `MODELS["teaching"]` in `tools/build.py`.

### One category is borrowed, not invented

`scale` already exists on Awards, where it means the size of the field a result
was won against — `86 teams`. Here it means the size of the cohort a course was
taught to — `12 students`. Same question, same grey, same rule.

This is [`awards.md`](awards.md) rule 3 working in the direction it was meant
to: pages share a category name only when they genuinely mean the same thing by
it, and define their own when they do not. Only `level` and `workload` are new.

### Why this order

**`level` first.** It is the altitude of the record and the reason the page
exists: teaching a Master's Year 2 cohort is a different claim from tutoring
undergraduates, and everything after it is read in that light.

**`workload` second.** It is the substance of the appointment — how much
teaching this actually was, broken into the three things it consisted of. It
sits directly under `level` because together they answer *what was taught, and
how much of it*.

**`scale` last, and quiet.** A cohort size is context for the record rather
than a claim of its own, which is why it takes the regular-weight grey and the
terminal position — exactly as on Awards.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `level` | Integer `1` or `2`; the renderer produces `Master's Year 1` / `Master's Year 2` |
| `workload` | `{"lecture": 20, "lab": 8, "project": 4}` — hours per component, in teaching order. The renderer sums them and produces `32 h · 20 lecture + 8 lab + 4 project` |
| `scale` | `{"count": 12, "unit": "students"}` → `12 students` |
| `term` | `Fall` or `Spring` (not a tag — see below) |

**Every one of these is stored raw and labelled by the renderer**, per
[`awards.md`](awards.md) rule 7. The `workload` total is the clearest case: a
hand-written `32 h` sitting beside a breakdown that adds to 30 is a
contradiction nobody notices, so the total is summed from the parts and can
never disagree with them.

---

## When is not a tag

A course carries two facts about time — the semester and the academic year —
and neither is a category. Both live in `.entry__period`, the italic line that
already answers *when* on every record on the site:

```
Data Engineering 2
Fall 2025 – 2026
```

The period string is derived from `term` and `year` (an integer), so
`{"term": "Fall", "year": 2025}` renders `Fall 2025 – 2026`. A `term` tag would
have bought a category and a colour to say something the line beneath the title
was already there to say.

### Newest first, and why a sort was needed

Records render most recent first, like every other page. Here that could not be
left to the order of the JSON file, because **Fall precedes Spring inside one
academic year**: Fall 2024 – 2025 is *older* than Spring 2024 – 2025, even
though they share a label. Sorting on the year alone gets it wrong.

`course_sort_key` in `tools/build.py` sorts on `(year, TERM_ORDER[term])`
descending, which makes the invariant structural rather than something the next
person has to remember when appending a record.

---

## Technologies are not tags

An earlier draft gave the model a `stack` category — a list of tool names
rendering one tag each, capped at four with the remainder in a `Full stack`
line. It was removed, and the rule it broke is worth keeping:

> **A category holds one value.** A run of tags whose length changes from
> record to record destroys the positional reading that the fixed order exists
> to provide. Two records with a different number of tags in the same category
> can no longer be compared down the column.

Tools are now named **inside the syllabus module that teaches them** —
*"Monitoring, dashboards and alerting in Datadog"* rather than a `Datadog` chip.
This is better on both counts the tags were meant to serve:

- **Context.** `Airflow` in a list says the course mentioned Airflow.
  "Orchestration, scheduling and backfills with Apache Airflow" says what was
  taught with it.
- **Searchability is unchanged.** The name is still on the page in full, still
  in the page description, and still greppable.

---

## The syllabus

The body of a course record is its module outline, built from `.entry__group`
and `.entry__group-title` — the component the Career page already uses to
subdivide a long record. No new component was needed.

```
Module 4 — Logging & Monitoring
  – Structured logging and error tracking with Loguru.
  – Monitoring, dashboards and alerting in Datadog.
```

**Module numbers are produced by the renderer, never written into the data.**
Same reasoning as `placement` and `level`: a hand-numbered list is how a
reordered syllabus ends up with two Module 3s.

### Editorial rules for a module

1. **A module is a topic, not a session.** Five modules over twenty lecture
   hours; do not split a syllabus into twenty one-hour rows.
2. **Name the concept, not the syllabus heading.** "Data warehousing concepts"
   is a table of contents. "Why analytical storage is shaped differently from
   the transactional systems it draws from" is what a student left with.
3. **Name a tool where the tool is the point.** Datadog earns its mention in
   the monitoring module. Python does not need one in every module it appears
   in.
4. **Distinguish courses that share a name.** Data Engineering 1 and 2 are a
   sequence, and the modules have to make the progression visible — building a
   pipeline, then operating one that fails safely.
5. **Claim the level, not the label.** Say what made it graduate-level —
   gradient descent as a mechanism rather than a library call, failure treated
   as the normal case — instead of asserting rigour.
6. **`entry__summary` frames, the modules enumerate.** One sentence on what the
   course was for, then the outline.
7. **One lab per module, and say what was built.** The workload claims eight
   lab hours across five modules; a module with no lab point makes that claim
   unverifiable from the page. The lab point is prefixed `<b>Lab:</b>` and
   states the artefact and the problem it forced &mdash; *"made to fail mid-run
   and repaired with a dated backfill"*, not *"practical exercise on Airflow"*.
   It is the one place the register turns concrete: the other points name the
   concept, the lab names the thing that was handed in.

### The capstone is not a sixth module

The four project hours render as their own `.entry__group`, titled `Final
Project &mdash; <name>` rather than `Module 6`:

```
Module 5 — Packaging & Delivery
  – …
Final Project — Fault-Tolerant Ingestion Pipeline
  – …
```

It is stored under a sibling `capstone` key, not appended to `syllabus`:

```json
"capstone": {
  "title": "Fault-Tolerant Ingestion Pipeline",
  "points": ["…", "…", "…"]
}
```

The reason is the same one that keeps module numbers out of the data. The block
intro states *5 modules (4 hours each)* plus a separate project session; a
`Module 6` in the outline would contradict the hours it is counted in, and the
contradiction would be invisible to anyone editing the JSON. The renderer knows
which group is which, so it cannot drift.

Three points is the working shape: **what was built**, **what else was graded
besides the data flow**, and **what was submitted and defended**.

---

## What is deliberately not in the model

The appointment is one job with three courses under it, so anything constant
across all three is stated **once, in the block intro**, and never as a tag
repeated three times:

- **Institution and programme.** IHEC Sfax and [*M.Sc. Data Science*](https://ihecsf.rnu.tn/fr/article/765/master-professionnel-en-data-science-for-business-amp-economics) were on
  every entry of an earlier version of this page. Three identical tags
  discriminate nothing; the intro carries them, with the link.
- **Appointment and dates.** *University Lecturer (part-time), September 2024 –
  May 2026* is the frame around all three records, not a property of any one.
- **Mode.** All three were taught on-site. Unlike Workshops, where mode varies
  between records and therefore earns a category, here it is a constant of the
  appointment.
- **Language.** Taught in French with English materials — a genuine
  differentiator, but again constant, so it belongs to the appointment.
- **Format.** An earlier draft carried a `Lectures & Labs` tag. `workload`
  replaced it: *20 lecture + 8 lab + 4 project* states the same thing and
  proves it with hours.
- **Subject.** *Machine Learning*, *Data Engineering* are the entry titles. A
  tag repeating the title is noise.

The test is not "is this fact interesting?" but **"does it distinguish this
record from its neighbours?"** A fact that is true of every record on a page
belongs to the page, not to the records.

### What the block intro therefore carries

**This is the site's one exception to the single-line intro rule**
([`DESIGN.md`](DESIGN.md) §11.1), and it is an exception on the same argument
§9 of that document makes for tags: these are constants true of every course on
the page, and a reader scans them positionally rather than reading them.

Those constants are not prose scattered through a paragraph. The intro is a
`ul.points.block__intro` of four labelled items, so that a reader looking for
one of them finds it positionally, exactly as they read the tags on the records
below:

```
• Appointment:            who, where, when, on what programme, in what mode
• Course Structure & Workload (32 h per course):
    • Lectures (20 h):    5 modules, 4 hours each
    • Labs (8 h):         1 per module, 1.5–2 hours
    • Final Project (4 h): the capstone session
• Language & Tooling:     French and English delivery, English materials
• Assessment Scheme:      Exam 50% · Homework 20% · Project 15% · Attendance 15%
```

Three of these were already implied by the model and are stated here so they
are said once rather than three times. Two are genuinely new and exist only
here:

- **The workload breakdown is stated twice, deliberately, and at two
  altitudes.** The `workload` tag on each record proves the hours; the nested
  list in the intro says what those hours *were* — that the 20 lecture hours
  are five four-hour modules, and the 8 lab hours are one lab per module. That
  is what makes the syllabus below countable: five modules, five labs, one
  capstone. It is not a repeated fact, it is the key to reading the record.
- **The assessment scheme has no home in the model at all.** It is a property
  of the appointment, identical across all three courses, and there is no
  category it could take without appearing three times. It is also the fact a
  reader most often wants and least often finds on a teaching page.

**Why `ul.points` and not `.deflist`.** [`DESIGN.md`](DESIGN.md) §10 gives
`.deflist` as the component for `Label: values` content, and on the face of it
this intro is exactly that. It is not, because of the second item: *Course
Structure & Workload* carries a nested list of three sub-items, and a `<dd>`
holding another list is no longer the one-line label-and-values pairing
`.deflist` exists to render. The other three items follow the flat shape, so if
the workload breakdown ever moves elsewhere, this intro should become a
`.deflist`.

If a future course is assessed differently, that is the point at which the
scheme stops being a constant of the appointment — and it earns a category, or
a second `.block`, rather than a footnote on one record.

---

## Adding a course

1. Append a record to `src/data/teaching.json` — position in the file does not
   matter, `course_sort_key` orders it. Give it `term`, `year`, `level`,
   `workload`, `scale`, a `summary`, a `syllabus` and a `capstone`.
2. Use a value from the vocabulary table above, or add the new value to that
   table in the same change.
3. `python3 tools/build.py` then `python3 tools/check.py`. Never edit the root
   `teaching.html`; it is build output.

If the appointment changes — a new institution, a different programme — the
block intro in `src/pages/teaching.html` is what changes, and a second
appointment means a second `.block` with its own intro, not a new category.
