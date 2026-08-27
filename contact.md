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

## 5. What is still open

**`Opportunities & Services` is hand-written and offers consulting.**
[`CLAUDE.md`](CLAUDE.md) §3 is that Data Engineering is the role and that a
change making the target role harder to name in one word is wrong. A row
offering *Consulting & services* beside *founding engineering positions* is in
tension with that, and a reader can conclude the author is shopping rather than
targeting. This is a positioning call and therefore the author's: either the
row goes, or §3 is revised, because at the moment one of the two is wrong.

**There is no closing route to this page.** Nothing on the site links here
except the navigation. Home ends on its longest block with no next step, and
the invitation sentence now renders here and nowhere else. A closing line on
Home was proposed and deliberately not built: it would be a new element on the
front page and [`DESIGN.md`](DESIGN.md) Principle 1 deserves an argument for
it, made in writing first.
