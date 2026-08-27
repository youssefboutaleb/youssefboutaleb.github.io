# The French version

`CLAUDE.md` M4. The mechanism is built and Awards is translated end to end as
the pilot; the remaining prose is author-led. This is what was measured, what
was decided, and what the pilot taught that the plan had not predicted.

Third in the series with [`theme-options.md`](theme-options.md) and
[`sidebar-options.md`](sidebar-options.md).

---

## What the scope actually is

Measured, not estimated.

| | Words | Who |
|---|---|---|
| `points`, the record bullets | 2,220 | author |
| Page fragments (headings, intros) | 1,742 | author |
| `summary` | 644 | author |
| `impact`, `text`, `description` | 332 | author |
| Fields needing a ruling | 862 | author |
| Chrome, tags, months, units | ~150 | done |
| Names, tech, URLs, ids | 359 | stay English |

**Roughly 5,000 words of author prose**, which is why the pilot exists: the
engineering is finished and the rest is translation that can happen at any
pace, with the build reporting what is still missing on every run.

## The four things that were going to bite, and did

Named during scoping, before any code was written. All four were real.

1. **The chrome is not free.** 28 user-facing English strings lived in
   `tools/build.py`, not in the data: eight aria-labels, the skill standings,
   link titles, `MONTHS`, `ONGOING`, and `tenure()` building `"2 years 3 months"`
   with English pluralisation. They are `tr()` calls now, with English as the
   fallback default so nothing changed for the English build.

2. **Ids must not be translated, and it is load-bearing.** `impact.json` cites
   bullets by id, `skills.json` carries 40 citation targets, and the page
   context rail anchors on the same strings. Ids are now stamped once by
   `with_ids` from the **English** source field, before anything renders, and
   the seven renderers that each derived their own read `record["id"]` instead.
   The refactor was verified by rebuilding and diffing: **byte-identical
   output**, which is the only way to be sure a rename of this kind changed
   nothing.

3. **The impact-figure guard versus French numbers.** Still open, see below.

4. **The French CV.** Resolved during the pass: the French pages now link
   `data/Youssef_BOUTALEB_cv_fr.pdf`. The file itself is still a byte-identical
   copy of the English one, so the wiring is done and the document is not.

## What was decided

| Decision | Why |
|---|---|
| **Sidecar overlay**, `src/i18n/fr.json` keyed `<id>.<field>` | Data files untouched, English stays the source, citations and anchors keep working. Rejected: inline `{"en":…, "fr":…}` pairs (every file doubles in noise, 11 renderers change) and per-locale data directories (M4 rules it out: it forks the content model) |
| **`/fr/` subdirectory** | Standard, keeps every existing URL working. Chosen without asking: the alternative bought nothing |
| **Whole-fragment translation** for page prose | A heading and a `block__intro` are sentences with markup threaded through them. Keying those by id produces an overlay nobody can read and a translator cannot work in |
| **Fallback to English, never to a hole** | A half-translated page is readable and an empty one is not. Only defensible because the gap is reported on every build |
| **Links, not buttons**, for the language switch | Each language is a real page at a real URL, so it is navigation and needs no script. `DESIGN.md` §12.1 |

Staying English, on the author's ruling: certifications, degrees, employers,
tech stack, paper titles. Declared as `keep` patterns so the missing-strings
report stays worth reading. The **metadata tag vocabulary is translated**, which
was the author's call against the cheaper option.

## What the pilot found that the plan did not

This is the part that justifies piloting one page before committing 5,000 words.

- **Enumerating ordinals is not a design.** The overlay first carried
  `placement.1`, `.2` and `.3`. The French page then rendered **"13th Place"**
  and **"643rd Place"** in English, because nothing supplied `placement.13` and
  `placement.643` is not a string anyone would write. Ordinals are a rule per
  language now (`{"1": "1re", "other": "{n}e"}`), and the phrase around them is
  a separate pattern, because two different things vary and neither is a suffix.

- **Thousands separators are language.** `7,094 teams` must be `7 094 équipes`
  in French, with a narrow no-break space (U+202F). `Locale.number()` owns it,
  and the stored integer is never touched.

