# The dark rendering

What was proposed, what was measured, what shipped, and what is still open.
The rules live in [`DESIGN.md`](DESIGN.md) §2 and §6; this is the record of how
they got there.

---

## Where it started

Three enhancements were put forward together: a dark theme, a French version,
and a left-hand section menu. The analysis recommended starting with the dark
theme, and the reasoning is worth keeping because two of the three are still
open questions.

| Proposal | Verdict | Why |
|---|---|---|
| **Dark / light, system default** | **Built** | Already 80% paid for: every colour literal was in `:root`, so the work was a token block, not a repaint. No content risk, no claim touched, fully reversible. |
| **French version** | Deferred, unchanged | It is `CLAUDE.md` M4 and the roadmap already rules on the timing: after the English site is stable. Measured at roughly 8,000 words across 15 data files and 8 fragments. The build work is moderate; the translation is author-led and not delegable, because §6's voice map and banned register have to be re-decided in French. M1 and M2 are both open, and each would force a retranslation. |
| **Left section menu** | Overtaken by events | The analysis argued against it on measurements: no `h4` subsections exist anywhere on the site, five of eight pages have one or two sections, and Teaching's 1,635 words sit inside a *single* section, so a table of contents could not help the page that most needs help. It also reversed `DESIGN.md` §4, which had removed the left rail for costing a quarter of the viewport on exactly the pages whose records are widest. **It was implemented independently and committed as `3acc1b9` while the analysis was being written.** The argument above is recorded here, unaltered, so that if the sidebar is ever revisited the measurements do not have to be taken again. |

---

## The blocker that was not

`DESIGN.md` §2 had a standing decision against dark mode:

> *Light-only, and it prints cleanly. Dark mode is deliberately deferred: the
> brand logos in `images/icons/` are fixed-colour SVGs that would each need a
> treatment, and half-solving it is worse than not solving it.*

The reasoning was sound. The measurement behind it had never been taken. When
it was, the sixteen files in `images/icons/` sorted like this:

| | Count | Detail |
|---|---|---|
| **Actually break on a dark ground** | **3** | `github.svg` (no `fill` attribute at all, so it inherits the SVG default of black), `anthropic-light.svg` (`#000`), `opencv.svg` (`#050505` wordmark) |
| Survive unaided | 9 | Saturated brand colours. Five sit lower-contrast than ideal but stay legible |
| Never rendered | 2 | `linkedin.svg`, `medium.svg`. `socials[].icon` in `src/site.json` is read only for the JSON-LD `sameAs`, which takes the `href` |
| Not content | 1 | `icon.svg`, the favicon, referenced from `<link>` on all 8 pages |
| Renders as inline SVG | 1 | The sidebar's `book-toc__icon` uses `currentColor` and was already theme-safe. It has since been deleted: it was the only `<svg>` on the site. [`sidebar-options.md`](sidebar-options.md) |

Three is a solvable number, so the deferral no longer held. Recorded here
because the pattern is the lesson: **a deferral whose stated cost was never
measured is a deferral worth re-measuring**, not a decision.

---

## What shipped

### The palette

Built to mirror the light theme's contrast *relationships* rather than invent
new ones, so the page keeps the weight it reads with in light.

| Role | Light | | Dark | |
|---|---|---|---|---|
| heading | `#222222` | 15.9:1 | `#e9ebed` | 14.9:1 |
| h2 | `#393939` | 11.6:1 | `#dcdfe2` | 13.3:1 |
| h3 | `#494949` | 9.0:1 | `#ccd0d4` | 11.5:1 |
| body | `#373737` | 11.9:1 | `#c3c7cc` | 10.5:1 |
| meta | `#676767` | 5.7:1 | `#9aa0a6` | 6.7:1 |
| muted | `#6b6b6b` | 5.3:1 | `#8b9197` | 5.6:1 |
| link | `#267cb9` | 4.5:1 | `#6fb3e8` | 7.9:1 |
| link hover | `#006699` | 6.3:1 | `#9ecdf5` | 10.6:1 |

Ground `#16181a`, surface `#1e2124`. The link is the one value deliberately
raised: 4.5:1 is the AA floor and reads thin as a blue on a dark ground at
15px. All seven status families were re-derived; the weakest, accent at 7.5:1,
is stronger than the weakest in light (accent, 5.6:1). Every value above was
verified by resolving the tokens out of the shipped stylesheet, not from the
design notes.

