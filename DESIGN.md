# Portfolio design system

The reference for every visual and structural decision on this site.
The implementation lives in [`assets/css/main.css`](assets/css/main.css); this
document explains the reasoning so the system can be extended without drifting.

Its companion is [`awards.md`](awards.md), which owns the *information* model:
what a record states about itself and in what order (with
[`workshops.md`](workshops.md) and [`teaching.md`](teaching.md) declaring the
models built on it). This document owns how any of that looks. The two meet at one point (a metadata category name binds to a
`.tag--<category>` rule) and neither restates the other.

---

## The brief

Classic, restrained, academic. This site descends from the orderedlist
**Minimal** theme by way of [elyesmanai.github.io](https://elyesmanai.github.io/),
and that lineage is the design: a plain document, one typeface, one blue for
links, hairlines for structure.

The theme's sticky identity rail is the one piece of the lineage that has been
dropped. It is recorded in §4, with the reason, because a reader of this
document will otherwise keep finding rail-shaped holes in the CSS.

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
only: 400 and 700**. The family ships no others, so any 500 or 600 would be a
synthesised fake. Emphasis comes from weight, colour and size.

A second typeface was the single biggest thing that tipped an earlier draft out
of register: a serif for titles reads as *magazine*, not as *academic page*.

| Token | Size | Step | Use |
|---|---|---|---|
| `--text-xs` | 12px | | Tags |
| `--text-sm` | 13px | 1.08 | Dates, "last update", footer |
| `--text-md` | 14px | 1.08 | Contact rows, tag-adjacent meta |
| `--text-base` | 16px | 1.14 | Body copy, navigation |
| `--text-lg` | 17px | 1.06 | Record titles (`h3`) |
| `--text-xl` | 20px | 1.18 | The name in the brand bar, the page lede |
| `--text-2xl` | 32px | 1.60 | Section headings (`h2`) |
| `--text-3xl` | 64px | 2.00 | Page title (`h1`), and nothing else |

The bottom of the scale is the original theme's, with **one change: body copy
moved from 14px to 15px.** That step is the whole accessibility argument and
costs nothing visually.

**The top two steps are not the theme's, and the reason is arithmetic.** The
scale ran 12, 13, 14, 16, 17, 19, 25, and four of its six steps were under 15%,
at or below the increment Butterick calls the smallest that makes a visible
difference. Five of the seven sizes sat between 12px and 17px, nothing existed
above 25px, and **25px was the page title and the brand-bar name at once**, so
the `h1` was exactly the size of the link 40px above it and could not be raised
without dragging that link with it. The hierarchy was carried almost entirely
by colour and weight, because size had almost nothing left to say.

Split, and given a display step. `--text-2xl` moved down to the section
headings, `--text-xl` moved down to the brand bar, and `--text-3xl` is new and
has exactly one user.

**Where the display size came from.** Measured against three references rather
than chosen:

| | Body | `h1` | `h2` | `h1` ÷ body | `h1` : `h2` |
|---|---|---|---|---|---|
| andrewng.org | 17px | 48 → 72px | 30 → 36px | 4.24 | 2.00 |
| Tufte CSS | 21px | 48px | 33px | 2.29 | 1.45 |
| **This site** | 16px | **64px** | **32px** | **4.00** | **2.00** |
| This site, at 40px | 16px | 40px | 24px | 2.50 | 1.67 |
| This site, before that | 16px | 25px | 19px | 1.56 | 1.32 |

Read in that order, because the site has now been here twice and moved further
the second time. **The first pass measured andrewng.org and deliberately did
not follow it**, landing at 2.50 on the argument that 5.14 was a landing page's
ratio and Tufte's 2.29 was a document's. That arithmetic was wrong in one
place: the reference's body is 17px, not 14px, so its title is 4.24 times its
body and not 5.14, which is a good deal closer to Tufte than the table then
said. The second pass was asked for the reference's design directly, and 4.00
is where the same reasoning lands once the ratio is right.

Tufte CSS is still the load-bearing reference, and for the same reason: it is
unambiguously a document and still sets 48px, so **large type is not what makes
a page stop being a document.** What makes it stop is decoration, and the
change below removes some.

### The display pair is one treatment at two sizes

This is the reference's heading rule, and it is the whole of it:

```css
h1, h2 {
  color: var(--color-heading);          /* the darkest ink, darker than body */
  font-weight: var(--weight-regular);   /* 400, both of them */
  letter-spacing: -0.02em;
  line-height: var(--leading-display);  /* 1.15 */
}
h1 { font-size: var(--text-3xl); }      /* 64px */
h2 { font-size: var(--text-2xl); }      /* 32px */
```

Four shared declarations and a size each. **The ranks are separated by size
alone**, at exactly 2.00, which is what andrewng.org does and what this site
previously did not.

What it replaced separated them three times over. The title was 400, tracked
and `#393939`; the section heading was 700, untracked, `#494949` and carried a
hairline underline. Size, weight, colour and a rule were all saying the same
thing at once, and the section heading was the element paying for it: at 24px
bold with a line under it, it was shouting to be told apart from records it is
already twice the size of.

**Weight 400 on the title is the older half of the argument and is unchanged.**
At 64px the size is the whole signal, and bold on top of it is the combination
that reads as a landing page; Tufte sets its 48px `h1` in 400 for the same
reason. What is new is that the section heading joins it rather than answering
it.

**The negative tracking now covers both**, at `-0.02em`, which is the site's
existing principle pointed the other way: the only other letter-spacing rules
here are *positive*, on 12px tags and 10px diagram labels, because small type
wants opening up. Large type wants closing, and neither 64px nor 32px sets
tight on its own.

**The hairline under the section heading is gone.** It is the one place this
system's own founding line, *hairlines for structure*, was overruled on
purpose. It was drawn when the heading was 19px and bold, where a heading does
need help not to read as a bold paragraph. At 32px it had stopped separating
anything and had become decoration. What replaces it is space: `.block`'s
bottom margin went from 32px to 60px in the same edit, which is how the
reference separates its own sections, and the two changes are not separable.
`.spec__title` still carries that hairline and keeps it: a 14px column label
has no size to fall back on.

**One token died of it.** `--color-heading-2` (and `--ink-800`, the `#393939`
step behind it) had exactly one consumer, the page title's colour override.
With the title on the darkest ink there was nothing left reading them, and
`check.py`'s token audit said so, so the ramp is a step shorter: §4's palette
descends `#222222`, `#494949`, `#373737`.

Line height: 1.15 for the display pair, 1.2 for other headings, 1.45 for
short-measure text, 1.6 for prose.

**The display step comes down twice, and nothing else moves with it.** At
≤720px `--text-3xl` is 48px and `--text-2xl` 28px; at ≤480px, 40px and 24px. A
64px title is sized against a 908px column and below 720px there is not one.
The ratio loosens to 1.71 and then 1.67 rather than holding at 2.00, and that
is deliberate: at weight 400 with no rule beneath it, a section heading has to
stay clear of the 16px body, and 24px is the floor that keeps it clear. The
reference does the same, dropping its title 72 → 48 while its heading only goes
36 → 30. Everything 20px and below is sized for reading rather than for the
column and stays where it is.

**The Home hero is the one place the size had to be checked rather than
chosen**, because it is the only `h1` that is not alone in a full-width header:
it sits beside the portrait, in the track `--spine` leaves it (§4). Measured
from the shipped face at weight 400, `Ingénieur Data` (the longer of the two)
is **435px** at 64px. The bio column is 668px at the widest container and
narrows to **452px** at a 1024px viewport, which is where the rail is present
and the container has not finished widening to absorb it. It holds one line at
every width, with about 17px to spare at the tightest. **72px, the reference's
own number, is what this ruled out**: the same string is 489px and wraps.

**Two of those numbers used to be different, and the correction matters more
than the change did.** This paragraph read *453px against a bio column of 492px
and 489px*, measured when the portrait track was 180px. The 453 was never right
(the shipped face gives 435), the 492 was, and the spine has since cost the bio
40px. The margin got smaller and the claim got true, which is the opposite of
what usually happens when a layout tightens under a documented measurement: the
document was carrying a figure nobody had re-derived. Re-measure with
`fontTools` against `assets/fonts/`, do not scale the old number.

**Print does not inherit this ramp, deliberately.** The tokens are in `rem` and
the print stylesheet does not override the root, so a 64px title would set at
48pt on a document whose entire reason for printing is that it doubles as a CV
with a page budget the screen does not have. Print sizes in points against its
10.5pt body: `h1` 20pt, `h2` 13pt, the lede 12pt, the brand-bar name 14pt, and
both headings' tracking is reset, because it was an optical correction for 64px
and 32px and not for 20pt and 13pt.

**Print is also where the section heading keeps its weight and its hairline.**
The underline was dropped on the argument that 32px separates a section on its
own. 13pt against a 10.5pt body does not, and 60px of white between blocks is
not affordable on a page being rationed, so print takes back the 700 and the
rule and brings the block gap down to 32px. It is the only rank the two media
disagree about, and the disagreement is the size argument applied honestly in
both.

**Prose is capped at `--measure` (74ch), and that cap is load-bearing.** The
column is 1100px wide; at 15px, an uncapped line runs to roughly 110 characters,
which is past the width a reader tracks without losing the return sweep. The cap
is on the text and never on the column, so tag rows, spec strips and runs of
records still use the full width. Every prose container carries it: `.prose`,
`.page-lede`, `.block__intro`, `.block__note`, `.entry__summary`,
`.entry__meta`, `.points` and `.hero-facts`.

### Heading ramp

The theme's signature was a *stepped* grey ramp, each heading level one notch
lighter than the one above. It still is from the record title down; the top of
it is now a pair rather than two steps (§1):

| Level | Element | Size | Weight | Colour | Role |
|---|---|---|---|---|---|
| Page title | `h1` `.page-title` | 64px | **400** | `#222222` | One per page |
| Section | `h2` `.block__title` | 32px | **400** | `#222222` | One treatment with the title, at half the size |
| Lede | `.page-lede` | 20px | 400 | `#494949` | Home, Contact, Teaching, Workshops (§11.1) |
| Paper | `h3` `.entry__title` inside `.entries--offprint` | 20px | 700 | `#222222` | Research's Publications block, and only it (§9.5) |
| Figure | `.result__figure` in `.entries--impact` | 32px | 700 | `#222222` | Home's Impact in Numbers, and only it (§9.4) |
| Record | `h3` `.entry__title`, `.issuer`, `.skill__name` | 17px | 700 | `#222222` | One per record |
| Group | `h4` `.entry__group-title` | 16px | 700 | `#494949` | A part of a record |
| Body / `strong` | | 16px | 400 / 700 | `#373737` / `#222222` | |

Note that body text and a record title are *darker* than the section heading
above them. That is not a mistake; it is the original ramp and it is why the
page reads calm rather than shouty. It is also why the ramp is stated by role
here rather than assumed to descend with the tag number.

**The Figure row is the section heading's size at the other weight.** It is the
second rank in this table set by what a record is rather than by its element,
and it is admissible for the reason the row above it is: a block whose whole
subject is numbers has one element that is the number. It does not read as an
`h2`, because `h2` is weight 400 in a column of its own with 32px of air under
it, and this is bold inside a bordered card. The row exists here because this
table is where a component that wants a rank of its own has to declare it.

**The Paper row is the one rank set by what a record is, not by its element.**
Every other row in this table is an element or a component; that one is an
`.entry__title` that happens to be a paper, and it takes the lede's step
because a peer-reviewed article is the highest-credibility record the site
carries and was set at exactly the rank of the Medium post one block below it.
The argument is §9.5's. It is stated as its own row rather than as a
parenthesis on the Record row because a reader checking what 20px means on
this site should find both users of it in the same column, and because the
next component that wants a rank of its own should have to add a row here.

**The weight column is not decoration in this table.** It is the only place the
ramp does not descend with the size, and the exception is the top two rows: the
two largest things on the page are the lightest headings on it. That is what
keeps a 64px title from reading as a shout, and it is why `h1, h2` override the
shared `h1..h6` weight rather than inheriting it.

**The two top rows are also where the colour ramp stops descending.** They sit
on the same `#222222` the record titles do, which is the reference's rule (one
heading colour, darker than the body) and which retired the `#393939` step
entirely: nothing else was using it. The stepped greys resume beneath them, and
the sentence above about body text being darker than the heading over it is now
true only of the lede and the group title.

