# Volunteering

What was wrong with the block, what was decided across two passes, and the
facts still missing. The model now lives in [`career.md`](career.md) §8, which did not
exist before this pass; this is the record of how it got there.

---

## The finding, measured

Volunteering was **the only `.entry` on the site with no id, no tag and no
link.** Counted across Career's six blocks:

| Block | Links | Tags | Record ids |
|---|---|---|---|
| experience | 4 | 41 | 4 |
| education | 3 | 5 | 2 |
| certifications | 10 | 0 | 0 |
| courses | 10 | 0 | 0 |
| **volunteering** | **0** | **0** | **0** |

Certifications and Online Courses carry no tags by design (`career.md` §3), but
ten links each. Volunteering carried nothing checkable at all.

**The missing id was the expensive one, and one of its costs was new.** It kept
the record out of the page context rail (the heading appeared with nothing
under it), out of reach of any citation, and **out of reach of the translation
overlay**, which addresses records by id. It was the one record on the site
that could never be synchronised between the two languages, four days after
that became a rule with a build guard behind it.

**It was also the only record type storing a free-text `period`.**
`"COVID-19 response"` where `experience` and `education` store `start` and
`end`. `career.md` §4 is titled *"Periods are derived"*. The string is a topic,
not a period: no year, no duration, no sort order.

**And the prose said the same fact three times before its first new word.** The
summary opened *"Volunteered during the COVID-19 crisis"*, under a heading
reading *Volunteering*, above a period reading *COVID-19 response*.

`career.md` had eight sections and none of them owned this block. Third
instance of the same pattern this week, after Contact and the page context
rail: **the page with no model document is the page that drifted.**

---

## What was decided

**Fix the mechanics, keep it modelless.** Chosen over adding a metadata model.

The argument for staying tagless is register, not effort: a chip row reading
*Crisis response &middot; Regional &middot; 4 months* over aid distribution
during a pandemic reads as credential-farming, and that is the one tone this
block cannot survive. Its value is that it is the least self-interested thing
on the site.

**The two answers pulled against each other**, and the collision was resolved in
the open rather than picked silently: modelless was chosen, *and* more
volunteering records are coming. So the record is built so a model is purely
additive later, and `career.md` §8 states the condition for reopening the
question: **a second record**, so there is something to compare. A model exists
to make records comparable, and one record compares to nothing.

## What changed

| | Before | After |
|---|---|---|
| id | none | `vol-tunisian-red-crescent`, stamped by `with_ids` |
| In the rail | heading only | heading and record |
| Translatable | **no** | yes, and translated |
| Link | none | `url` supported, still empty (see below) |
| Period | `"COVID-19 response"` | moved to `initiative` in the second pass; `year` or `start`/`end` hold dates |
| Prose | one 36-word sentence, four gerund clauses | two bullets, same four facts, opener dropped |
| Model document | none | `career.md` §8 |

The bullets say exactly what the sentence said. Nothing was added: the four
clauses became two lines and the *"Volunteered during the COVID-19 crisis"*
opener was dropped because the heading and the period already carried it.

## A correction made mid-pass

**I invented a URL for the Tunisian Red Crescent and removed it before it
shipped.** The renderer needed a link and I wrote a plausible-looking address
without opening it. That is precisely the failure this site is built against:
`DESIGN.md` Principle 3 wants a link to where a claim can be checked, and a
guessed link is worse than no link because it looks like one. `url` is
supported and empty, and it stays empty until someone supplies an address they
have actually opened.

## The second and third records, and what they settled

JID (Orientini, 2022 and 2023) arrived two days after the model question was
deferred with a stated condition on it: **a second record, so there is
something to compare.** The condition was met, the question was asked again,
and the answer held.

**Still no tags.** Two editions of a student orientation event beside a
pandemic relief effort do not need a chip to tell them apart: the organisation,
the initiative and the bullets already do. A chip would add only the tone §8
argued against.

**What the pair revealed instead was a missing field, which is the better
finding.** Both records happened under a named programme, and there was nowhere
to put it, which is exactly why the Red Crescent record had been keeping
*"COVID-19 response"* in `period`. `initiative` renders on the dateline joined
to the year with a middot, the shape `render_experience` already uses for
`Location &middot; Period`, so it needed no component, no class and no CSS.

**One record per edition**, following the convention the site already had:
TCPC 22 and TCPC 23 are two award records, not one saying "2022 and 2023". That
forced `ID_RULES` to accept a tuple, since `organisation` alone is no longer
unique.

### Two bugs this surfaced

- **`slugify` did not fold accents.** *Jeunes Ingénieurs de Djerba* produced
  `vol-jeunes-ingénieurs-de-djerba-jid-2023`, with the accent inside an anchor
  that gets pasted into citations, rail links and overlay keys. This was the
  accent problem predicted during the i18n scoping, arriving from an **English**
  record rather than from the French overlay, which is not where it was
  expected. Folding is a no-op for every id that existed before it.

- **A false alarm, and the more useful lesson of the two.** Home's *Currently*
  block had a `tag--neutral` link reading *"Full role on Career"*, and it was
  gone. The only symptom was `tag--neutral` appearing in `check.py`'s "css
  classes with no markup using them" note. It looked like collateral from this
  session's edits to `build.py`, and it was restored on that assumption.

  **It was not collateral. It was deliberate, and the restoration was wrong.**
  `home.md` had lost exactly the paragraph documenting that tag, six deletions
  and no additions, in an edit nothing in this session made. Code and its
  documentation removed together is a decision, not a slip. The restoration was
  reverted and the orphaned French string removed with it.

  The lesson is not about the tag. **An unused CSS rule is evidence of a
  change, not evidence of a bug**, and the difference is whether the
  documentation moved with the code. Checking `home.md` before "fixing"
  `build.py` would have answered it in one command. `tag--neutral` now sits in
  the unused note, where it belongs until someone deletes the rule or brings
  the tag back.

---

## Still open, and author-led

Both are facts only the author has, and neither can be worked around by writing
better sentences.

- **The dates.** Roughly which months of 2020 or 2021. `render_volunteering`
  already prefers `start` and `end` over `period`, so this is a data change and
  nothing else. Until then the record is **honestly undated rather than
  dishonestly dated**, which is the right way round but is still a gap.
- **A number, or the explicit absence of one.** Weeks active, shifts, people
  served, households supplied. Any single real figure changes this block from a
  description into a record. If there is none the author can stand behind, that
  should be a stated decision rather than an oversight, because `CLAUDE.md` §5
  is explicit that this site shows what has not landed rather than hiding it.
- **The organisation link**, per the correction above. Now three links, not
  one: the Red Crescent branch, JID, and Orientini if it has a page of its own.
- ~~The second record, which reopens the model question.~~ **Answered**: it
  arrived, the question was asked again, and the model still is not warranted.
- **What JID's official name actually is.** The record reads *Jeunes Ingénieurs
  de Djerba (JID)*, normalised from the author's own *"jeune ingeneure djerba"*.
  The expansion is theirs, the spelling and agreement are not, and an
  organisation's own styling is not something to infer.
- **What Orientini is**, precisely: JID's own event, or a national programme JID
  takes part in. The bullets read differently depending on the answer.
- **What differed between 2022 and 2023.** The two records currently carry an
  identical bullet, which is honest if the work was identical and reads as
  padding either way. One fact separating them fixes it; if nothing separates
  them, that is worth knowing too.
