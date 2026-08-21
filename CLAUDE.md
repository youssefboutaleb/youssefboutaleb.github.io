# Working on this site

The operating brief for anyone — human or agent — editing this repository.
[`DESIGN.md`](DESIGN.md) owns how the site looks. [`awards.md`](awards.md) owns
what a record says. **This document owns why any of it exists**, and it wins
when the three disagree about intent.

---

## 1. What this site is

**A configurable, evidence-backed CV — not a portfolio sitting next to a CV.**

The distinction is the whole architecture. A portfolio is a gallery you browse.
This is the *long* version of a CV: everything that would not fit on two pages,
held in one place, with every claim linked to where it can be checked — and,
once the depth dial ships (§7), readable at whatever length the reader wants.

That solves a problem two PDF files cannot. A recruiter wants a fast career
summary but a deep look at the projects. A hiring manager wants the reverse. A
PDF forces the author to guess and pick one; this site lets the reader choose,
per visit, without asking anyone for a different file.

**Consequences that follow, and are not up for renegotiation:**

- Length is not a defect here. This site exists precisely to hold what the
  two-page version had to cut.
- Nothing is "extra content". If it is on the site it is CV material and must
  survive the same scrutiny as a line on the PDF.
- The PDF CV in the rail and this site are two renderings of one career. They
  must never contradict each other on a date, a title or a number.

## 2. Who reads it, and what success is

Three readers, at **mid-to-top-tier technical companies**, in this order:

| Reader | Gives it | Is deciding | Wants |
|---|---|---|---|
| **Recruiter / HR** | Seconds | Is this the right shape of candidate? | Titles, stack, dates, credentials — fast |
| **Hiring manager** | Minutes | Is there potential and trajectory here? | Scale, ownership, judgement, effort |
| **Engineer** | As long as it takes | Is this real? | Records, links, code, pull requests |

**Success is a first interview.** Verification, depth and the hard questions all
happen *in* that interview — the site's job is to make it happen, not to
pre-empt it. A page that is scrupulously accurate and gives nobody a reason to
keep reading has failed at its actual task.

## 3. The claim

**Data Engineering is the role. Everything else is supporting evidence for it.**

The site must leave no ambiguity about what job is wanted. Cloud and integration
experience is real and valuable, but it is a *qualifier* — it may sharpen the
Data Engineering claim and must never dilute it into "generalist". If a change
makes the target role harder to name in one word, the change is wrong.

### The thread: everything feeds data engineering

The profile spans data engineering, ML research, teaching and open source. Read
carelessly that looks scattered, and a scattered profile loses to a focused one.
The site's answer is **not** to hide the range — it is to make the connection
explicit. Data engineering is the trunk; the rest are branches that prove depth
in it:

- **ML and research** taught what pipelines have to feed, and what bad data
  costs downstream.
- **Teaching** forced the systems to be explained clearly to people who will ask
  why — the same skill that produces architecture docs a team can act on.
- **Open source** is the same debugging instinct, applied to somebody else's
  codebase and submitted back.
- **Competitions** are where the algorithmic reflex was built.

When adding or rewriting anything, ask: *does this visibly feed the data
engineering claim?* If a section cannot answer, it is the section that needs
work — not the thread.

## 4. Markets

Written for **France / EU**, **remote international**, and the **Gulf / MENA**.

- **English only, for now.** A French version is planned (§8) and is not a
  reason to write hedged or translatable English in the meantime.
- **Tunisian context is not glossed.** *1st of 86 teams*, *national*,
  *international, 7,094 teams* are legible to a reader who has never heard of
  the contest or the school. The scope and scale tags already do this work —
  see [`awards.md`](awards.md). Do not add explanatory asides about local
  institutions; link them and let the numbers carry it.
