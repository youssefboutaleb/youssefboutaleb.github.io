# Working on this site

The operating brief for anyone (human or agent) editing this repository.
[`DESIGN.md`](DESIGN.md) owns how the site looks. [`awards.md`](awards.md) owns
what a record says. **This document owns why any of it exists**, and it wins
when the three disagree about intent.

---

## 1. What this site is

**A configurable, evidence-backed CV, not a portfolio sitting next to a CV.**

The distinction is the whole architecture. A portfolio is a gallery you browse.
This is the *long* version of a CV: everything that would not fit on two pages,
held in one place, with every claim linked to where it can be checked, and,
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
- The PDF CV in the brand bar and this site are two renderings of one career.
  They must never contradict each other on a date, a title or a number.

## 2. Who reads it, and what success is

Three readers, at **mid-to-top-tier technical companies**, in this order:

| Reader | Gives it | Is deciding | Wants |
|---|---|---|---|
| **Recruiter / HR** | Seconds | Is this the right shape of candidate? | Titles, stack, dates, credentials: fast |
| **Hiring manager** | Minutes | Is there potential and trajectory here? | Scale, ownership, judgement, effort |
| **Engineer** | As long as it takes | Is this real? | Records, links, code, pull requests |

**Success is a first interview.** Verification, depth and the hard questions all
happen *in* that interview: the site's job is to make it happen, not to
pre-empt it. A page that is scrupulously accurate and gives nobody a reason to
keep reading has failed at its actual task.

## 3. The claim

**Data Engineering is the role. Everything else is supporting evidence for it.**

The site must leave no ambiguity about what job is wanted. Cloud and integration
experience is real and valuable, but it is a *qualifier*: it may sharpen the
Data Engineering claim and must never dilute it into "generalist". If a change
makes the target role harder to name in one word, the change is wrong.

### The thread: everything feeds data engineering

The profile spans data engineering, ML research, teaching and open source. Read
carelessly that looks scattered, and a scattered profile loses to a focused one.
The site's answer is **not** to hide the range: it is to make the connection
explicit. Data engineering is the trunk; the rest are branches that prove depth
in it:

- **ML and research** taught what pipelines have to feed, and what bad data
  costs downstream.
- **Teaching** forced the systems to be explained clearly to people who will ask
  why: the same skill that produces architecture docs a team can act on.
- **Open source** is the same debugging instinct, applied to somebody else's
  codebase and submitted back.
- **Competitions** are where the algorithmic reflex was built.

When adding or rewriting anything, ask: *does this visibly feed the data
engineering claim?* If a section cannot answer, it is the section that needs
work, not the thread.

## 4. Markets

Written for **France / EU**, **remote international**, and the **Gulf / MENA**.

- **English only, for now.** A French version is planned (§8) and is not a
  reason to write hedged or translatable English in the meantime.
- **Tunisian context is not glossed.** *1st of 86 teams*, *national*,
  *international, 7,094 teams* are legible to a reader who has never heard of
  the contest or the school. The scope and scale tags already do this work,
  see [`awards.md`](awards.md). Do not add explanatory asides about local
  institutions; link them and let the numbers carry it.
- **Mobility is stated, not left to be guessed.** *EU residence permit holder.
  Open to relocation within the EU and to fully remote roles.* A recruiter who
  has to wonder filters silently, and the candidate never finds out it happened.

  **The sentence has one owner: `availability` in [`src/site.json`](src/site.json).**
  It renders in Home's hero and on Contact, from that one string, and it is
  never typed into a fragment. This is not tidiness. When the three places that
  carried it each held their own copy, all three said something slightly
  different, which is exactly the drift the next paragraph forbids.

  **The wording is deliberately bounded and must not be strengthened.** It says
  the EU residence question is already solved, which is the fact that matters,
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
| No photo, no personal detail | Keeps the portrait and a first-person voice | A hiring manager hires a person. The warmth is bounded, see §6. |
| Stuff keywords for the ATS | Writes for humans, accepts some filter loss | This site is read by people who chose to open it. Keyword padding would corrupt the prose for readers who matter, to satisfy a machine that was going to be bypassed anyway. |
| Show only the wins | Shows in-progress papers, honest placements (643rd of 7,094), and capabilities with no production record at all | An engineer trusts a page that admits what has not landed yet. Selective reporting is the fastest way to lose the third reader. |

