# The page context rail

The component landed as commit `3acc1b9` without going through
[`CLAUDE.md`](CLAUDE.md) §10, which is not a criticism of the component: it is
the reason this document exists. This is the pass that reconciled it with the
documents it contradicted.

Companion to [`theme-options.md`](theme-options.md), which records the dark
rendering and carries the original analysis of the three proposals that opened
the session.

---

## The correction that matters

**The recommendation against building this was wrong, and specifically wrong.**

The argument was that there was nothing to navigate: no `h4` exists anywhere on
the site, five of eight pages carry one or two sections, and Teaching's 1,635
words sit inside a *single* section, so a table of contents could not help the
page that most needed it.

Every one of those measurements was correct **about headings**. The
implementation does not index headings. It parses the rendered page and indexes
**records**, and that difference is the whole thing:

| Page | Sections | Rail entries |
|---|---|---|
| Teaching | 1 | **23** (courses, then their modules, three levels) |
| Career | 6 | 12 (sections, then employers and schools) |
| Awards | 2 | 10 |
| Projects | 2 | 6 |
| Home, Contact | 3 | 3, no subitems |

Teaching is the page the analysis said a rail could not help. It is the page it
helps most. Recorded plainly because the failure is reusable: **a measurement
taken against the wrong unit answers a question nobody asked.** The unit here
was never headings, it was records, and this site has always been a pile of
records.

---

## What was wrong with it, and what was done

### Fixed

**It printed.** `@media print` hides `.nav`, `.skip-link` and `.site-footer`;
`.sidebar-context` was not on that list. Below 1024px the rail keeps its
bordered card styling on `--color-surface`, and a printed page evaluates at
roughly 816px, so **every printed page carried a tinted rounded panel of dead
anchor links** on a document whose stated reason for printing is that it
doubles as a CV. Now hidden, with `.page-body` reset to `display: block` so the
grid track does not outlive the media query that set it.

**Three names for one component.** The stylesheet's contents list said *page
context*, its section header said *BOOK SHORTCUTS SIDEBAR*, `DESIGN.md` §12.1
said *Book shortcuts sidebar navigation*, and the classes say `.sidebar-context`
and `.book-toc`. Standardised on **page context**, chosen because it was
already in two of those places and matches the class. No new name was invented:
inventing a fourth to settle three is how there come to be five.

**`DESIGN.md` §4 described a layout the site does not have.** It said *"One
centred column, `1100px` at most"*; the container is 1240px above 1024px. §4
now carries both figures and the reason for the second.

**§4's own argument had been reversed without being answered.** It removed the
original identity rail partly because *"it cost a quarter of the viewport on
every page, including the pages whose records are widest: Career's tag rows,
Teaching's spec strip."* The new rail is 240px plus a 60px gap, which is
**24.2% of 1240**: the same quarter, on the same two pages. §4 now answers this
rather than ignoring it. The container widened to absorb most of the cost, so
the content column runs 940px against the old 1100px. The real loss is 160px,
prose does not notice because `--measure` caps it at 74ch long before either
figure, and the two named cases wrap 160px earlier than they did.

**Principle 1 had no argument for it.** `CLAUDE.md` §7 admits the depth dial as
the single exception to *"a document, not an interface"* and requires any
second control to have "an argument this strong, made in writing first." The
rail shipped without one. §7 now carries it, and records that it was written
after the fact.

The argument itself, in short: the rail **fails the dial's test**, because the
dial is admissible precisely for not being navigation and the rail is
navigation. It passes a different one, taken from Principle 1's own second
sentence, *a reader should be able to print the page and lose nothing*:
**deleting the rail costs the reader nothing but convenience**, because every
line in it is an anchor to a record already on the page. That is why it is
correct for it to vanish in print, and why its vanishing is not a loss.

**A duplicate this pass created.** The rail was documented in a new §4
subsection before `DESIGN.md` §12.1 was found to be describing it already, in
prose that had escaped the file's wrapping. Reconciled rather than left: §4
holds the argument, §12.1 holds the reference, neither restates the other.

**A mechanism claim asserted in two documents was wrong.** §4 said the rail is
generated "from the same data the page renders from". `render_page_context`
parses the rendered markup. The practical consequence is identical (a record
added to `src/data/` appears with no second edit) but the mechanism is not, and
parsing output is the better of the two: an index built from data would assert
what a page contains, and this one observes it, so it cannot name a record that
failed to render. Corrected in `DESIGN.md`, in the `build.py` docstring, which
still said "book shortcuts TOC", and noted in `README.md`.

### Reported and not touched, at the time

**Four dead classes**, which `check.py` listed on every run:
`book-toc__item--level-4`, `book-toc__subitem`, `book-toc__sublist--level-3`,
and `is-active`. Left alone in this pass on the reasoning that deleting another
author's styling days after they committed it, assuming they were not midway
through wiring it, is not a mechanic.

**The audit pass below deleted all four**, on the author's instruction, once
the cause was known: three of them belonged to a level 4 that the parser never
produced. `.is-active` went with them. If a scroll-spy is ever built it comes
back, and it comes back with the argument `CLAUDE.md` §7 asks for, because
**wiring it would introduce scroll position as state**, which is the one thing
the first two Principle 1 exceptions were careful to avoid.