- **Mobility is stated, not left to be guessed.** The rail carries an
  *Availability* block on every page: *EU residence permit holder. Open to
  relocation within the EU and to fully remote roles.* A recruiter who has to
  wonder filters silently, and the candidate never finds out it happened.

  **The wording is deliberately bounded and must not be strengthened.** It says
  the EU residence question is already solved — which is the fact that matters,
  because hiring someone already resident in the EU is a different proposition
  from hiring from outside it. It does **not** claim EU-wide work authorisation,
  and phrasings like *"no visa sponsorship required"* or *"no visa problem in
  Europe"* must not be substituted: a permit issued by one member state does not
  automatically confer the right to work in another, and a recruiter who acts on
  an overclaim and then discovers otherwise has been given a reason to distrust
  everything else on the site. The specific issuing country is intentionally not
  named; the detail belongs in the conversation. Never paraphrase, upgrade or
  "clarify" a residence or work-authorisation status without the author.

## 5. Recruitment rules deliberately broken

These are **choices, not oversights**. An agent that "fixes" one of them has
damaged the site. Any proposal to reverse one goes to the author first.

| Convention | What this site does instead | Why |
|---|---|---|
| Keep it to one or two pages | Holds the long version, in full | That is the entire point of §1. Brevity is served by the depth dial, not by deletion. |
| No photo, no personal detail | Keeps the portrait and a first-person voice | A hiring manager hires a person. The warmth is bounded — see §6. |
| Stuff keywords for the ATS | Writes for humans, accepts some filter loss | This site is read by people who chose to open it. Keyword padding would corrupt the prose for readers who matter, to satisfy a machine that was going to be bypassed anyway. |
| Show only the wins | Shows unmerged PRs, in-progress papers, honest placements (643rd of 7,094) | An engineer trusts a page that admits what has not landed yet. Selective reporting is the fastest way to lose the third reader. |

## 6. Voice

### The map

**Warmth in the curiosity half; clinical precision in the credential half.**

| Warm — first person, personal, allowed to show delight | Clinical — factual, dated, checkable |
|---|---|
| Projects · Workshops · Writing · Teaching | Career · Education · Certifications · Research (journal) |

The contrast is itself the argument: *this person can be human and rigorous, and
knows which situation calls for which.* A site that is warm everywhere reads
informal to a formal reader; a site that is clinical everywhere reads like every
other CV. Keeping the line sharp is what makes both halves land.

### Register

Write as a person. Curiosity, effort and intent are the point.

**Banned:** *leveraged*, *demonstrated*, *consistent track record of*,
*passionate about*, *results-driven*, *spearheaded*, *synergy*. The whole visual
system exists to avoid looking like a template; the prose must not undo it.

### The one prose rule

**A `block__intro` is a single punchy line, and it is a pitch.** One sentence,
no run-up, no mechanics, no second paragraph. Full rule, rationale and the one
declared exception (Teaching) in [`DESIGN.md`](DESIGN.md) §11.1.

Reference examples, from Awards:

> *Engineering background plus competitive programming edge.*
>
> *Rapid prototyping, product design, and fast technical delivery.*

### Where each kind of sentence lives

| | Says | Where |
|---|---|---|
| **Pitch** | Why this work exists, what it shows about the person | `block__intro` — one line per block |
| **Evidence** | What was built, where, when, with what result | `.entry` records, from `src/data/` |
| **Provenance** | Where a hand-copied figure came from, and when | `block__note`, beneath the records |
| **Mechanics** | How a block works, what a tag means, why | The model documents — never the page |

## 7. The depth dial (planned)

The feature that makes §1 true rather than aspirational.

**Model: one global two-state control — Brief / Full.** Not per-section, not
progressive disclosure, not three levels. One switch, one thing to explain, one
thing to keep correct, and it prints correctly in both states.

**Brief keeps, per record:** title · period · tags · **one** bullet.

That works because the tag vocabulary already carries the metrics — *1st Place*,
*86 teams*, *Accepted upstream* — so a single bullet still says something real.
And it requires **no second body of prose**: Brief is a projection of the
existing data, never a parallel set of hand-written summaries that would drift
out of sync with the first.

**Full is the default and the canonical version.** Brief is a lens on it.