The clearest current example is Home's Skills & Evidence. Two rows carry no
production citation: Airflow is certified twice and taught, and Spark is taught
only, and both say so. Leaving them out would make the block shorter and
stronger-looking and would destroy it, because a matrix where everything is
maximally proven is a matrix nobody believes. The Kanboard pull requests used to
be the example here; they were shown while open, and they have since merged,
which is the ordinary way this rule pays off.

## 6. Voice

### The map

**Warmth in the curiosity half; clinical precision in the credential half.**

| Warm: first person, personal, allowed to show delight | Clinical: factual, dated, checkable |
|---|---|
| Projects · Workshops · Writing · Teaching | Career · Education · Certifications · Research (journal) |

**Home sits on the line, deliberately, and that is why it is the hardest page
to write.** The hero and the Profile paragraph are first person and warm; the
Currently block, Skills & Evidence and Impact in Numbers are records and read
clinically. The pitch lines carry the warmth so the records do not have to.

The contrast is itself the argument: *this person can be human and rigorous, and
knows which situation calls for which.* A site that is warm everywhere reads
informal to a formal reader; a site that is clinical everywhere reads like every
other CV. Keeping the line sharp is what makes both halves land.

### Register

Write as a person. Curiosity, effort and intent are the point.

**Banned:** *leveraged*, *demonstrated*, *consistent track record of*,
*passionate about*, *results-driven*, *spearheaded*, *synergy*. The whole visual
system exists to avoid looking like a template; the prose must not undo it.

### No dashes, anywhere in the repository

**The em dash and the en dash are banned.** Not discouraged: banned. That
covers the characters themselves (U+2014 and U+2013) and their HTML entities.
It holds for every file, not only the prose a visitor reads: page fragments,
`src/data/*.json`, the model documents, this file, CSS comments and the
docstrings in `tools/`.

**Neither character is printed in this paragraph, deliberately.**
`tools/check.py` fails the build on all four forms, and until it did, the rule
was enforced by searching the repository. A rule that spelled out the thing it
forbids was then the one hit that search always returned, which is the whole
reason it names them by codepoint now.

The em dash is the single loudest tell that a passage was machine-written, and
this site's whole argument is that a person wrote it. One survivor in a
paragraph undoes the rest.

Use the punctuation that actually fits the job:

| Instead of a dash | Use | Example |
|---|---|---|
| Statement then its elaboration | `:` | `Lectures: 20 h` |
| An aside inside a sentence | `( )` | `the tags (fixed order) carry the metadata` |
| A clause opening with *and, but, so, which, not, see* | `,` | `stated once, so a tag would restate it` |
| Two peers on one line | `&middot;` | `Company &middot; Role`, `Teaching &middot; Youssef Boutaleb` |
| A range | `-` | `2021-2024`, `Aug 2024 - Present`, `1.5-2 h` |

A colon is the default and is right most of the time. It is wrong before a
conjunction: *"stated once: so a tag would restate it"* is not English, and
that case takes a comma.

`&middot;` is the site's established peer separator, used by the tag renderer,
by every `.entry__title` that joins a role to a company, and by the dateline
that joins a location to a period. Do not invent a third one.

It is *not* how a list of tools is written any more. Tools render as outlined
`.tag--stack` chips on Career, Projects and Home alike, which is one vocabulary
for *a thing this was built with*: [`skills.md`](skills.md) and
[`projects.md`](projects.md).

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
| **Pitch** | Why this work exists, what it shows about the person | `block__intro`: one line per block |
| **Capability** | What I can do, and the records that prove it | `.skill` rows, from `src/data/skills.json` |
| **Evidence** | What was built, where, when, with what result | `.entry` records, from `src/data/` |
| **Consequence** | What changed for the business because it shipped | `.point__impact`, one line under the bullet that earned it |
| **Provenance** | Where a hand-copied figure came from, and when | `block__note`, beneath the records |
| **Mechanics** | How a block works, what a tag means, why | The model documents, never the page |

