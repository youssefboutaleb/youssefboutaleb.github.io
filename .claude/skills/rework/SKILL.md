---
name: rework
description: The working method for changing anything on this site: investigate the existing implementation, name the root cause, put 2-3 costed options and a recommendation to the author, ask with AskUserQuestion, then build, verify, propagate to the documents and record the outcome. Use for any visual, structural, editorial, data or copy change to a page, block or component, and whenever the author says a section is not good, not well designed, badly positioned, or asks to upgrade, rebuild, enhance or investigate one.
---

# Rework

The executable form of [`CLAUDE.md`](../../../CLAUDE.md) §10. That section says
what pair-programming mode is. This says how to run it, and it accumulates what
each pass taught.

**Do not skip phases to be helpful.** Skipping the investigation is how a
symptom gets patched and the cause survives. Skipping the questions is how the
author's positioning gets decided by an agent.

---

## The three things that are never yours

1. **Claims, numbers, positioning, legal status.** Titles, metrics, proficiency
   levels, residence and work authorisation, what role is being targeted. No
   option list makes one of these safe to decide alone.
2. **Generated files.** Root `*.html` is build output. Records are
   `src/data/*.json`. Headings and intros are `src/pages/*.html`.
3. **New claim prose.** You may retire a sentence, move it, or derive it from
   data. Writing a new sentence that asserts something about the author is
   theirs.

Everything else is in scope, including deleting things.

---

## Phase 1: ground yourself before forming an opinion

Read, in this order, and do not propose anything until you have:

- [`CLAUDE.md`](../../../CLAUDE.md): why the site exists, the three readers,
  the rules deliberately broken, the voice map, the dash ban.
- The **model document that owns the page**: `home.md`, `career.md`,
  `projects.md`, `research.md`, `writing.md`, `teaching.md`, `workshops.md`,
  `awards.md`, `skills.md`. Contact has none, which is itself a finding.
- [`DESIGN.md`](../../../DESIGN.md) for the components involved.
- The actual implementation: the fragment, the data file, the renderer in
  `tools/build.py`, and the CSS rule.

**The model document may argue against the change you are about to propose.**
That is not a blocker, it is context. If you overrule it, say so explicitly and
record both the old argument and why it lost. A documented decision reversed
knowingly is fine; one reversed silently is not.

## Phase 2: investigate

Gather evidence, not impressions. A finding is only worth reporting if you can
point at something.

- `grep`/`sed` the CSS, the renderer and the data. Quote `file:line`.
- **Measure.** Column widths, character counts, `--measure` in `ch` at the
  relevant font size, image dimensions. "It looks cramped" is not a finding;
  "the value runs 740px under a lede capped at 630px" is.
- **Look at images** with the Read tool before deciding a crop.
- **Check the whole site, not one directory.** A fact you cannot find in
  `src/data/` may be sitting in a page fragment. This has already cost one
  wrong conclusion.
- Check inbound links (`grep -rn "#anchor"`) before proposing to delete a
  section.

## Phase 3: find the cause, not the symptoms

Group findings that share a cause and say so. The best change removes a
surface; the worst reworks one instance of it.

Two examples from this site:

- Home's duplicated prose and duplicated credentials looked like two bugs. They
  were one: two blocks competing to introduce the same person. Merging removed
  it; rewording either one would not have.
- The Languages line's merged "English and French" looked like a wording
  problem. The cause was that a middot cannot both divide a list and bind each
  item to its value, so the fix was a grid, not a better sentence.

## Phase 4: options, 2-3, each costed

Every option gets three lines, and the third is the one that keeps you honest:

- **Costs**: work, what breaks, what has to move.
- **Gains**: which numbered findings it closes.
- **Weakens**: what gets worse. An option with nothing in this line is
  described dishonestly.

Include the cheap repair-in-place option even when you will not recommend it,
so the author can see what they are paying for.

## Phase 5: recommend, and answer the strongest objection

State one recommendation plainly. Then find the best argument against it,
usually a rule in `CLAUDE.md`, and answer it in the open rather than hoping it
goes unnoticed.

> §1 says length is not a defect and the site holds what the CV had to cut. It
> does not say every fact deserves a block. Three proficiency ratings are not
> depth.

## Phase 6: ask

Use `AskUserQuestion`. One question per genuine fork, at most four.

- Recommended option **first**, labelled `(Recommended)`.
- Use `preview` for anything visual or textual: ASCII mockups of the before and
  after, competing wordings, layout sketches. The author decides with their
  eyes.
