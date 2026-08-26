# Home: Languages

The last block on the page, and the last one that was never rebuilt.

```html
<section class="block" aria-labelledby="languages">
  <h3 class="block__title" id="languages">Languages</h3>
  <p class="block__intro">Three, and I have taught in two of them.</p>
  <dl class="deflist">
    <div class="deflist__item"><dt>Arabic</dt><dd>Bilingual proficiency (native)</dd></div>
    <div class="deflist__item"><dt>English</dt><dd>Full professional proficiency</dd></div>
    <div class="deflist__item"><dt>French</dt><dd>Full professional proficiency</dd></div>
  </dl>
</section>
```

---

## Part 1: what is wrong

### 1.1 It is the only block left on Home with nothing to check

Every other block on the page answers to a mechanism. *Currently* projects a
record. *Skills & Evidence* cites them. *Selected Impact* quotes them. The
opening's credentials are generated from `certifications.json`.

Languages is three self-assessments. No link, no record, no tag, nothing a
reader can verify.

That is not a new standard being applied to it. It is the standard that already
removed the other two. [`home.md`](home.md) records why `Domains` was deleted:

> One `.deflist` row listing five industries: no citation, no record, nothing
> to check. It was the one capability-shaped claim Skills & Evidence did not
> govern.

Word for word, that is this block. Domains was deleted, the Profile paragraph
merged away last pass, and Languages is the last one standing.

### 1.2 The intro asserts something the site cannot support

> *Three, and I have taught in two of them.*

`teaching.json` has no language field. Neither does `workshops.json`. Nothing
anywhere in `src/data/` records what language anything was delivered in, so the
claim is unverifiable on a site whose Principle 3 is that claims carry a number
and a link.

It is also the wrong *kind* of sentence. [`DESIGN.md`](DESIGN.md) §11.1 says a
`block__intro` is a pitch. This one is a statistic, and a statistic with no
record under it.

### 1.3 The proficiency scale is the wrong one for the market

*Bilingual proficiency* and *Full professional proficiency* are LinkedIn's
labels, from the US ILR scale.

[`CLAUDE.md`](CLAUDE.md) §4 names France and the EU as the first market. The
standard there is **CEFR**: A1 to C2. It is what Europass uses, what language
certificates are issued in, and what EU job postings ask for. A French or German
recruiter reads *C1* instantly and has to translate *Full professional
proficiency*.

The block whose entire subject is speaking the reader's language is the one
block not doing it.

### 1.4 Arabic restates itself

*Bilingual proficiency (native)*. In the scale being used, "bilingual
proficiency" **is** "native or bilingual". The parenthesis says the label again.

### 1.5 It closes the site on its weakest block

Home's last block is the last thing a reader who scrolls the whole page sees.
Right now that is three unverifiable self-ratings, sitting after the block that
says what changed because something shipped.

### 1.6 The component question and the evidence question are the same question

[`DESIGN.md`](DESIGN.md) §10 draws the line, and Languages is the only thing
left on the correct side of it:

> **A list stays in its page fragment when that page is the only place its
> facts live. It becomes data when it restates facts held elsewhere on the
> site.**

True today, and *only* while 1.1 stays unfixed. The moment a language cites a
record, it starts restating facts held elsewhere and the rule moves it into
`src/data/`. So this cannot be decided as "which component": deciding whether
the block carries evidence decides the component for you.

It is also the last `.deflist` on the site. If Languages leaves it, about 20
lines of CSS become dead and `DESIGN.md` §10 becomes a section about a component
with no users.

---

## Part 2: what evidence actually exists

The site already holds facts that bear on this, and does not connect them:

| Record | Where | What it could evidence |
|---|---|---|
| JACQUEMUS, Paris, France, Aug 2024 to present | `experience.json` | working professionally with a French company |
| OLIVESOFT, REGIM Lab, OEM, Sfax, Tunisia | `experience.json` | Arabic and French working context |
| Engineering degree, ENIS Sfax; Bachelor, ISSAT Mahdia | `education.json` | language of instruction |
| 3 university courses, 2024 and 2025 | `teaching.json` | the intro's "taught in two of them" |
| Peer-reviewed Elsevier paper, Medium articles | `research.json` | writing professionally in English |