**Consequence is written once and may be read twice.** Home's Impact in Numbers
does not summarise a bullet, it quotes the bullet's own `impact` line through an
id, so the two pages share a sentence rather than keeping two in agreement. If a
sentence would be true on Home and on Career, that is the signal it belongs on
the record and is cited from Home, never that it should be written in both
places. [`home.md`](home.md).

## 7. The depth dial (planned)

The feature that makes §1 true rather than aspirational.

**Model: one global two-state control: Brief / Full.** Not per-section, not
progressive disclosure, not three levels. One switch, one thing to explain, one
thing to keep correct, and it prints correctly in both states.

**Brief keeps, per record:** title · period · tags · **one** bullet.

That works because the tag vocabulary already carries the metrics (*1st Place*,
*86 teams*, *Accepted upstream*) so a single bullet still says something real.
And it requires **no second body of prose**: Brief is a projection of the
existing data, never a parallel set of hand-written summaries that would drift
out of sync with the first.

**Full is the default and the canonical version.** Brief is a lens on it.

**The mechanism is no longer theoretical.** Home already renders two blocks as
projections of records held elsewhere: *Currently* prints `experience[0]`'s
title, dateline and tags with no content of its own, and *Impact in Numbers*
quotes a bullet's `impact` line through an id. Both prove the thing M2 depends
on, which is that a shorter rendering can be a *view* of the data rather than a
second body of prose. What they do not prove is the hard part: a global control,
and a Brief projection for every record type on the site rather than two.
[`home.md`](home.md) carries what was learned.

**On Principle 1.** [`DESIGN.md`](DESIGN.md) opens with *"a document, not an
interface"*, and a control is an interface element. The dial is admissible as
the single exception because it is a **reading aid, not a feature**: it changes
how much of the document is shown and nothing else: no state, no navigation, no
animation, no content that exists only in one mode. That reasoning is the
boundary. A second control needs an argument this strong, made in writing first.

### The second exception: the page context rail

Written after the fact, which is the wrong order and is recorded as such: the
rail shipped before the argument for it existed.

**It fails the dial's test and passes a different one.** The dial is admissible
because it is not navigation. The rail *is* navigation, so that reasoning
cannot be borrowed, and the honest question is whether Principle 1 forbids a
table of contents. It does not, and the reason is in the principle's own second
sentence: *a reader should be able to print the page and lose nothing.*

**Removing the rail loses no information.** Every line in it is an anchor to a
record that is already on the page, generated from the same data that rendered
the record. It carries no prose of its own, no state, no mode, and no
JavaScript: it is a list of links, which is what a contents page has been since
long before there were interfaces to confuse it with. That is the test a second
exception has to pass, and it is stricter than it sounds: an element is part of
the document, not an interface on top of it, **when deleting it costs the
reader nothing but convenience.** The rail is deleted in print for exactly that
reason, and the printed page is not poorer for it.

**Where the boundary now sits.** `main.css` styles `.book-toc__link.is-active`,
and nothing sets that class. Wiring it up would add scroll position as state,
which is the thing the first two exceptions were careful not to introduce. It
would need its own argument, and this paragraph is not it.

### The third exception: the theme switch

**This one stores something, and the paragraph above had just finished saying
that was the line.** Recorded that way round on purpose. The author asked for
the control after the dark rendering shipped without one, having chosen
system-only when it was first put to them; reversing a decision is theirs to
do, and the argument then has to be made honestly rather than retrofitted to
look like it was always fine.

**What it stores is not about the document.** One key holds one of two strings,
naming a rendering the reader prefers. It changes no content, adds no page to
the site, appears in nothing that prints, and is invisible to every other
reader. The scroll-spy fails on exactly the count this passes: it would make
the document react continuously to how the page is being read, which is what
turns a document into an application. A theme preference is set once and then
does nothing, more like the browser's own zoom than like a feature.

