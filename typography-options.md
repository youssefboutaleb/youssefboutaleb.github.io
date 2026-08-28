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

---

# Second pass: the display pair

The site came back to the same reference nine days later, with a sharper brief:
*follow andrewng.org's title and subtitle design exactly; the size may be
modified.*

## What "exactly" turned out to mean

The first pass measured Ng's **sizes** and rejected them. It never read the
rule. Fetched and read this time, the whole of it is:

```css
h1,h2,h3,h4,h5,h6 { font-family:"ABCSynt",Georgia,serif; color:#0f0f23;
                    letter-spacing:-.02em; line-height:1.15 }
h1,h2 { font-weight:400 }
h1 { 48px → 72px @768px }   h2 { 30px → 36px }   /* body 17px, #3a3a4a */
```

**The design is that h1 and h2 are one treatment at two sizes.** Four shared
declarations, a size each, ratio exactly 2.00, and the size is the only thing
separating the ranks. This site was separating them four times over: 400 vs
700, `#393939` vs `#494949`, tracked vs untracked, and a hairline under the
second one.

**One number in the first pass's table was wrong.** It recorded Ng's body as
14px, making the title 5.14 times it, and that ratio is most of why the pass
argued against following the reference. The body is 17px. The real ratio is
4.24, much nearer Tufte's 2.29 than 5.14 suggested, and this pass lands at 4.00.

## The three questions put to the author

| | Options | Chosen |
|---|---|---|
| **Size** | 64/32 · 56/28 · 72/36 (Ng literal) | **64 / 32** |
| **The h2 hairline** | remove and add air · keep · keep but lighten | **remove, add air** |
| **Typeface** | keep Noto Sans · add a serif for headings | **keep Noto Sans** |

72/36 was costed and rejected on one measurement: `Ingénieur Data` sets 510px
at 72px against a 492px bio column at a 1024px viewport, so Home's title would
wrap across most laptop widths. At 64px it is 453px and holds one line
everywhere, with about 36px to spare at the tightest (721px).

Ng's serif heading face was offered and declined, which keeps
[`DESIGN.md`](DESIGN.md)'s *"a second (serif or display) typeface"* exclusion
standing. Everything else about the treatment is now the reference's.

## What shipped

| | Before | After |
|---|---|---|
| `--text-3xl` | 40px | **64px** |
| `--text-2xl` | 24px | **32px** |
| `h1` : `h2` | 1.67 | **2.00** |
| `h2` weight | 700 | **400** |
| `h2` tracking | none | **-0.02em** |
| `h1` colour | `#393939` (`.page-title` override) | **`#222222`**, the override deleted |
| `h2` colour | `#494949` | **`#222222`**, one heading ink |
| Heading line height | 1.2 | **1.15**, new `--leading-display`, the pair only |
| `.block__title` underline | `1px solid --rule-soft` | **gone on screen**, kept in print |
| `.block` bottom margin | 32px | **60px** |
| Responsive | 40/32/28 and 24/22/20 | **64/48/40** and **32/28/24** |
| Print | `h1` 400, `h2` inherits | `h2` takes back 700 and its hairline, block gap back to 32px |

Two tokens were deleted rather than left unread: `--color-heading-2` and the
`--ink-800` `#393939` step behind it. The page-title colour override was their
only consumer, and `check.py`'s token audit reported them the moment it went.
Deleting them also closed the one item this file left open, which was that the
`h1` had dropped to weight 400 and could buy the optical weight back by
darkening. It has.

**No markup changed, in either language, and no content changed.** The `h1` is
`.page-title` on eight pages and the `h2` is `.block__title` on twenty; nothing
else uses either token.

## Still open

- **Nothing here has been seen rendered.** Again. The widths are measured from
  the shipped face with `fontTools` and the columns from the CSS; there is no
  browser in this environment, and `firefox` is a stub that asks to be
  installed. The one place that matters is Home, because its `h1` is the only
  one sharing a line with anything, and that is the case the arithmetic above
  covers most carefully.
- **The mobile ratio loosens on purpose**, to 1.71 at ≤720px and 1.67 at
  ≤480px, because a weight-400 section heading with no rule under it has to
  stay clear of the 16px body and 24px is the floor. Ng does the same thing
  (72 → 48 for the title, 36 → 30 for the heading). If the section headings
  read weak on a phone, that floor is the number to raise.
- **`.block`'s 60px is the hairline's replacement and is the value most likely
  to want tuning** once it is seen. The pair moves together: less space wants
  the rule back.