**None of this is safe for me to assert.** Which language a course was taught in,
or a degree delivered in, is a fact only the author holds. I have not guessed at
any of it, and the options below that use evidence are all blocked on it.

---

## Part 3: options

### A. Sharpen in place

Keep the block, the `.deflist` and the fragment. Change the scale to CEFR, drop
the Arabic redundancy, rewrite the intro as a pitch that does not assert
anything unverifiable.

```
Languages
<a pitch line>
  Arabic:  Native
  French:  C1
  English: C1
```

- Costs: minutes. Nothing else on the site moves.
- Gains: 1.2, 1.3, 1.4.
- Weakens: nothing. Leaves 1.1 and 1.5: still the one block with nothing to
  check, still closing the page.

### B. Evidence it

`src/data/languages.json`, one record per language, each citing records that
already exist, rendered the way Skills & Evidence renders a capability and its
proof.

```
French   C1    Worked in French at JACQUEMUS  ·  Engineering degree, ENIS
English  C1    Peer-reviewed paper, Elsevier  ·  3 technical articles
Arabic   Native
```

- Costs: a data file, a renderer, and facts only the author has (Part 2). The
  `.deflist` retires and `DESIGN.md` §10 loses its last user.
- Gains: closes 1.1. The block finally matches the page it sits on.
- Weakens: it is a lot of machinery for three rows, and a language section with
  footnotes can read as trying too hard. Arabic would carry no citation, which
  is honest but leaves the strongest one looking weakest.

### C. Move it into the opening

Delete the block. Languages becomes a third fact line beside Availability and
Certified:

```
Data Engineer

I build and operate enterprise-scale data platforms on Microsoft Azure: ...

Availability: EU residence permit holder. Open to relocation within the EU ...
Certified:    Microsoft ×3 · Astronomer ×2 · MuleSoft · Talend · Datadog ×3
Languages:    Arabic (native) · French C1 · English C1
```

- Costs: the block, its intro, and any room for evidence. The last `.deflist`
  retires.
- Gains: the three recruiter-filter facts sit together in the first screen,
  where a filter belongs, and two of them are already there.
  [`home.md`](home.md) defends keeping Languages on Home rather than Contact
  because *"a filter a recruiter has to open a second page for is a filter that
  gets applied by guessing"*, and that argument is about reaching the reader
  early. Last on the page is the least early place there is.
  It also leaves **Selected Impact** closing Home, which fixes 1.5: the page
  would end on what changed because something shipped.
- Weakens: one line has no room for nuance, and [`CLAUDE.md`](CLAUDE.md) §1 is
  explicit that this site exists to hold what the two page CV had to cut.
  Compressing is the instinct this site is supposed to resist.

---

## Part 4: recommendation

**C, with A's corrections applied to the wording.**

The argument for C is the one already written in `home.md` and not followed
through: Languages is on Home because it is a hiring filter and a filter must
reach the reader early. Availability and Certified are the other two facts a
recruiter filters on, they now sit together under the pitch, and Languages is
the third. Splitting it from them and putting it 1,200 pixels lower serves
nothing.

Against C is [`CLAUDE.md`](CLAUDE.md) §1, and it deserves a straight answer
rather than being waved past. §1 says length is not a defect and the site holds
what the CV had to cut. **It does not say every fact deserves a block.** What
was cut from a two page CV is depth: pipelines, failures, what changed. Three
proficiency ratings are not depth, and a block heading plus a pitch line plus a
`<dl>` does not add any. It is the one place on Home where the format is larger
than the fact.

**B is the right answer only if the author wants to record language per
record**, and that is a real content decision, not a formatting one. Held.

---

## Part 5: what needs the author

1. **CEFR levels.** *Full professional proficiency* maps to roughly B2 or C1,
   and *bilingual* to C2 or native. Self-assessment is the author's, and I will
   not pick a level.