**Why the default is not enough on its own.** `prefers-color-scheme` reports
the machine, and the machine is often wrong about the room: a laptop pinned to
dark all year is being read at noon by a window, and a reader who wants this
page light for an hour has no way to say so. That is an accessibility
affordance, and the cost of not having one is paid by the reader who cannot
comfortably read the page at all.

**What keeps it a reading aid.** *System* is the default and a state the
control can return to, not a third palette, so the honest answer is that most
readers never touch it and are followed by their own machine. It renders only
when JavaScript runs, it is hidden in print, and the entire mechanism is one
attribute on `<html>` feeding the `color-scheme` property. If a future change
needs it to do more than that, it has outgrown this argument.

## 8. Roadmap

Recorded so they are worked toward deliberately, and so an agent knows what is
merely *not done yet* versus what was *decided against*.

| # | Milestone | Notes |
|---|---|---|
| **M1a** | ~~Skills & Evidence block~~ **done** | Home's Skills list became a capability → evidence block: a fixed label column carrying the capability and its derived standing, and a flowing column carrying its tools and every record on the site that proves them. A true five-column matrix was considered and rejected on measurements; the argument is in [`skills.md`](skills.md). |
| **M1** | **Prove data engineering ability, harder** | The author's first concern, and the site's biggest gap. **Partly landed.** Done: job bullets naming systems, volumes and failure modes, each with its consequence on a `.point__impact` line; Home's *Currently* block; Impact in Numbers quoting those bullets rather than paraphrasing them; and now the **diagram mechanism**, which draws a declared architecture as inline SVG with no JavaScript, prints, and inherits the page's ink ([`diagrams.md`](diagrams.md)). Still open, and **author-led**: pipeline case studies (problem, architecture, trade-offs, what broke, what changed), the content of at least one real diagram, and possibly a *How I work* page from the doctrine now in Career's Summary. **Do not auto-generate this content.** `src/data/diagrams.json` is empty on purpose. |
| **M1b** | ~~Home rebuilt~~ **done** | Home became the page it claims to be: one rule (restate only by projection, citation or quotation), a *Currently* projection, Impact in Numbers quoting the bullets it cites, Volunteering moved to Career, Domains deleted, and a model document that did not exist before. [`home.md`](home.md). |
| **M2** | **The Brief / Full depth dial** | Spec in §7. Build after M1, so there is something worth reading in Full. Two blocks on Home are already projections, which proves the mechanism but not the control. |
| **M3** | ~~Mobility line~~ **done** | EU residence permit, open to EU relocation and remote. One string, `availability` in `src/site.json`, rendered in Home's hero and on Contact. |
| **M4** | ~~French version~~ **mechanism done, all eight pages published, intro lines open** | The overlay reaches the content now, and it did not before: ten of twelve renderers read `record[...]` directly, six data files carried no record ids, `cite_index` walked raw English, and `t()` never reported a list as missing, so most of the words on most of the pages were unreachable while this row claimed the mechanism had landed. Fixed, then translated: every user-visible field routes through `t()`, nested `groups`, `roles`, `syllabus` and `capstone` are addressable, impact `figure` objects translate (so `check_figure` compares like with like per locale), and the renderer labels, standings, proof key, month names, `Present` and the French colon are all locale-aware. Coverage runs 55% to 89%, every page clears `MIN_TRANSLATED`, and the switch works site-wide. **Still author-led: every `block__intro` and the Home lede are literal drafts marked BROUILLON in `src/i18n/fr/pages/`, and `availability` renders in English on the French pages because §4 reserves that sentence.** |
| **M5** | **Refresh cloud & integration framing** | Author intends to revisit how this is presented so it sharpens rather than dilutes the Data Engineering claim (§3). |

## 9. Honesty, and why there is no second rulebook

The site's honesty rules already exist and are enough:

- **Principle 3**, [`DESIGN.md`](DESIGN.md): claims carry a number and a link to
  where the number can be checked.