- Never ask what you can verify yourself. Measure it instead.
- Never ask "shall I proceed".
- Questions that depend on an answer you do not have yet go in a later round,
  not into a guess.

## Phase 7: build only what was decided

- Do everything that does not depend on an open question.
- If an answer collides with something (a chosen wording that will not fit a
  chosen layout), **say so and resolve it visibly**, do not silently pick.
- **Dead code created by the change is deleted in the same pass**, not left for
  `check.py` to note. A component that loses its last user goes, along with its
  stylesheet section, its contents entry, and its section number.

## Phase 8: verify

```sh
python3 tools/build.py && python3 tools/check.py
```

`build.py` fails first and on different things (unknown template key, citation
naming a missing id, duplicate bullet ids, an impact figure absent from the
text it cites). `check.py` then checks the markup, the CSS agreement, the
links, the build drift and the dash ban across every file.

Then **read the rendered output**. `sed -n` the block out of the built page and
look at it. Passing checks is not the same as being right.

Say plainly what you could not verify. There is no headless browser here, so
layout is reasoned from metrics, not seen, and that gets stated rather than
implied.

## Phase 9: propagate

A change that leaves the documents describing the old site has not landed. In
one pass, update every file the change invalidates:

- The page's model document (the rules, the block order, the reader table).
- `DESIGN.md` if a component, token, section number or responsive rule moved.
- `README.md` if the way to add a record changed.
- `CLAUDE.md` if a roadmap item advanced or an example it cites is now stale.
- The comments in `tools/build.py` and the CSS section headers.

`grep -rn` the old class or field name afterwards and clear every hit.

## Phase 10: record the outcome

Append to the options document, in the repository root, named
`<area>-options.md`:

- A before/after table.
- **Every correction you made to your own earlier claims**, plainly.
- What was decided but not built, and why.
- What is still open and author-led.

The next agent reads this file, not the transcript.

---

## The quality bar

| Not a finding | A finding |
|---|---|
| "The hero looks dated" | "The `h1` is 25px, the same size as the brand-bar name 40px above it" |
| "Too much text" | "The lede and the Profile paragraph both name Azure, ETL/ELT, integration and observability, in that order" |
| "Should be more consistent" | "`\|` appears in the `h1` and nowhere else in the repository; `&middot;` is the documented separator" |
| "Add evidence" | "This is the only block on the page with no link, no record and no tag" |

---

## Lessons, and where they came from

Append here every pass. This is the part that makes the file worth keeping.

1. **Look outside `src/data/` before calling a claim unverifiable.** The
   Languages intro was retired as unsupported; `src/pages/teaching.html` had
   been stating the instruction language in its spec strip all along.
2. **A rule that quotes what it forbids becomes the permanent false positive
   of the search that enforces it.** `CLAUDE.md`'s dash ban printed all four
   banned forms. It names them by codepoint now, and `check.py` enforces it.
3. **Grouping to make something fit is a layout failure, not an edit.** Two
   languages were merged onto one line because the level printed twice was too
   long. The line was wrong, not the content.
4. **Ask about the format and the content together.** Approving LinkedIn's
   wording and a one-line layout separately produced a combination that did not
   fit.
5. **The literal reference is rarely the right borrow.** andrewng.org puts the
   photograph above the text at column width. Copied here it would push the
   claim below the fold, so the treatment was taken and the placement was not.
6. **A component borrowed from the wrong job creates every symptom at once.**
   Impact in Numbers used `.entry`, which is for a dated record living on its own
   page. That one decision produced the topic-as-title, the repeated dateline,
   the figure demoted to a chip and four identical `Career` tags. Findings that
   all trace to one component choice are one finding.
7. **Renumber and re-check after inserting a stylesheet section.** Adding
   `13. COMPONENT: RESULT` silently produced two section 13s.
8. **Check `href` targets exist before writing them.** `build.py` fails on a
   citation naming an id nothing carries, which is faster than being told.
9. **A summary that hand-formats its own labels drifts in three directions at
   once.** Awards' header strip wrote `f"{gold_count}st Place Regional"`, which
   fused two tag categories, would have printed *2st* on a second gold, and
   invented three chrome strings that then rendered in English on the French
   page. Rebuilding it through `meta_label`, the function that renders the tags
   on the records below, made the wording, the medal, the bold figure and the
   French all correct for free. **Derive a summary through the renderer the
   records already use, never through a format string.**
10. **Deleting a component can falsify a stylesheet section header, which is
    lesson 7 in the other direction.** `.awards-stats` went and `.hero-facts`
    stayed in a section headed `(HOME ONLY)` that Awards had just stopped
    making true. After removing or moving a rule, read the section header and
    the comment above it, not only the rule.
