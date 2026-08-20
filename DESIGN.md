# Portfolio design system

The reference for every visual and structural decision on this site.
The implementation lives in [`assets/css/main.css`](assets/css/main.css); this
document explains the reasoning so the system can be extended without drifting.

---

## The brief

Classic, restrained, academic. This site descends from the orderedlist
**Minimal** theme by way of [elyesmanai.github.io](https://elyesmanai.github.io/),
and that lineage is the design — a sticky identity rail on the left, a plain
document on the right, one typeface, one blue for links, hairlines for
structure.

**What this system changes is discipline, not style.** The original look was
hand-tuned page by page, which is why it had drifted: three different contact
blocks, one section rule that existed only on the Projects page, icons squashed
by percentage widths. Everything below reproduces that look from tokens and
named components, so it stays consistent as the site grows.

### Explicitly out of scope

These were considered and rejected as wrong for the register:

- Uppercase letterspaced eyebrow labels
- Large display numerals for metrics
- A second (serif or display) typeface
- Filled or outlined buttons in the content flow
- Cards, tinted panels, drop shadows on content
- Hover animations, scroll effects, entrance transitions

If a future addition needs one of these, the addition is probably wrong.

---

## Principles

1. **A document, not an interface.** Structure comes from headings, bullets,
   hairlines and whitespace. A reader should be able to print the page and lose
   nothing.
2. **Coherence over novelty.** One type scale, one spacing scale, one accent,
   one content component. A new page is assembled from parts that already exist.
3. **Credibility before persuasion.** Claims carry a number and a link to where
   the number can be checked.
4. **Timeless over current.** Nothing here should look dated in five years,
   because none of it looks current now.
5. **Restraint in motion.** Interaction is acknowledged with colour and an
   underline, never performed.
6. **Single source of truth.** Every literal is a token; every shared region of
   markup is generated from one template. Duplication is a defect.

---

## 1. Typography

**One family: Noto Sans**, self-hosted (woff2 / woff / ttf), in **two weights
only — 400 and 700**. The family ships no others, so any 500 or 600 would be a
synthesised fake. Emphasis comes from weight, colour and size.

A second typeface was the single biggest thing that tipped an earlier draft out
of register: a serif for titles reads as *magazine*, not as *academic page*.

| Token | Size | Use |
|---|---|---|
| `--text-xs` | 11px | Tags |
| `--text-sm` | 12px | Dates, "last update", footer |
| `--text-md` | 13px | Navigation, sidebar, contact |
| `--text-base` | 15px | Body copy |
| `--text-lg` | 16px | Page lede, entry titles, sidebar headings |
| `--text-xl` | 18px | Section headings (`h3`) |
| `--text-2xl` | 24px | Page title (`h1`) |
| `--text-3xl` | 28px | The name in the sidebar |

These are the original theme's proportions with **one change: body copy moved
from 14px to 15px.** That step is the whole accessibility argument and costs
nothing visually.

Line height: 1.2 for headings, 1.45 for short-measure text, 1.6 for prose.
Prose is capped at `--measure` (74ch).

### Heading ramp

The theme's signature is a *stepped* grey ramp — each heading level one notch
lighter than the one above:

| Level | Colour | Role |
|---|---|---|
| `h1` / the name / `strong` | `#222222` | Strongest |
| `h2` / page title | `#393939` | Page-level |
| `h3` / section headings | `#494949` | Section-level |
| Body | `#373737` | — |

Note that body text is *darker* than `h3`. That is not a mistake; it is the
original ramp and it is why the page reads calm rather than shouty.

## 2. Colour

One grey ramp and one blue. Nothing else may be introduced.

- **Links** — `--blue-600` `#267cb9`, the theme's blue (4.6:1 on white, AA).
  Hover is `--blue-800` `#006699`.
- **Rules** — `--rule` `#e5e5e5` for structural hairlines, `--rule-soft`
  `#eaeaea` for the lighter underline beneath section headings.
- **Muted text** — the theme's `#777` was darkened to `#6b6b6b`, the smallest
  change that clears AA at 12px.

**Semantic layer.** Components address `--color-text`, `--color-heading`,
`--color-link`, `--color-border` and so on — never a primitive. Re-theming
means editing one block. `tools/check.py` fails on an undefined token and
reports any token nothing consumes.

**Status colours** exist for tags alone — see §7.

Light-only, and it prints cleanly. Dark mode is deliberately deferred: the
brand logos in `images/icons/` are fixed-colour SVGs that would each need a
treatment, and half-solving it is worse than not solving it.

## 3. Spacing

Built around the theme's **20px block rhythm** rather than a generic 8pt grid,
so the vertical texture of the original page survives:

`--space-1` 4 · `--space-2` 8 · `--space-3` 12 · `--space-4` 16 ·
**`--space-5` 20** · `--space-6` 32 · `--space-7` 40 · `--space-8` 60

`--space-5` is the default bottom margin on every block-level element.
`--space-7` is the column gap and the separation between sections.

## 4. Layout & containers

`--container-max` 1120px at `--container-fluid` 95%, holding a fixed
`--sidebar-width` 280px rail and a fluid content column, `--column-gap` apart.

The rail is sticky and scrolls independently, so identity, credentials, the CV
link and contact details stay reachable from anywhere in a long document —
the most useful thing a portfolio can do for someone reading it in order to
get in touch.

## 5. Borders, radius & elevation

`--radius-sm` 3px (tags), `--radius-md` 5px (code blocks), `--radius-full`
(portrait only).

**The system is flat.** There is exactly one shadow token,
`--shadow-portrait`, applied to exactly one element. Content is never lifted.
Separation is a 1px hairline.

## 6. Iconography

Brand logos arrive in wildly different aspect ratios — square, 2500×1184
wordmarks, 412×800 portraits. **Every icon renders inside a fixed square box
with `object-fit: contain`** via `.icon` plus a size modifier (`--xs` 12,
`--sm` 15, `--md` 18, `--lg` 32). This is the rule that keeps logos
undistorted and optically aligned. Icons are never sized inline; the original
sized social marks with `width="15%"`, which is why they never lined up.

Decorative icons take `alt=""`; an icon that is the only content of a link
carries that link's accessible name in its `alt`.

## 7. Tags

The one addition to the classic vocabulary, and the one piece of colour on the
page. Tags **classify**; they never decorate. Five semantic variants, no sixth:

| Variant | Meaning | Example |
|---|---|---|
| `.tag--neutral` | Factual context | `Azure`, `86 Teams` |
| `.tag--accent` | Role or category | `Instructor`, `Graduate Level` |
| `.tag--success` | Verified, published, shipped | `Official Plugin PR #585` |
| `.tag--honor` | Distinction or pending status | `1st Place`, `In Progress` |
| `.tag--critical` | Downloadable artefact | `Slides (.pptx)` |

## 8. Interactive states

Every interactive element defines rest, hover and `:focus-visible` (2px blue
outline, 2px offset).

Links get colour plus an underline on hover — **never a weight change**. The
original's `a:hover { font-weight: bold }` reflowed the sentence under the
cursor.

There are no buttons in the content flow. The CV is a plain link under a
"Downloadables" heading, as it was.

## 9. Content records

One component, `.entry`, is used for every record on the site: a job, a
project, a paper, a course, a workshop, an award. It is a **bulleted list
item**, exactly as the original CV pages were written by hand:

```
• Title — Role                    .entry__title / .entry__role
  Aug 2024 – Present              .entry__period   (italic, muted)
  [tags]                          .tag-list
  – point                         .points
  – point
```

Optional `.entry__group` subdivides a long record (Data Integration / Cloud &
Security / Observability), and `.issuer` heads a certification group with its
brand mark.

Entries are **never boxed**. A CV is a document, not a feed of cards.

## 10. Definition lists

`.deflist` handles all "category: values" content — skills, languages, impact.
The original wrote these as `<li><b>Label:</b> values</li>`: correct on screen,
but the pairing lived only in the punctuation.

`.deflist` renders **identically** — bullet, bold label, colon, values, all on
one line — while being a real `<dl>`. The `.deflist__item` wrapper `<div>` is
valid inside a `<dl>` and is what lets a `dt`/`dd` pair share one list marker.

## 11. Page structure

Every page is the same stack:

```
page-header   h1 + optional lede
block         h3 (underlined) + optional intro + entries or deflist   ← repeated
```

Each page has exactly one `<h1>` — its own title. The site name in the rail is
a link styled to the old `h1`'s size, not a heading, so every page gets a
unique document outline. Enforced by `tools/check.py`.

## 12. Navigation

The original rendered this as a `<table>` row, which meant the site's real
tables inherited its styling and **no page could show which one you were on**.
`.nav` keeps the look — evenly distributed links over a hairline — as a list,
with `aria-current="page"` rendered as bold ink.

## 13. Responsive behaviour

| Breakpoint | Change |
|---|---|
| >960px | Two columns, sticky rail |
| ≤960px | One column; the rail becomes a centred band above the document (the theme's own breakpoint) |
| ≤720px | Padding tightens; nav items shrink-wrap |
| ≤480px | Navigation scrolls horizontally, bleeding to the viewport edges so the affordance is visible; type steps down |

## 14. Motion

A single `--duration` of 150ms, on colour and opacity only. Fully disabled
under `prefers-reduced-motion: reduce`.

## 15. Accessibility

- Skip link to `<main>`.
- Landmarks: rail `<header>`, `<nav aria-label="Primary">`, `<main>`.
- One `<h1>` per page; every block labelled with `aria-labelledby`.
- `:focus-visible` outline on every interactive element.
- Every `<img>` has an `alt` (empty when decorative).
- Every `target="_blank"` carries `rel="noopener"`.
- Body text 15px; 11px is used only for tags, which always repeat information
  present in the surrounding prose.
- Pinch-zoom is not disabled. The removed `scale.fix.js` set
  `user-scalable=no` on iOS, violating WCAG 1.4.4.
- `prefers-contrast: more` darkens the secondary and muted ramps.

## 16. Content hierarchy

The site answers hiring questions in order:

| Question | Where |
|---|---|
| Who is this engineer? | Rail identity + Home page title |
| How do they work? | Home → Profile |
| What technologies do they actually use? | Home → Skills |
| What impact did they create? | Home → Selected Impact |
| What problems have they solved? | Career → Experience |
| What can they build? | Projects |
| How technically deep are they? | Research, Workshops, Teaching |
| Can I trust their engineering practices? | Career → Certifications (all verifiable) |
| Where can I verify their work? | Every entry links to source, badge or DOI |
| How do I reach them? | The rail, on every page |

## 17. Extending the system

1. Reach for an existing component first. `.entry` and `.deflist` cover almost
   everything on the site.
2. If a new component is genuinely needed, build it from tokens only. A literal
   in a component rule is a bug.
3. Check it against **Explicitly out of scope** at the top of this document.
4. Add it here and to `assets/css/main.css` under a numbered section.
5. Run `python3 tools/check.py` — it fails on classes used in markup but absent
   from the stylesheet, undefined tokens, inline styles and broken links, and
   reports any CSS rule or token nothing uses.
