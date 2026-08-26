# Career experience: three copy-ready content models

All variants use the repository's rendered schema: `start` and optional `end`
derive the visible period, `stack` is capped at four key technologies, and
either `groups` or `points` supplies the bullets. Bold tags are intentional:
they give a recruiter an immediate scan path while preserving readable prose.

## Evidence control

The supplied brief supports mechanisms, system constraints, and three hard
metrics: 30-minute telemetry, about 2,000 frames per second, and a 100x
preprocessing speedup. The existing portfolio also records EUR1,400/month in
Azure savings; retain it only if it can be supported by a cost report, ticket,
or manager confirmation. No throughput, source-count, freshness, recovery,
incident, or ML-quality baseline was supplied, so none is invented below.

The referenced Google Doc was not accessible to the browser session. The
review therefore follows the formula in the brief rather than claiming to
audit that document's exact formatting: clear ownership, concrete technical
mechanism, stated constraint or metric, and outcome.

## Option A: Grouped Architectural Focus (published default)

Best for the portfolio: it makes Data Engineering the primary thread, gives
JACQUEMUS enough structure to show integration, processing, and operations,
then presents ML and signal processing as supporting systems depth. The exact,
production-ready JSON is [`src/data/experience.json`](src/data/experience.json).
It uses these architectural lenses:

| Employer | Architecture headings |
| --- | --- |
| JACQUEMUS | Data Integration & Analytics; Distributed Processing & Operations |
| OLIVESOFT | API-Led Data Integration |
| REGIM Lab | Smart-Meter Analytics; Telemetry Integrity |
| OEM ENGINEERING | Low-Latency Classification; Signal Preprocessing |

## Option B: Metric & Impact-First Model

This is the strongest CV model only after the current evidence gaps are filled.
Where a hard metric is not supplied, the opening names a measurable system
constraint rather than pretending an outcome was measured.

```json
[
  {
    "company": "JACQUEMUS",
    "url": "https://www.linkedin.com/company/jacquemus/posts/?feedView=all",
    "role": "Data Engineer &amp; Data Operations Engineer",
    "start": "2024-08",
    "domain": "E-commerce &amp; Retail",
    "stack": ["Azure Data Factory", "Azure Fabric", "Apache Spark", "Datadog"],
    "points": [
      "Reduced Azure infrastructure spend by <b>&euro;1,400 per month</b> by automating resource schedules.",
      "Built <b>Azure Data Factory</b> integration pipelines that landed enterprise data in <b>Azure Data Lake</b> and <b>Azure SQL Database</b>.",
      "Implemented <b>Azure Fabric PySpark/Python notebooks</b> for ingestion, transformation, and exploration; developed <b>Apache Spark</b> jobs for batch and near-real-time workloads.",
      "Instrumented data pipelines with <b>Datadog monitoring and logging</b> to speed incident triage and resolution."
    ]
  },
  {
    "company": "OLIVESOFT",
    "url": "https://www.linkedin.com/company/olivesoft/posts/?feedView=all",
    "role": "Data Engineer Intern",
    "start": "2024-02",
    "end": "2024-07",
    "domain": "Customer Service",
    "stack": ["MuleSoft", "Salesforce Service Cloud", "Diduenjoy", "RAML"],
    "points": [
      "Prevented a slow or unavailable downstream feedback platform from blocking service-desk workflows through <b>asynchronous MuleSoft API-led integration</b>.",
      "Connected <b>Salesforce Service Cloud</b> and <b>Diduenjoy</b> with RAML/REST contracts, retries, and explicit error-handling flows."
    ]
  },
  {
    "company": "REGIM Lab",
    "url": "",
    "role": "Machine Learning Engineer Intern",
    "start": "2023-06",
    "end": "2023-08",
    "domain": "Smart-Meter Telemetry",
    "stack": ["Regression Models", "Ausgrid Dataset", "Web3", "Ethereum"],
    "points": [
      "Ingested smart-meter telemetry at <b>30-minute intervals</b> through a <b>Web3 monitoring platform</b>.",
      "Reduced false positives by tuning a <b>regression-based anomaly-detection pipeline</b> on the Ausgrid smart-meter dataset.",
      "Stored hashes of meter readings with <b>Ethereum smart contracts</b>, creating a tamper-evident integrity record."
    ]
  },
  {
    "company": "OEM ENGINEERING S.A.R.L",
    "url": "https://www.linkedin.com/company/oem-engineering-s-a-r-l/posts/?feedView=all",
    "role": "Machine Learning &amp; Statistical Engineer",
    "start": "2022-09",
    "end": "2023-05",
    "domain": "Industrial Instrumentation",
    "stack": ["C++", "scikit-learn", "NIR Spectroscopy"],
    "points": [
      "Sustained approximately <b>2,000 frames per second</b> inference by engineering a <b>C++ pipeline</b> with Savitzky-Golay filtering.",
      "Trained a <b>scikit-learn Random Forest classifier</b> for real-time metal classification from NIR spectroscopy signals."
    ]
  },
  {
    "company": "OEM ENGINEERING S.A.R.L",
    "url": "https://www.linkedin.com/company/oem-engineering-s-a-r-l/posts/?feedView=all",
    "role": "Data Analysis &amp; Signal Processing Intern",
    "start": "2022-06",
    "end": "2022-08",
    "domain": "Industrial Instrumentation",
    "stack": ["C++", "Savitzky-Golay Filtering"],
    "points": [
      "Delivered a <b>100&times; preprocessing speedup</b> by building a C++ Savitzky-Golay filter for NIR signals used in metal classification."
    ]
  }
]
```

