# Home: the opening

What the first screen of the site says, and why it currently says it twice.

Scope: the `.hero-header` and the Profile block, in `src/pages/index.html`.
Everything below Profile (Currently, Skills & Evidence, Selected Impact,
Languages) closed in the previous pass and is not reopened here.

---

## Part 1: what is wrong

### 1.1 The `<h1>` uses a separator the site does not own

```html
<h1 class="page-title">Data Engineer | Cloud &amp; Integration</h1>
```

`CLAUDE.md` section 6 names one peer separator, `&middot;`, and gives the rule:
*two peers on one line* takes it. The pipe is a third separator, it appears
nowhere else in the repository, and it is in the largest text on the site.

### 1.2 The same line dilutes the claim it is supposed to make

`CLAUDE.md` section 3: Data Engineering is the role, cloud and integration is a
*qualifier*, and *"if a change makes the target role harder to name in one word,
the change is wrong."*

A pipe is the punctuation of *and also*. It sets the two sides up as peers, in
the one sentence a recruiter reads before deciding what shape of candidate this
is. Roadmap M5 (*refresh cloud & integration framing*) is this line.

### 1.3 The lede and the Profile paragraph restate each other

> **Lede.** I build and operate enterprise-scale data platforms on **Microsoft
> Azure**: ETL/ELT pipelines, API-led integrations between business-critical
> systems, and the observability that keeps them dependable in production.

> **Profile.** I have been building on **Microsoft Azure** since **2024**, and
> working in engineering roles since **2022**: end-to-end **ETL/ELT** pipelines
> with **Talend** and **MuleSoft**, and the **Datadog** instrumentation that
> says when one of them stops.

Azure, ETL/ELT, integration, observability: both. Same four nouns, same order,
about 45 words spent twice, inside the first screen.

`home.md` opens on the two occasions a fact on Home drifted from the record it
restated, and its rule is that Home may restate *only* by projection, citation
or quotation. These two sentences are hand-written on both sides. They are the
one restatement on the page that nothing generates and nothing checks.

### 1.4 Profile's intro describes the page, not the work

> *Data engineering is the job, and everything below it is the evidence.*

That is a reading instruction. `CLAUDE.md` section 6 puts mechanics in the model
documents and never on the page, and every other `block__intro` on the site
describes work:

> *Engineering background plus competitive programming edge.*
> *Rapid prototyping, product design, and fast technical delivery.*

### 1.5 The credentials list is a hand-typed summary of structured data

`site.json` carries four strings:

```
MuleSoft & Talend Certified
Datadog Certified in Fundamentals, APM & Log Management
Astronomer Certified in Apache Airflow 3
Microsoft Certified in Azure Databases, Fabric Engineering & Analytics
```

`src/data/certifications.json` carries ten records, each with an issuer and a
verification URL. The four strings are currently a correct summary of the ten
records. Nothing makes them stay one.

They are also the second time the same certifications appear on this page: the
`certification` chips in Skills & Evidence are generated and link to
`career.html#certifications`. One page, one set of facts, two renderings, one
generated and one typed.

The list has no label, either. Four certification names hang under a paragraph,
and the reader is left to infer what they are.

### 1.6 Availability is the smallest text in the hero

13px grey, under a 17px lede. Its placement says it matters in the first three
seconds (and it does: `CLAUDE.md` section 4 is explicit that a recruiter who has
to wonder filters silently). Its size says it is a footnote. One of the two is
wrong.

### 1.7 The portrait is an avatar rendered at 16% of its source

`images/me.jpg` is 800 x 800. It is displayed at 130px, circular, with
`--shadow-portrait`, which is the single declared exception to *no shadows* in
the whole design system.

130px round with a soft shadow is the visual grammar of a social profile. The
system's own grammar is hairlines and whitespace.

### 1.8 The page has two openings

| | Hero | Profile |
|---|---|---|
| Heading | `h1` role line | `h3` Profile |
| Pitch | the lede | the intro |
| Body | availability | the prose paragraph |
| Data | portrait | credentials |

Both are *who I am* blocks and they are stacked. A reader gets two
introductions, roughly 110 words, before the first piece of evidence
(*Currently*) appears. This is the finding the other seven hang off: 1.3 and 1.5
are duplication *because* there are two blocks competing to open the page.

---

## Part 2: the portrait, and what andrewng.org actually does

`.layout` already carries the comment *"single-column centered document layout
(Andrew Ng style)"*, so the column is borrowed. The photograph is not.

**What that site does:** the photograph sits *above* the text, at the full width
of the column, rectangular, no border radius, no shadow. It is a photograph in
a document. The name and bio follow beneath it.

**Why it cannot be copied exactly here:** the source is square. At the full
1060px column a square image is 1060px tall, which puts the `h1` and every word
of the pitch below the fold on a laptop. Cropping a square to a wide band
(`aspect-ratio: 5/2`) leaves a letterbox strip of a face. Andrew Ng is not
selling in three seconds; `CLAUDE.md` section 2 says this site is.

**What is worth taking:** the treatment, not the placement. Larger. Rectangular
or at least not a 130px badge. A hairline instead of a shadow, which is what the
rest of the system uses for structure and which would retire the system's only
elevation exception.

**The unused space.** The column is 1100px, and `.page-lede` is capped at 74ch,
about 630px. Portrait plus gap plus lede comes to roughly 800px, so about 260px
of the column is empty beside the hero. A larger photograph costs nothing.

---

## Part 3: options

### Structure

**A. Repair in place.** Keep the hero and Profile as two blocks. Fix the
separator, delete the duplicate sentence from one side, generate the credentials
from `certifications.json`, grow the portrait.