**`.page-title` no longer overrides its bottom margin.** It used to reduce the
site's default `--space-5` to `--space-3`, which was right for 25px and wrong
for 40px: 12px is a quarter of the title's own line box, and on Awards it put
the title 12px above a card grid. The override is deleted rather than retuned,
so the title takes the same default every other block-level element does.

**The tags used to say something different from the page.** `h2` was defined
at 25px and used on exactly one page, every other page ran `h1` straight to
`h3`, and every record title on the site was a `<p>` in a bold class, so seven
of eight documents had no second level and none had a record in its outline.
Contact meanwhile used the one `h2` for the same visual rank the others got
from an `h3`, with a hardcoded `font-size` covering the difference.

Retagging changed the outline and not one pixel: the element defaults above are
set to exactly what those components already rendered. **A component that has
to override its own element's default is the warning sign**, and
`.contact-section__title` was it.

### 1.1 The one drawn element

`.diagram` is inline SVG generated at build time, and it is the only element on
the site whose content is a shape rather than type. It is admissible under
Principle 1 on the strictest reading of it: **a reader can print the page and
lose nothing**, because the diagram prints. Colour comes from `currentColor`
and one surface token, so it takes the page's ink in light, dark and print with
no second palette.

Mermaid was the alternative and was rejected for the reasons
[`diagrams.md`](diagrams.md) §2 states: about 100KB of JavaScript per page
carrying one, nothing where scripts are blocked, an empty box in print. An
element that disappears on paper fails Principle 1 on its own terms.

**No diagram is currently drawn**, and this paragraph has now said the opposite
twice, which is the finding worth keeping. `src/data/diagrams.json` is `[]`,
the six `diagram*` classes are back in `STAGED_CSS`, and the renderer is
untouched and tested. Career carried the JACQUEMUS order path and Research the
Ausgrid pipeline; the author withdrew both, the Ausgrid one first and the
JACQUEMUS one two days later. [`CLAUDE.md`](CLAUDE.md) M1 still reserves what a
diagram may claim: the container is the system's, the content is the author's.

**Three have now been built and three removed**, counting the Workshops one.
That drew the teaching stack as five layers read downward, which cost the
renderer a second orientation and the page 380px of its header, and the
author's verdict on it is the one that matters here: it did not earn the space.
Recorded because the shape will look tempting again, and because the test in
[`diagrams.md`](diagrams.md) §1 is harder to pass than it reads: a picture of
what a page already says in words is decoration, however accurate it is. Three
withdrawals is the test working, not the mechanism failing, and the next
proposal should expect to meet the same standard.

**Whoever draws the fourth updates this paragraph and CLAUDE.md M1 in the same
commit.** Both documents spent three days asserting two diagrams that no page
rendered, because emptying the data file is a one-line change and the prose
describing it is not generated from anything.

## 2. Colour

One grey ramp and one blue. Nothing else may be introduced.

- **Links**: `--blue-600` `#267cb9`, the theme's blue (4.6:1 on white, AA).
  Hover is `--blue-800` `#006699`.
- **Rules**: `--rule` `#e5e5e5` for structural hairlines, `--rule-soft`
  `#eaeaea` for the lighter one beneath `.spec__title` and the label columns.
  It was named for the underline beneath section headings, which it no longer
  draws on screen (§1); print still asks it for that.
- **Muted text**: the theme's `#777` was darkened to `#6b6b6b`, the smallest
  change that clears AA at 12px.

**Semantic layer.** Components address `--color-text`, `--color-heading`,
`--color-link`, `--color-border` and so on, never a primitive. Re-theming
means editing one block. `tools/check.py` fails on an undefined token and
reports any token nothing consumes.

**Status colours** exist for tags alone, see §7.

### The dark rendering

**This section used to defer it.** It read: *"Light-only, and it prints
cleanly. Dark mode is deliberately deferred: the brand logos in
`images/icons/` are fixed-colour SVGs that would each need a treatment, and
half-solving it is worse than not solving it."* The reasoning was sound and the
measurement behind it was never taken. When it was, the blocker turned out to
be **three logos, not sixteen**: `github.svg` (which carries no `fill` at all
and so inherits the SVG default of black), `anthropic-light.svg`, and
`opencv.svg`. Nine others are saturated brand colours that read on either
ground, `icon.svg` is the favicon and never appears in content, and
`linkedin.svg` and `medium.svg` are not rendered anywhere: `socials[].icon` in
`src/site.json` is read only for the JSON-LD `sameAs`, which takes the `href`.
Three is a solvable number, so the deferral no longer holds. §6 carries how
those three are handled.

**It defaults to the reader's system setting, and a switch in the brand bar
can pin it.** The default is the important half: *System* is a state the
control returns to, not a third palette, so a reader who never touches it is
followed by their own machine. The control shipped after the theme did, on the
author's call; the argument admitting it is in `CLAUDE.md` §7 with the other
two, and it is the first thing on this site to store anything.

**It is one set of tokens, not two.** Every token that differs is written once
as `light-dark(light, dark)`, and the whole mechanism is the `color-scheme`
property: `light dark` on `:root` follows the system, and
`:root[data-theme="light"]` / `[data-theme="dark"]` pin it. That is the entire
implementation, and the switch sets one attribute.

The alternative was a second block repeating the same forty names under a dark
selector, which Principle 6 calls a defect and which is not theoretical: the
first version of this was written that way, and it immediately grew a
scheme-aware copy of `prefers-contrast: more` to go with it. Merging the palette
deleted that copy, because `--ink-900` now *is* the far end of the ramp
whichever way the ramp runs.

It mirrors the light theme's contrast *relationships* rather than inventing new
ones, so the page keeps the weight it reads with:

| Role | Light | | Dark | |
|---|---|---|---|---|
| heading | `#222222` | 15.9:1 | `#e9ebed` | 14.9:1 |
| body | `#373737` | 11.9:1 | `#c3c7cc` | 10.5:1 |
| muted | `#6b6b6b` | 5.3:1 | `#8b9197` | 5.6:1 |
| link | `#267cb9` | 4.5:1 | `#6fb3e8` | 7.9:1 |

The link is the one value deliberately raised: a 4.5:1 blue on a dark ground
reads thin at 15px. All seven status families were re-derived the same way and
the weakest of them, accent at 7.5:1, is stronger than the weakest in light
(accent, 5.6:1). The ground is `#16181a` rather than `#000000`, because pure
black under light text haloes on long prose and this site is long prose.

The metals carry over unchanged; only the ring flips. On paper it is a darker
shade of the same metal and reads as a struck edge, and on a dark ground a
darker ring dissolves into the page, so it becomes a lighter shade and reads as
a rim light instead.

**One token is a pair for a reason that is easy to get backwards.**
`--color-on-accent` is the ink on `--color-link`, which today is the skip link
alone. It was written as a fixed `#ffffff` on the reasoning that the accent
beneath it is "a strong blue in both renderings". That is false: the link blue
is *dark* in light (`#267cb9`, taking white ink at 4.5:1) and was *lightened*
in dark to clear the ground (`#6fb3e8`), where white falls to **2.3:1** and the
skip link becomes unreadable precisely when a keyboard reader needs it. The ink
flips with the accent instead, and clears 7.9:1. A colour that is dark in one
rendering and light in the other cannot take the same ink in both.

**It still prints cleanly**, and print does it with one declaration:
`color-scheme: light` in §21 resolves every `light-dark()` pair to its light
half, whatever the reader pinned on screen, including the tag families and the
logo treatments. The overrides beside it then flatten what remains to black,
because a CV wants ink rather than the theme's greys.

## 3. Spacing

Built around the theme's **20px block rhythm** rather than a generic 8pt grid,
so the vertical texture of the original page survives:

`--space-1` 4 · `--space-2` 8 · `--space-3` 12 · `--space-4` 16 ·
**`--space-5` 20** · `--space-6` 32 · `--space-7` 40 · `--space-8` 60

`--space-5` is the default bottom margin on every block-level element.
`--space-7` is the column gap and the separation between sections.

## 4. Layout & containers

**One centred column, `--gutter` of padding either side.** Above it sits
`.site-header`: the name, the role, the CV link, and the horizontal `.nav`.
Below it, `.site-footer`.

The container is **`1100px` up to 1024px of viewport, and `1240px` above it**,
where the page context rail appears alongside the column. The extra 140px is
not the site getting wider: it is most of what the rail takes back, so the
records keep close to the width they had. The arithmetic is in the next
section, because it is the whole argument for the rail being admissible.

### `--spine`: the one vertical edge inside the column

**Home is a two-column document, and the second column starts at one x.**
`--spine` is 13rem and the gutter beside it is `--space-6`, so every flowing
column on the page begins at 240px: the bio beside the portrait, the
consequence beside a `.result` figure, the evidence beside a `.skill` name, and
the value beside a `.hero-facts` label.

**It is a token because it was four literals, and they nearly agreed.** The
portrait's track ended at 180 and its text began at 200; the block heading's at
208 and 240; the result figure's at 208 and 228; the skill name's at 240 and
260. Four gutters inside 60px of each other, down one page. Nothing was off by
enough to look intended, and everything was off by enough to see: the page read
as *almost* aligned, which is worse than either alternative, because a reader
cannot tell a system from an accident and stops trusting the ones that are real.

**13rem is where the arithmetic lands, not a preference.** The widest
`.result__figure` (*150+ jobs under alerting*) is 194px, so the figures still
set on one line; the flowing column left at the widest container is 668px
against a 652px `--measure`, so prose keeps its full line. A wider spine eats
the measure and a narrower one wraps the figures.

**What it does not buy is unwrapped capability names**, and that was the
argument for the 15rem `.skill` used to set. Measured, English wraps 3 of 10
names at 15rem and 7 of 10 at 13rem, and French wraps 6 and 9: they wrap at any
width the column can afford, in both languages, so the extra 32px was buying
the one track that agreed with nothing else on the page. A label column that
wraps is a label column; a page with four gutters is a defect.

The spine is Home's today. Any page that grows a second two-column record takes
it rather than choosing its own width.

### The rail, and why it is gone

The theme this site forked from put identity in a sticky 280px rail on the
left: portrait, name, credentials, CV link, contact details and social icons,
scrolling independently of the document. This site shipped that for a year.

It was replaced by a brand bar and a top navigation, and contact moved to its
own page. Three things drove it:

- **The rail answered one question twice.** Identity was in the rail *and* in
  Home's page title, and the two had to be kept in agreement by hand.
- **It cost a quarter of the viewport on every page**, including the pages
  whose records are widest: Career's tag rows, Teaching's spec strip.
- **It put contact details on eight pages** to make them reachable from one. A
  nav item does that for the price of one line.

What the rail was actually good at, keeping the CV link reachable from anywhere
in a long document, is now `.site-header__cv`, at the top of every page, and it
prints.

`--container-max`, `--container-fluid`, `--sidebar-width` and `--column-gap`
were the rail's tokens. They were deleted rather than orphaned: a token nothing
reads is how a stylesheet starts describing a site that no longer exists.

Three came back when the second rail did, under plainer names: `--container`
(1100px), `--container-wide` (1240px) and `--rail-width` (240px). They are
tokens and not literals for a reason worth stating, because the rail shipped
with the numbers written into the component and it took an audit to notice that
`1240px` there had been contradicting the `1100px at most` in this section for
as long as both existed.

### The page context rail, and why it is different

A rail came back. Not the one above, and the distinction is the reason it is
allowed to exist: **the identity rail restated the page, and this one indexes
it.** `.sidebar-context` holds `.book-toc`, a sticky outline of the records on
the current page. It is generated in `tools/build.py` by parsing the page after
it has been rendered, so it indexes exactly what shipped and cannot describe a
record that is not there. It is the left column of `.page-body` above 1024px
and stacks above the content below it.

**It answers each of the three objections above.**

- *The rail answered one question twice.* This one answers a question the page
  never answered at all. Nothing in it is restated: it is a projection of the
  records, in the sense `CLAUDE.md` §7 uses the word, and there is no second
  body of prose to keep in agreement.
- *It cost a quarter of the viewport.* It still does, near enough: 240px of
  track plus a `--space-8` gap of 60px is 300px of 1240, or **24.2%**. What
  changed is that the container widened to absorb most of it. The content
  column runs 940px against the old 1100px, so the cost is 160px, not 300.
  Prose does not notice, because `--measure` caps it at 74ch long before
  either figure. The two cases §4 named as worst affected, Career's tag rows
  and Teaching's spec strip, wrap 160px earlier than they did.
