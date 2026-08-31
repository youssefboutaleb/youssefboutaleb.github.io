# Repository Operating Rules

All agent interactions and modifications across this repository MUST follow the standardized **4-Stage Collaborative Method** specified in [`.agents/skills/rework/SKILL.md`](skills/rework/SKILL.md), [`.claude/skills/rework/SKILL.md`](../.claude/skills/rework/SKILL.md), and [`CLAUDE.md`](../CLAUDE.md):

## The 4-Stage Collaborative Method

### Stage 1: Investigation & Audit
- Read the relevant model document (`career.md`, `projects.md`, `research.md`, `workshops.md`, `home.md`, `awards.md`, `skills.md`, `teaching.md`, `writing.md`, `contact.md`, `diagrams.md`), [`CLAUDE.md`](../CLAUDE.md), and [`DESIGN.md`](../DESIGN.md).
- Inspect `src/data/*.json`, `src/i18n/*.json`, `src/pages/*.html`, `assets/css/main.css`, and `tools/build.py`.
- Identify root causes, orphaned code/content, and outdated claims before making any proposals.
- Run baseline verification: `python3 tools/build.py --check && python3 tools/check.py`.

### Stage 2: Technical Review & Analytics
- Analyze grammar, tone, conciseness, and alignment with high-tier Data Engineering positioning.
- Ensure strict adherence to factual accuracy: **Never invent fake business impact numbers or alter legal claims/dates**.
- Enforce single-source-of-truth rules: `availability` lives exclusively in `src/site.json`, citable bullets live in `src/data/*.json`.

### Stage 3: Collaborative Options & Questions
- Present 2-3 costed options for review in prose (detailing Costs, Gains, Weakens).
- Ask targeted clarifying questions (via interactive questions modal) to gather precise metrics, stack details, or scale figures.
- Always prefix the recommended option with `(Recommended)`.

### Stage 4: Implementation & Verification
- Edit source files (`src/data/*.json`, `src/i18n/*.json`, `src/pages/*.html`, `.md` files). Never hand-edit root `*.html` build outputs.
- Re-stamp translation locks and rebuild synchronously:
  ```bash
  python3 tools/build.py --sync && python3 tools/check.py
  ```
- Propagate changes to model documents and verify rendered outputs across both English and French locales.

## Strict Operational Rules
- **No Em or En Dashes**: U+2014, U+2013, and their HTML entities are strictly banned in all files (`.md`, `.json`, `.html`, `.css`, `.py`).
- **No Direct Root HTML Editing**: Root `*.html` files are generated build outputs. Always modify `src/` sources.
- **Dual Locale Synchronization**: Any edit to English data or prose must be synchronized with French i18n overlays via `python3 tools/build.py --sync`.
