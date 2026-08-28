# Contact: the visual pass

The record of the pass that reset how Contact is *set*, after an earlier pass
had already reset what it is *made of*. [`contact.md`](contact.md) owns the
rules; this file owns what changed and why, for the next agent.

The brief was a restrained, minimal, classic redesign with andrewng.org as a
structural reference only. What it found was not a design problem. It was four
components diverging from the one they are stacked against, plus one link
treatment opting out of the site's own rule.

---

## Before and after

| | Before | After |
|---|---|---|
| Right edge of the rows | 908px, the full content column, against 611px on the strip 40px above it | `max-width: var(--measure)`, one edge |
| Value alignment | `text-align: right`, the only right-set value in the label-column idiom | Flush left |
| Row rule | `border-bottom`, a trailing hairline under each block's last row | `border-top` with the first row reset, as `.hero-facts`, `.skill` and `.result` do |
| Label column | 10rem here, 7.5rem on `.hero-facts` | 10rem on both |
| Row padding | `--space-4` here, `--space-3` on `.hero-facts` | `--space-3` on both |
| Collapse breakpoint | 480px here, 600px on `.hero-facts` | 600px on both, label going bold |
| Address at rest | `--color-heading`, indistinguishable from the inert rows | `--color-link`, underline on hover |
| Block order | Contact Details, Opportunities & Services, Connect | Contact Details, Connect, Opportunities & Services |

Nothing else moved. No wording, no claim, no number, no address, no heading, no
new component, no new token, no new pattern. `availability` is untouched, which
[`CLAUDE.md`](CLAUDE.md) §4 requires.

## The measurements the decisions rest on

Taken from the shipped font with `fontTools`, at the sizes the page actually
renders, rather than estimated:

| | |
|---|---|
| `--measure`, 74ch at 15px | **611px** |
| Content column at 1024px and above | 1240 minus 32 padding minus 240 rail minus 60 gap = **908px** |
| Value column once capped, at a 10rem label | **435px** |
| `Consulting & services` label | **141px** (7.5rem is 120px) |
| `Telephone / WhatsApp`, French | **150px** |
| `Cloud data platforms, reliable ETL/ELT pipelines, warehousing, and data quality` | **520px**, so it wraps |
| The French counterpart of that value | **612px**, so it wraps harder |
| `Availability` 71px, `Based in` and `Certified` 56px, `Languages` 72px | all clear 10rem comfortably |

Those numbers settled two things an eye could not. The label columns had to be
reconciled **upward** to 10rem, because the content will not fit 7.5rem; and
right-alignment had to go, because capping the rows makes two values wrap and a
wrapped value set right sets ragged against the label it answers.

## What was decided and not built

- **Leading with Opportunities & Services**, which is andrewng.org's shape.
  Rejected with the author: his routing block *is* the address list, each
  purpose carrying the email that serves it, and all three addresses here reach
  the same person. Copying it would have manufactured a distinction that does
  not exist and put two rows of delay in front of what a recruiter came for.
- **A routed contact list**, one block of purpose-plus-address rows. Same
  reason, and it would have needed new claim prose about which purpose reaches
  which address, which is the author's to write, not a renderer's to infer.
- **Retitling `Contact Details`**, which is close to a tautology under an `h1`
  reading `Contact`. Left alone: the rail reads better with it than without,
  and the id is already `direct-contact`.
- **Raising the channel value to `--text-base`** for more hierarchy.
  [`DESIGN.md`](DESIGN.md) §1 assigns `--text-md` to contact rows by name, and
  a token role is not worth breaking for a rung on a ramp.
- **Contact-only spacing.** The page is eight rows and the temptation was to
  open it up. `.block`'s `--space-6` is the site's rhythm and the page is not
  entitled to its own.

## Corrections made to this pass's own claims

- I wrote into [`DESIGN.md`](DESIGN.md) that *the idiom's label column is
  10rem*. It is not: `.result` is 13rem and `.skill` is 15rem, each sized to
  what it holds. The rule that actually holds is narrower and is what got
  written instead: **label columns stacked on the same page share a width**;
  ones that are not stacked do not have to.
- The obvious reading of the label mismatch was to pull `.contact-list` down to
  the strip's 7.5rem, and the measurement killed it before it was proposed. Two
  English labels and two French ones exceed 120px.

## Still open, and author-led

- **There is still no closing route to this page.** Nothing links here but the
  navigation. Moving Opportunities & Services last gives Contact a closing
  line of its own, which is not the same thing as Home gaining a way in.
  [`contact.md`](contact.md) §8.
- **`Opportunities & Services` and [`CLAUDE.md`](CLAUDE.md) §3.** Untouched
  here and untouchable by an agent: raised, deleted, restored by the author.
  [`contact.md`](contact.md) §5.
- **[`contact.md`](contact.md) §4 is stale against §6** and was already so
  before this pass. §4 describes the merged single `Based in` row; §6 records
  that arrangement as one of four that failed and lists the page header as the
  one that shipped. Not corrected here, because §4 reads as history and only
  the author knows whether it is meant to.