- *It put contact details on eight pages.* It puts nothing on eight pages. Its
  contents differ per page because they are that page's records.

**What earns it is Teaching.** That page is 1,635 words inside a *single*
section, so nothing derived from headings could have helped it: an outline of
this site's headings yields one entry there, and one or two on five of the
eight pages. Indexing records instead yields 23 entries on Teaching, its
courses and then their modules, three levels deep. Career gets 12, its sections
and then the employers and schools inside them. That is the difference between
a control worth having and furniture.

**It does not print.** Section 21 hides it with `.nav` and `.site-footer`, and
resets `.page-body` to `display: block`. An anchor link is dead text on paper,
and the page it would head is a CV.

**On Principle 1**, which says a document rather than an interface: the
argument for admitting a second exception is in `CLAUDE.md` §7, beside the
first.

## 5. Borders, radius & elevation

`--radius-sm` 3px (tags), `--radius-md` 5px (code blocks and the portrait),
`--radius-full` (the award medals, which are drawn in CSS).

**The system is flat, and now completely.** There is no shadow token. There
was exactly one, `--shadow-portrait`, on exactly one element, and it went when
the portrait stopped being a 130px round badge and became a 208 x 260
photograph bounded by the same 1px hairline as everything else the system
gives an edge to. Content is never lifted. Separation is a hairline.

### The hairline has two weights, and they are a rank

`--color-border` and `--color-border-soft` are not two shades of the same idea.
**The strong rule closes a section; the soft rule separates two records inside
one.** Home is where the distinction was first made to carry weight, because it
is the page with the fewest sections and the most rows: three blocks holding
fifteen ruled rows between them, every rule drawn at the same value, so a
reader scanning it got fifteen equal divisions on a document with three parts.

`.block--ruled` draws the strong one. `.result` and `.skill` draw the soft one,
which is the rule `.hero-facts__row` had been drawing since it was written, so
the change made Home agree with its own header rather than introducing
anything. A component that rules its rows takes the soft weight unless it is
ending a section.

## 6. Iconography

Brand logos arrive in wildly different aspect ratios: square, 2500×1184
wordmarks, 412×800 portraits. **Every icon renders inside a fixed square box
with `object-fit: contain`** via `.icon` plus a size modifier (`--xs` 12,
`--sm` 15, `--md` 18, `--lg` 32). This is the rule that keeps logos
undistorted and optically aligned. Icons are never sized inline; the original
sized social marks with `width="15%"`, which is why they never lined up.

Decorative icons take `alt=""`; an icon that is the only content of a link
carries that link's accessible name in its `alt`.

### Logos in the dark rendering

Logos ship as `<img>`, so the stylesheet cannot reach inside them and recolour
a path. Two modifiers say what a mark is *made of*, and §2's dark block acts on
that. Neither does anything in light: the marks are already correct on paper.

| Modifier | For | Dark treatment |
|---|---|---|
| `.icon--mono` | a single-colour black mark | `filter: invert(1)`, which yields white |
| `.icon--plate` | a coloured mark carrying black ink | keeps its colours, gains a white ground |

Both are single unconditional rules reading `--icon-invert`, `--icon-plate-bg`
and `--icon-plate-pad`, which are `light-dark()` pairs like everything else.
`invert(0)` is a no-op and a transparent plate with no padding is invisible, so
the light rendering leaves both marks exactly as authored without a second rule
saying so, and a reader who pins dark on a light machine gets the right marks
because nothing here consults the system directly.

Inverting a monochrome mark is colour substitution, not an effect: there is
nothing else in the mark for the filter to touch, and white is the dark variant
those brands publish themselves. It is wrong for a *coloured* mark, which is
why OpenCV takes the plate instead: inverting it would turn its red, green and
blue discs cyan, magenta and yellow, and it cannot simply be left alone either
because its wordmark path is 7,688 characters against roughly 600 for each of
the three discs, so most of the logo would vanish. The plate is the one fill
the out-of-scope list at the top of this document would otherwise forbid,
admitted because the alternative is a broken logo.

**The treatment is data, not markup.** `ICON_TREATMENT` in
[`tools/build.py`](tools/build.py) keys it by filename so a logo declares
itself once instead of at every call site. A logo absent from that table gets
no treatment, which is correct for a coloured mark and silently wrong for a
black one: nothing fails the build, it simply goes invisible on a dark ground.
Check a new logo's fills before adding it.

## 7. Tags

The one addition to the classic vocabulary, and the one piece of colour on the
page. Tags **classify**; they never decorate. There are two families.

### 7.1 Metadata tags: one treatment per category

A record describes itself through a fixed, declared set of metadata categories
rendered in a fixed order. **That model (which categories exist, what they
mean, what order they take) is defined in the model documents
([`awards.md`](awards.md), [`workshops.md`](workshops.md),
[`teaching.md`](teaching.md), [`research.md`](research.md),
[`writing.md`](writing.md), [`projects.md`](projects.md),
[`career.md`](career.md)), not here.** What belongs here is the single
visual rule that makes it work:

> **The treatment belongs to the category, never to the value.** Amber does not
> mean "good", it means *this tag is a placement*. That is what lets a tag list
> be read positionally after the first record instead of word by word, and it
> is why a value may never be given styling of its own.

Every declared category therefore binds to exactly one `.tag--<category>` rule.
There is one model per record type. The nine in use today:

**Awards**: declared in [`awards.md`](awards.md)

| Variant | Colour |
|---|---|
| `.tag--placement` | Amber (+ medal disc, below) |
| `.tag--distinction` | Amber |
| `.tag--scope` | Violet |
| `.tag--scale` | Grey, regular weight |
| `.tag--duration` | Grey, regular weight |
| `.tag--track` | Grey, regular weight |
| `.tag--stack` | Outlined, regular weight: *the same rule as Career and Projects* |

`.tag--type` was the eighth and is gone. It rendered `Competitive Programming`
and `Hackathon`, which are the two block headings the page's own filter
produces, so every record repeated the `h2` three lines above it; at 181px
`Competitive Programming` was also the widest chip on the page. Removing it
took the rule out of `main.css` with it, because a `.tag--*` rule with no
markup is what `check.py` fails the build on. [`awards.md`](awards.md), *One
model, two blocks*, carries the argument.

`.tag--stack` arrives on this model for the record that built something: the
hackathon's five tools were `<b>` spans inside its prose, which is the device
Projects uses for a bullet's *topic*. One vocabulary for *a thing this was
built with*, per [`CLAUDE.md`](CLAUDE.md) §6.

**Workshops**: declared in [`workshops.md`](workshops.md)

| Variant | Colour |
|---|---|
| `.tag--format` | Blue |
| `.tag--mode` | Violet |
| `.tag--duration` | Grey, regular weight |
| `.tag--audience` | Amber |
| `.tag--scale` | Grey, regular weight |
| `.tag--host` | Grey, regular weight |

**Teaching**: declared in [`teaching.md`](teaching.md)

| Variant | Colour |
|---|---|
| `.tag--level` | Amber |
| `.tag--workload` | Blue |
| `.tag--scale` | Grey, regular weight: *the same rule as Awards* |

**Research**: declared in [`research.md`](research.md)

| Variant | Colour |
|---|---|
| `.tag--status` | Amber |
| `.tag--authorship` | Blue |
| `.tag--publisher` | Grey, regular weight |

**Writing**: declared in [`writing.md`](writing.md)

| Variant | Colour |
|---|---|
| `.tag--format` | Blue: *the same rule as Workshops* |
| `.tag--reach` | Violet: *the same hue as Awards' `scope`* |
| `.tag--platform` | Grey, regular weight |

**Projects**: declared in [`projects.md`](projects.md)

| Variant | Colour |
|---|---|
| `.tag--kind` | Blue |
| `.tag--upstream` | Amber: *the same rule that puts `status` in amber on Research*, and carries a link to the pull request |
| `.tag--stack` | Outlined, regular weight, one chip per tool |

**Skills**: declared in [`skills.md`](skills.md)

| Variant | Colour |
|---|---|
| `.tag--production` | Green: *the hue §7.2 gives to verified/shipped* |
| `.tag--certification` | Blue |
| `.tag--taught` | Violet |
| `.tag--published` | Amber |
| `.tag--applied` | Grey, regular weight |

> **The one model whose categories repeat.** Everywhere else a category is a
> *dimension* of the record and holds one value. On Skills the categories are
> *citations*, and citations accumulate: three certifications are three
> artifacts, not one dimension with three values. Positional reading is given
> up for colour-run reading: the fixed order means a row that starts green ran
> in production and a row that starts blue did not.
> [`skills.md`](skills.md) argues it in full. This is an exception with a
> written case, not a precedent: a second one needs its own.
>
> **There is now a second, and it made its case on different ground.** `stack`
> renders one chip per tool because it is the *terminal* category in every
> model that declares it, so a run of varying length shifts no earlier
> position, and because a joined value did not fit a phone. Skills gave up
> positional reading in exchange for colour-run reading; `stack` gives up
> nothing, which is why the two exceptions do not generalise into a third.
> [`projects.md`](projects.md) carries it.

**Experience**: declared in [`career.md`](career.md)

| Variant | Colour |
|---|---|
| `.tag--domain` | Blue |
| `.tag--engagement` | Amber: *the standing of the record, as `placement` is on an award* |
| `.tag--mode` | Violet: *the same variant Workshops uses, for the same question* |
| `.tag--scale` | Grey, regular weight, figure in bold: *the same rule as Awards and Teaching* |
| `.tag--stack` | Outlined, one chip per tool: *the same rule as Projects* |

**Education**: declared in [`career.md`](career.md)

| Variant | Colour |
|---|---|
| `.tag--programme` | Amber: *the standing slot, as `engagement` is on a job* |
| `.tag--focus` | Blue: *the substance slot, as `domain` is on a job* |
| `.tag--accreditation` | Grey, regular weight, and carries a link to the accrediting body |

**Impact in Numbers had a model here and no longer has one.** It declared
`result` (amber), `figure` (grey, value in bold) and `source` (grey, linked,
the one linked tag that stayed inside the site). All three are deleted with the
block's move to `.result` (§9.3): a figure that leads at 17px does not need a
chip to carry it, and a provenance line says what the `source` chip said
without repeating the word *Career* in four rows out of five.

It is worth keeping as the worked example of the rule below. The category was
`result` and not `kind` because Projects already spends `kind`
on what sort of artefact a project is, and the rule allows a shared name
only where two models mean the same thing by it. *Kanboard Plugin* and
*Recurring saving* are not the same kind of answer, so they do not share a name.

**Whether a linked tag opens away from the page is derived from its address**,
never declared beside it: `render_meta` marks a tag `.link-external` and gives
it `target="_blank"` when the URL has a scheme, and leaves an internal citation
bare. Marking an internal link would tell the reader it leaves the site.

Education is the one model where **no record renders every category**, by rule
rather than by accident: a category renders only where its answer is not
already in the record's own title. Two records, two tags then one.
[`career.md`](career.md) §2 works it through.

`status` is the sharpest illustration of the rule above. *Published* and *In
Progress* take the **same** amber, because the treatment says *this tag is a
status* and never *this status is the good one*. The hand-written version of
the Research page gave *Published* a green and *In Progress* an amber, which
read as a verdict on the record rather than as a category, and would have made
the tag unreadable positionally the moment a third status appeared.

`scale` is borrowed rather than added: it means the size of the thing a record
involved wherever it appears (`86 teams`, `12 students`, `150+ pipelines`) so
it keeps one name, one meaning and one rule across the models that use it. What
is being counted changes with the page and the unit says which; the question
the category answers does not change, which is what makes it one category and
not three. A shared name
that meant two different things would be the defect; a shared name that means
one thing is the system working. `format` is borrowed on the same terms: on
Workshops and on Writing alike it names the shape the deliverable takes (a
`Hands-on Lab`, a `Configuration Guide`) so it too keeps one rule.

`reach` is the reverse case done right: a **new name** on a **reused hue**.
Violet is what this system already spends on how far something travelled
(`scope` for an award, `mode` for a room, `reach` for an article) so a reader
who has learned the mapping anywhere reads it here without being taught again.
The hue was not picked for the category; it was already the answer to the
question the category asks. Reuse the *treatment* whenever the question is the
same; reuse the *name* only when the answer means the same thing.

`publisher` and `platform` are the reverse test, and the reason the Research
page's two blocks do not share a model. Both sit last, both are grey, and both
answer *who stands behind this*, but *Elsevier* peer-reviewed the work and
*Medium* hosted it, which are not the same claim, so they take separate names.
The shared treatment is what lets a reader scan the page and find the answer in
the same position both times; the separate names are what stops the second
block borrowing the first block's authority. Reuse a category when the meaning
is identical, never when only the position is.

