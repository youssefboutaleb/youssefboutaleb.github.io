# youssefboutaleb.github.io

Personal engineering portfolio — a static site with no runtime dependencies,
served directly by GitHub Pages.

## Architecture

The seven published pages share an identical head, sidebar, navigation and
footer. Those are written **once** and rendered into the pages by a build step,
so the site cannot drift out of sync with itself again.

```
src/
  site.json          identity, contact details, social profiles, navigation
  layout.html        the page shell — head, sidebar, nav, footer
  partials/          item templates for the repeated lists in the shell
  pages/*.html       page content only, one file per page
assets/
  css/main.css       the entire design system (see DESIGN.md)
  fonts/             self-hosted Noto Sans (woff2 / woff / ttf)
images/, data/       portrait, brand icons, CV, workshop slides
tools/
  build.py           renders src/ → the *.html files in the repository root
  check.py           verifies the built site
*.html               BUILD OUTPUT — generated, do not edit by hand
```

Deployment stays build-free: the generated `*.html` files are committed and
GitHub Pages serves them as-is. `.nojekyll` disables Jekyll processing.

## Working on the site

Edit content in `src/pages/`, shared chrome in `src/layout.html`, and identity
or navigation in `src/site.json`. Then:

```bash
python3 tools/build.py      # regenerate the root *.html files
python3 tools/check.py      # verify before committing
```

Preview by opening `index.html` in a browser, or:

```bash
python3 -m http.server 8000
```

`tools/build.py --check` exits non-zero if the committed pages are stale, which
makes it usable as a pre-commit or CI gate.

### What `check.py` verifies

- Every local `href`/`src` resolves to a file that exists, and every in-page
  anchor points at an id that exists
- No inline `style=` attributes and no inline event handlers
- Every `<img>` has an `alt`; every `target="_blank"` has `rel="noopener"`
- Exactly one `<h1>` per page, and no duplicate `id`s
- Every class used in the markup has a rule in `main.css`, and every rule and
  token is used by something (dead CSS is reported, not fatal)
- Every `var(--token)` is defined
- Tags are balanced and correctly nested
- The committed pages match their sources

Requires only Python 3 from the standard library. No Node, no bundler, no
package manager.

## Design system

A classic academic stylesheet in the lineage of the orderedlist **Minimal**
theme this site was forked from: a sticky identity rail, a plain document, one
typeface, one blue for links, hairlines for structure.

Typography, colour, spacing, components, responsive behaviour and accessibility
rules — plus an explicit list of what is *out of scope* — are documented in
**[DESIGN.md](DESIGN.md)**. Read it before adding a component; almost
everything on the site is already expressible with `.block`, `.entry`,
`.deflist` and `.tag`.

## Credits

Originally forked from [elyesmanai.github.io](https://github.com/elyesmanai/elyesmanai.github.io);
theme lineage [orderedlist](https://github.com/orderedlist). The current design
system, markup and build are original work.
