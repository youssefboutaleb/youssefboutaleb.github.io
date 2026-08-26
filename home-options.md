# Home page: what is out of sync, and three ways to rebuild it

Written after reading `src/layout.html`, all eight fragments in `src/pages/`,
every file in `src/data/`, `tools/build.py`, `assets/css/main.css`, and the four
model documents that claim to govern them. Nothing has been changed. This is
the discussion artefact `CLAUDE.md` §10 asks for before code moves.

`python3 tools/build.py && python3 tools/check.py` both pass today. Everything
below is a defect the checker cannot see, because the checker validates markup
and links, not whether the documentation still describes the site.

---

## Part 1: the desyncs

Ordered by how much damage each one does if left alone.

### 1.1 The rail is gone. Every document still describes it.

`src/layout.html` is now a top header, a horizontal `.nav`, `<main>`, footer.
There is no sidebar. The design system has not been told:

| Document | Says | Reality |
|---|---|---|
| `DESIGN.md` §4 | `--container-max` 1600px, `--sidebar-width` 280px rail, `--column-gap` | None of those four tokens exist in `main.css`. The container is 1100px, one column |
| `DESIGN.md` §13 | ">960px: two columns, sticky rail" | One column at every width |
| `DESIGN.md` §15 | "Landmarks: rail `<header>`" | The `<header>` is the top brand bar |
| `DESIGN.md` §16 | "Who is this engineer? Rail identity"; "How do I reach them? The rail, on every page" | Neither is true. Contact is now its own page |
| `DESIGN.md` §1 | "Prose is capped at `--measure` (74ch)" | `--measure: 100%` (`main.css:215`). The cap is a no-op |
| `CLAUDE.md` §4 | "The rail carries an *Availability* block on every page" | It carries it on Home and on Contact, in two different wordings |
| `CLAUDE.md` §8, M3 | "*Availability* block in the rail. Text in `src/site.json`" | `site.availability` is read by nothing |
| `README.md` §Architecture | "The seven published pages share an identical head, sidebar, navigation" | Eight pages, no sidebar |
| `main.css` header comment | "sticky identity rail on the left, a plain document on the right" | Same |

The `--measure` one has a visible consequence, not just a documentary one. At
1100px with 15px body text, a line of Profile prose runs to roughly 110
characters. `DESIGN.md` chose 74ch for a reason and the reason has not changed.

### 1.2 Home is the only page with no model document

`career.md` · `projects.md` · `research.md` · `writing.md` · `teaching.md` ·
`workshops.md` · `awards.md` · `skills.md` exist. There is no `home.md` and no
`contact.md`. Home's rules currently live in two HTML comments inside
`src/pages/index.html` and a paragraph in `DESIGN.md` §10.

That is why Home drifted first: it is the one page where "the document that
owns the rule" (`CLAUDE.md` §12) does not exist, so there was nothing to
contradict when the page changed.

### 1.3 Dead data, and two sources of truth for contact

`src/site.json` keys that nothing reads any more:

- `portrait_alt` (the hero hard-codes its own `alt`)
- `availability` (the hero hard-codes its own wording)
- `contact_invitation`
- `contact[]` (three entries)
- `socials[]` (three entries)

`src/partials/contact-item.html` and `src/partials/social-link.html` render
nothing. `build.contact` and `build.socials` are still computed twice each in
`tools/build.py` (in `blocks` and again in `context`) and substituted nowhere.
`.social`, `.icon--lg`, `.sidebar`, `.sidebar__portrait`, `.sidebar__section`
are dead CSS: `check.py` already prints them in its unused-class note.

Meanwhile `src/pages/contact.html` hand-writes the email, the academic email,
the phone number and the three social URLs that `site.json` still holds. The
phone number now exists in two places, in two formats. `CLAUDE.md` §11 says
records are data; Contact is the first page to break it.

### 1.4 The availability line exists in three wordings