**No two categories in one model may share a treatment.** Two *different*
models may reuse a hue, because they are never read side by side: a reader
learns the mapping per page, from the first record. What breaks the system is
ambiguity within a single tag list, not across the site. Adding a category
means adding one row here and one rule in `main.css`, never a colour decision
inside a page.

`.tag--scale`, `.tag--duration`, `.tag--track`, `.tag--host`, `.tag--publisher`,
`.tag--platform` and `.tag--accreditation` are the metadata tags at
regular weight: a field size, an event duration, a hackathon track, a cohort size,
the organisation that ran the room, the house that published the paper, the site
that hosts the article, the tools a project is built from, the body that accredits
the degree. All are context for the record rather than claims of their own, so
the eye lands on the categories before them first.

`accreditation` is the newest member and the one that had to be *moved* into
the family. The hand-written Career page gave it `.tag--success` (the green
below, reserved for *verified / published / shipped*), which graded the value
instead of naming the category, and borrowed a utility treatment for a
dimension of a record. It answers the same question `publisher`, `host` and
`platform` answer, so it takes their treatment and keeps its own name.

**A metadata tag may carry a link without changing colour.** Two categories do:
`upstream` points at the pull request and `accreditation` at the accrediting
body, and in both cases the destination is the evidence for the claim the tag
makes, so the tag is the route to it. One is amber and one is grey, which is
the rule working: the link is a destination, not a kind, so it changes
nothing about the treatment the category already had.
Utility tags such as `.tag--critical` on a slide deck link for the different
reason that the artefact *is* the tag.

**A category holds one value.** An earlier draft of the Teaching model gave
`stack` a list of tool names, rendering one tag per tool. It was removed: a run
of tags whose length changes per record destroys the positional reading the
fixed order exists to provide, and a tool name means more beside the thing it
was used for than it does in a row. Technologies are now named inside the
syllabus module that teaches them.

The hand-written Career page was the last place that rule was broken, and it
broke it twice in one tag list: three to five loose technology chips per job,
with the headline tool given `.tag--accent` and the rest `.tag--neutral`. The
varying length meant no column existed to read down, and the accent graded a
*value* (*Talend is the important one*), which is the thing rule 4 forbids.

**`stack` is the one declared exception, and it is an exception about
position.** It renders one chip per tool, because it is the terminal category
in every model that declares it and a run whose length varies at the *end*
shifts nothing before it: every earlier category still lands where the reader
expects. It is also the only way the value fits a narrow viewport, since a
`.tag` is `white-space: nowrap` and a joined stack ran to 58 characters. The
two defects above are unaffected and still forbidden: the chips render *after*
the fixed categories rather than instead of them, and no tool is graded above
another. [`projects.md`](projects.md) carries the full argument, and the
boundary is that `stack` stops being splittable the day it stops being last.

To keep the two readings apart, tool chips are **outlined rather than
filled**: a filled chip is a dimension of the record, an outlined one is an
item inside a dimension. That is the third exception on the site to one
treatment per category, after Skills and the medal disc, and like them it earns
its place by drawing a distinction the reader would otherwise have to infer.

**Medals.** First, second and third place carry a small struck-metal disc
(`.medal--gold` / `--silver` / `--bronze`) before the label. It exists so the
top results are recognised *before* the text is read, and it is what makes
wording like "Winner", "Champion" or "Runner-up" unnecessary: the label stays
factual and the medal does the signalling. The disc is drawn in CSS, sized in
`em` so it tracks the type, `aria-hidden` because the text beside it already
says "1st Place", and forced through to the printer because greyscale would
lose the one thing it encodes.

### 7.2 Utility tags: single facts

For the things that are not dimensions of a record. Written by hand where they
apply; no ordering rule, because they do not form a sequence.

| Variant | Meaning | Example | In use |
|---|---|---|---|
| `.tag--neutral` | Factual context | `Azure`, `Graduate Level` | - |
| `.tag--accent` | Role or category | `Instructor` | - |
| `.tag--success` | Verified, published, shipped | `Article on Medium` | Projects |
| `.tag--honor` | Distinction or pending status | `In Progress` | - |
| `.tag--critical` | Downloadable artefact | `Slides (.pptx)` | Workshops |

Violet is the only hue this system added, and it was added for scope alone: it
had to be unmistakable beside the blue that a record's type carries, without
borrowing the green that means *verified* or the red that means *download*.

**Three of the five currently have no markup using them**, and `check.py`
reports that as a note rather than a failure. It is the expected end state, not
neglect: `.tag--neutral`, `.tag--accent` and `.tag--honor` were what the
hand-written pages reached for whenever a record had a fact and no category to
put it in: `Azure` on a job, `Instructor` on a course, `In Progress` on a
paper. Every one of those facts is now a declared category on a model, which is
the point of §7.1. The rules stay because a genuine one-off will appear again;
what may not happen is a page reaching for one *instead of* declaring the
category it needs.

## 8. Interactive states

Every interactive element defines rest, hover and `:focus-visible` (2px blue
outline, 2px offset).

Links get colour plus an underline on hover, **never a weight change**. The
original's `a:hover { font-weight: bold }` reflowed the sentence under the
cursor.

**Colour is the rest state, not the hover state.** `a` and `.entry__title a`
are `--color-link` before anything touches them, and the underline is what
hover adds. `.contact-list__link` was the one component that opted out, painting
its value in `--color-heading` so that six rows on the page whose entire job is
to be acted on looked exactly like the two rows that are statements. It follows
the rule now, and gets a second thing for free: three blocks share one
component there, and the ink is what separates an address a reader can act on
from a description of the work being accepted.

There are no buttons in the content flow. The CV is a plain link under a
"Downloadables" heading, as it was.

## 9. Content records

One component, `.entry`, is used for every record on the site: a job, a
project, a paper, a course, a workshop, an award. It is a **bulleted list
item**, exactly as the original CV pages were written by hand:

```
• Title · Role                    .entry__title / .entry__role
  Aug 2024 - Present (2 years)    .entry__period   (smaller, muted, upright)
  [tags] [tags] [tags]            .tag-list        (§7, fixed order)
  One or two framing sentences.   .entry__summary  (optional)
  - point                         .points
  - point
```

**That order is fixed for every record on the site**, and it is the order the
three readers arrive in (§2 of [`CLAUDE.md`](CLAUDE.md)): what and when, then
the scan line, then the framing, then the evidence. A recruiter reading for
seconds gets the first three lines and stops; the summary and the bullets are
there for whoever keeps going.

Experience was the one renderer that broke it, printing a sixty-word company
summary between the dateline and the tags, which put the page's densest
paragraph in front of its fastest layer on the page a recruiter opens first.
Six renderers against one settled it and Experience moved.

The sanctioned insertions are Research's citation line
(`.entry__meta`), which sits between the period and the tags because a paper's
authors and venue are part of identifying it rather than commentary on it:
[`research.md`](research.md) argues it; and Projects' proof footer, which sits
after the project's technical group because a repository, demo, article, or
slide deck is a **place a reader can go and look** rather than a fact about the
record. [`projects.md`](projects.md) carries that exception, and the line it
draws is now sharp: the upstream pull request used to render in that footer and
does not, because an acceptance is a standing rather than a destination, and
every other record on the site states its standing in the scan line. It carries
no visible label either; the hairline draws the rank, and the deleted `Project
proof` line named the component instead of saying anything about the record.

The period line is **never italic**. A smaller size and the muted ink already
say *secondary*, and a third de-emphasis signal on top of those buries a fact
the recruiter reader scans for first. Career's records carry the location on
this line too (`Paris, France &middot; Aug 2024 - Present`), because a city is
the same kind of fact as a date and belongs beside it, not inside the title.

A title line separates its parts with `&middot;`, the site's one peer
separator. There is no second separator glyph: a run of pipes flattens facts of
different rank into one rank, which is how a header stops being scannable.

The tags carry the record's *metadata*; the bullets carry its *substance*. A
fact stated by a tag is not repeated in a bullet: "1st Place" and "86 teams"
are the tag list's job, so the bullets are free to say what was actually done.

**Records are stored as data, not markup: whether or not they carry a
metadata model.** Every file in `src/data/` holds records; the matching
fragment in `src/pages/` holds only the section heading and its intro, and
interpolates the rendered block. This is what makes the ordering and colour
rules structurally true rather than a convention someone has to remember.
[`awards.md`](awards.md) states the rules a new page follows to do the same;
[`workshops.md`](workshops.md), [`teaching.md`](teaching.md),
[`research.md`](research.md), [`writing.md`](writing.md),
[`projects.md`](projects.md) and [`career.md`](career.md) are the worked
models.

Certifications, Online Courses and Volunteering are the case that shows the two
halves are separable: they are data (`src/data/certifications.json`,
`src/data/courses.json`, `src/data/volunteering.json`) and they carry **no**
metadata model. Who issued a
credential is its only dimension a reader needs, and that is already the
`.issuer` heading the group sits under, so a tag would restate the heading on
every row. [`career.md`](career.md) §3 has the reasoning. Volunteering is a
single record and still comes from data, because one hand-written `.entry` is
how the second one gets hand-written too. §10 carries the matching rule for
the "label: values" content that is *not* records.

Optional `.entry__group` subdivides a long record (Data Integration / Cloud &
Security / Observability) and is emitted by one helper, `render_group`, shared
by a job's disciplines, a course's syllabus modules and a workshop's parts.
`.issuer` heads a credential group with its brand mark.

**Projects use that group as a dossier detail.** Their technical bullets sit below a
`What was built` label directly under the summary. All artefact links (repository, live demo,
slides, article) render alongside `kind`, `upstream` and `stack` in the top metadata scan
line tag list directly under the title.

**The workshop case is the one that arrived by conversion**, and it is the
clearest statement of what the component is for. A two-part series carried its
structure inside its own bullet text: `<b>Part 1.a: Efficient data &amp; code
execution:</b>` opened a bullet with two bold spans and two colons, so the
record was rendered flat while its own prose insisted it was not. The group
title states the part and the bullet keeps `<b>` for its topic, which is the
single job that device has on this site ([`CLAUDE.md`](CLAUDE.md) §6). A record
whose bullets are numbering themselves is asking for this component.

Entries are **never boxed**. A CV is a document, not a feed of cards.

### 9.1 The one record that is not an `.entry`

`.skill` is the exception, and it earns it by being a different kind of
statement. Every `.entry` on the site reports **something that happened**: a
job held, a paper published, a contest entered. A skill is a **claim about
capability**, which is the one assertion a portfolio cannot be trusted on, so
the component is built so the claim cannot appear without its proof:

**It is the one two-column record on the site.** A `--spine` label column (§4)
holds what the capability *is*; the right column flows and holds the proof:

```
In production, and verified outside it                     .skills__band
──────────────────────────────────────────────────────────────────────
.skill__name (--spine)      .skill__proof (flows)
Data pipeline engineering   [Azure Data Factory & Fabric at JACQUEMUS]
                            [API-led integration at OLIVESOFT]
                            [Talend Data Integration] [MuleSoft L1]
                            [Astronomer ×2] [Data Engineering 1 & 2]
                            (Talend) (MuleSoft) (Apache Airflow)
                               .tag-list (§7, fixed order) then .skill__tools
```

**A five-slot presence gutter was built between the two and deleted on the
author's verdict**, which is the same standard the third diagram was held to
([`CLAUDE.md`](CLAUDE.md) §8, M1). It rendered which kinds of proof each row
had as five discs, filled or empty. It was accurate, it cost 82px and three
French chip lines, and it summarised in marks what the row already says in
words one column to the right. Accuracy is not the test; earning the space is.

**The standing left the row and became `.skills__band`**, printed once above
the run of rows that share it, with each run its own `<ul>` labelled by its
band. Seven of the ten rows derive the strongest standing, so as a caption it
printed one string seven times down the column that exists to be run down, and
it was the second rendering of a fact the leading chip's colour already gave.

**The three bands are named compositionally**, and they were not: they read
*Production-proven*, *Run in production* and *Verified: not yet in production*,
so the top two were near-synonyms in an order no reader could derive from the
words, and the second was **verbatim** the first chip of the key above it. They
are *In production, and verified outside it*, *In production* and *Verified,
not yet in production*: the same two booleans `standing()` reads, ranked by
inclusion, so the second band is visibly the first one minus a clause.
The band is a `<p>`, not a heading, so the block still runs `h2` then `h3` and
the page context rail does not index it. [`skills.md`](skills.md) carries the
argument, including the one it overrules.

