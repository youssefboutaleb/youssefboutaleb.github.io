# Portfolio design system

The reference for every visual and structural decision on this site.
The implementation lives in [`assets/css/main.css`](assets/css/main.css); this
document explains the reasoning so the system can be extended without drifting.

---

## Principles

1. **Coherence over novelty.** One typographic scale, one spacing scale, one
   accent colour, one content component. A new page should be assemblable from
   parts that already exist.
2. **A document, not an interface.** Structure comes from hairlines, whitespace
   and typographic hierarchy — never from boxes, tinted panels or shadows. The
   page should read like a well-set academic document.
3. **Credibility before persuasion.** Claims carry a number and a link to where
   the number can be checked. No superlatives that a reader cannot verify.
4. **Timeless over current.** Nothing on this site should look dated in five
   years, which rules out large radii, gradients, glassmorphism, hero
   animations and full-bleed marketing sections.
5. **Restraint in motion.** Interaction is acknowledged (colour, underline,
   border), never performed. No entrance animations, no scroll effects, no
   scale-on-hover.
6. **Single source of truth.** Every literal is a token; every shared region of
   markup is generated from one template. Duplication is treated as a defect.

---

## 1. Typography

Two families, deliberately contrasted:

| Role | Family | Where |
|---|---|---|
| Titles | System serif stack (Charter → Sitka → Cambria → Iowan → Palatino → Georgia) | Page titles, block titles, the name, stat figures |
| Everything else | Noto Sans (self-hosted, woff2/woff/ttf) | Body, meta, navigation, tags, buttons |
| Code | System monospace stack | `code`, `pre` |

The serif is a *system* stack, so it costs zero network requests and cannot fail
to load. It carries the academic register; the sans carries the engineering one.

**Only two weights exist — 400 and 700.** The self-hosted family ships no others,
so any use of 500/600 would be a synthesised fake. Emphasis is achieved with
weight, colour and size — never with a third weight.

### Scale

| Token | Size | Use |
|---|---|---|
| `--text-2xs` | 11px | Eyebrows, contact labels |
| `--text-xs` | 12px | Tags, dates |
| `--text-sm` | 13px | Meta lines, navigation, footer |
| `--text-md` | 15px | Sidebar body |
| `--text-base` | 16px | Body copy |
| `--text-lg` | 18px | Entry titles, page lede |
| `--text-xl` | 22px | Block titles |
| `--text-2xl` | 28px | Stat figures |
| `--text-3xl` | 34px | Page titles |

Line height: `--leading-tight` (1.2) for titles, `--leading-snug` (1.4) for
short-measure text, `--leading-normal` (1.65) for prose.
Prose is capped at `--measure` (72ch) regardless of viewport.

At ≤720px the three largest steps shrink; nothing else changes, so the hierarchy
survives the breakpoint intact.

## 2. Colour

One neutral ramp and one accent. Nothing else may be introduced.

**Neutrals** — `--ink-900` (headings) through `--ink-400` (muted meta), on
`--paper`, separated by `--rule` hairlines.

**Accent** — a deep navy (`--accent-600` `#17466f`, 9.9:1 on white). Restrained
enough to read as institutional rather than promotional, dark enough to pass
AA at every size it is used.

**Semantic layer.** Components never reference a primitive directly. They use
`--color-text`, `--color-heading`, `--color-link`, `--color-border`,
`--color-surface`, `--color-action` and so on. Re-theming means editing the
semantic block only. `tools/check.py` fails the build on an undefined token.

**Status colours** exist for tags alone, in five meanings — see §7.

The site is light-only and prints cleanly. Dark mode is deliberately deferred:
the brand logos in `images/icons/` are fixed-colour SVGs that would need
per-mark treatment, and half-solving it would be worse than not solving it.

## 3. Spacing

A 4px base scale: `--space-1` (4px) through `--space-8` (64px).
No layout value is written as a literal.

Rhythm in practice: `--space-2` inside a component, `--space-3`–`--space-4`
between elements of a component, `--space-5` between components,
`--space-7` between blocks, `--space-8` between page regions.

## 4. Layout & containers

Two columns: a sticky `--sidebar-width` (288px) identity rail and a fluid
content column, inside `--container-max` (1180px), separated by `--column-gap`.

The sidebar is sticky and scrolls independently, so identity, credentials,
contact details and the CV link stay reachable from anywhere on a long page —
the single most useful thing a portfolio can do for a recruiter.

Content is capped at `--measure` for readability even when the column is wider.

## 5. Borders, radius & elevation

Radii are small on purpose: `--radius-sm` 2px (tags), `--radius-md` 4px
(buttons), `--radius-lg` 6px (code blocks), `--radius-full` (portrait only).
Large radii read as consumer software.