---

## The audit pass

A full review of the design and the implementation, after the reconciliation
above had documented the component without ever reading it critically. Fourteen
defects, four causes.

### Cause 1: it was written in a different design language

| What | Rule it broke |
|---|---|
| `text-transform: uppercase; letter-spacing: 0.05em` on the header | `DESIGN.md` **Explicitly out of scope**, item one: *"Uppercase letterspaced eyebrow labels"* |
| `background-color` + `border` + `border-radius` below 1024px | Same list: *"Cards, tinted panels, drop shadows on content"* |
| 10 literal values, including a `1.5px` border and `line-height: 1.4` | *"Every value comes from a token. No literals in component rules."* |

Desktop was mostly right, because the ≥1024px block stripped the card back to
bare type. The uppercase eyebrow survived at every width, and the card was what
every phone reader saw. The component is now type, whitespace and the same 2px
left hairline `.entry__group--homework` already uses. **Zero literals remain**,
and `1240px` and `240px` became `--container-wide` and `--rail-width`, which is
how `1240px` had been silently contradicting §4's "1100px at most".

### Cause 2: content knowledge had leaked into the build tool

```python
text = text.replace("IEEEXtreme Programming Competition", "IEEEXtreme")
text = text.replace("A2SV (Africa to Silicon Valley)", "A2SV")
```

Two award names hardcoded inside `BookTocParser`. Rename either in
`awards.json` and the abbreviation silently stops applying. They are a `short`
field on the record now, emitted as `data-toc-title` through a new `entry_li`
helper that all eight record renderers share, and the parser no longer knows
anything about what the site is about.

Two more of the same shape:

- **A hardcoded id-prefix allowlist**, `("course-", "exp-", "edu-", ...)` for
  records and `("mod-", "hw-", "cap-", "grp-")` for groups. Both were **dead**:
  every record carries `class="entry"`, every indexed group carries
  `entry__group`, and **no id on the site has ever begun with one of those four
  group prefixes**. They matched nothing while promising that a new prefix
  would be handled. Deleted.
- **A silent fallback to a mangled id**, `node.title or node.id.replace("-", " ").title()`.
  It raises now, and the guard was tested rather than assumed: feeding it a
  labelless node produces the error rather than a rail entry reading
  *Exp Jacquemus 1*. `CLAUDE.md` §9's table gained the row.

### Cause 3: a tier was designed and never built

`TocNode` documented `level  # 1: Section, 2: Course/Entry, 3: Module/Group, 4: Lab`.
The parser never created a level 4; max depth emitted across all eight pages
was 3. That one fact explained **three of the four dead classes** `check.py`
had been reporting on every run, plus a `Lab:` truncation branch that shortened
nothing (no `.entry__group-title` on the site starts with `Lab:`, and labs are
`.point--lab` items the rail never indexes) and a regex stripping tags from
text that `HTMLParser` never puts tags into.

All of it is gone, along with the `--level-N` modifiers themselves: every depth
is styled identically, so the modifier carried no information and only
guaranteed that the stylesheet kept rules for depths nothing produced.
`check.py`'s dead-class note is down from 8 entries to 4, and the 4 remaining
belong to other components.

### Cause 4: the mobile case had never been decided

No `max-width` rule existed. Below 1024px the rail rendered above the content
at full length:

| Page | Links | Space before the first word |
|---|---|---|
| Teaching | 23 | **~668px** |
| Career | 12 | ~382px |
| Awards | 10 | ~330px |

On a phone, Teaching opened with about a screenful of navigation, and Teaching
is the page the rail is best on at desktop width. It is a closed `<details>`
now: one line, no JavaScript, keyboard accessible, and forced open above
1024px so the desktop rail is unchanged. Forcing it open needs two
declarations, `display: block` on the children and `content-visibility: visible`
on `::details-content`, because browsers hide `details` contents two different
ways and overriding one leaves it collapsed on half the web.

### The accessibility note

`<aside aria-label="Page shortcuts">` wrapped `<nav aria-label="On this page">`
wrapping a visible "On this page" heading: three names for one region. The
aside is unlabelled now and the nav is `aria-labelledby` the summary.

### What was left alone

`.tag` carries `letter-spacing: 0.02em` and four other literals. It is a
different component, it is not an uppercase eyebrow, and rewriting it was not
what was asked for. Worth a look the next time tags are open.

---

## Still open, and author-led

- **The rail is unseen.** No headless browser here. Its behaviour is reasoned
  from the CSS and verified by `check.py`; the sticky track, the 940px content
  column and the card at narrow widths have not been looked at. The dark
  rendering shipped in the same session is unseen for the same reason. Open the
  site at a desktop width, then below 1024px, then with the system set to dark.
- **Home and Contact get a three item rail with no subitems**, which is close
  to furniture on pages that are already short. A threshold (render the rail
  only where the index is worth having) was offered and not taken. It remains a
  reasonable change and it is a `build.py` one, not a CSS one.