- **Rule 5**, [`awards.md`](awards.md): missing data is omitted, never invented.
- The dating rule in [`writing.md`](writing.md): a hand-copied figure and its
  *as of* date move in one change, or neither does.

**Do not add another layer of prohibitions on top of these.** They are already
enforced by the data model, which is stronger than a list of things not to do.
What the build refuses to produce, today:

| The build fails on | So this cannot happen |
|---|---|
| A citation pointing at a page or anchor that does not exist | A skill or an impact line citing proof the site does not carry |
| A Impact in Numbers figure absent from the bullet it cites | A bullet edited and its figure on Home left behind |
| An impact record with both `cite` and `evidence`, or neither | Two hand-written copies of one sentence, drifting apart |
| Two bullets sharing an id | A citation landing on the wrong evidence |
| A `result` written beside `upstream_prs` | Home calling a pull request *submitted* while Projects calls it *accepted* |
| A built page that has drifted from its source | A hand-edit to a generated file surviving a rebuild |
| A page context entry with no label the parser could read | The rail printing a slug back at the reader as if it were a title |
| A translated string whose English original has since changed | The French confidently saying last month's number while the English says this month's |
| A translated fragment missing an anchor or a `{{ build.* }}` block | A citation pointing at nothing, or a block of records absent from one language only |
| A record field a renderer reads directly instead of through `t()` | Content that looks translated because the build reports nothing missing, on a page that is still English |
| A page whose locale rendering is under `MIN_TRANSLATED` different from its source | A URL announcing `lang="fr"` over English prose, with an `hreflang` and a language switch pointing readers at it |
| A `reach` figure with no `as_of` | A hand-copied view count shown undated, which starts lying the moment it drifts |
| A heading level skipped on the way down | A document whose outline says something different from what the page looks like |
| The same word spelled two ways across the built pages | `colorisation` in a page description and `Colorization` in the record it describes |
| A CSS class no markup uses, unless declared in `STAGED_CSS` with a reason | A styled component nothing renders, cited in these documents as though it worked |

Every one of those was added *after* the failure it prevents actually shipped.
That is the pattern to follow: when a claim goes wrong, the fix is a guard in
`tools/` or a shape in the data, not another sentence in this file. Judgement
covers the rest, and a borderline claim goes to the author rather than to a
rule.

What the pitch layer gets is one line per block to be persuasive in (§6). It
does not get to claim what the records below it cannot support, not because a
rule forbids it, but because the third reader checks, and a pitch the evidence
cannot carry is the one failure this site cannot recover from.

## 10. Working agreement

**Pair-programming mode is the default, for every kind of change.**

Visual, structural, editorial, code, data or documentation: the sequence is
the same, and it applies to the whole site, not to whichever section prompted
it:

1. **Analyse the existing implementation first.** Read the fragment, the data,
   the CSS and the model document that owns the rule before forming an opinion.
2. **Challenge constructively and present 2-3 concrete options**, each with its
   trade-off: what it costs, what it gains, what it weakens.
3. **Ask targeted clarifying questions early.** Probe for missing facts, exact
   metrics, problem counts, or ambiguous data before committing to changes.
4. **Discuss and align on architecture with the author.** The author chooses and
   refines the direction.
5. **Only then modify code or documentation.**
6. **Work and close sections incrementally.** Complete one section end-to-end
   (discuss architecture → clarify/fill missing facts → apply changes → rebuild & verify)
   and close it cleanly before starting the next.

**The runnable form of this is [`.claude/skills/rework/SKILL.md`](.claude/skills/rework/SKILL.md).**
This section says what the method is; that file says how to run it, phase by
phase, and carries the lessons each pass has taught. Invoke it with `/rework`,
or just follow it. When a pass teaches something worth not relearning, it goes
in that file's **Lessons** section, not here: this document stays the argument,
the skill stays the procedure.

Two things are unchanged by this:

- **Positioning, claims, numbers, legal status**: always the author's call,
  never inferred: no option list makes one of these safe to decide alone.
