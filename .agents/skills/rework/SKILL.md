---
name: rework
description: The standardized 4-stage collaborative workflow for changing anything on this site: investigate existing implementation, analyze technical root causes, present 2-3 costed options and recommendations to the user, collect feedback via interactive questions modal, then edit sources, re-stamp translation locks (tools/build.py --sync), and verify via check.py.
---

# Rework

The executable form of [`CLAUDE.md`](../../../CLAUDE.md) §10 and [`.agents/AGENTS.md`](../../../.agents/AGENTS.md). It defines the compulsory 4-Stage Collaborative Method for pair programming, audits, copy changes, and system refactoring across this portfolio repository.

Do not skip phases to be helpful. Skipping investigation causes symptom-patching; skipping questions causes positioning decisions to be made without the author.

---

## The Three Principles That Belong Strictly to the Author

1. **Claims, numbers, positioning, legal status.** Job titles, metrics, proficiency levels, residence permit status, work authorization, targeted roles. No option list makes one of these safe to decide alone.
2. **Generated build outputs.** Root `*.html` files are build outputs. Edit records in `src/data/*.json`, fragments in `src/pages/*.html`, overlays in `src/i18n/`, and model documents.
3. **New claim prose.** You may retire a sentence, move it, or derive it from structured data. Writing a new sentence that asserts a new claim about the author is the author's decision.

---

## Stage 1: Investigation & Audit

Ground yourself before forming an opinion or proposing changes:

- Read [`CLAUDE.md`](../../../CLAUDE.md), [`DESIGN.md`](../../../DESIGN.md), and the specific **page model document** (`home.md`, `career.md`, `projects.md`, `research.md`, `writing.md`, `teaching.md`, `workshops.md`, `awards.md`, `skills.md`, `contact.md`, `diagrams.md`).
- Inspect `src/data/*.json`, `src/i18n/*.json`, `src/pages/*.html`, `assets/css/main.css`, and `tools/build.py`.
- Run baseline verification: `python3 tools/build.py --check && python3 tools/check.py`.
- Identify root causes, orphaned content, and outdated claims before making any proposals.

---

## Stage 2: Technical Review & Analytics

Gather evidence and analyze alignment:

- Analyze grammar, tone, conciseness, and alignment with high-tier Data Engineering positioning.
- Ensure strict adherence to factual accuracy: **Never invent fake business impact numbers or alter legal claims/dates**.
- Verify single-source-of-truth policies (`availability` in `src/site.json`, citable `impact` lines in bullets).
- Enforce the dash ban: Em dashes (U+2014) and En dashes (U+2013) are strictly forbidden across all repository files.

---

## Stage 3: Collaborative Options & Questions

Present 2-3 costed options for review before editing:

- **Costs**: Work required, what has to move or change.
- **Gains**: Which findings or issues it resolves.
- **Weakens**: What gets worse or what trade-offs exist.

Use the interactive questions modal (`ask_question`) to gather targeted user choices, stack details, or scale metrics. Always prefix the recommended option with `(Recommended)`.

---

## Stage 4: Implementation & Verification

Execute edits and verify output integrity:

- Edit source files in `src/` and model `.md` files. Never hand-edit root `*.html`.
- Synchronize translation locks and rebuild:
  ```bash
  python3 tools/build.py --sync && python3 tools/check.py
  ```
- Propagate changes to model documents and verify rendered outputs across English and French locales.
