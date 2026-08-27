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
`font-size: var(--text-xl)` so that an `h2` would render at the size the rest
of the site gets from its section heading. One visual rank spelled two ways,
with the stylesheet correcting the difference so that nothing, and nobody,
could see it was there. Both classes are deleted.

**`.contact-list` stays, and is the one genuinely local component.** A quiet
label naming a channel, its actionable address on the right edge. It is the
label-column idiom [`DESIGN.md`](DESIGN.md) §11 names and three other blocks
use. Keep it; do not reinvent it as a definition list, because these are
choices a reader acts on rather than terms being defined.

## 3. Nothing on this page is typed twice

| Row | Source |
|---|---|
| The invitation, as `block__intro` | `contact_invitation` in [`src/site.json`](src/site.json) |
| Primary email, Academic email, Phone / WhatsApp | `contact[]` in `src/site.json`, via `render_contact_channels` |
| Based in | `location` and `availability` in `src/site.json`, joined |
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
> **Availability** EU residence permit holder. Open to relocation within the
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

## 6. Based in, and Availability, are two rows

The availability sentence has its own row and it comes **first**:

> **Availability** EU residence permit holder. Open to relocation within the
> EU and to fully remote roles.
> **Based in** Sfax, Tunisia

They were two rows originally, in the other order, and §4 above is why that
failed. They were then merged into one row to remove the surface entirely, and
the author asked for the sentence back on a line of its own, which is right:
it is the longest and most consequential string on the page and as a tail on a
location it read like a footnote to Tunisia.

**Separated, but ordered.** The decisive fact leads and the location follows it
as context, which is the reverse of the arrangement that caused the problem.
Both strings come from [`src/site.json`](src/site.json) and neither is edited
here.

## 7. What is still open

**There is no closing route to this page.** Nothing on the site links here
except the navigation. Home ends on its longest block with no next step, and
the invitation sentence now renders here and nowhere else. A closing line on
Home was proposed and deliberately not built: it would be a new element on the
front page and [`DESIGN.md`](DESIGN.md) Principle 1 deserves an argument for
it, made in writing first.