11. **Verify a rule before citing it, even one written in `DESIGN.md`.** I
    quoted §9.3's *"entries are still never boxed"* to argue against a boxed
    strip, having already grepped up `.entries--grid > .entry`, which boxes
    Career's credential cards. A documented rule can be stale, and an
    undocumented component (that grid) is exactly how it gets that way. One
    grep would have caught it: check whether the repository agrees with the
    document before you quote the document at the author.
12. **Ask the claim question and the design question in the same round.** The
    author said "I am also an African finalist" while the data said
    *Quarter-finalist*. That is a factual correction to make or decline, not a
    wording preference, and it is `CLAUDE.md` §5 territory. Putting it beside
    the component choice cost one question and settled it before anything was
    built.

13. **Read the model document before calling a claim unsupported.** An audit
    reported Career's *"three years in"* as contradicted by the datelines
    below it. `career.md` §4 already said the count is paid roles minus the two
    internships, which is exactly what the records show. The finding cost a
    question that did not need asking, and the fix was a comment pointing at
    the rule rather than a change to the page. Lesson 11 said to check the
    repository before quoting a document at the author; this is the same
    lesson pointing the other way, and both directions cost a pass.
14. **A fallback that is fine for a string can be a lie at page scale.** A
    missing French string falls back to English and is reported, which is
    right. Enough of them and the page is English while `<html lang="fr">`,
    the `hreflang` and the language switch all still announce French. The
    quantity changed what the mechanism *was*. When a graceful degradation is
    introduced, ask what it looks like at 0%, not only at 90%.
15. **Validate before you write, not after.** The translation threshold
    deleted seven withheld pages in pass 2, then hit a stale-translation
    failure and returned 1: a build that reported doing nothing had already
    removed seven files. Every check that can fail the build has to run while
    the tree is still untouched.
16. **An id is an address, and not every address is a place worth listing.**
    Adding anchors so Home's evidence chips could name one certificate instead
    of the whole block immediately pushed eleven issuer names into Career's
    rail. `data-toc-skip` separates the two jobs. A new anchor is a rail entry
    by default, and usually should not be.
17. **Removing state beats making state honest.** The rail's `<details>` was
    forced open by CSS on desktop while the element stayed closed, so it
    reported itself collapsed while painting its contents. The obvious fix was
    to emit `open` and close it with CSS on small screens. The better one was
    to notice the disclosure only existed because the tree went three levels
    deep, cap the tree, and delete the control. Ask what the control is *for*
    before fixing how it behaves.
18. **Set the element default to what the component already renders.**
    Retagging every section and record heading on the site could have been a
    visual redesign by accident. Writing the new `h2/h3/h4` sizes and colours
    to exactly what `.block__title` and `.entry__title` were already producing
    meant the outline changed and the rendering did not, and no component rule
    had to be touched. A component overriding its own element's default is the
    warning sign that the tags are wrong: `.contact-section__title` hardcoded
    `--text-xl` on an `h2` for exactly that reason.
19. **A guard is fatal only when the data to satisfy it exists.** `check_reach`
    fails the build over a missing `as_of` because the figures were read on
    some date and the author knows it. The undated in-progress paper gets a
    report instead, because a submission date is a fact only the author has,
    and a guard that fails the build over data nobody can supply is a guard
    the next person deletes.
20. **Two passes of audit, five corrections to the audit.** Lesson 13 fired
    again: the Awards summary's "broken parallelism" was a documented rule in
    the renderer's own docstring, and the job-summary finding was answered in
    `career.md` §5. Before reporting that a rule is missing, read the function
    that implements it and the document that owns it. Findings that survive
    that check are worth acting on; the rest cost a question each.
21. **A mechanism is not landed until it reaches the content.** `CLAUDE.md`
    M4 said "mechanism landed, translation open" for months. The overlay
    addressed records by id, and ten of twelve renderers read `record[...]`
    directly, six data files had no ids, and `t()` never reported a list as
    missing, so the build cheerfully reported 61 missing strings for a site
    with 3,250 untranslated words. **The absence of reported work is not
    evidence that the work is small.** Before trusting a coverage number, check
    that the thing producing it can see what it claims to measure.
22. **A guard written for one locale will fire on another.** `check_figure`
    asserts a hand-written figure appears in the prose it cites; in French,
    `1 400 EUR` does not contain `&euro;1,400` and `zéro` does not contain
    `Zero`. The fix was to make the figure translatable so the check compares
    like with like, not to weaken the check. Likewise the new spelling audit
    reported the correct French `vectorisation` against the correct English
    `vectorization`, and had to be scoped to the source locale.