| Where | Text |
|---|---|
| `src/site.json` | "EU residence permit holder. Open to relocation within the EU and to fully remote roles." |
| `index.html` hero | "EU residence permit holder &middot; Open to EU relocation &amp; Remote roles" |
| `contact.html` | "EU residence permit holder &middot; Open to relocation and remote roles" |

`CLAUDE.md` §4 is explicit that this wording is bounded and must not be
paraphrased. Two of the three are paraphrases. None of them is *wrong*, but the
rule exists so that the sentence has one owner, and right now it has three.

### 1.5 `impact.json` carries two fields the renderer throws away

`title` and `label` were added to all four records. `render_impact()`
(`tools/build.py:992`) reads `figure`, `evidence` and `source` only. So:

```
"title": "Azure cost control",          <- rendered nowhere
"label": "Documented recurring saving", <- rendered nowhere
```

Either the renderer was never finished, or the data was written ahead of a
design decision that has not been made. This is the single clearest signal that
Home was left mid-move.

### 1.6 Home does not follow the page grammar the other seven use

Every other page opens each block with a `block__intro`: one punchy line that
`CLAUDE.md` §6 and `DESIGN.md` §11.1 both call the pitch. Home has four blocks
and one intro:

| Block | Intro |
|---|---|
| Profile | none (a `.prose` paragraph instead) |
| Skills & Evidence | "What I can do, and what proves it." |
| Selected Impact | none |
| Languages | none |
| Volunteering | none |

The page a recruiter opens first is the page with the fewest pitch lines on it.

### 1.7 Home carries none of the site's tag vocabulary

Seven pages speak in `.tag-list`: fixed category order, one colour per
category, figures in bold inside `.tag--scale`. Home's only chips are the Skills
citations, which `skills.md` declares as an *exception* to that language, not an
instance of it.

So the front page is the one page that does not use the visual system the site
spent `DESIGN.md` §7 arguing for. A reader who lands on Home, scrolls it, and
clicks through to Career meets the tag vocabulary for the first time on page two.

### 1.8 Skills ordering floats ML above the Data Engineering claim

`skill_sort_key()` ranks by standing, then by evidence count. Four skills tie at
"Production-proven", so the tiebreak decides the front page, and it currently
renders:

1. Data pipeline engineering (6 citations)
2. **Machine learning & computer vision** (6 citations)
3. Data warehousing & analytics (5)
4. Programming & scripting (5)
5. Observability & incident response (5)
6. Cloud platform operations (4)
7. Systems integration & APIs (4)

`CLAUDE.md` §3: "Data Engineering is the role. Everything else is supporting
evidence for it." The second thing a hiring manager reads on the front page is
computer vision. The sort is doing exactly what it was written to do, which is
why this is a *design* question and not a bug: the ordering rule optimises for
evidence density and the site's thesis optimises for one claim.

### 1.9 The strongest DE figures on the site never reach Home

`experience.json` now holds, in the JACQUEMUS record alone:

- ~5,000 orders per hour at sale events
- ~800,000 events and records a day, hundreds of gigabytes
- `scale`: 150+ pipelines, of which 20+ built and maintained
- refresh schedules from 10 minutes to daily, payloads to 150 MB
- Datadog alert coverage across the 150+ job estate

Home's Selected Impact instead shows: EUR1,400/month saved, a 100x C++ speedup,
two open-source PRs, and a 1st-of-86 contest placement. Two of the four are not
data engineering, and the two that are, are the *smallest* DE facts the site
holds. M1 in `CLAUDE.md` §8 ("prove data engineering ability, harder") was
delivered on Career and never propagated forward.

### 1.10 Contact invented components the design system does not know about

`.contact-section`, `.contact-section__title`, `.contact-list`,
`.contact-list__item`, `.contact-list__link`, `.contact-list__row`,
`.contact-list__label`, `.contact-list__value`: eight new classes, none in
`DESIGN.md`. `DESIGN.md` §17 rule 1 is "reach for an existing component first",
and `.deflist` is precisely the "category: values" component this page needed.
Contact is also the only page whose sections are not `.block` and whose headings
are `<h2>` where every other page uses `<h3 class="block__title">`.