**On Principle 1.** [`DESIGN.md`](DESIGN.md) opens with *"a document, not an
interface"*, and a control is an interface element. The dial is admissible as
the single exception because it is a **reading aid, not a feature**: it changes
how much of the document is shown and nothing else — no state, no navigation, no
animation, no content that exists only in one mode. That reasoning is the
boundary. A second control needs an argument this strong, made in writing first.

## 8. Roadmap

Recorded so they are worked toward deliberately, and so an agent knows what is
merely *not done yet* versus what was *decided against*.

| # | Milestone | Notes |
|---|---|---|
| **M1** | **Prove data engineering ability, harder** | The author's first concern, and the site's biggest gap. Content to be written by hand: deeper job bullets naming systems, volumes and failure modes; pipeline case studies (problem → architecture → trade-offs → what broke → what changed); at least one real architecture diagram; possibly a *How I work* page from the operating doctrine already on Home. **Author-led — do not auto-generate this content.** |
| **M2** | **The Brief / Full depth dial** | Spec in §7. Build after M1, so there is something worth reading in Full. |
| **M3** | ~~Mobility line~~ **done** | *Availability* block in the rail: EU residence permit, open to EU relocation and remote. Text in `src/site.json`. |
| **M4** | **French version** | After the English site is stable. Must not fork the content model — one source, two renderings, or it is not worth doing. |
| **M5** | **Refresh cloud & integration framing** | Author intends to revisit how this is presented so it sharpens rather than dilutes the Data Engineering claim (§3). |

## 9. Honesty, and why there is no second rulebook

The site's honesty rules already exist and are enough:

- **Principle 3**, [`DESIGN.md`](DESIGN.md): claims carry a number and a link to
  where the number can be checked.
- **Rule 5**, [`awards.md`](awards.md): missing data is omitted, never invented.
- The dating rule in [`writing.md`](writing.md): a hand-copied figure and its
  *as of* date move in one change, or neither does.

**Do not add another layer of prohibitions on top of these.** They are already
enforced by the data model — records come from `src/data/`, figures render from
stored values, external markers are derived from URLs — which is stronger than a
list of things not to do. Judgement covers the rest, and a borderline claim goes
to the author rather than to a rule.

What the pitch layer gets is one line per block to be persuasive in (§6). It
does not get to claim what the records below it cannot support — not because a
rule forbids it, but because the third reader checks, and a pitch the evidence
cannot carry is the one failure this site cannot recover from.

## 10. Working agreement

**Propose options, then implement.**

- **User-facing prose** — intros, headlines, summaries, anything a recruiter
  reads: bring **2–3 concrete options** with the trade-off of each, and let the
  author choose. Do not write the final copy first and ask for approval after.
- **Structure, code, styles, docs, refactors**: proceed directly, then report
  the diff.
- **Positioning, claims, numbers, legal status**: always the author's call,
  never inferred.

## 11. Before you touch anything

- **Records are data.** Edit `src/data/*.json`. The `.html` files at the
  repository root are **generated** — never edit them.
- **Fragments are sources.** Section headings and intros live in
  `src/pages/*.html`.
- **Always rebuild and check:**

  ```sh
  python3 tools/build.py
  python3 tools/check.py
  ```

  `check.py` fails on dead links, a class used in markup with no rule in
  `main.css`, an inline style, a missing `alt`, a duplicate `id`, and on a built
  page that has drifted from its source.

## 12. Where the reasoning lives

| Document | Owns |
|---|---|
| `CLAUDE.md` (this file) | Why the site exists, who it is for, how to work on it |
| [`DESIGN.md`](DESIGN.md) | The visual and structural system, and the intro rule |
| [`awards.md`](awards.md) | The entry metadata convention every page follows |
| [`README.md`](README.md) | How to add each kind of record |
| `career.md` · `projects.md` · `research.md` · `writing.md` · `teaching.md` · `workshops.md` | The model for one page each |

If a rule is worth following twice, write it into the document that owns it.
