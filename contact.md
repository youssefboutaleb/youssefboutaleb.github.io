# Contact

The model for [`src/pages/contact.html`](src/pages/contact.html).

This document exists because its absence was the finding.
[`CLAUDE.md`](CLAUDE.md) §12 named Contact as the one page with no model
document, the one hand-writing details `src/site.json` already held, and the
one carrying component classes [`DESIGN.md`](DESIGN.md) had never heard of, and
said those three facts were one fact: **the page with no owner is the page that
drifted.** They were. This is that document.

---

## 1. What the page is for

**The only page that asks the reader to do something.** Every other page
answers *is this real*. This one answers *how do I start the conversation*, and
[`CLAUDE.md`](CLAUDE.md) §2 says success is a first interview, so this is the
page the whole site is arranged to make somebody reach.

That gives it one job and a short one. It is not a summary of the site, it does
not restate a claim, and it carries no evidence: everything on it is an address
or a statement of what is being looked for.

## 2. The components are the site's, and they used to not be

Contact runs `section.block` and `h2.block__title` like every other page.

It did not. It had `.contact-section` and `.contact-section__title`, which were
those two components under private names, and the title hardcoded
`font-size: var(--text-xl)`, 19px at the time, so that an `h2` would render at
the size the rest of the site gets from its section heading. (Both numbers have
since moved: [`DESIGN.md`](DESIGN.md) §1.) One visual rank spelled two ways,
with the stylesheet correcting the difference so that nothing, and nobody,
could see it was there. Both classes are deleted.

**`.contact-list` stays, and is the one genuinely local component.** A quiet
label naming a channel, its address beside it. It is the label-column idiom
[`DESIGN.md`](DESIGN.md) §11 names and three other blocks use. Keep it; do not
reinvent it as a definition list, because these are choices a reader acts on
rather than terms being defined.

**Being the site's component was not the same as being set like one.** Sharing
a name with `section.block` fixed the vocabulary and left the settings alone,
and this page stacks `.hero-facts` and `.contact-list` about 40px apart, so
every divergence between them was visible in one glance. There were four:

| | Was | Is |
|---|---|---|
| Measure cap | None: rows ran the full 908px content column while the strip above stopped at 611px, so the page had two right edges | `max-width: var(--measure)`, one right edge |
| Value alignment | `text-align: right`, the only right-set value in the idiom | Flush left, like every other one |
| Row rule | `border-bottom`, leaving a hairline under each block's last row a row's height above the next heading's underline | `border-top` with the first row reset, like `.hero-facts`, `.skill` and `.result` |
| Rhythm | 10rem label and `--space-4` padding against the strip's 7.5rem and `--space-3` | 10rem and `--space-3` on both, collapsing together at 600px |

**The label column was reconciled upward, not down.** 7.5rem is 120px and
`Consulting & services` measures 141px, the French `Telephone / WhatsApp`
150px, so the strip is what moved. The reconciliation is **10rem, and it is
this page's**: it is the width `.hero-facts` and `.contact-list` can meet at
when they are stacked 40px apart, which happens here and nowhere else.

**It no longer travels to Home, and that is the rule working rather than
breaking.** This paragraph used to end by noting that the change widened Home's
hero strip by 40px as a side effect. Home has since put its own label columns
on `--spine` (13rem), so the strip there takes the width of the `.result` and
`.skill` rows it is read above, and the override is scoped to
`.hero-header__content > .hero-facts`. [`DESIGN.md`](DESIGN.md) §10.2 states
the principle both pages are obeying: **columns sharing a page share a width,
not the idiom.** Do not "reunify" these two numbers. They are answers to two
different questions.

**Right-aligning held only while nothing wrapped.** Capped at the measure the
value column is 435px and the consulting sentence measures 520px, so it wraps,
and a wrapped value set right sets ragged against the label it is answering.
The availability sentence one block above wraps identically and has always
been set left.

## 3. Nothing on this page is typed twice

| Row | Source |
|---|---|
| Availability, Based in, in the page header | `availability` and `location` in `src/site.json`, via `render_contact_facts` |
| Primary email, Academic email, Phone / WhatsApp | `contact[]` in `src/site.json`, via `render_contact_channels` |
| LinkedIn, GitHub, Medium | `socials[]` in `src/site.json`, via `render_contact_socials` |
| Opportunities & Services | Written in the fragment. See §5 |

**`site.json` was always the source and the page ignored it.** The JSON-LD that
a search engine reads was built from `contact[0]` and `socials[]`, while the
text a person read was typed into the fragment, with no guard between them.
They had already drifted: the data said `Email` / `University` / `Phone` and
the page said `Primary email` / `Academic email` / `Phone / WhatsApp`. Two
renderings of one fact, disagreeing, is the exact failure every other guard in
`tools/build.py` exists to prevent, sitting on the page with no model document.

**Do not type an address into the fragment.** Add it to `site.json` and it
appears in both renderings and in the structured data at once.

## 4. Based in, and why it is one row

It was two, in this order:

> **Location** Sfax, Tunisia
> **Availability** EU Visa Holder. Open to relocation within the
> EU and to fully remote roles.

Which handed a recruiter the disqualifying half first and left them to
reconcile two adjacent facts themselves. [`CLAUDE.md`](CLAUDE.md) §4 exists
because *a recruiter who has to wonder filters silently, and the candidate
never finds out it happened*: this was the page meant to prevent that,
producing it.