- Costs: least work, nothing else moves.
- Gains: closes 1.1 to 1.7.
- Weakens: leaves 1.8. The page still opens twice.

**B. One opening.** Delete the Profile block. The hero carries portrait, `h1`,
one pitch paragraph, availability, and a generated credentials strip. The page
becomes: Opening, Currently, Skills & Evidence, Selected Impact, Languages.

- Costs: the `#profile` anchor disappears (nothing on the site links to it,
  checked). One block fewer means the warm first-person voice has one paragraph
  rather than two to live in.
- Gains: closes all eight. First evidence arrives roughly 80 words earlier.
- Weakens: the hero has to carry more, so the one paragraph in it has to be
  good.

**C. B, plus the photograph above the text at column width.** The literal
andrewng.org form.

- Costs: needs a landscape source photo, or a crop that survives 5:2.
- Gains: the photograph reads as a photograph.
- Weakens: pushes the claim below the fold, against section 2.

### The `h1`

**H1. `Data Engineer` alone.** The qualifier moves into the pitch sentence.
Sharpest possible answer to *name the role in one word*.

**H2. `Data Engineer &middot; Cloud & Integration`.** Minimum change: fixes the
separator only. Still sets the two up as peers, so 1.2 survives.

**H3. `Data Engineer`, with a second line that subordinates the qualifier**,
for example *Cloud and integration, in service of the pipelines*. Names the role
in one word and states the relationship section 3 asks for, rather than leaving
a punctuation mark to imply it. Costs one new element.

### The portrait

**P1. Bigger circle.** 130px to 180px, keep the radius and the shadow.

**P2. Author photo.** About 180 x 220, `--radius-md`, a hairline border instead
of the shadow. Reads as a document photograph, uses the slack column width, and
retires the system's only shadow.

**P3. Column-width band.** `aspect-ratio: 5/2`, `object-fit: cover`. Needs a
different source image.

---

## Part 4: recommendation

**B, H1, P2.**

B because 1.3 and 1.5 are not really two bugs, they are one bug (two blocks
competing to introduce the same person) showing up twice, and repairing them
separately leaves the thing that generates them.

H1 because section 3 is unambiguous and the `h1` is where it is tested. Cloud
and integration does not vanish: it is the first clause of the pitch, where it
qualifies rather than competes, and it is the whole of Skills & Evidence rows 3
and 4 further down.

P2 because it takes what is worth taking from andrewng.org (a photograph, not a
badge) without paying what C costs (the claim below the fold), and because
replacing the shadow with a hairline removes the one exception the design system
currently has to apologise for.

---

## Part 5: what needs the author

These are claims and positioning, so section 10 says they are not mine to
decide.

1. **The pitch paragraph.** If the lede and the Profile prose merge, one
   sentence is written and one is retired. Which facts survive: the dates
   (2022, 2024), the tool names (Talend, MuleSoft, Datadog), or neither,
   because *Currently* and Skills & Evidence already carry both structurally?

2. **The warm paragraph.** Section 6 says Home sits on the warm/clinical line
   and that the hero and Profile are the warm half. If Profile goes, does the
   opening keep a first-person sentence about *why* this work, or does Home
   become clinical throughout and the warmth live only on Projects and
   Teaching?

3. **Credentials, generated from what?** Ten records grouped by issuer is a
   longer strip than four hand-written lines. Options: all ten, issuers only
   (six names), or a count per issuer.

4. **The photograph.** P2 crops 800 x 800 to roughly 4:5. Does the framing
   survive losing 20% of the width, or is a re-crop needed first?

---

## Part 6: what was decided and built

All four recommendations taken (B, H1, P2, generated credentials).

| | Before | After |
|---|---|---|
| Openings | Hero and Profile, stacked | One `.hero-header` |
| `h1` | `Data Engineer \| Cloud & Integration` | `Data Engineer` |
| Words before the first evidence | about 110 | about 40 |
| Credentials | 4 strings typed in `site.json` | generated from `certifications.json` |
| Portrait | 130px circle, `--shadow-portrait` | 180 x 220, `--radius-md`, hairline |
| Shadow tokens in the system | 1 | 0 |
| Availability | `--text-sm`, uncapped | `--text-md`, capped to the measure, paired with Certified |

**One correction to Part 3.** The strip renders **five** issuers, not six:
`certifications.json` holds ten certificates across Microsoft, Astronomer,
MuleSoft, Talend and Datadog.

**One documented decision reversed.** [`home.md`](home.md) previously defended
the pipe in the `h1` (*"the pipe is doing role, then qualifier, which is a
rank, where `&middot;` joins peers. Do not fix it to a middot"*). Choosing
`Data Engineer` alone overrules that entry rather than overlooking it, and
`home.md` now records both the old argument and why it lost.

### Still open, and author-led

1. **The retired Profile paragraph carried one fact that now appears nowhere
   on Home:** *working in engineering roles since 2022*. Azure since 2024 is
   still on the page, projected by *Currently* through the JACQUEMUS dateline.
   Total years of experience is not, and it is something the first reader wants
   in seconds. It could be derived from the earliest `start` in
   `experience.json` rather than typed.

2. **Home is now clinical throughout.** [`CLAUDE.md`](CLAUDE.md) §6 puts Home
   on the warm/clinical line and names the hero and Profile as the warm half.
   The lede survived and it is first person, but it is a capability sentence,
   not a curiosity one. Whether the opening keeps a warm sentence about *why*
   this work, or whether the warmth now lives only on Projects, Workshops,
   Writing and Teaching, is a positioning call.
