# The type ramp

The record of the pass that gave the site a display step, after eight pages had
spent their whole life with a page title the same size as the link above it.

The brief was Andrew Ng's `text-5xl md:text-7xl` as a reference for the page
titles, across every page, with the references and the options laid out first.

---

## The references, measured rather than remembered

Each was fetched and read.

| | Body | `h1` | `h2` | `h1` ÷ body | `h1` : `h2` | Weight |
|---|---|---|---|---|---|---|
| **andrewng.org** | 14px | 48 → **72px** | 30 → 36px | **5.14** | 2.00 | separate `font-heading` family, `tracking-tight` |
| **Tufte CSS** | 21px | **48px** | 33px | 2.29 | 1.45 | **400**, h2/h3 italic, `line-height: 1` |
| **Butterick** | | | | | | *"It's fine to make the point size bigger, but just a little... The best way to emphasize a heading is by putting space above and below."* |
| **This site, before** | 16px | 25px | 19px | 1.56 | 1.32 | 700 throughout |
| **This site, after** | 16px | **40px** | **24px** | **2.50** | **1.67** | 400 on the title, 700 below it |

`text-5xl md:text-7xl` is 48px below 768px and 72px above, `line-height: 1`.
andrewng.org's container is `max-w-5xl`, 1024px, on a page of roughly 180 words.

**The useful finding was Tufte, not Ng.** Tufte CSS is unambiguously a document
and still sets 48px, which means large type is not what stops a page being a
document. The ratio is. 5.14 is a landing page's number and 2.29 is a
document's, so this landed at 2.50, nearer Tufte, and the argument in
[`DESIGN.md`](DESIGN.md) §1 is written that way round.

## Findings in the old scale

1. **`--text-2xl` had two users**: `h1` and `.site-header__name`, both 25px,
   about 40px apart on the page. The page's own title was exactly the size of
   the site's name above it, and the token could not be raised without dragging
   the brand bar with it. This is the example the rework skill's own quality-bar
   table uses to define what a real finding looks like; it had never been fixed.
2. **The scale was bottom-heavy with no display step.** 12, 13, 14, 16, 17, 19,
   25: five of seven sizes between 12px and 17px, four of six steps under 15%,
   nothing above 25px. Hierarchy was carried by colour and weight because size
   had run out of things to say.
3. **Space was the unused lever.** The title had 20px above it and 12px below.
4. **No negative tracking existed, because no large type existed.** The two
   letter-spacing rules on the site were both positive, on 12px tags and 10px
   diagram labels.

## What shipped

| | Before | After |
|---|---|---|
| `--text-3xl` | did not exist | **40px**, one user: the page title |
| `--text-2xl` | 25px, `h1` **and** the brand bar | 24px, section headings |
| `--text-xl` | 19px, section headings | 20px, the brand bar and the page lede |
| `h1` weight | 700 | **400** |
| `h1` tracking | none | `-0.02em` |
| `.page-lede` | 17px | 20px |
| `.page-title` bottom margin | `--space-3` override | override deleted, takes the site default |
| Responsive | `--text-2xl` → 22px at ≤480px | `--text-3xl` 40/32/28, `--text-2xl` 24/22/20 |
| Print | inherited the screen tokens | its own point sizes against the 10.5pt body |

Everything 17px and below is untouched. No markup changed, in either language.
No content changed.

## The two decisions that were not on the question card

- **`--text-xl` is 20px, not the 19px in the approved preview.** One token then
  serves both the brand-bar name and the page lede instead of adding a ninth,
  and it repairs a step finding 2 had named: 17 → 19 is 1.12, below the
  visible threshold, where 17 → 20 is 1.18.
- **`.page-title`'s margin override was deleted.** It reduced the site default
  to 12px, which was right for a 25px title and is a quarter of a 40px one's
  line box. On Awards it put the title 12px above a card grid. Deleting the
  override was preferred to choosing a new number, because `h1` already carries
  the right default.

## Measurements the layout was checked against

Taken from the shipped faces with `fontTools`. There is no browser here, so
this is arithmetic, not observation.

**Home is the only page whose `h1` is not alone in a full-width header.** It is
`Data Engineer` / `Ingénieur Data` in `.hero-header__bio`, beside the 180px
portrait. At weight 400 and 40px the French title is 283px:

| Viewport | Bio column | Title | Clearance |
|---|---|---|---|
| 1240px | 708px | 283px | 425px |
| 1024px | 492px | 283px | 209px |
| 768px | 536px | 283px | 253px |
| 721px | 489px | 283px | 206px |

That margin is the reason weight 400 mattered beyond taste: at 700 and Ng's
72px the same string is **546px against a 552px column at 768px**, six pixels,
which is what ruled out copying the reference literally.

Section headings at 24px bold, the longest on the site: `Opportunités et
prestations` 336px, `Certifications & Credentials` 329px, against a 908px
column.

## Still open, and author-led

- ~~**Seven pages have no lede.**~~ **Closed, in a later pass, and not the way
  this file expected.** No prose was written. Six of the seven pages already
  opened with a sentence one heading below the title, so a new lede would have
  put a second opening above an existing one, which is the exact surface
  Career's deleted lede was deleted for. Three of those sentences turned out to
  be page statements rather than block pitches and were **promoted** into the
  header: Teaching's appointment line (which retired
  [`DESIGN.md`](DESIGN.md) §11.1's only declared exception), Workshops' single
  pitch, and Contact's invitation. The remaining four got 40px of air under the
  title instead. `.page-header`'s margin was `--space-5` and was *collapsing*
  with the title's own, not adding to it, so the real gap had been 20px.
  Projects, Research and Awards would still need one author-written line each
  if they are ever to have a lede.
- **The `h1` colour was left at `#393939`.** Dropping from 700 to 400 loses
  optical weight, and darkening to `#222222` would buy it back without changing
  the size. Not done, because [`DESIGN.md`](DESIGN.md) §1 documents that colour
  as part of the deliberate stepped ramp and it reads as calm rather than weak
  in the arithmetic. Worth a look on a real screen.
- **Nothing here has been seen rendered.** Every number above is measured from
  the font files and the CSS, not from a browser.