One row now, labelled **Based in**, rendering `location`, a full stop, then
`availability` **verbatim**.

**The availability sentence is not edited, joined, shortened or smoothed.**
§4 forbids paraphrasing a residence or work-authorisation status, and the
reason the site once carried three different wordings of it is that three
places each held their own copy. The joining here is punctuation and nothing
else. If the merged line ever reads awkwardly, the fix is the author changing
the one string in `site.json`, never this page rewording it in passing.

## 5. Opportunities & Services

Two rows: **Engineering roles**, and **Consulting & services**.

**The consulting row is deliberate, and it has already survived being
deleted.** An audit raised it against [`CLAUDE.md`](CLAUDE.md) §3, which says
Data Engineering is the role and that a change making the target role harder to
name in one word is wrong. The argument was that a consulting offer beside
*founding engineering positions* lets a reader conclude the author is shopping
rather than targeting. The row was removed on that reading, and the author put
it back.

**That is the author's call and it is now made.** Do not remove the row again
on §3's authority: the argument has been put and answered, and re-deleting it
would be an agent overruling a positioning decision, which
[`CLAUDE.md`](CLAUDE.md) §10 reserves absolutely to the author. If the tension
still seems worth resolving, the thing to change is §3, in writing, with the
author, not this page in passing.

What §3 does still govern is everything above this block: the `h1` on Home is
one word, the hero lede leads with the role, and Skills & Evidence is ordered
`trunk` before `branch`. The claim is made there. This block states what work
is being accepted, which is a different question from what the role is.

## 6. Availability and Based in are page facts, and live in the page header

```
Contact
  Availability   EU Visa Holder. Open to relocation
                 within the EU and to fully remote roles.
  Based in       Sfax, Tunisia
```

**They are not contact channels and they spent three arrangements inside a
list of them.** `Contact Details` answers *how do I reach you*; a residence
status and a city answer neither. A reader scanning addresses met a sentence
about EU work authorisation in the middle of them.

The four arrangements, because the sequence is the argument:

| | Why it failed |
|---|---|
| Two rows, `Location` above `Availability` | Handed a recruiter the disqualifying half first: the silent filter §4 exists to prevent, produced by the page meant to prevent it |
| One merged row, `Based in` | Fixed the ordering, cost the sentence its own line, where it read as a tail on a city |
| Two rows, availability first | Fixed both, and left them in a section that answers a different question |
| **Page header** | A fact about the page, in the page's own header |

**`.hero-facts`, reused rather than reinvented.** It is the label column Home
renders this exact sentence in, so a reader who saw it on the front page meets
the same shape where the decision gets made, and [`DESIGN.md`](DESIGN.md) §11
asks a fifth label-column case to use the idiom rather than invent a sixth.
The *shape* is what carries across, not the track: Home sets its labels on
`--spine` and this page on 10rem, each matching what it is stacked against.
Nothing in its stylesheet was coupled to the hero; only the section header
claimed so, and that comment is corrected.

**Both strings render verbatim from [`src/site.json`](src/site.json).** §4
forbids paraphrasing a residence status, and the reason the site once carried
three wordings is that three places each held a copy. Do not join them, shorten
them, or move either into the `block__intro`: an intro is one line and a pitch
([`DESIGN.md`](DESIGN.md) §11.1), and this is neither.

## 7. The order of the blocks

```
Contact Details            invitation, then the three addresses
Connect                    the three profiles
Opportunities & Services   what work is being accepted
```

**It used to read actionable, inert, actionable.** Opportunities sat between
the two channel lists, so the statement of what work is accepted split the
addresses from the profiles, and a reader who wanted the second list had to
read past a block that asks nothing of them to reach it.

Nothing here changed except the order. The reasoning:

- **A recruiter still meets the address first**, which is the whole point of
  §1. Leading with Opportunities was the other candidate, and it is
  andrewng.org's shape, but his routing block *is* the address list: each
  purpose carries the email that serves it. Ours cannot do that, because all
  three addresses reach the same person, so a purpose-first block here is two
  rows of delay in front of the thing the reader came for.
- **The two lists a reader can act on now sit together**, which is also what
  the ink says: `.contact-list__link` paints its value in `--color-link` and
  the Opportunities rows are not links and stay in heading ink. One component
  renders all three blocks and the colour is what separates an address from a
  statement, so the two blue blocks being adjacent is the page agreeing with
  itself.
- **The page closes on the offer** rather than on a handle list.

§5 governs the consulting row itself and is untouched by this: moving a block
is not removing one.

## 8. What is still open

**There is no closing route to this page.** Nothing on the site links here
except the navigation. Home ends on its longest block with no next step, and
the invitation sentence now renders here and nowhere else.

**The invitation moved up to the page header.** It was the `block__intro` of
Contact Details, which made it read as an introduction to three email
addresses; it speaks for the whole page, because Connect and Opportunities are
equally what it invites. It is a `.page-lede` now, above the fact strip, and
Contact Details opens straight onto its rows. The rule that separates the two
ranks is [`DESIGN.md`](DESIGN.md) §11.1. Nothing was written: the sentence is
still `contact_invitation` in `src/site.json`, verbatim, in both languages. A closing line on
Home was proposed and deliberately not built: it would be a new element on the
front page and [`DESIGN.md`](DESIGN.md) Principle 1 deserves an argument for
it, made in writing first.