- **The two languages move together.** A change to an English record, fragment
  or chrome string is not finished until its French counterpart is changed with
  it. This is not a habit to remember: `tools/build.py` records the English each
  translation was made from and **fails the build** when that English moves,
  and `python3 tools/build.py --sync` is how you say the translation has caught
  up. The rule exists because a stale translation is worse than a missing one.
  A missing string falls back to English and is reported; a stale one reads as
  fluent, confident and wrong, in a language nobody proofreads.

  **The same rule holds at page scale, and it did not used to.** Enough missing
  strings and the fallback stops being a fallback: seven pages shipped as
  English prose under `<html lang="fr">`, each with an `hreflang` telling a
  crawler it was the French rendering and a switch inviting a French recruiter
  to click. The declaration was the lie, not the English. `MIN_TRANSLATED` in
  `tools/build.py` is the guard: below it the page is withheld, its `hreflang`
  is not emitted, the switch does not offer it, and the navigation links to the
  English URL instead, which says `lang="en"` and is English. Raising the
  French coverage is how a page comes back, and the build prints how far each
  one has to go.
- **Trivial, reversible mechanics** (a typo, a rebuild, a dead link, applying
  a decision already taken) do not need an option list. Do them and report the
  diff. Anything a reader would notice does.

## 11. Before you touch anything

- **Records are data.** Edit `src/data/*.json`. The `.html` files at the
  repository root are **generated**, never edit them.
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

  **`build.py` fails first, and on different things.** It raises on an unknown
  template key, a citation naming an id nothing carries, two bullets sharing an
  id, an impact figure absent from the text it cites, and the contradictory
  record shapes in the table in §9. A build that completes has already passed
  those; `check.py` then checks what the markup says.

- **Every page has a model document, and it owns the rules for that page.**
  Read it before changing the page: [`home.md`](home.md),
  [`career.md`](career.md), [`projects.md`](projects.md),
  [`research.md`](research.md), [`writing.md`](writing.md),
  [`teaching.md`](teaching.md), [`workshops.md`](workshops.md),
  [`awards.md`](awards.md), [`skills.md`](skills.md). Contact is the one page
  with no model document yet, which is why it is also the one page carrying
  components [`DESIGN.md`](DESIGN.md) does not know about.

## 12. Where the reasoning lives

| Document | Owns |
|---|---|
| `CLAUDE.md` (this file) | Why the site exists, who it is for, how to work on it |
| [`DESIGN.md`](DESIGN.md) | The visual and structural system, and the intro rule |
| [`awards.md`](awards.md) | The entry metadata convention every page follows |
| [`README.md`](README.md) | How to add each kind of record |
| [`skills.md`](skills.md) | The Skills & Evidence block: the proof model, and the rule it breaks |
| [`home.md`](home.md) | Home: the page that restates, and the three mechanisms that keep it honest |
| [`contact.md`](contact.md) | Contact: the page that asks, and the drift that came of having no owner |
| [`diagrams.md`](diagrams.md) | Architecture diagrams: the container, and why the content is the author's |
| `career.md` · `projects.md` · `research.md` · `writing.md` · `teaching.md` · `workshops.md` | The model for one page each |

**Contact has a model document now, and its absence was the finding.** It was
the newest page, it hand-wrote contact details `src/site.json` already held for
the JSON-LD, and it carried eight component classes [`DESIGN.md`](DESIGN.md)
had never heard of. Those three facts were one fact: the page with no owner is
the page that drifted, and it had, in every direction at once. It listed
`Location: Sfax, Tunisia` directly above the availability sentence, handing a
recruiter the disqualifying half first; its labels disagreed with the data the
structured markup was built from; and its two section classes were
`section.block` and `h2.block__title` under private names, with a hardcoded
`font-size` covering the difference. All of it is now shared components and
generated rows. [`contact.md`](contact.md) owns the rest, including the one
thing still open: `Opportunities & Services` offers consulting, which is in
tension with §3 and is the author's call.

If a rule is worth following twice, write it into the document that owns it.