**`.skill__head` is gone with it.** With the standing out of the row the
wrapper held one `h3`, so the `h3` is the grid's first child.

**The tools list moved below the evidence.** It led every proof column with
outlined grey chips, which made [`skills.md`](skills.md)'s colour-run claim
(*a row that starts green ran in production*) false of the markup: every row
started grey. That document argues against **merging** the two lists and never
argued for their order.

The split exists because the block could not be read without it. Capability,
tools and forty citations all ran from one left edge, so the ranking the block
computes for itself was invisible: nothing lined up well enough to look ordered.
A fixed label column is the same device `.contact-list` uses (§11), for the same
reason. It collapses to one column at ≤720px, where the spine beside a chip run
would leave the chips about nine characters wide.

**The column was 15rem and is now `--spine`.** It was the widest of the four
label tracks on Home and the only one nothing else agreed with. The 32px it
gave up does not cost what it looks like: capability names wrap at both widths
in both languages (§4 carries the counts), so what the wider column was buying
was a longer first line on three rows out of ten, at the price of the page's
alignment.

**It is not boxed and it is not a table.** §9 above: a CV is a document, not a
feed of cards. And a true five-column proof matrix (production / certification /
taught / published / applied) would need every citation cut to roughly fifteen
characters to fit the column, which is exactly the specificity that makes a chip
worth clicking, and would leave 23 of 50 cells empty. The hairline between rows
does what a card border would, at none of the cost.

**Boxing it was re-measured when Impact in Numbers took a card grid, and it
fails worse than that paragraph says.** `.tag` is `white-space: nowrap`, so a
chip is an atom: at three 255px tracks the chip run packs into 60 lines instead
of 28, and two English chips and **seven French ones** are wider than the box
they would sit in. The gutter is the only form of the matrix this column can
hold, because it states which kinds exist without trying to lay the citations
out in columns.

Five things make it work, all argued in [`skills.md`](skills.md):

1. **Every chip is a link to a record elsewhere on this site**, so `check.py`
   fails the build on a citation that points nowhere.
2. **The standing is derived** from which kinds of evidence exist, never
   typed, never chosen, and the block sorts itself by it.
3. **The standing carries no colour.** It is a *value*, and §7.1 forbids
   styling a value. The gradient is carried by the chips, whose fixed category
   order makes the leading colour of a row meaningful on its own.
4. **Tools take the site-wide `stack` treatment**: outlined, one chip per tool,
   regular weight, exactly as Career and Projects render them, so "a thing this
   was built with" looks the same everywhere. They render on their **own list
   below** the evidence and are never merged into it. The colour-run reading in
   point 3 is a claim about the colour of a row's *first* chip, and an outlined
   tool chip in front of the run would destroy it, which is what it was doing
   while this line said *above*.
5. **A key (`.tag-list--key`) names the five colours once, above the block.**
   Five specimen chips rather than a worded legend, because the thing being
   explained is a chip. It is the only tag list on the site whose chips cite
   nothing, and the only one that does not print: the print stylesheet forces
   every colour it explains to black.

No percentages, no ratings, no bars. A self-assessed level is an opinion; "run
in production and certified twice" is a pair of facts with links on them.

### 9.2 `.point__impact`: the second register inside a bullet

A bullet on Career does two different jobs. It states **what was built**, which
is what the engineer reader is scanning for, and it states **what changed
because it shipped**, which is what the hiring manager is scanning for. Written
as one sentence, the second half arrives after a semicolon or inside a trailing
participle (*"...; preserved morning reporting SLAs"*), where neither reader
finds it.

`.point__impact` is a block-level `<span>` at the end of the `<li>`, opened by a
bold `Impact:` label:

```
- Reduced Azure infrastructure spend by €1,400 per month by automating
  development-environment shutdowns, matching compute size to each
  environment, and redesigning shared Spark pools.
      Impact: a recurring saving, taken with no SLA impact on the morning
      reporting pipelines.
```

Three decisions:

- **The label keeps the heading ink, the sentence does not.** The sentence is
  muted and one step down in size, so the bullet still reads as the primary
  statement; the label stays dark because it is the anchor a recruiter scans a
  column of bullets for. The inverted weighting `.specs` uses (§10.1), applied
  to prose.
- **It is a span, not a nested list.** A second `<ul>` inside the `<li>` would
  say *these are sub-points*, and there is only ever one. Printed, the line
  stays with its bullet.
- **It is not on every bullet, and that is enforced editorially, not
  visually.** The rule for which bullets earn one is in
  [`career.md`](career.md) §6. A page where every bullet carries an impact line
  teaches the reader to skip the line by shape.

The label text lives in `IMPACT_LABEL` in `tools/build.py`, never in the data:
[`awards.md`](awards.md) rule 7.

### 9.3 `.result__*`: the parts of a figure-led record

Four parts, in this order and this rank, used by Awards' scope summary,
Workshops' host cards and Home's Impact in Numbers:

```
€1,400                                                        result__figure
per month                                                     result__unit
A recurring monthly saving on the platform budget, taken      result__consequence
with no SLA impact on the morning reporting pipelines.
JACQUEMUS · Since 2024 · Career                               result__source
```

The figure leads at `--text-xl` in heading ink (`--text-2xl` in Impact in
Numbers, §9.4), with the unit on the line beneath it at `--text-md` in muted
ink. The consequence follows at body size, capped to the measure. The
provenance line closes it at `--text-sm` in muted ink.

**There is no `.result` row component any more, and there was.** It was a
two-column record hanging the figure on `--spine` with the consequence beside
it, and it was retired on its own measurements: the widest figure cell is 125px
in English and 143px in French against a 208px track, so a third of the column
was idle on every row, and the five records rendered as five 112px rows with
nothing saying which one the author put first. Impact in Numbers is
`.entries--grid` now (§9.4). The parts above are unchanged, which is the point:
they were never the thing that was wrong.

**The provenance line carries a year, and for two months it carried none.**
[`home.md`](home.md) documented the period as one of three things derived from
the `cite` id, and argued that it is what stops *100x faster* (2022) from
reading as current beside two *Aug 2024 - Present* results. The renderer
printed the company and the page and nothing else the whole time. It is years
rather than the `month_year` range the dateline uses, because *Aug 2024 -
Present* already renders in Currently one block above and a saving accrues
across a job rather than in a month.

**It was one line at `--text-lg`, the slot and the size `.entry__title` had,
with the unit set beside the value and separated from it by weight alone.**
That is the rank `.skill__name` also holds, so the number the block exists to
show was the fourth of the page's seven type steps, 1.06 times body. And the
five values never formed a column, because what filled the track was the
value-plus-unit pair, at 88, 141, 155, 188 and 194px.

**The one-line guarantee that used to stand here was measured in one
language.** It read *"every figure the block carries fits it on one line; the
widest, 150+ jobs under alerting, is 194px against 208px, and that measurement
is one of the two that set the spine's width."* True in English. The French
*Zero donnée d'avis perdue* is **216.6px in a 208px track** and wrapped.
Split into two ranks, the widest cell in either language is the French
*donnée d'avis perdue* at 143px, so the guarantee holds now for a reason
rather than by luck. The spine's width is still set by the other of its two
measurements (§4).

**`result__unit` is not `result__scale`.** The two look alike and sit in the
same place under a figure, and they answer different questions: `scale` is how
large the field was (*of 7,094 teams*), a unit is what the figure counts (*per
month*). §7.1 lets two models share a name only where they mean the same thing
by it, which is the rule that keeps `publisher` and `platform` apart.

**Why this is not an `.entry`.** It was one. `.entry` is the component for a
dated record living on its own page: a job, a project, an award, each with a
title, a period and a body of its own. An Impact in Numbers record has none of
those. It is a pointer to a result, and forcing it into `.entry` required
inventing all three:

| `.entry` required | The block invented | The cost |
|---|---|---|
| A title | A topic label (*Azure cost control*) | 17px bold for a category |
| Metadata tags | A `figure` chip | 12px grey for the number the block exists to show |
| A period | A company dateline | *Aug 2024 - Present* rendered three times on one page |
| A uniform shape | A bare `2026` | The one non-job record looking broken |
| Nothing that links | A `source` chip | An identical grey *Career* in four rows of five |

A reader scanning the block got categories, not outcomes. §10.1 had already
stated the correct principle for the spec strip (*the reader is scanning the
figures, so the label recedes and the value carries the weight*) and it is far
more true here.

**This is the fourth user of the label-column idiom** (`.contact-list__row`,
`.skill`, `.hero-facts`, `.result`). That is now the site's answer to "a short
fixed thing and a long flowing thing side by side", and a fifth case should use
it rather than invent a sixth shape.

**`.perf` is the fifth, and it is the one that lives inside a record.** A
contest result's score and team size, on Awards. It takes the idiom at its
smallest: `--text-md`, **no hairline between rows** (a rule inside a bulleted
record draws a table inside a bullet), and **no left inset of its own**,
because `.entries` already carries the 1.4em that makes the bullet gutter.

**Its pairs sit side by side, not stacked**, on `.specs`' own
`repeat(auto-fit, minmax(14rem, 1fr))` (§10.1). A contest carries two
measurements and both are short: the widest cell is the French
`Problemes 11 / 26 resolus` at 224px against the 290px each column gets, so
stacked they left most of a 589px strip empty and read as the opening of a
longer list. The outer grid and the inner rows collapse **together** at 600px,
because auto-fit alone still fits two 14rem tracks at that width and would
stack the labels inside columns that had not collapsed: two columns of
label-over-value, which is neither layout.

**Going sideways cost it two things it had been given while stacked, and this
is the general lesson.** A fixed 7rem label track is what a label column needs
when its labels *share* one column and align down it. Side by side each label
sits alone in its own cell, so the track became air: `Team` used 37px of 112px
and its figure sat 75px away, while the two pairs were only 20px apart, so the
gap inside a pair beat the gap between pairs and the eye read four things
instead of two. The label sizes to its content now, at 16px inside a pair
against 32px between them. **When a label column turns through ninety degrees,
re-derive its track and its gaps; they were solving a problem it no longer
has.**

**Its ink is `.spec__row`'s, and briefly was not.** `dt` in `--color-text` at
regular weight, `dd` in `--color-heading` **bold, unit included**, exactly as
`.spec` renders `20 h`, for the reason that component's own comment gives:
*the reader is scanning the figures, so the label recedes and the value carries
the weight.* It had shipped with a third recipe, a muted label against a
heading-ink value with a `<b>` inside that was heading ink too, so a figure and
its unit differed by weight alone and one two-word cell carried three inks. The
`<b>` is gone from the renderer as well: emphasising the numerator and not the
unit would have been [`awards.md`](awards.md) rule 4 broken, styling part of a
value rather than the whole category. It has **no left inset**, as the
paragraph above says: the sentence that used to stand here claimed it took
`.points`' 1.4em, which was true of the first version and was removed in the
same pass that turned it sideways, because a `<ul>` earns that inset by drawing
markers into it and a `<dl>` draws none.
What it replaced was four facts welded into a prose sentence in the data
([`awards.md`](awards.md), the performance spec); what it is *not* is two more
chips, because a tag files a record under a category and a solve count is a
measurement.

**`.hero-facts` is the one that travels.** It renders in Home's hero and in
Contact's page header, carrying the same `availability` sentence in both, which
is the point: a reader who met the shape on the front page meets it again where
the decision gets made. Its stylesheet section is headed `(HOME ONLY)` for
`.hero-header`, which is true, and said the same of `.hero-facts`, which was
never enforced by a single selector.

**Travelling made two of the four meet, and they did not agree.** Contact
stacks `.hero-facts` and `.contact-list` about 40px apart, and they were set
differently on four counts: `.contact-list` carried no measure cap and ran the
full 908px content column while the strip above it stopped at 611px, ruled its
rows on the bottom edge instead of the top, used `--space-4` of row padding
against the strip's `--space-3`, and set a 10rem label column against the
strip's 7.5rem. Reconciled at **10rem**, which is the width the
content forces (`Consulting & services` measures 141px and the French
`Telephone / WhatsApp` 150px, so 7.5rem was not a width the two could meet
at): both cap at `--measure`, both rule on the top edge with the first row
reset, and both collapse to one track at 600px.