23. **Sharing a component's name is not sharing its settings.** Contact was
    given `section.block` and `h2.block__title` in an earlier pass and the
    finding was recorded as closed. Its channel list still carried no measure
    cap, ruled its rows on the wrong edge, right-aligned its values and used a
    different label width and row padding from the label column stacked 40px
    above it on the same page. Renaming a component to the shared name fixes
    the vocabulary and touches none of the numbers. After adopting a shared
    component, diff its declarations against the thing it now claims to be.
24. **Measure the labels before proposing to align the columns.** The obvious
    fix for two label widths on one page is to pull the wider one down to the
    narrower. `fontTools` on the shipped font said `Consulting & services` is
    141px and the French `Telephone / WhatsApp` is 150px against a 120px
    column, so the reconciliation had to go the other way and cost a change to
    Home. That reversal is a question for the author, and it only exists if the
    measurement happens before the option list, not after.
25. **The reference's structure can be right and its content wrong for you.**
    andrewng.org routes each purpose to the address that serves it, which is
    the shape this page seemed to want. It works there because the five
    purposes reach five different organisations. All three addresses here reach
    one person, so the same structure would have invented a distinction and
    delayed the recruiter. Lesson 5 said the literal reference is rarely the
    right borrow; this is the version where the borrow is structurally sound
    and still fails on the data.
26. **The quality-bar table is a bug list nobody was reading.** This file has
    cited *"the `h1` is 25px, the same size as the brand-bar name 40px above
    it"* as its model of a real finding since it was written, and the h1 was
    still 25px. An example good enough to teach with is usually a defect good
    enough to fix. Read the examples in this file as a to-do list once.
27. **Fetch the reference's numbers, do not infer them from the screenshot in
    your head.** andrewng.org turned out to be 72px against a 14px body, a
    ratio of 5.14, and Tufte CSS 48px against 21px, a ratio of 2.29. Those two
    numbers are what turned "how big should the title be" from taste into a
    decision, and neither was guessable. `curl` the page and `curl` the
    stylesheet.
28. **A token with two users cannot be raised.** The page title and the brand
    bar shared `--text-2xl`, so every proposal that started "make the h1
    bigger" was really "separate these two first". When a change to one value
    seems to have an unreasonable blast radius, count the users of the token
    before designing around it.
29. **A rule that keeps needing an exception is usually a rank error.**
    Teaching's `block__intro` stated an appointment, not a pitch, and two
    passes narrowed the exception without removing it. The sentence was fine;
    it was one rank too low. Moved into the page header as a `.page-lede` it
    became simply correct and `DESIGN.md` lost its last declared exception.
    Before bending a rule for a stubborn case, check whether the content is in
    the wrong slot.
30. **"Add X to every page" is a request to check what every page already
    has.** Asked to apply page ledes to seven pages, the finding was that six
    of them already opened with a sentence one heading down, and that a lede
    had been *deliberately deleted* from the seventh for exactly that reason.
    The answer was to promote three sentences and write none. Grep the thing
    you are about to add before adding it: the site had already solved most of
    it at a different rank.
31. **When a model document contradicts itself, the page is already broken.**
    `awards.md` rule 7 said to store raw facts and let the renderer label them;
    its bullet rule three sections later mandated the hand-written string
    `Solved 8 / 8 problems in 4h (Team of 2)`. The result was one page printing
    `4h` in bullets and `48 h` in a tag, and the two languages disagreeing about
    the format of the same figure. Read the whole model document before
    proposing a change to one section of it: the rules that conflict are the
    change.
32. **Grep the codebase for the argument before writing it.** The comment on
    `duration` in `meta_label` already said, in the author's words, exactly why
    the awards bullets were wrong: *"a value formatted at the call site is a
    value that drifts from every other call site."* Quoting the repository back
    to itself is worth more than a fresh argument, because it shows the rule
    was already agreed and only unenforced.
33. **Parse the old prose, do not retype the numbers.** The seven welded
    sentences were converted with a regex that pulled solved, total, hours and
    team out of each string and failed loudly on anything that did not match.
    Retyping 28 integers by hand out of a terminal is how a 6 becomes an 8 in
    one record and nothing catches it.

---

## Upgrading this file

When a pass teaches something a future pass would repeat: add it to **Lessons**
with the specific case that taught it, in one or two sentences. Keep the phases
stable. If a phase genuinely needs to change, change it and say so in the
message, because the author is the one who has to keep trusting the method.

No dashes in this file either. `check.py` reads it.