Flagged here rather than in a separate document because Home and Contact are the
two pages that moved together and the two that need the same decision.

### 1.11 Home and Projects contradict each other today, in the build

Both Kanboard pull requests are `"state": "merged"` in `projects.json`.
`projects.html` renders *Accepted upstream &middot; PR #586*. `index.html`
renders:

> **2 plugins authored and submitted upstream**
> Draw.io embedding and a file-attachment rework, **both open** against the
> official Kanboard plugin directory: PR #586 and PR #585.

This is the exact failure the `render_impact()` docstring was written to record,
recurring in the opposite direction: last time Home overclaimed, this time it
underclaims. The docstring's fix (move the record into data, make `source`
mandatory) made the citation reliable and did nothing about the sentence, which
is the part that drifted both times. Whatever Impact becomes in step 5, the
lesson is that a hand-written figure beside a machine-derived one will always
lose, so `figure` should be the only hand-written part of the record and the
*state* should come from the same place Projects gets it.

---

## Part 2: three architectures for the new Home

Each is a complete position, not a menu to mix freely. Sections 3 and 4 give the
component-level choices that sit inside whichever one is picked.

### Option A: Repair in place

Home keeps its five blocks. Fix only what is provably broken.

- Give every block a `block__intro`.
- Finish `render_impact()` so `title` and `label` render, or delete both fields.
- Restore `--measure: 74ch`.
- Delete the dead `site.json` keys, partials and CSS; move Contact onto
  `site.json` data.
- Rewrite `DESIGN.md` §4, §13, §15, §16, `CLAUDE.md` §4/M3, `README.md`
  §Architecture and the `main.css` header for the top-nav layout.
- Write `home.md`.

| | |
|---|---|
| **Gains** | The documentation becomes true again. Lowest risk, one afternoon, nothing a reader has to relearn |
| **Costs** | 1.7, 1.8 and 1.9 survive. Home still does not speak the tag language and still leads its impact block with a contest placement |
| **Weakens** | Nothing |

### Option B: Home as the proof page

Home stops being a summary and becomes the argument. Six blocks:

```
Hero            portrait, title, lede, availability     (as today)
Profile         one prose paragraph + linked credentials
Current work    NEW. Generated from experience[0]
Skills & Evidence                                       (as today, resorted)
Selected Impact rebuilt as .entry records with tags
Languages                                               (as today)
```

Volunteering moves to Career. Languages stays (it is a genuine hiring fact and
belongs above the fold-ish, not on a page nobody opens).

**Current work** is the new block and the reason to pick this option. It renders
from `experience[0]` in `experience.json`, so it cannot drift from Career by
construction:

```
JACQUEMUS · Data Engineer          Paris, France · Aug 2024 - Present (2 years)
[Luxury E-commerce & Retail] [Permanent] [Remote] [150+ pipelines]
[Azure Data Factory] [Azure Fabric] [Apache Spark] [Datadog]
Order, customer, product and pricing data into a medallion lakehouse:
~800,000 events a day, order flows peaking near 5,000 per hour.
```

That single block answers 1.7 (Home now speaks in tags), 1.9 (the real DE
figures arrive on page one) and `DESIGN.md` §16's "who is this engineer",
without one hand-written sentence that can go stale.

| | |
|---|---|
| **Gains** | Home finally makes the Data Engineering case with the numbers that support it. One shared vocabulary across all eight pages. Zero new drift surface: the block is a projection |
| **Costs** | One new renderer (~20 lines, reusing `render_meta`). Career's first record now appears twice on the site, which is a restatement `CLAUDE.md` §9 tolerates only when it is generated. It is |
| **Weakens** | Home gets longer. Acceptable under `CLAUDE.md` §5 ("length is not a defect here"), but it front-loads more before Skills & Evidence |

### Option C: Home as the Brief projection (M2 groundwork)

Home becomes what the Brief state of the depth dial will look like for the whole
site: every block is a generated, one-line-per-record digest of one other page,
with its tag list intact and a link through.