**The rule is that columns sharing a page share a width, not that the idiom
has one.** It is now stated twice on one site, in two widths, and the second
statement is what proves it is a rule rather than a number.

On **Contact**, `.hero-facts` is stacked 40px above `.contact-list`, so it
takes that pairing's width: **10rem**, forced by `Consulting & services` and
the French `Telephone / WhatsApp`.

On **Home**, the same component is stacked above `.result` and `.skill`, so it
takes theirs: **`--spine`**, 13rem, which is why `Availability`, `Certified`
and `Languages` begin their values at the same x as every figure and capability
below them (§4). The override is scoped to `.hero-header__content > .hero-facts`
and held in a `min-width: 601px` query, so the 600px collapse both pages share
still wins without a specificity race.

**One component, two widths, and neither is drift**: each is the width of the
column it is read beside. A third page adopting `.hero-facts` measures what it
sits next to before choosing.

What the other
three do share, and what `.contact-list` alone was opting out of, is the top
edge rule with a `:first-child` reset: ruling on the bottom left a hairline
under each block's last row, a row's height above the next section heading,
which in those days carried an underline of its own.

**Values in this idiom are set flush left.** `.contact-list__value` was the
one exception, set right, which held only while nothing wrapped: capped at the
measure the value column is 435px and the consulting sentence is 520px, so it
wraps, and a wrapped value set right sets ragged against the label it answers.
The availability sentence one block above it wraps the same way and has always
been left.

**A record in a reading list is never boxed**, and neither is this. That
sentence used to read *entries are never boxed*, flatly, and it was never
true: `.entries--grid` has boxed the credential cards on Career since long
before it was written. The distinction it was reaching for is real and is
§9.4's subject: a record you **read** is a bulleted item in a column of prose,
and a record you **count** is a cell in a grid.

### 9.4 `.entries--grid`: the card grid

The one place a record is boxed. `.entries` becomes
`repeat(auto-fit, minmax(18rem, 1fr))`, drops its bullets, and each `.entry`
inside gains `--space-3`/`--space-4` of padding, `--color-surface`, a
`--color-border-soft` hairline and `--radius-md`.

```
┌────────────────────────────┐  ┌──────────────────┐  ┌───────────────────────┐
│ Microsoft                  │  │ Regional         │  │ Custom YOLOv8 for…    │
│ • Azure Database Admin…    │  │ 1st Place        │  │ 2023                  │
│ • Fabric Data Engineer…    │  │ of 86 teams      │  │ ───────────────────── │
│ • Fabric Analytics Eng…    │  │ Hello World v4.0 │  │ • Annotates the meter…│
└────────────────────────────┘  └──────────────────┘  └───────────────────────┘
  Career, Certifications          Awards, the scope       Research, Technical
                                  summary                 Articles
```

**What earns a box.** A cell whose records are a **set to be counted, not a
sequence to be read**. Three Microsoft certificates and one MuleSoft is a
shape the reader takes in at a glance and never reads top to bottom; so is
*this person reached four scopes and here is the best result in each*. A job
history is the opposite: it is read in order, one record informs the next, and
boxing it would cut the thread. That is the whole test, and it is why Career's
Experience and Awards' own eight records stay unboxed on the same pages that
carry a grid.

**Technical Articles is the case that tested the word *counted*.** Two Medium
posts are read, in the ordinary sense that a reader opens one and reads it, so
the test looks as though it should refuse them. It does not, because the test
is about the *list* and not about the thing at the end of the link: nobody
reads a list of two articles top to bottom to see how the second follows from
the first. They scan it to see what is there and whether the reach figure is
worth a click, which is a set being counted.

**The shape of the record was read as evidence for that, and it has since
changed.** An article used to carry a title, a year, three chips and one
sentence and **no `.points`**, so it was the only record on the page with
nothing to read in order. In the reading column that did not make it look
different from a paper; it made it look like a paper that had run out of
content, which is the defect the grid actually fixes. It carries three bullets
now ([`writing.md`](writing.md)), and the verdict is unchanged, because the
test above is about the *list*: the empty array was corroboration, not the
reason. What the box then turned out to be good for is in §9.6.

**It is also where the page changes register**, from the clinical half of
[`CLAUDE.md`](CLAUDE.md) §6 to the warm one, and the grid is what makes that
visible: Research's column breaks exactly once, on the line the voice map
already draws. That is a second reason and not the first. A block does not earn
a box by being a different register; it earns it on the test above, and this
one passes before the register is mentioned.

**Home's Impact in Numbers is the fourth cell, and the one that takes a track
of its own.** `.entries--impact` sets `minmax(20rem, 1fr)` and spans the first
record across both columns. Two numbers force both decisions. The base `18rem`
track lets `auto-fit` place **three** columns in the 908px content column,
which leaves 255px of measure and sets a 185-character quoted sentence as seven
lines; `20rem` needs 1000px for a third track, so it holds at two, which is the
444px card (410px of measure) the block was measured against. And the lead card
spans because [`home.md`](home.md) says the order of that block is the
argument and the block had no way of showing it: five equal rows said nothing
about which record was chosen to open. It is `:first-child` and not a modifier
class, because the lead is not a property a record can carry, it is whichever
record is first.

Its figure steps to `--text-2xl` (§1), which is the one rank change: at
`--text-xl` the unit was the wider mark on four of five English rows and three
of five French ones, so on the block whose title promises numbers the eye
landed on 14px muted text first. `2` measured 11px of ink above *Kanboard
plugins* at 117px.

**It takes the base `18rem`, not `--compact`.** The compact track was cut for a
card of four short lines; an article card holds a wrapping title of eighty-odd
characters and three bullets under it. Two tracks and one `--space-5` gutter in
the 908px column give a card 444px, about 410px of measure inside the padding,
which the title fills in two lines and each bullet in one or two. That is the
opposite of the failure `.awards-stats` is charged with below, where a visibly
bordered element was half empty.

**The four cells are not the same cell, and that is the point.** A
certifications cell is a heading and a list: the issuer in `.issuer` (it has a
logo, so it is a flex row) and its certificates in `.points`, because three
certificates are a set to be counted. An Awards cell is one result stated one
fact per line: the scope as a quiet label, the result at title weight, the
field size beneath it, and the record that earned it as provenance. **A
Workshops cell is the Awards cell, reused whole**: the host in `.result__scope`,
the head count at title weight, the sessions and hours in `.result__scale`, and
the sessions themselves as links in `.result__source`, one to a line on
`.result__source--stacked` because two forty-character titles are not the short
peers `&middot;` exists for. That it needed no new
line and no new class is the argument for the component: *a set of things each
carrying one figure and one citation* turned out to describe three different
pages. **An article cell is none of those three**: it is the plain `.entry`
the reading column renders, boxed, plus four rules that give the box a foot
(§9.6). It invents no cell language of its own, and the four rules move parts
the record already had rather than adding any. The Awards cell carries
no chips, because the record 300px below carries the same chips and a
projection styled identically to its source reads as the page saying
everything twice ([`awards.md`](awards.md), the scope summary). **Nothing in
the Awards cards is written**: every value comes from `meta_label`, the
function that renders the tags on the records below, so a card cannot say
*Quarter-finalist* while the entry it links to says something else.

**Four columns, and the measurement that said two was stale.** This paragraph
used to read *two columns, not four*, and it declined a narrower `minmax`
because at `11rem` the fit against a ~764px content column was exact to the
pixel, which is the width a grid turns into 3+1 at the first thing that moves.
That number was measured before the page context rail brought
`--container-wide` with it. The document column is 908px now, not 764px, and
the argument does not survive the extra 144px: four `12rem` tracks and their
three `--space-5` gutters come to 828px, so the row seats four with 80px in
hand rather than none.

So the summary carries `.entries--grid--compact`, which lowers the track
minimum for this one grid. **The base `18rem` is untouched**, because it was
chosen for the cell that needs it, the certifications card listing `Microsoft
Certified: Fabric Analytics Engineer Associate`, and a scope card holding four
short lines is not that cell. What the change recovers is air: at `18rem` two
cards stretched to ~440px apiece and spent the remainder on nothing, which is
the same emptiness the `.awards-stats` table below charges the old box for.

**The minimum is `9rem`, and it was `12rem` until the card changed shape.**
`12rem` seated four cards only above 1240px and stepped to three below it,
which put the fourth scope under the first at the width most readers open the
page at. That number had been measured against a card of two long lines, and
those lines were the problem the card was rebuilt to fix: 192px of measure
against a 215px sentence, breaking wherever it landed and leaving *teams*
standing on its own. Four short lines need far less width than one long one,
so the track came down to what the content actually asks for, and the row
seats four from full width to roughly 620px before stepping to one.

**It is still a minimum and not `repeat(4, 1fr)`.** `awards.md` rule 5 lets a
scope render no card at all, `auto-fit` collapses the empty track, and so
three scopes lay out as three cards rather than as three cards and a hole.
Nothing here is pinned to the number of scopes.

**It replaced `.awards-stats`**, a bordered box that sat in the same place and
is deleted along with its section of the stylesheet. The box is the shape a
summary keeps wanting to be, so this records why that one was wrong, and none
of the reasons is *it was boxed*:

| The box did | The cost |
|---|---|
| Invent its own surface, border and radius | A seventh shape where §9.3 had already named the idiom to reuse, and it is this grid |
| Carry no `--measure` cap and no internal structure | ~415px of 13px text floating in a ~764px bordered element, so half of a visibly bordered thing was empty |
| Fuse two tag categories into *1st Place Regional* | `awards.md` rule 4: one category, one treatment, and `placement` is not `scope` |
| Format an ordinal off a count | A second gold would have rendered *2st Place Regional*, and *Regional* was hardcoded beside a number that never measured it |
| Sum every field size into *13,999+ Teams Competed* | The largest and boldest number on the page, 96% of it carried by the 643rd and 1,432nd placements |
| Summarise the Competitions block only | The African hackathon, and the whole second half of the page, absent from its own summary |
| Invent three chrome strings | All three rendered in English on `fr/awards.html` |

Every one of those followed from hand-writing a component instead of composing
one out of the parts already on the page.

### 9.5 `.entries--offprint`: the rank a paper takes

Research's Publications block, and nothing else on the site. It is **a rank,
not a component**: a paper keeps every part `.entry` gives every other record,
in the same fixed order §9 sets, and changes three measurements.

```
Secure and transparent energy management using blockchain      20px, was 17px
and machine learning anomaly detection…
2025
N. Moumni, Y. Boutaleb, F. Chaabane, and F. Drira ·            hanging indent
    Computers & Industrial Engineering
[ Published ] [ Second Author ] [ Elsevier ] [ Dataset ]
Decentralized energy data architecture combining…
- Data pipeline & auditability: …
                                                               32px, was 20px
Dual verification-based multimodal approach…
```

**What it fixes.** The site's highest-credibility record was set at exactly the
rank of the Medium post one block below it: same 17px title, same period line,
same chip row. A recruiter scanning for seconds ([`CLAUDE.md`](CLAUDE.md) §2)
got no signal from the geometry that one of the four records on the page had
cleared peer review and the others had not. Principle 3 is credibility before
persuasion, and this is that principle done in type rather than in prose.

**The title takes `--text-xl`, which the scale already held.** No new step, no
new size: 20px is the lede's step and the brand-bar name's, and it lands the
page's ramp on 32 / 20 / 16 where the block ran 32 / 17 / 16. §1's heading ramp
carries the row, and this is the one rank on the site set by what a record *is*
rather than by its element.

**The citation gets a hanging indent, not a box or a rule.** At the measure the
four linked authors and the italic journal wrap, and wrapped flush left the
second line sets under the title and reads as a new statement. Hung on the
`1.4em` that `.entries` and `.points` already use, the run reads as one line of
bibliography, which is what it is. The site has one indent; this is it, used a
third time rather than a fourth value invented.

**Per-record rhythm goes to `--space-6`.** Two papers rather than five records
in the block, each now carrying a 20px title, so `--space-5` put the second
title close enough to the first record's last bullet to read as part of it.

**What it deliberately does not do.** No border, no surface, no left rule, no
second colour: §9's *entries are never boxed* holds, and §9.4's grid is the one
exception, which this is not. Nothing here is a new component, a new token or a
new treatment. If a future block wants a rank of its own it adds a row to §1's
ramp and an argument here, and *the records on this page feel important* is not
one: **the argument has to be that the reader is currently being told something
false by the geometry.** That was true here, twice over, because the two blocks
sat on one page and looked identical.

### 9.6 `.entries--article`: the card that has a foot