## Option C: High-Density Technical Summary Model

This version is tuned for a five-second recruiter scan and a senior engineer's
second pass. It removes explanatory headings and limits every role to the
minimum number of proof-bearing bullets.

```json
[
  {
    "company": "JACQUEMUS",
    "url": "https://www.linkedin.com/company/jacquemus/posts/?feedView=all",
    "role": "Data Engineer &amp; Data Operations Engineer",
    "start": "2024-08",
    "domain": "E-commerce &amp; Retail",
    "stack": ["Azure Data Factory", "Azure Fabric", "Apache Spark", "Datadog"],
    "points": [
      "Built <b>Azure Data Factory</b> integration pipelines into <b>Azure Data Lake</b> and <b>Azure SQL Database</b>; developed <b>Azure Fabric PySpark/Python</b> workloads for ingestion and transformation.",
      "Developed <b>Apache Spark</b> jobs for batch and near-real-time processing, and instrumented pipeline monitoring and logs in <b>Datadog</b> for incident triage.",
      "Automated <b>Azure resource schedules</b>, reducing infrastructure spend by <b>&euro;1,400 per month</b>."
    ]
  },
  {
    "company": "OLIVESOFT",
    "url": "https://www.linkedin.com/company/olivesoft/posts/?feedView=all",
    "role": "Data Engineer Intern",
    "start": "2024-02",
    "end": "2024-07",
    "domain": "Customer Service",
    "stack": ["MuleSoft", "Salesforce Service Cloud", "Diduenjoy", "RAML"],
    "points": [
      "Built an asynchronous <b>MuleSoft API-led integration</b> between Salesforce Service Cloud and Diduenjoy; RAML/REST contracts, retries, and error handling kept downstream failures from blocking service desks."
    ]
  },
  {
    "company": "REGIM Lab",
    "url": "",
    "role": "Machine Learning Engineer Intern",
    "start": "2023-06",
    "end": "2023-08",
    "domain": "Smart-Meter Telemetry",
    "stack": ["Regression Models", "Ausgrid Dataset", "Web3", "Ethereum"],
    "points": [
      "Built a regression-based anomaly-detection pipeline on Ausgrid smart-meter readings, reducing false positives; ingested Web3 telemetry at <b>30-minute intervals</b> and stored reading hashes through <b>Ethereum smart contracts</b>."
    ]
  },
  {
    "company": "OEM ENGINEERING S.A.R.L",
    "url": "https://www.linkedin.com/company/oem-engineering-s-a-r-l/posts/?feedView=all",
    "role": "Machine Learning &amp; Statistical Engineer",
    "start": "2022-09",
    "end": "2023-05",
    "domain": "Industrial Instrumentation",
    "stack": ["C++", "scikit-learn", "NIR Spectroscopy"],
    "points": [
      "Trained a scikit-learn <b>Random Forest</b> for NIR metal classification and engineered a <b>C++ Savitzky-Golay pipeline</b> sustaining approximately <b>2,000 fps</b> inference."
    ]
  },
  {
    "company": "OEM ENGINEERING S.A.R.L",
    "url": "https://www.linkedin.com/company/oem-engineering-s-a-r-l/posts/?feedView=all",
    "role": "Data Analysis &amp; Signal Processing Intern",
    "start": "2022-06",
    "end": "2022-08",
    "domain": "Industrial Instrumentation",
    "stack": ["C++", "Savitzky-Golay Filtering"],
    "points": [
      "Built a <b>C++ Savitzky-Golay filter</b> for NIR preprocessing, delivering a <b>100&times; speedup</b> for metal classification."
    ]
  }
]
```

## Hiring-manager verdict

Option A is the best live portfolio model. It makes the reader understand the
architecture before the technology list and does not force short internships
to masquerade as broad organisational ownership. Option B is the best
one-page-CV model only after missing measurements are verified; otherwise it
draws attention to the gaps. Option C earns the fastest scan, but compresses
the design choices that distinguish a data engineer from a tool user.

