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
Order:  domain → stack

  domain  what the data was about        "E-commerce & Retail"
  stack   what the work was built with   "Talend · Azure · Datadog · Salesforce"
```

The order is defined once, in `MODELS["experience"]` in `tools/build.py`.

### Why two categories and not five

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

What replaced them is two categories, because two is what the records honestly
support:

**`domain` first, and blue.** It is the substance of the record: the slot
`type` takes on an award and `kind` takes on a project. It answers the question
a job title does not: *what was the data about.* Two of the three roles here
are titled *Data Integration Engineer*, and one moved e-commerce orders while
the other moved service-desk tickets. That difference is the single most useful
fact on the record and it was previously invisible.

**`stack` last, and quiet.** Reused from [`projects.md`](projects.md), same
name, same meaning, same rule, capped at four names and rendered as one tag
joined by `·`. [`awards.md`](awards.md) rule 3: when a page needs a category
another model already defines, it takes that category rather than coining a
synonym.

**No `engagement` category**, tempting as it is. Whether a role was permanent,
a contract or an internship is genuinely useful and genuinely *not recorded*:
neither the CV nor the LinkedIn entries state it. Rule 5: an entry with nothing
to say in a category renders one tag fewer, and a plausible-looking placeholder
is worse than a visible gap. Add the category the day the fact is known for all
three records, not before.

### Vocabulary

| Category | Shape and permitted values |
|---|---|
| `domain` | `E-commerce &amp; Retail` · `Customer Service` · `Industrial Instrumentation` |
| `stack` | A list of at most four tool names, rendered as one tag |

`domain` names the business the data belonged to, not the discipline the
engineer practised. *Data Engineering* is the discipline and is the job title;
*Industrial Instrumentation* is where infrared sensor readings come from. Each
value is derived from what the record's own bullets describe, and a role whose
domain cannot be read off its bullets should get the fact added to a bullet
rather than a tag invented for it.

`stack` names tools, not techniques. The OEM role reads `C++` alone: a
Savitzky-Golay filter and a Random Forest classifier are things that were
*built*, and they are named in the bullets that describe building them. A
one-name stack is the honest rendering of a role that used one language.

---

## 2. The education model

```
Model:  education
Order:  accreditation

  accreditation  who vouches for the programme   "EUR-ACE® Accredited"
```

One category. This is [`awards.md`](awards.md) rule 3 taken at its word
(*categories are chosen for the reader, not for symmetry*) and it is worth
stating plainly, because the pull towards padding it is real.

Everything else an education record carries is already on the record and would
be a restatement if tagged. The degree is the title. The institution trails it
in `entry__role`. The years are the period line. A `field` category would say
*Computer Science* underneath a title reading *Computer Science Engineer's
Degree*, and a `level` category would say *Engineer's Degree* underneath the
same. [`awards.md`](awards.md) rule 1: a fact that does not belong to a declared
category belongs in the record, and a fact already in the record does not get a
category invented for it.

That leaves exactly one thing a reader cannot get from the title: whether the
programme is accredited, and by whom. So the model is one category, and the
second record renders zero tags because ISSAT Mahdia's bachelor carries no
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

`accreditation` now joins `scale`, `host`, `publisher`, `platform` and `stack`
in the regular-weight grey family, because it answers the identical question
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

### The external marker is derived, not declared

Whether a credential link leaves the site is computed from the URL, in
`render_credentials`:

| Link | Renders as |
|---|---|
| `https://www.credly.com/badges/…` | `.link-external`: the issuer's own record, checkable at the source |
| `data/DP-300.png` | a plain link: a copy of the certificate, served from this site |

Nothing in the data says which; the scheme says it. This keeps the external
marker meaning one thing on this page (*the issuer, not me, is showing you
this*) and it is why the two Microsoft entries look different from the rest.
They are scans this site hosts, and the page should not dress a file it serves
itself as third-party verification.

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

`tenure_sort_key` sorts newest-first on `start`, not on `end`. Sorting on the
end date would need a sentinel that outranks every real date just to keep the
current role (the one record with no end date) at the top.

Education stores plain integer years and sorts the same way.

---

## 5. Editorial rules for the bullets

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
5. **A group title names a discipline, not a project.** *Data Integration*,
   *Cloud & Security Operations*, *Observability*: three of them, and a reader
   scanning for whether this person has run anything in production finds the
   third without reading the first two.

---

## 6. Adding a record

**A job.** Append to `src/data/experience.json` with `company`, `url`, `role`,
`start`, `domain`, `stack`, and either `groups` or `points`. Omit `end` only if
it is the current role. Use a `domain` from the vocabulary table above, or add
the new value to that table in the same change.

**A qualification.** Append to `src/data/education.json` with `degree`,
`institution`, `institution_full`, `url`, `start` and `end`. Add
`accreditation` only if the programme actually holds one and the accrediting
body has a page to point at.

**A credential.** Append to the right group in `src/data/certifications.json`
or `src/data/courses.json`, or add a new group with its `icon` filename: the
SVG goes in `images/icons/`. The link is the issuer's record of the credential;
see the rule above.

Then `python3 tools/build.py` and `python3 tools/check.py`. Never edit the root
`career.html`; it is build output.