```
Hero
Profile
Skills & Evidence     (unchanged: already the proof layer)
At a glance           counts computed from the data files
Currently             experience[0]
Selected work         top project + top publication + top award, generated
Languages
```

"At a glance" is computed by the builder, never typed: `len(awards)` contest
results, `len(certifications[].credentials)` certifications, upstream PRs where
`state != null`, courses taught, students taught from `teaching[].scale`.

| | |
|---|---|
| **Gains** | Builds M2's machinery a page early and proves the projection model works before betting the whole site on it. A recruiter's "seconds" pass is genuinely served for the first time |
| **Costs** | The largest build. Needs a `record_digest()` abstraction across six different record shapes, which is real design work, not plumbing. Risks §7's boundary: a Home made of projections starts to look like an interface, not a document |
| **Weakens** | The distinction between Home and the other pages. If Home shows the top of every page, some readers never leave it, which is the opposite of what a long-form CV wants |

---

## Part 3: component-level options

These apply inside A, B or C.

### 3.1 Selected Impact: what to do with `title` and `label`

**Option i: revert.** Delete both fields, keep the `.deflist`.
*Gains:* smallest diff, `deflist` is already documented in `DESIGN.md` §10.
*Costs:* the block stays the site's weakest, least scannable component and the
one place `CLAUDE.md` admits claims can drift.

**Option ii: enrich the `deflist`.** `dt` becomes `figure`, `dd` becomes
`<b>label</b>. evidence (source)`.
*Gains:* uses both fields, three lines of Python, no new component.
*Costs:* `label` and `evidence` are both prose in the same `dd`; the bold label
is a new treatment with no rule behind it.

**Option iii (recommended): promote Impact to `.entry` with a tag list.**

```
Azure cost control                                    entry__title
[Documented recurring saving] [€1,400 per month] [Career]   tag-list
Development-environment shutdowns, per-environment          entry__summary
compute sizing, and shared Spark-pool redesign, with
no SLA impact on morning reporting.
```

A new `impact` model in `MODELS`: `("kind", "figure", "source")`. `kind` takes
the amber standing slot (as `engagement` does on a job), `figure` takes grey
regular weight with the number bold (the `scale` treatment, `awards.md` rule 4),
`source` is the linked citation, replacing the parenthetical.

*Gains:* the block joins the site's vocabulary, the figure gets the emphasis it
has everywhere else, `title`/`label` both earn their place, and the citation
stops being a parenthesis.
*Costs:* a ninth model. `DESIGN.md` §17 asks for a written case; this document is
it, and the case is that Impact is a record type, has always been one, and was
only a `deflist` because it started as three lines in a fragment.
*Watch:* `label` should be renamed `kind` in the data if this is chosen, so the
field name matches the category name the way every other model's does.

### 3.2 Credentials in Profile

Today: four unlinked `<li>` strings in `site.json`, in a `.credentials` list
with no component in `DESIGN.md`. Career's Certifications block links every one
of the same certificates.

**Option i:** leave it. Four lines, fast to read, no maintenance.
**Option ii (recommended):** make each line a link to `career.html#certifications`.
One anchor, no per-certificate mapping, and it stops being the one capability
claim on Home with nothing to click. Also fixes the DP-600 gap: the string still
reads "Azure Databases & Fabric" while `certifications.json` gained
*Fabric Analytics Engineer Associate (DP-600)* this week.
**Option iii:** derive the four strings from `certifications.json` by issuer, so
adding a certificate updates Home automatically. Most correct, most work, and the
grouping wording ("Datadog Certified in Fundamentals, APM & Log Management") is
editorial in a way a grouper cannot reproduce.

### 3.3 Skills ordering (1.8)

**Option i:** leave the sort alone. It is honest and it is derived.
**Option ii (recommended):** add a third sort key ahead of evidence count: a
`thread` field on each skill, `"trunk"` or `"branch"`, straight out of
`CLAUDE.md` §3's trunk-and-branches metaphor. Trunk skills sort first within a
standing. ML stays "Production-proven" with all six citations, it just stops
being the second thing on the page.
*Costs:* one hand-set field per skill, which is the thing `skills.md` was proud
of not having. Defensible because it encodes positioning, not level: the field
says *which claim this supports*, never *how good I am at it*.
**Option iii:** split the block into "Data Engineering" and "Adjacent depth".
Loudest, and it makes the branches look like an apology. Not recommended.