- **`BookTocParser` and `render_toc_node` keep the old name internally.** Left
  alone: they are private to `build.py` and renaming them churns a diff for no
  reader's benefit. Worth doing the next time that file is open for another
  reason.

---

## The header pass

The author said the header was not good design and asked for options. Three
findings and one cause, plus one claim of mine that was wrong in a way that
changed the fix.

### The cause

**The header was written as a UI widget label. Everything under it is a
document.** Five symptoms, one decision.

| Before | After |
|---|---|
| A 16px inline SVG of a book, `aria-hidden`, beside the label | Deleted, with `.book-toc__icon` |
| Header `--text-xs` **bold** in `--color-heading` | `--text-xs` **regular** in `--color-muted` |
| `display: flex` on the summary | No `display` at all: the browser's `list-item` |
| `chrome.on_this_page` = *On this page* / *Sur cette page* | `chrome.contents` = *Contents* / *Sommaire* |
| 151 CSS classes | 150 |

### What each one was

**The book was the only `<svg>` on the site.** `grep -c "<svg" *.html` returned
exactly `1` per page, and it was this. `DESIGN.md` §17's icons are all `<img>`
of a real brand mark (GitHub, OpenCV, an employer): a picture that identifies
an external thing and says something a word could not. This one identified
nothing and drew the three words beside it. Keeping it meant maintaining an
icon vocabulary of one, which is the definition of an exception rather than a
system.

**It also sat outside the component it looked like it belonged to.** §17's own
rule is *"Icons are never sized inline"*, and this one carried
`width="16" height="16"` in `tools/build.py`, no `.icon` class, and a `16` that
is on none of `--icon-xs` (12), `--icon-sm` (15), `--icon-md` (18). The audit
above reported *"zero literals remain"*: it was reading the CSS, and two
literals were living in the renderer. **A component audit that stops at the
stylesheet misses whatever the build tool prints.**

**The ornament outweighed the word.** A 16px glyph beside 12px type is roughly
1.9x the label's cap height, and it was `--color-muted` against a
`--color-heading` label, so the largest object in the header was also the
palest.

**And the header was smaller than its own first child.** 12px bold, over 13px
bold `.book-toc__link`. One step down in size, identical in weight and colour:
it read as a broken first item, not as the title of the list. It is furniture
now, in the treatment this site has used for furniture fourteen times over
(`.entry__period`, the lang and theme separators), and the first bold ink in
the rail is the first link.

### The correction

**I reported that the closed mobile summary showed a native disclosure triangle
next to the icon, and called that three signifiers on one line. There was no
triangle.** `display: flex` on a `summary` replaces its default
`display: list-item`, which is precisely how the marker is generated, so the
flex box laying the icon out beside the word had been suppressing it at every
width since the component shipped.

Two consequences, and the second is why the correction mattered before the
build and not after:

- The desktop block's `list-style: none` and
  `.book-toc__header::-webkit-details-marker { display: none }` had never had a
  marker to hide. Two dead rules that `check.py` cannot see, because the class
  is used and the property is valid.
- **Below 1024px the decorative, `aria-hidden` glyph was the only thing saying
  the control opened.** Deleting it as asked, without touching `display`, would
  have shipped a bare word that discloses a tree with nothing to announce it.

The fix is that the header sets no `display`. The summary is `list-item` again,
the browser draws its own triangle where the `details` is a real control, and
the two desktop rules take it back where it is not. No CSS chevron, no literal,
no new device: the affordance is the browser's.

**The lesson: check what a `display` declaration replaced before deleting the
thing it was there to lay out.** `display: flex` on a `summary` is a
well-known way to remove the triangle, and here it was doing that as a side
effect nobody had recorded.

### Reported, decided against for this pass

Three defects found on the way, left alone on the author's call so the header
closed end to end (`CLAUDE.md` §10.6). Each needs a decision, not a mechanic:

- **Research's rail restates its records verbatim at a quarter width.** Its four
  sublinks are entire paper titles: 133, 108, 88 and 85 characters, in a ~222px
  column at `--text-xs`, which is roughly 37 characters a line, so 4, 3, 3 and
  3 lines each. That is the *"answers one question twice"* objection §4 claims
  this rail avoids. The mechanism to fix it exists and is the `short` field the
  award names already use; **the short titles are the author's words to write.**
- **Career prints `Jeunes Ingénieurs de Djerba (JID)` twice, consecutively and
  identically**, `career.html:528` and `:535`, two anchors. The records are the
  2023 and 2022 editions and differ only by a dateline, which the rail drops. A
  `short` of *JID (2023)* and *JID (2022)* fixes it in the data.
- **Home and Contact still get three links and no subitems**, which is the
  threshold question this document already had open above. Still open.

### Still unseen

No headless browser here, so the same caveat as the passes above holds and is
stated rather than implied: the new header is reasoned from the tokens and the
cascade, not looked at. **Worth checking by eye in this order**: below 1024px,
that *Contents* now carries a disclosure triangle and opens; above 1024px, that
the triangle is gone and the label reads as a caption rather than as a first
item; and both in the dark rendering, where `--color-muted` is `#8b9197`.