Research's Technical Articles, and nothing else on the site. §9.4 says what
earns a box; this says what a box lets a record do that a reading column
cannot, which is have a foot.

```
Simplify Your Log Management: Configuring
DataDog Integration with Log4j2 In Mulesoft
2024
------------------------------------------  head closed by a hairline
- A Log4j2 HTTP appender POSTs JSONLayout
  events straight to the Send Logs API.
- No agent on the host, and no collector
  in between.
- The appender is asynchronous, so logging
  never blocks a Mule execution thread.
                                            body, then the space auto takes
[ Configuration Guide ] [ 723 views ...     foot, pinned to the bottom edge
[ Medium ]
```

**What it fixes.** The card was four flat rows in the order §9 sets: title,
year, chips, one sentence. Nothing in it said which row was the claim and
which was the proof, and the reach figure, the only external evidence this
block has, sat as the middle of three identical chips. Four rows is not a
hierarchy; it is a list of four things that happen to be in a box.

**It is four rules and no new part.** The `.entry` is a flex column, the
period takes a `--color-border-soft` bottom rule, the bullets step to 14px on
a `1.1em` inset, and the tag list takes `margin-top: auto`. Nothing is added
to the record, nothing is removed from it, and no new token, colour or
component appears. `render_article` moves the chip row to the end of `parts`
and changes nothing else.

**`margin-top: auto` is the whole reason it is a flex column.** It pins the
chip row to the bottom edge of the card, so two cards whose bullets run to
different lengths still line their evidence up across the row. Without it the
reach figure floats at whatever height the prose above it happened to end,
which is the thing a grid is supposed to fix and the thing an `auto-fit` row of
equal-height cards makes worse: the cards were already the same height, and the
content inside them was not.

**The chips render last here and first everywhere else, and the row itself is
untouched.** §9 fixes the order of a record's parts, and this is the one place
that order changes, on the ground that a box has a foot and a reading column
does not. What does *not* change is the row's contents or its treatment:
`platform` still takes the quiet grey terminal position that `publisher` takes
one block above it, which is the parallel [`writing.md`](writing.md) rests its
whole argument on. A reader scanning the page reads **Elsevier** in one block
and **Medium** in the other, same slot, same colour. Moving the row down the
card leaves that intact; dissolving the row into a bespoke footer would not
have, which is why the alternative was declined.

**The bullets step to `--text-md` and inset `1.1em`.** The site has one reading
indent, `1.4em`, used by `.entries`, `.points` and the offprint citation, and
this is the one measure where it is wrong: at roughly 280px of card, `1.4em`
spends a tenth of every line on nothing. The type step is the same reasoning
`.entry__context` already carries: 14px is the body of a card, 15px is the body
of the page.

**What it deliberately does not do.** No second surface inside the card, no
uppercase eyebrow above the title, no bespoke footer row replacing the chips,
and no reach figure promoted to a `.result`-style number. Each of those was on
the table and each one buys hierarchy by spending the tag vocabulary, and the
tag vocabulary is what makes the two blocks on this page comparable at a
glance. **The rank a component earns is paid for out of space and order, not
out of a new language**, which is §9.5's rule stated a second time on the other
half of the same page.

## 10. The rule that emptied a component

`.deflist` handled "category: values" content: a real `<dl>` rendering as a
bullet, a bold label, a colon and the values, all on one line. **It is gone.**
Not deprecated: deleted, along with its section of the stylesheet, because the
rule below took its last user.

That rule is the one worth keeping:

> **A list stays in its page fragment when that page is the only place its
> facts live. It becomes data when it restates facts held elsewhere on the
> site.**

§9 settles it for `.entry`: those are records and always come from
`src/data/`. `.deflist` was the case that needed a rule of its own, because
Skills, Languages, Domains and Impact in Numbers once looked like one component
doing four different jobs. Applying the rule to each in turn is what emptied
it, one user at a time, and each departure is the rule working rather than a
component falling out of favour.

**Domains** was one row listing five industries. §10.1 already says that shape
should be a sentence, and it was the one capability-shaped claim on Home that
Skills & Evidence did not govern: no citation, no record, nothing to check. It
is deleted. Career's `domain` tags say the same thing with a dated record under
each one, which is the difference between a keyword and a claim.

**Skills** began citing the records that prove each capability, which is the
second half of the rule, and moved to `src/data/skills.json` on its own
component (`.skills`, §9.1). See [`skills.md`](skills.md).

**Impact in Numbers** went further than the rule asked. Every line in it is a
second telling of a record on another page, so it is the one block that can
quietly contradict the site it sits on. It did, twice, in both directions: the
front page read *2 plugins accepted upstream, both listed in the official
directory* while `projects.json` had both pull requests `open`, and later read
*submitted upstream, both open* after they had merged.

Moving it into `src/data/impact.json` fixed the link and left the sentence
alone, which was the half that had drifted. So the block stopped being a
`.deflist` and stopped writing sentences: it is now `.entry` records on the
`.result` component (§9.3), and each one **quotes** the bullet it cites through an
id. The sentence, the period line and the anchor all come out of that id.
[`home.md`](home.md) carries the mechanism.

The figure is the one claim still written by hand, and deliberately: deriving
"€1,400 per month" would mean parsing a prose bullet, and a parser that guesses
is a worse liar than a person who checks. It is linted rather than parsed, by
asserting the value appears verbatim in the text the record cites, which catches
the failure that actually happens without pretending to understand prose.

**Languages** was the last user, and it left for the other reason: not because
it restated anything, but because a block heading, a pitch line and a `<dl>`
were more format than three proficiency ratings can fill. It is one
row of `.hero-facts` in Home's opening now (§10.2), beside Availability and
Certified, which are the other two facts a recruiter filters on. A filter
reached last on the page is a filter applied by guessing. It is also data now,
`src/data/languages.json`, because two of its three rows cite Teaching: the
first half of the rule above, applied to the block that the second half had
just moved.

**Nothing should bring `.deflist` back.** A new "label: values" list is either
data (so it is `.entry` records, §9) or it is one line of prose, and the
component existed to sit between those two answers.

### 10.1 `.specs`: the spec strip

The variant the retired `.deflist` could not absorb, and the reason it
outlived it. A `.deflist` was one label and its values on **one line**; the
Teaching appointment needed three *groups* of several rows each, aligned as
columns, and a `<dd>` holding another list stopped being the pairing that
component existed to render.

```
Workload              Language & Tooling     Assessment
32 h per course       Instruction  FR & EN   Final Exam        50%
Lectures       20 h   Materials         EN   Module Homework   20%
  5 modules × 4 h       Slides, code…       Final Project      15%
Labs            8 h                          Attendance        15%
```

`.specs` is a `repeat(auto-fit, minmax(13rem, 1fr))` grid of `.spec` columns.
When modified with `.specs--cards`, each column is rendered as an elevated spec card (`.spec--card`) with a subtle surface background (`var(--color-surface)`), border (`var(--color-border-soft)`), header badge (`.spec__badge`), and optional visual progress indicators (`.spec__progress-bar`).
Each column is a `.spec__title` (a `<p>`, like `.entry__group-title`: block
subdivisions stay out of the document outline, §11), an optional
`.spec__lead` or `.spec__badge` for a headline figure, and a `.spec__rows` definition list of
`.spec__row` pairs. A row may carry a `.spec__detail` that drops full-width
beneath it.

Three decisions worth keeping:

- **It is not a table, and must not become one.** The columns are independent
  groups that happen to sit alongside each other; no cell means anything by its
  row and column position. `auto-fit` is what lets them collapse to one column
  on a narrow screen with no breakpoint of their own, and what keeps Principle
  1 intact: printed, it is still three headed lists.
- **The weighting is inverted from the old `.deflist`.** There the bold label
  was what you scanned for; here the reader is scanning **figures**, so the
  label recedes to regular weight and the value takes the heading ink and the
  right edge.
  Hours and percentages stack into a readable column instead of hiding
  mid-sentence.
- **It is the one intro-level component with no `--measure` cap.** The cap
  governs prose, and a column of label/figure rows is not prose. The sentence
  above the strip keeps its cap; the strip uses the full content column.

Reach for it only when a block has **several constants of different kinds** to
state at once. One or two labelled facts are a sentence, or a `.hero-facts`
row if the page is Home (§10.2).

**Teaching is still its only user, and Workshops was briefly the second.** A
three-column strip stated that page's constants for one revision and became the
card grid in §9.4 instead, on the author's call. The reason is worth keeping
where the next person will look for it: a `.spec` row states a figure and
nothing else, and every figure on that page belongs to a host who invited him.
A card can carry the link; a spec row cannot.


### 10.2 `.hero-facts`: the fact strip

Home's opening carries the three things a recruiter filters on before reading
anything else: **mobility, credentials, languages.** They sit under the pitch
as a label column.

```
Availability   EU residence permit holder. Open to relocation within the EU
               and to fully remote roles.
Certified      Microsoft ×3 · Astronomer ×2 · MuleSoft · Talend · Datadog ×3
Languages      Arabic     Native
               French     Full professional proficiency
                          Taught in French
               English    Full professional proficiency
                          Taught in English · Published in English
```

**Why a grid and not three sentences with a bold label.** The first two rows
work either way. Languages does not: it is three pairs, so an inline run needs
one separator to divide the languages and another to bind each name to its
level, and a middot cannot do both jobs at once. What that collapses into,
and what shipped for one revision, was:

> Languages: Arabic (native) · English and French (full professional proficiency)

Two languages merged because printing the level twice was too long, and the
reader has to work out whether the middot is separating languages or
qualifying one. The grid separates by alignment and needs no punctuation.

**The middot survives on one row, correctly.** Five issuers are short peers
with no internal structure, which is precisely the case §6 of
[`CLAUDE.md`](CLAUDE.md) gives it.

**Rows are heterogeneous by design**: a sentence, a link run, and a nested pair
list. That is why the hairline between them is the one `.skill` uses, and why
`dt` recedes to `--color-muted` while the values carry the ink.

**What may go in it.** Only a fact the first reader filters on. Anything else
is a record, and records go in blocks with a citation. The strip is not a
place to park things that failed to earn a block.

## 11. Page structure

Every page is the same stack:

```
page-header   h1 + optional lede (§11.1)
              + optional page summary: a card grid (§9.4) or a spec strip (§10.1)
block         h2 + optional intro (§11.1)
              + entries or skills          
              + optional note                                        ← repeated
```

A page summary is **derived from the records below it**, never written: it
states what the page's records add up to, and every figure in it comes from the
fields those records render from.

Each page has exactly one `<h1>`: its own title. The site name in the brand bar
is a link, not a heading, so every page gets a unique document outline.
Enforced by `tools/check.py`. It **used to be styled to the `h1`'s size**, and
that sentence stood here while the two shared `--text-2xl`: one rank spelled
twice, with the page's own title no larger than the site's name 40px above it.
The brand bar is `--text-xl` now and the title is `--text-3xl` (§1).

### 11.1 Section intros: one line, and it is the pitch

**A `block__intro` is a single punchy line.** One sentence, no second sentence,
no conversational run-up, no explanation of how the block works.

The intro is the one place on the site that is allowed to *sell*. The people
who read this page are a hiring manager, a recruiter and an engineer, in that
order, and each of them decides in a second whether the block below is worth
their attention. An intro that opens with mechanics (where a link points, what
a tag means, which records were filtered in) spends that second on plumbing
nobody asked about, and the block loses the reader before its first record.

So the intro says **why this work exists and what it shows about the person who
did it**; the records below it carry the evidence. The reference pair is
Awards:

> Competitions: *Engineering background plus competitive programming edge.*
>
> Hackathons: *Rapid prototyping, product design, and fast technical delivery.*

This does not soften Principle 3, *credibility before persuasion*. The intro
persuades **once**, in one line, and every claim underneath it still carries a
number and a link to where the number can be checked. A pitch that the records
cannot back is a defect, not a stronger pitch.

Rules:

1. **One sentence.** If it needs a semicolon it is probably still one line; if
   it needs a full stop and a second clause, cut the second clause.
2. **No mechanics.** *"Each entry links to the issuer's own record"*, *"a pull
   request tag says whether it was merged"*, *"author names link to Scholar"*:
   all true, all obvious on sight, none of it earns the first line of a block.
   Mechanics that genuinely need stating go in the model document for the page.
3. **No per-record facts.** A fact true of one record is a tag or a bullet on
   that record (§7, §9). The intro speaks for the whole block or it does not
   belong there.