- **Punctuation spacing is language.** French sets a narrow no-break space
  before a colon. `Theme:` was hardcoded in the layout with the colon outside
  the translatable string, which made `Thème:` unavoidable. The label owns its
  own punctuation now.

- **`<html lang>` shipped as `en` on the French pages.** The locale's `lang`
  went into `Locale.lang` but never into the template context. It is the one
  metadata error a translation cannot survive: it tells a screen reader which
  voice to use and a search engine which audience to serve.

- **Every asset path 404'd on the French pages**, and `check.py` caught all 24.
  `images/icons/*.svg`, `data/DP-*.png` and the portrait were emitted as
  root-relative literals inside `build.py`, which resolve wrongly from `/fr/`.
  There is an `asset()` helper now. Links *between* pages needed nothing:
  `awards.html` from inside `/fr/` already means `/fr/awards.html`, which is
  the French page, which is what was wanted.

  Worth noting that this was found by extending `check.py` to the new pages
  before looking at anything by eye. A locale nobody proofreads is exactly
  where a broken image survives.

## Guards added

| The build now refuses | So this cannot happen |
|---|---|
| A translated fragment missing an anchor the English one has | A citation or a rail entry pointing at nothing, in a language the author does not proofread |
| A translated fragment missing a `{{ build.* }}` block | A whole block of records silently absent from one language |
| A translated fragment carrying an anchor the source does not | Two languages disagreeing about what the page contains |

And on every build, not as a failure: **the count and the names of untranslated
keys, per locale.** Currently 49, all outside Awards.

## The synchronisation guard

Added on the author's instruction that the two languages move together from
now on. A sentence in a document would not have held it, so it is a guard.

**The gap it closes is not the obvious one.** The fallback in `t` already
covered a string that was never translated, and the build already counted
those. Nothing covered the opposite and worse case: a string translated once,
then edited in English, where the French keeps saying the old thing with no gap
for anyone to notice. Two pages then disagree about a figure in a language the
author does not proofread.

`src/i18n/<code>.lock.json` records a fingerprint of the English each
translation was made from. A mismatch is **fatal**, not a warning, because a
stale translation is not less complete than a missing one, it is wrong.
`--sync` re-stamps and is how the author says the translation has caught up.

Verified by breaking it on purpose: editing `4h` to `3h` in an English bullet
whose French said `4 h` failed the build and named the key; updating the French
and re-stamping cleared it. Both `build.py` and `check.py` exit 1.

**One bug this test found immediately.** `load_locales()` globbed
`src/i18n/*.json`, so it discovered `fr.lock.json` as a language called
`fr.lock`, built a site at `/fr.lock/`, and wrote `fr.lock.lock.json`, which it
then discovered as `fr.lock.lock`. One build produced **48 pages across five
imaginary languages**. Lock files are excluded from the glob now. It is the
clearest argument in this document for testing a guard by triggering it rather
than by reading it.

---

## Still open, and author-led

- **~5,000 words**, listed by the build. Suggested order: Contact and Home
  first (shortest, highest traffic), Career last (densest).
- **The two `block__intro` lines on the French Awards page are literal drafts**
  and are marked as such in `src/i18n/fr/pages/awards.html`. They are pitch
  lines and `CLAUDE.md` §6 makes them the author's voice: they need rewriting,
  not reviewing.
- **The impact-figure guard.** `build.py` fails when a Selected Impact figure
  is absent from the bullet it cites. The figure is `&euro;1,400`; a French
  bullet would naturally say `1 400 €`. Home is not translated yet so it has
  not fired, and it will the moment `impact.json` and `experience.json` are.
  The fix is for the guard to compare figures per locale, and it should be
  written when the first French bullet needs it rather than guessed now.
- ~~No French CV.~~ **Wired**: the French pages link
  `data/Youssef_BOUTALEB_cv_fr.pdf`. **The file is currently a byte-identical
  copy of the English CV** (same MD5), so the French pages serve English
  content under a French name until a real translation replaces it.
- **Unseen.** Nothing here has been opened in a browser: no headless browser in
  this environment. The pages build, pass every check, and carry correct
  `lang`, `hreflang` and asset paths, which is not the same as looking right.