The reference's Staff Engineer standard is a writing bar, not a seniority
claim. The supplied record demonstrates strong early-career data engineering
depth; it does not yet evidence Staff scope such as multi-team technical
direction, a platform standard adopted by others, mentoring, or ownership of
an explicit business/data SLA. Do not imply any of those.

Before using Option B in an application, collect attributable values for: data
sources and records/bytes processed; pipeline freshness and run frequency;
failure rate, retry recovery, and incident-detection time; the baseline and
test set behind the false-positive reduction; and the cost baseline behind the
EUR1,400/month saving. A manager-confirmed range is better than an invented
precise number.

---

# Pass 2, 2026-08-26: the lede and the Summary merged

## The request

The author: the Career intro and the Summary are redundant, general and not
useful; make them one, get to the point, describe the person. A reference
summary was supplied, in the conventional CV shape: a capability paragraph
followed by three quantified achievement lines.

## Findings

Two blocks were competing to introduce one career, which is the same cause
`home-options.md` and `home-opening-options.md` recorded for Home's hero and
Profile.

| # | Finding | Evidence |
|---|---|---|
| F1 | The lede and Summary paragraph 1 said the same thing at two lengths | Lede, 28 words: *the industrial sensor work that taught me what a pipeline has to survive, and the luxury retail platforms where it now runs*. Paragraph 1, 66 words: *I started on sensor data ... Luxury retail came next* |
| F2 | Paragraph 1 previewed the records below it | JACQUEMUS, OLIVESOFT and Kenzo Paris / LVMH all appear in the `summary` field of `src/data/experience.json`, which career.md section 5 says owns *what is this place and what did I own* |
| F3 | Nothing above the records named the role | Home's `h1` is *Data Engineer*. Career's is *Career*, and 139 words passed before the job being wanted was named |
| F4 | The doctrine, the strongest prose on the page, read third | *the pipelines I ship, I also run* sat behind a paragraph that restated records |

Measured: at `--measure: 74ch`, the opening ran about 2.3 lines of 17px lede
plus about 9 lines of 16px prose, roughly 330px before the first job.

## Options put to the author

| | Structure | Figures | Wording |
|---|---|---|---|
| **A** | **One Summary block, `page-lede` deleted** (chosen) | **Prose only** (chosen) | **49 words** (chosen) |
| B | One lede, Summary block deleted | One figure inside the paragraph | 62 words, keeps the data domains |
| C | Keep both, trim each | Paragraph plus three achievement lines | 55 words, capability-first |

## Before and after

| | Before | After |
|---|---|---|
| Blocks above Experience | `page-lede` plus a two-paragraph `Summary` | `Summary`, one paragraph |
| Words | 139 | 49 |
| Names the role | no | first two words |
| Names companies | 4, all named again within one screen | 0 |
| Carries figures | 0 | 0, unchanged |
| Pages carrying a `page-lede` | Home and Career | Home only |

After:

> Data Engineer, three years in: I build enterprise data pipelines and I run
> them. Industrial sensor data taught me what a pipeline has to survive; a
> luxury retail platform is where it runs now. Error handling, alerting,
> recovery plans and written architecture documentation are part of the
> deliverable, not follow-up.

## Decided against, and why

**The reference summary's three achievement lines were not reproduced.** They
already exist on this page as `.point__impact` lines under the bullets that
earned them, and on Home as *Selected Impact*, which quotes those same bullets
by id. Adding them here would reinstate the `.specs` strip that career.md
section 7 records deleting after *150+* printed three times on one page. The
author chose prose only.

**No figure was woven into the paragraph either.** That variant was offered and
declined; it would have overruled career.md section 7 for one number.

**Seniority is not self-labelled.** The reference opens *Mid-level backend
engineer*. *Data Engineer, three years in* states the same shape from a fact
the page already carried and leaves the grading to the reader.

## Propagated

- `src/pages/career.html`: header reduced to the `h1`, Summary rewritten, the
  block comment rewritten to record why the lede is gone.
- `career.md` section 7: *Summary: the layer the records cannot supply* now
  documents one paragraph and three sentences rather than two paragraphs, and
  carries the no-company and no-figures rules.
- `career.md` section 4: the durations note referred to a claim *in the page
  lede*; the claim is now in the Summary.
- `assets/css/main.css` section 07: the comment said every other page opens on
  *a title and, on Career, a lede*.

`.page-lede` keeps its Home user, so no CSS was orphaned. `check.py` reports
the same four unused classes as before this pass.

## Still open, author-led

The reference's real ask underneath the wording was quantified proof at the top
of the page, and this pass answered it by pointing at the records rather than
by repeating them. Whether that is enough for a recruiter reading for seconds
is the M1 question in `CLAUDE.md`, and the answer there is pipeline case
studies, not a longer summary.
