# Audit, phase 1: the seven critical fixes

What a hostile audit found, what was decided, what shipped, and the three
things it got wrong. The audit itself is not reproduced here; this is the
record of the pass that acted on it.

Everything below is built and verified: `python3 tools/build.py` and
`python3 tools/check.py` both pass.

---

## Before and after

| # | Finding | Before | After |
|---|---|---|---|
| C1 | French pages published untranslated | 8 URLs at `lang="fr"`, 5 of them byte-identical English, all named by `hreflang` and the language switch | 1 published (Awards, 62% translated). 7 withheld, deleted from disk, named by nothing. Build prints the worklist |
| C2 | Contact led with the disqualifier | `Location: Sfax, Tunisia` above `Availability: EU residence permit holder...` | One row, `Based in`, both strings from `src/site.json`, neither reworded |
| C3 | Career's tenure claim | *"Data Engineer, three years in"* | Unchanged. The audit was wrong, see below |
| C4 | Scale chip overstated scope | `150+ pipelines` (the estate; 20+ were owned) | `20+ of 150+ pipelines`, from `"count": 20, "of": 150` |
| C5 | Nav label did not match page title | nav *Projects* → h1 *Open Source & Projects*, and two more | h1 adopts the nav label on all three |
| C6 | Authoring comments shipped | `index.html` 14.8% comment bytes, including *"INTERIM, awaiting the author's sentence"* | 0.7%, the generated-file banner only. `index.html` 32,343 → 27,546 bytes |
| C7 | Evidence chips landed on block headings | 45 links → 9 destinations | 49 links → 39 destinations |

## Corrections to the audit's own claims

Three, and they matter more than the fixes.

1. **C3 was wrong.** The audit called *"three years in"* contradicted by the
   datelines below it. [`career.md`](career.md) §4 already documents the
   counting rule: paid roles, excluding the two internships, which is
   JACQUEMUS 24 months plus OEM part-time 9 months and rounds to three. The
   number is defensible and was defended in writing before the audit ran. What
   survives is narrower and is the author's to weigh: 9 of those 33 months
   carried the title *Machine Learning & Statistical Engineer*, so the noun
   covers 30 of them. The author chose to keep the sentence. The rule is now
   also a comment in `src/pages/career.html`, so the next auditor finds it
   before reopening this.

   The lesson is the skill's lesson 11 in a new costume: **verify a rule before
   citing it, and read the model document before calling a claim unsupported.**

2. **The audit said the French pages link the English CV.** They link
   `Youssef_BOUTALEB_cv_fr.pdf`, which exists and is git-tracked.
   [`CLAUDE.md`](CLAUDE.md) §8 M4 said otherwise and was the stale party;
   the audit repeated the document instead of checking the build. M4 is
   corrected.

3. **`impact.json`'s unrendered `title` field was called dead data.** It is
   documented in `render_impact`'s own docstring as the record's handle:
   what a build error names. Deliberate, not drift.

## What shipped, in detail

### C1: the translation threshold

`MIN_TRANSLATED = 0.50` in `tools/build.py`. A page is rendered in every
locale, then its visible words are compared against the English it was built
from; under the threshold it is withheld.

Withholding is total, and that is the point. The page is not written, a copy
left by a previous build is deleted, no `hreflang` names it, the language
switch does not offer it, and its navigation entry on a **published** locale
page points at the English URL carrying `lang="en" hreflang="en"`.

That last part is the distinction the whole fix turns on. **The failure was
never the English, it was the declaration.** `/fr/career.html` saying
`lang="fr"` over English prose tells a screen reader to use a French voice and
tells a crawler it has found the French rendering. Sending the reader to
`/career.html`, which says it is English and is, tells the truth. This is
`t()`'s own fallback applied one level up.

Current measurements, printed on every build:

```
  fr: 7 page(s) withheld, under 50% translated:
      career.html      6%
      index.html       0%
      projects.html    0%
      research.html    0%
      teaching.html    0%
      workshops.html   0%
      contact.html     0%
```

0.50 is set where it is because a finished translation still shares proper
nouns, tool names, companies and certificate titles with its source. Awards,
the pilot, measures 62%.

**A bug was found and fixed while building this.** The first version validated
after writing, so a run that failed on a stale translation lock had already
deleted seven pages before returning 1. Validation now runs between the two
passes, while the tree is untouched.

### C7: from 9 destinations to 39

The block's premise was that a claim can be checked in one click. It could not:
sixteen chips went to `career.html#certifications`, twelve to
`career.html#experience`, ten to `teaching.html#courses-taught`. The reader
landed on a heading and searched.

Root cause: **certifications carried no ids.** Career had 21 anchors and not
one of them was a certificate, so the linker had nowhere precise to point.

- Every certification now has a stable short id (`cert-dp-700`,
  `cert-talend-di`) and every issuer group has one (`cert-astronomer`).
  Online-course platforms get group ids (`learn-coursera`).
- All 37 repointable chips moved to the record that proves them. Career bullets
  that already had ids (`jq-finops`, `jq-observability`, `olivesoft-dlq`,
  `oem-speedup`) are now cited directly.
- *Data Engineering 1 & 2* named two courses in one chip and became two chips.
- Three aggregates keep a block anchor because they genuinely have no single
  record: *8 contest results*, *2 Kanboard plugins*, *2 upstream pull requests*.

**`data-toc-skip` was added to the rail parser.** The new ids would otherwise
have pushed eleven issuer and platform names into a Career rail that already
runs to fifteen entries, to repeat what the block heading says. An id is an
address; not every address is a place worth listing. The rail is unchanged at
6 links and 9 sublinks.

## Still open, and author-led

1. **`PowerShell automation` cites nothing.** It renders as a green
   *production* chip and `PowerShell` appears in no bullet in
   `experience.json`. It is the one chip C7 could not repoint, because there is
   no record to point at. Either a bullet or a deletion; both are the author's.
   The block-level anchor was hiding this, which is the argument for C7 in one
   example.
2. **`Architecture & recovery docs`** now points at `career.html#summary`,
   where the claim genuinely appears, but the Summary is prose and not a
   record, so a green production chip is asserting more than a paragraph can
   carry. A bullet on a role record would fix it properly.
3. **The two French `block__intro` lines** on Awards are still literal drafts
   awaiting the author's voice, unchanged from before this pass.
4. **The French translation itself.** The threshold makes the gap visible and
   costs nothing until it is closed; it does not close it.

## Decided against, or out of scope for phase 1

- **Contact rebuilt on `block` / `block__title`.** The h2/h3 split and the
  eight orphan classes are untouched; only the Location row moved. Structural,
  and it belongs with writing `contact.md`.
- **Spelling normalisation.** `colorisation`/`colorization`,
  `containerised`/`containerized`, `Optimisation`/`optimization` all still
  coexist, one pair inside a single page. No guard was added.
- **`block__note`, `tag--accent`, `tag--honor`, `tag--neutral`,
  `medal--bronze`** are still dead CSS and still only a `check.py` note.
  `block__note` being unused means the provenance rule CLAUDE.md §6 describes
  is documented, styled, and implemented nowhere.
- **`tag--critical` rendering crimson for a `.pptx` download**, and
  `tag--upstream` covering both an accepted PR and a hosted demo.
- **`site.contact_invitation`** is still referenced nowhere in the repository.
- **The `<details>` rail shipping `open=false` on desktop** while CSS forces it
  visible, so assistive tech is told a painted region is collapsed.
