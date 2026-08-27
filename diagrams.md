# Architecture diagrams

The model for [`src/data/diagrams.json`](src/data/diagrams.json) and
`render_diagram` in [`tools/build.py`](tools/build.py).

**`diagrams.json` is empty, and that is the correct state until the author
fills it.** [`CLAUDE.md`](CLAUDE.md) §8/M1 says, in those words, *do not
auto-generate this content*. What is built here is the container: an agent may
extend the renderer, fix the geometry, and add a diagram the author has
described. It may not decide what connects to what.

---

## 1. What a diagram is for

M1 is the site's largest remaining gap: *prove data engineering ability,
harder*. A pipeline described in a bullet is a claim; the same pipeline drawn
is a claim a reader can check the shape of in about three seconds. That is the
whole job, and it sets the bar: **a diagram that does not tell the reader
something the bullets could not is decoration**, and
[`DESIGN.md`](DESIGN.md) Principle 1 does not admit decoration.

The test before adding one: *could a reader answer a question from this picture
that the prose beside it leaves open?* Where the data comes from, what it
passes through, what it lands in, and what breaks if one box stops. If not,
the record already says enough.

## 2. It is inline SVG, and Mermaid was considered

Drawn at build time as inline SVG. No library, no runtime, no external request.

Mermaid was the alternative and was rejected on cost stated plainly: roughly
100KB of JavaScript on every page carrying a diagram, nothing rendered where
scripts are blocked, an empty box in print, and a runtime dependency on a site
that currently ships about forty lines of inline JS in total. Principle 1 is
that this is a document and a reader should be able to print the page and lose
nothing. A diagram that disappears in print fails that on its own terms.

The cost of the alternative is one layout function, and it is already written.

## 3. The shape of a record

```json
{
  "id": "jq_platform",
  "title": "JACQUEMUS order and product data platform",
  "desc": "Salesforce, ORLI/WMS and PostgreSQL feed Azure Data Factory, which
           lands a medallion lakehouse served through Fabric and Power BI.",
  "caption": "The order path. Refresh runs from 10 minutes to daily.",
  "layers": [
    { "label": "Sources",   "nodes": [ { "id": "sf", "label": "Salesforce" } ] },
    { "label": "Ingestion", "nodes": [ { "id": "adf", "label": "Azure Data Factory" } ] }
  ],
  "edges": [ ["sf", "adf"] ]
}
```

| Field | What it is |
|---|---|
| `id` | The anchor, and the template key. **Underscores, not dashes**: `PLACEHOLDER` in `tools/build.py` does not admit a dash |
| `title` | The SVG's `<title>`. What the diagram is |
| `desc` | The SVG's `<desc>`, and **required**. See §5 |
| `caption` | The visible `<figcaption>` beneath it |
| `layers` | Columns, left to right. Each has a `label` and its `nodes` |
| `edges` | Pairs of node ids. The build fails on an edge naming a node no layer declares |

Place it in a fragment with `{{ build.diagram.jq_platform }}`.

## 4. What the build computes, and what it does not

**It computes geometry and nothing else.** Column positions, row positions,
the centring of a short column against the tallest one, the bezier from one
box's right edge to another's left, and where a label has to break.

**It infers no topology.** There is no layout solver deciding what belongs in
which layer, no edge routing that reorders nodes to reduce crossings, and no
attempt to work out a pipeline's shape from its prose. The author declares the
layers and the edges as facts, in the order they should read.

Labels break on words and never mid-word, and stop at three lines. A service
name that hyphenates is harder to recognise than one that overflows.

## 5. `desc` is required, and it is not a caption

The `<desc>` is what a screen reader gets instead of the picture, and it must
carry the architecture **as a sentence**: what feeds what, in what order,
ending where the data lands. A list of box labels is not a description; it is
the same disconnected nouns the drawing exists to connect.

The `caption` is different and is for everyone: the one thing about the diagram
a reader should take away that the boxes cannot say. A refresh interval, a
volume, the failure mode the shape is designed around.

## 6. Theme, print and width

**One palette, inherited.** Strokes and text are `currentColor` and the only
fill is `--color-surface`, so the diagram takes the page's ink in light, in
dark and in print without a second palette to keep in agreement.

**It prints**, unlike the rail and the evidence key, because its content *is*
its shape. `page-break-inside: avoid`, and the overflow container is released.

**Wide diagrams scroll inside the figure.** `.diagram__svg` holds a `min-width`
of `32rem`: a four-layer flow is about 900 user units, and a phone scaling that
to fit would render an 11px label at roughly 4px. Wide content scrolls in its
own container and the body never scrolls sideways.

## 7. Adding one

1. Write the record in `src/data/diagrams.json`.
2. Place `{{ build.diagram.<id> }}` in the fragment, under the record it
   belongs to.
3. Remove the six `diagram*` names from `STAGED_CSS` in
   [`tools/check.py`](tools/check.py). They are staged precisely because
   nothing uses them yet, and `check.py` will tell you they are now in use.
4. `python3 tools/build.py && python3 tools/check.py`.