2. **The intro's claim.** If a block survives, "taught in two of them" either
   gets a record behind it (which language, which courses) or is replaced.
3. **Arabic's label.** *Native* or *C2*, not both.

---

## Part 6: what was decided and built

| Question | Answer |
|---|---|
| Placement | **C**: a third fact line in Home's opening |
| Scale | **LinkedIn's, kept.** CEFR considered and declined |
| The "taught in two of them" claim | **Dropped** with the block |

| | Before | After |
|---|---|---|
| Languages | last block on Home, `.deflist`, `<dl>` in the fragment | one `.hero-header__fact` line in the opening |
| Home's last block | Languages | Selected Impact |
| Blocks on Home with nothing to check | 1 | 0 |
| `.deflist` | 1 user | **component deleted** |
| CSS classes | 123 | 121 |

**One adjustment I made and did not ask about.** Keeping LinkedIn's wording and
moving to a single line collide: printing *full professional proficiency* twice
runs the line past 130 characters. The two languages that share a level are
grouped, which prints the scale verbatim once instead of twice:

> **Languages:** Arabic (native) · English and French (full professional proficiency)

Arabic reads *native* rather than *bilingual proficiency (native)*, which was
finding 1.4: in that scale the top tier is "native or bilingual", so the
original said one thing twice. Both are one string,
`languages` in [`src/site.json`](src/site.json), so either is a one word change.

### Consequences beyond the block

- **`.deflist` is deleted**, not deprecated: its rules, its stylesheet section
  and its entry in the contents list. Sections 13 to 20 of `main.css`
  renumbered to 12 to 19.
- **[`DESIGN.md`](DESIGN.md) §10 was rewritten** from "Definition lists" to
  "The rule that emptied a component". The rule outlived the component, and the
  section now records all four departures (Domains, Skills, Selected Impact,
  Languages) as the rule working, plus a line saying nothing should bring it
  back.
- Stale `.deflist` references cleared from `DESIGN.md` (7) and `README.md` (1).

### Not done

**Option B, evidencing the languages, was not built and is not scheduled.** The
records in Part 2 that could support it are real, but which language a course,
a degree or a paper was delivered in is a fact only the author holds, and
nothing in `src/data/` records it. If that data is ever added, §10's rule moves
Languages out of `site.json` and into `src/data/` on its own, which is the
rule working rather than a reversal.

---

## Part 7: the second pass, and a correction

Part 1.2 said the intro's claim (*"three, and I have taught in two of them"*)
was unverifiable because no language field exists anywhere in `src/data/`.

**That was true and it was the wrong conclusion.**
[`src/pages/teaching.html`](src/pages/teaching.html) has been stating it in its
spec strip the whole time:

```
Language & Tooling
  Instruction    French & English
  Materials      English
```

The claim was sound. The citation was missing, and I looked for the fact in the
data directory rather than on the page. Option B, which Part 6 recorded as
blocked on facts only the author holds, was never blocked.

### What changed

The one line collapsed under its own punctuation:

> Languages: Arabic (native) · English and French (full professional proficiency)

Languages is three pairs, so an inline run needs one separator to divide the
three and another to bind each name to its level. A middot cannot do both. The
merge of English and French was the symptom: printing the level twice was too
long for one line, so two languages that are not one fact got written as one.

It is a label column now, `.hero-facts` ([`DESIGN.md`](DESIGN.md) §10.2):

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

- **No separator inside Languages.** Alignment does the work punctuation was
  failing at.
- **The middot survives on the Certified row**, which is its correct use: five
  short peers with no internal structure.
- **Two of the three languages now cite a record**, like every other claim on
  Home. Arabic cites nothing and that stays visible.
- **Languages became data**, `src/data/languages.json`, not by preference but
  by §10's rule: it cites records held elsewhere, so it is no longer a string
  in `site.json`.

### Note for whoever reads this next

The proficiency wording is LinkedIn's scale and is the author's, kept after
CEFR was considered and declined for the EU market. **Do not convert it.** The
one thing that was changed is that Arabic no longer says *bilingual proficiency
(native)*, which stated one thing twice; it says *Native*.