### The four changes nobody asked for, and why each was required

The theme could not be added without them.

1. **Six component rules bypassed the semantic layer.** `main.css` had
   `color: var(--paper)` in `.skip-link` (×2), `var(--rule-soft)` in four entry
   and group rules, and `var(--paper-soft)` in `.book-toc`. `DESIGN.md` §2's
   own instruction is that components address a semantic token and never a
   primitive. In dark mode those four hairlines would have stayed `#eaeaea` and
   glowed. **Not six bugs, one:** they now route through `--color-border-soft`,
   `--color-surface` and a new fixed `--color-on-accent`. Zero visual change in
   light, because the tokens resolve to identical values there.

   Worth noting that `.book-toc`, the newest component on the site, had already
   acquired the same defect. The leak is not historical.

2. **`@media (prefers-contrast: more)` was a live bug waiting for a dark
   palette.** It repointed the semantic tokens at `--ink-900` and `--ink-400`.
   Under the dark palette those are the *lightest* values, not the darkest, so
   one block would have put `#222` text on a `#16181a` page for any reader with
   both settings on. It is now two blocks, and the dark variant walks the ramp
   the other way.

3. **`@media print` reset the ink but never the ground.** It now names
   `--color-bg`, `--color-surface` and the two borders explicitly, so a reader
   printing from the dark rendering gets paper. Source order does the rest: the
   dark block sits above it.

4. **Two section 13s.** The sidebar was inserted as §07 without renumbering,
   which left `13. SPEC STRIP` and `13. RESULT` and put every header after it
   one behind the Contents list at the top of the file. Body headers 13-20 are
   now 14-21 and the list matches 1:1. This is Lesson 7 in
   [`.claude/skills/rework/SKILL.md`](.claude/skills/rework/SKILL.md)
   reoccurring, which is an argument for the lesson, not against it.

### The icons

Decided: invert the monochrome marks, plate the one that cannot be inverted.

```
LIGHT                     DARK
[GitHub, black]      ->   [GitHub, white]        .icon--mono, filter: invert(1)
[Anthropic, black]   ->   [Anthropic, white]     .icon--mono
[OpenCV, RGB+black]  ->   [OpenCV] on white      .icon--plate
```

Inverting a monochrome mark is colour substitution, not an effect: there is
nothing else in the mark for the filter to touch, and white is the dark variant
those brands publish themselves. OpenCV takes the plate because inverting it
would turn its three discs cyan, magenta and yellow, and leaving it alone was
not viable either: its wordmark path is 7,688 characters against roughly 600
for each disc, so most of the mark would have vanished.

The treatment is data. `ICON_TREATMENT` in `tools/build.py` keys it by
filename, so a logo declares itself once rather than at each of the three call
sites. `medium.svg` is in the table as `mono` although nothing renders it
today, so that the social marks come back correct if they are ever restored.

---

## Corrections made during the pass

- **Every line number in the first investigation went stale mid-session.** The
  working tree was committed as `3acc1b9` and rebuilt at 17:49 while the
  analysis was being written, moving `main.css` by +961 lines and `build.py` by
  +1,003. All five findings were re-verified against the new HEAD before
  anything was edited, and all five survived, one of them having gained a
  seventh instance (`.book-toc`).
- A grep for background rules was written so that it excluded every line
  containing `--`, which hid `body { background: var(--color-bg); }`. Caught
  and corrected before it reached a conclusion; the base was clean all along.

---

---

## The second pass: the switch

**The no-toggle decision was reversed by the author**, in the same session,
after seeing the theme run. That is theirs to do and it is recorded here in the
order it happened rather than tidied away: `CLAUDE.md` §7 now carries the
argument as the third exception, and says plainly that it was written
afterwards.

### The palette became one list

Adding a control means the scheme can be *pinned*, and a pinned scheme cannot
be expressed by `@media (prefers-color-scheme: dark)`. The obvious fix is a
second token block under `:root[data-theme="dark"]`, repeating all forty names.
Principle 6 calls duplication a defect, and this one would have been the
expensive kind: forty values that have to be edited in pairs forever.