**The system is flat.** `--shadow-sm` exists and is applied to exactly one
element — the portrait. Content is never elevated. Separation is a 1px
`--rule`, and emphasis is a 2px `--rule-strong`.

## 6. Iconography

All marks are SVG in `images/icons/`. Brand logos arrive in wildly different
aspect ratios (square, 2500×1184 wordmarks, 412×800 portraits), so **every icon
renders inside a fixed square box with `object-fit: contain`** via `.icon` plus
a size modifier (`--xs` 14, `--sm` 16, `--md` 20, `--lg` 24). This is the rule
that keeps logos undistorted and optically aligned; icons are never sized inline.

Decorative icons take `alt=""`; icons that are the only content of a link carry
the link's accessible name in `alt`.

## 7. Tags

Tags classify, they never decorate. Five semantic variants, and no sixth:

| Variant | Meaning | Example |
|---|---|---|
| `.tag--neutral` | Factual context | `Azure`, `86 teams` |
| `.tag--accent` | Role or category | `Instructor`, `Computer vision` |
| `.tag--success` | Verified, published, shipped | `Accepted upstream — PR #585` |
| `.tag--honor` | Distinction or pending status | `1st place`, `Under preparation` |
| `.tag--critical` | Downloadable artefact | `Slides (.pptx)` |

## 8. Buttons & interactive states

`.btn` is outline-by-default, filling on hover; `.btn--primary` is filled;
`.btn--block` spans its container. Every interactive element defines four
states: rest, hover, `:focus-visible` (2px accent outline, 2px offset) and
active.

Links get colour plus an underline on hover — **never a weight change**, which
was the old stylesheet's `a:hover { font-weight: bold }` and reflowed text under
the cursor.

## 9. Content records

There is one content component, `.entry`, used for every record on the site: a
job, a project, a paper, a course, a workshop, an award. It has a title, an
optional right-aligned period, a meta line, tags, and a body of prose or points.

Entries are separated by hairlines and are **never boxed**. A CV is a document,
not a feed of cards.

## 10. Page structure

Every page is the same stack:

```
page-header   eyebrow → h1 → lede
block         h2 + optional intro + body     ← repeated
block
site-footer
```

Each page has exactly one `<h1>` (its own title), and the site name in the
sidebar is a link, not a heading — enforced by `tools/check.py`.

## 11. Navigation

One horizontal bar under a hairline, with `aria-current="page"` on the active
item rendered as an accent underline. The previous build had no active state at
all: every page's navigation looked identical, so the reader never knew where
they were.

## 12. Responsive behaviour

| Breakpoint | Change |
|---|---|
| >1000px | Two columns, sticky sidebar |
| ≤1000px | One column; sidebar becomes a horizontal band of auto-fitting sections |
| ≤720px | Type steps down; dates move above titles; the spec list collapses to one column |
| ≤480px | Navigation scrolls horizontally, bleeding to the viewport edge so the affordance is visible; stats stack |

## 13. Motion

`--duration-fast` 120ms / `--duration` 180ms on `--ease`. Only colour, opacity,
border and the skip-link transform animate. Everything is disabled under
`prefers-reduced-motion: reduce`.

## 14. Accessibility

- Skip link to `<main>`.
- Landmarks: sidebar `<header>`, `<nav aria-label="Primary">`, `<main>`, `<footer>`.
- One `<h1>` per page; blocks labelled with `aria-labelledby`.
- `:focus-visible` outline on every interactive element.
- Every `<img>` has an `alt` (empty when decorative).
- Every `target="_blank"` carries `rel="noopener"`.
- Body text ≥16px; the smallest text (11px) is reserved for labels that repeat
  information available elsewhere.
- Pinch-zoom is not disabled. (The removed `scale.fix.js` set
  `user-scalable=no` on iOS, violating WCAG 1.4.4.)
- `prefers-contrast: more` darkens the secondary and muted ramps.

## 15. Content hierarchy

The site answers hiring questions in order:

| Question | Where |
|---|---|
| Who is this engineer? | Sidebar identity + Home page header |
| How do they work? | Home → Engineering profile |
| What technologies do they actually use? | Home → Technical expertise |
| What impact did they create? | Home → Selected impact |
| What problems have they solved? | Career → Experience |
| What can they build? | Projects |
| How technically deep are they? | Research, Workshops, Teaching |
| Can I trust their engineering practices? | Career → Certifications (all verifiable) |
| Where can I verify their work? | Every entry links to source, badge or DOI |
| How do I reach them? | Sidebar, on every page |

## 16. Extending the system

1. Reach for an existing component first. `.entry` covers almost everything.
2. If a new component is genuinely needed, build it from tokens only. A literal
   in a component rule is a bug.
3. Add it to §1–14 above and to `assets/css/main.css` under a numbered section.
4. Run `python3 tools/check.py` — it fails on classes used in markup but absent
   from the stylesheet, undefined tokens, inline styles and broken links.