4. **Dated or hedged facts go in a `block__note`**, below the records, see
   §11.2. They are provenance, and provenance is a footnote.
5. **Write it as a person, not as a résumé.** Curiosity, effort and intent are
   the point; "leveraged", "demonstrated" and "consistent track record of" are
   the register this whole site exists to avoid.

**There is no exception any more, and the way it went is the rule.** Teaching
was the one: its intro stated an appointment, *University Lecturer at IHEC
Sfax, on the M.Sc. Data Science programme*, where every other block on the site
opens with a pitch. Two passes had already narrowed it, moving the workload,
language and assessment facts out into a `.specs` strip (§10.1) so the shape
rule was satisfied and only rule 5's spirit was still broken.

The sentence never needed rewriting. **It was one rank too low.** A constant
true of every record on the page is what a page lede is for, and saying it
under a section heading was what made it look like a broken intro. Moved into
the page header it is simply correct, and the block opens straight onto its
strip.

### The two ranks, and the test between them

| | `.page-lede` | `block__intro` |
|---|---|---|
| Speaks for | the whole page | one block |
| May state | a constant true of every record on the page | a pitch for the records directly below |
| Size | 20px, in the page header | 15px, under the section heading |
| How many | at most one | one per block |

**The test is one question: would the sentence still be true and still be the
point if a second block were added to the page?** Teaching's appointment
survives that; *Engineering background plus competitive programming edge* does
not, because Awards' second block is Hackathons and that line is Competitions'.

**A page gets a lede only when it has something to say that the blocks cannot,
and never both.** A lede above a first block whose intro says the same thing is
two openings competing to introduce one page, which is the surface Career's
lede was deleted for (`src/pages/career.html`, see [`career.md`](career.md)) and the same
surface Home's rebuild removed. Five of the eight pages carry a lede and three do
not, and this paragraph gave the count as four and four while naming Projects,
Research and Awards among the pages without one, months after all three were
given a lede in the same commit. The census, re-derived from the fragments:

| Lede | Why |
|---|---|
| Home, Projects, Teaching, Workshops, Awards | A statement no single block on the page could make |
| Career | Deleted: its first block's paragraph already introduced the career (`career.md`) |
| Research | Deleted: its publications intro started making the lede's second claim (`research.md`) |
| Contact | Never had one: its page-level statement is the facts grid in the header (§9), the other thing a `page-header` may carry |

**Re-derive the census before quoting it.** Three of the four pages this
sentence named had changed underneath it, and the paragraph went on being read
as the site's rule for who gets a lede.

**Writing a new lede is the author's, not an agent's.** A lede asserts
something about the person, which [`CLAUDE.md`](CLAUDE.md) §10 reserves. What
an agent may do is what was done here: notice a sentence sitting at the wrong
rank and move it.

### 11.2 `block__note`: the dated footnote

Some figures come from a source that does not refresh them. A note in
`--text-sm` muted ink, placed **after** the records, carries their provenance
and an explicit *as of* date, so the intro is not forced to hold a disclaimer.

**It has no user, and it is staged rather than deleted.** Research → Technical
Articles was the one candidate: Medium's view and read counts are hand-copied,
and the note reading *Reach figures read from Medium, August 2026* was built
and then withdrawn on the author's call, because a footnote dating two chips is
a maintenance promise made in front of the reader. The discipline it existed to
enforce did not go with it: `as_of` is still required on every `reach` and
`check_reach` is still fatal, so the date is kept where it does the work, in
the record ([`writing.md`](writing.md)). The component stays in `STAGED_CSS`
because the next hand-copied figure on this site will want it.

A note is for provenance and dating. It is not an overflow bin for the
sentences the intro rule removed.

## 12. Navigation

The original rendered this as a `<table>` row, which meant the site's real
tables inherited its styling and **no page could show which one you were on**.
`.nav` keeps the look (evenly distributed links over a hairline) as a list,
with `aria-current="page"` rendered as bold ink.

### 12.1 The language switch

`.lang-switch`, in the brand bar above the theme switch. **Links, not buttons,
and the distinction is the design**: each language is a real page at a real
URL, so this is navigation. It needs no script, it survives with scripting off,
and a reader can bookmark or share the French page as itself. The theme switch
beside it has to be buttons for the opposite reason, because a theme is not a
place.

The language being read renders as plain text with `aria-current`, not as a
link to the page you are already on. It does not print (§21). It is absent
entirely when only one locale exists, so the site carries no dead control while
a translation is unfinished.

### 12.2 Page context

The second navigation on the site, and the only one whose contents differ per
page. **Why a rail is admissible here is in §4**, with the arithmetic; **why a
control is admissible at all is in `CLAUDE.md` §7**, beside the depth dial.
This section is the reference for what it renders.

| | |
|---|---|
| Slot | `.sidebar-context`, the `aside` |
| Component | `.book-toc`, a `nav` inside it |
| Built by | `render_page_context` in `tools/build.py` |
| Source | the page's own markup: `h2` inside `section[aria-labelledby]`, then `li.entry` inside each |
| Depth | two levels: sections, and the records in them. `TOC_DEPTH` |
| Skipped | anything carrying `data-toc-skip`, which is an address rather than a place |
| Labels | the record's own heading, unless it carries `data-toc-title`. Siblings sharing a label are disambiguated by the year in their id |

**It is a `nav` holding a list of links, and nothing a reader can operate.**

It was a `details`, forced open above `1024px` by two declarations while the
element itself stayed closed, because browsers hide the contents two different
ways. So the desktop rail painted its whole tree while telling assistive
technology the region was collapsed, and left a focusable `summary` that did
nothing visible when activated. [`CLAUDE.md`](CLAUDE.md) §7 admits the rail on
the ground that deleting it costs the reader nothing but convenience; **a
control that lies about its own state is not covered by that argument** and
was never argued for separately.

The disclosure became deletable once the tree stopped going three levels deep.
It existed to fold away Teaching's rail, which ran one top-level link over
twenty-two module names, roughly 668px of navigation in front of the page's
first word on a phone. Capped at records, that rail is four lines and the
longest on the site is Career at fifteen.

**Above `1024px`** it is the sticky left track of `.page-body`.

**At or below `1024px`** `.page-body` stacks and the rail sits above the
content, at full length, which is affordable now that full length means
sections and their records. It does not print (§21).

**It is built from type and whitespace**, like the rest of the site. It had
been written in a different vocabulary: an uppercase letterspaced heading and a
tinted rounded card, the first two items on the out-of-scope list at the top of
this document, plus ten literal values including a `1.5px` border that exists
nowhere else. The nesting device is now the same 2px left hairline
`.entry__group--homework` uses to tie a course's assignments to the course.

**The header is one word and no picture.** It opened with an inline SVG of a
book, and that was **the only `<svg>` on any page of this site**: §17's icons
are all `<img>` of a real brand mark, sized by a token, carrying something a
word could not. This one was `aria-hidden`, drew the three words next to it,
sat at a hardcoded `16px` that is on none of `--icon-xs` (12) or `--icon-md`
(18), and was painted `--color-muted` beside a
`--color-heading` label, so the largest object in the header was also the
palest. Keeping it meant maintaining an icon vocabulary of one.

The label went with it from ink and bold to `--color-muted` and
`--weight-regular`, the treatment `.entry__period` and the two switch
separators already carry. At `--text-xs` bold it sat one step *below* the 13px
bold `.book-toc__link` under it while matching it in weight, which read as a
broken first item rather than as the title of a list.

**And the header no longer sets `display`.** A `summary` is `display: list-item`;
the flex box that laid the icon out beside the word had replaced that, which
took the disclosure marker away at every width. Below `1024px` the control
therefore opened with nothing saying so except a decorative glyph, and the two
rules above that hide the marker on the desktop rail had never had a marker to
hide. They do now.

**It is not hand written.** A record added to `src/data/` appears in it with no
second edit, and `render_toc_node` raises rather than inventing a label from an
id: it used to fall back to the slug with its hyphens swapped for spaces and
title cased, so a record whose heading failed to parse would have shipped a
rail entry reading *Exp Jacquemus 1*.

**It is not stateful**, and there is no `--level-N` class on any item. Every
depth is styled identically, so a per-level modifier carried nothing and only
kept rules alive for depths the parser had stopped producing: a fourth level
was declared in `TocNode` for a "Lab" tier that was never built, and it held
three CSS rules and a truncation branch hostage for the whole of its life.

## 13. Responsive behaviour

The layout is one column at every width, so there is no column count to
collapse. What the breakpoints do is release the container, tighten space, and
keep the navigation usable once eight items stop fitting.

| Breakpoint | Change |
|---|---|
| ≥1024px | The cap goes to `--container-wide` (1240px) and `.page-body` becomes a grid: the page context rail takes a sticky 240px left track (§4) |
| >960px | The column is centred and capped at 1100px |
| ≥601px | Home's fact strip hangs its labels on `--spine`; below this the collapse row takes over (§10.2) |
| ≤960px | The cap is released and the column takes the viewport; footer centres |
| ≤720px | Padding tightens; nav items shrink-wrap; `--text-3xl` steps to 48px and `--text-2xl` to 28px; `.skill` collapses to one track |
| ≤600px | Home's hero stacks: portrait above the bio, centred; the brand bar stacks; every label column collapses to one track, its label going bold (`.hero-facts`, `.contact-list`, `.perf`) |
| ≤480px | Navigation scrolls horizontally, bleeding to the viewport edges so the affordance is visible; the portrait steps to 144 x 180; `--text-3xl` steps to 40px and `--text-2xl` to 24px |

**Four of those numbers were wrong before this table was last read.** It gave
the ≤720px steps as 32px and 22px and the ≤480px steps as 28px and 20px, which
were the values from before §1's display pair was rebuilt; the stylesheet has
said 48/28 and 40/24 since. The `≥1024px` row was missing entirely, so the
breakpoint that introduces the rail and widens the container, the largest
structural change on the list, was the one it did not mention. Read this table
against `main.css`'s `@media` blocks before trusting a row: there are seven,
and they are the whole set.

**One breakpoint left the file rather than joining it.** A `min-width: 1280px`
query used to give Home's hero a third track, moving the fact strip into a
14rem right-hand column with a left rule. It was the only right-aligned element
on the site, and it put the recruiter facts outside the spine on the one
viewport wide enough for the alignment to be visible. The strip runs full width
at every size now.

Prose stays readable at every one of these without a rule of its own, because
`--measure` is in `ch` and therefore already relative to the type size (§1).

## 14. Motion

A single `--duration` of 150ms, on colour and opacity only. Fully disabled
under `prefers-reduced-motion: reduce`.

## 15. Accessibility

- Skip link to `<main>`.
- Landmarks: `<header class="site-header">`, `<nav aria-label="Primary">`,
  `<main id="main">`, `<footer class="site-footer">`.
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
| Who is this engineer? | Brand bar + Home hero |
| What are they doing right now? | Home → Currently |
| What have they built with, and for how long? | Home → the opening, then Currently |
| How do they work? | Career → Summary |
| What can they actually do, and how would I know? | Home → Skills & Evidence |
| What impact did they create? | Home → Impact in Numbers |
| What problems have they solved? | Career → Experience |
| What can they build? | Projects |
| How technically deep are they? | Research, Workshops, Teaching |
| Can I trust their engineering practices? | Career → Certifications (all verifiable) |
| Where can I verify their work? | Every entry links to source, badge or DOI |
| How do I reach them? | Contact, and the CV link in the brand bar |

## 17. Extending the system

1. Reach for an existing component first. `.entry` alone covers almost
   everything on the site, and `.tag` covers most of the rest.
2. If a new component is genuinely needed, build it from tokens only. A literal
   in a component rule is a bug.
3. Check it against **Explicitly out of scope** at the top of this document.
4. Add it here and to `assets/css/main.css` under a numbered section.
5. Run `python3 tools/check.py`: it fails on classes used in markup but absent
   from the stylesheet, undefined tokens, inline styles and broken links, and
   reports any CSS rule or token nothing uses.

A new **metadata category** is not a new component. Declare it in the model
document for its page ([`awards.md`](awards.md), [`workshops.md`](workshops.md),
[`teaching.md`](teaching.md)), order it in `MODELS` in `tools/build.py`, give it
one `.tag--<category>` rule in `main.css`, and add its row to §7.1. Never decide
ordering or colour inside a page. Before adding one, check whether an existing
category already means what you need: reusing `format` and `scale` cost two
lines; a synonym would have cost a colour.
