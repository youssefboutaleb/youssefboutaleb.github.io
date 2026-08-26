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
   Selected Impact used `.entry`, which is for a dated record living on its own
   page. That one decision produced the topic-as-title, the repeated dateline,
   the figure demoted to a chip and four identical `Career` tags. Findings that
   all trace to one component choice are one finding.
7. **Renumber and re-check after inserting a stylesheet section.** Adding
   `13. COMPONENT: RESULT` silently produced two section 13s.
8. **Check `href` targets exist before writing them.** `build.py` fails on a
   citation naming an id nothing carries, which is faster than being told.

---

## Upgrading this file

When a pass teaches something a future pass would repeat: add it to **Lessons**
with the specific case that taught it, in one or two sentences. Keep the phases
stable. If a phase genuinely needs to change, change it and say so in the
message, because the author is the one who has to keep trusting the method.

No dashes in this file either. `check.py` reads it.