Instead every token that differs is now written once, as
`light-dark(light, dark)`, and the entire mechanism is the `color-scheme`
property. Three consequences, two of them unplanned:

| | |
|---|---|
| The switch | sets one attribute; `:root[data-theme="light"\|"dark"]` sets `color-scheme`, and nothing else in the stylesheet knows the switch exists |
| `prefers-contrast: more` | went back to **one** block. It had been split in two a pass earlier precisely because `--ink-900` meant opposite ends of the ramp in the two schemes. It no longer does: the pair *is* the ramp |
| The logo treatments | stopped being a media query. `--icon-invert`, `--icon-plate-bg` and `--icon-plate-pad` are pairs like everything else, so `invert(0)` and a transparent plate are the light rendering, and a reader who pins dark on a light machine gets the right marks |
| `@media print` | resolves the whole palette to its light half with `color-scheme: light`, one declaration, whatever is pinned on screen |

The cost is `light-dark()`, which is Baseline as of 2024. On a browser older
than that the pairs are invalid and the page degrades to unstyled colours
rather than to the light theme. Accepted deliberately given the date; it is the
one thing here that trades a compatibility floor for a maintenance property.

### A bug the merge introduced, and the check that caught it

`--color-on-accent` was written as a fixed `#ffffff` with a comment reasoning
that "the accent it sits on is a strong blue in both renderings."

**That was false.** The link blue is dark in light (`#267cb9`, white ink at
4.5:1) and was deliberately *lightened* in dark to clear the ground
(`#6fb3e8`), where white ink falls to **2.3:1**. The skip link, which exists
for keyboard readers, would have been unreadable in dark mode. It is a pair
now and clears 7.9:1.

Worth keeping because of how it surfaced: not by review, but by re-running the
contrast resolver over the shipped stylesheet after the rewrite, on the
assumption that a mechanical change to forty values had probably broken
something. It had. **A comment asserting a colour relationship is not evidence
that the relationship holds**, and this one was written by the same hand that
then lightened the blue it described.

### The control

`Theme: System · Light · Dark` in the brand bar, at the size of the CV link
beside it. Built from type rather than from a widget: no track, no knob, no
fill, and the active state is weight and colour, which is how the rest of the
site marks emphasis. Three buttons in a `role="group"`, `aria-pressed` kept
truthful by the wiring script.

- **The selected state is CSS**, reading `[data-theme]` off `<html>`, so it is
  correct on first paint whether or not the wiring script has run.
- **No flash.** The head script sets the attribute before first paint. It is
  the reason that script is inline and not deferred.
- **`localStorage` in `try`/`catch` both ways**, because a locked-down browser
  throws on access rather than returning null.
- **Not rendered without JavaScript.** `class="no-js"` ships on `<html>` and
  the head script removes it, so a reader with scripting off sees no dead
  buttons and still gets their system scheme from the tokens.
- **Does not print**, with the rest of the navigation.

---

## Decided and not built

- **No system-change listener.** Not needed: in *System* state the browser
  resolves `color-scheme: light dark` live, so a reader who flips their OS
  theme sees the page follow with no script running.
- **The five low-contrast coloured logos were left alone** (Coursera `#0056D2`,
  LinkedIn `#0A66C2`, Datadog `#632CA6`, Astronomer `#6F56A7`, ScrumStudy
  `#006eb7`). They are legible, they are correct brand colours, and plating
  them would have meant plating all twelve, which is the option that was
  rejected.

## Still open, and author-led

- ~~The `07` naming mismatch.~~ **Settled** in the pass after this one: the
  component is *page context* everywhere. [`sidebar-options.md`](sidebar-options.md).
- ~~The sidebar has no model document.~~ **Settled** in the same pass:
  `DESIGN.md` §4 owns why it is admissible, §12.1 owns what it renders.
  **Contact still has none**, and `CLAUDE.md` §12 already names the pattern:
  the page with no owner is the page that drifted.
- **Nothing here was seen.** There is no headless browser in this environment.
  The palette is verified numerically against WCAG and the markup is verified
  by `check.py`; the *look* of the dark rendering has not been looked at. Open
  the site with your system set to dark before trusting it.