### 3.4 Volunteering and Languages

Volunteering is the least DE-relevant block on the site and it currently closes
the front page. Three placements: keep on Home (status quo), move to Career
below Education, or move to Contact. Career is the better home: it is a dated
record among dated records.

Languages should stay on Home. It is a hiring filter for the France/EU and
Gulf/MENA markets in `CLAUDE.md` §4, and a recruiter should not need a second
page for it.

### 3.5 Section labels

| Today | Alternatives | Note |
|---|---|---|
| Profile | *In short* · *What I build* | "Profile" is CV-generic. "What I build" states the claim |
| Skills & Evidence | keep | `skills.md` owns it |
| Selected Impact | *Impact* · *Proof* | "Selected" quietly admits curation, which is honest. Keep |
| Languages | keep | |
| Volunteering | keep, wherever it lands | |
| (new) Current work | *Currently* · *Now* · *What I am running* | "Currently" is warmest and shortest |

---

## Part 4: recommendation

**Option B, with 3.1(iii), 3.2(ii), 3.3(ii), and Volunteering moved to Career.**

The reasoning:

1. Option A does not solve the problem the author actually named. Home is not
   merely stale, it is the only page that does not argue in the site's own
   language, and repair-in-place leaves that intact.
2. Option C is the right destination and the wrong next step. Its abstraction
   should be designed once, against M2's Brief/Full spec, not invented early for
   one page and then retrofitted. Doing C now risks locking M2 into whatever
   shape Home happened to need.
3. Option B is the only one that puts the JACQUEMUS figures on the front page
   without hand-writing them, which is what M1 was for and where M1 stopped.

**Sequence, one section closed end-to-end at a time (`CLAUDE.md` §10.6):**

| # | Step | Touches |
|---|---|---|
| 1 | Documentation truth pass: rail out of `DESIGN.md` §4/§13/§15/§16, `CLAUDE.md` §4/M3, `README.md`, `main.css` header. Restore `--measure: 74ch` | docs, one token |
| 2 | Dead-data sweep: drop unused `site.json` keys or wire them; delete the two dead partials, the doubled `build.contact`/`build.socials`, the `.sidebar`/`.social` CSS | build, data, css |
| 3 | Availability: one wording, one owner, `site.json`, rendered in both places | data, 2 fragments |
| 4 | Write `home.md` (and `contact.md`), so the page has an owner before it is rebuilt | new docs |
| 5 | Impact to `.entry` + `impact` model | build, data, css, `DESIGN.md`, `awards.md` cross-ref |
| 6 | New **Currently** block from `experience[0]` | build, fragment, `home.md` |
| 7 | Skills `thread` key; Volunteering to Career; block intros for every Home block | data, build, fragments |
| 8 | Contact onto `.block`/`.deflist` and `site.json` data | fragment, css |

Steps 1-4 are repairs with no design risk and can start immediately. Step 5 is
the first one that needs a decision from the author.

---

## Part 5: questions before step 5

1. **`impact` as a ninth model: yes or no?** Everything in 3.1(iii) hangs on it.
2. **What counts as impact now?** The four lines were chosen when Career was
   thin. With 5,000 orders/hour and 800,000 events/day available, should Impact
   stay four lines, and should the contest placement keep one of them?
3. **`5,000 orders per hour` and `~800,000 events a day`:** approved as
   publishable, and stated as approximate? They are in `experience.json` prose
   today, but a *tag* is a louder claim than a clause in a summary.
4. **The "2 years" tenure figure** now renders on Career. Should Home's
   Currently block repeat it, or is period enough?
5. **Volunteering: Career or Contact?** Career is the recommendation.
6. **Does Contact get folded into this pass, or its own?** It has the same
   disease and is a much smaller patient.
