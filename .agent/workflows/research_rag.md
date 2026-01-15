---
description: "Unified RAG Protocol: Research -> (Optional) Decision -> Dual Persistence (Chroma + MD)"
---

1) Analysis & Definition (Planning Gate)
- Consult the Leader Supervisor (`.agent/rules/global-validation-protocol.md`).
- **Strategic Alignment**: Verify `docs_custom/product_strategy.md` (Vision) and `docs_custom/domain_language.md` (Terms) to avoid drift.
- Determine objective: Pure Research (Discovery) or Architectural Decision (Commitment).

2) Memory Check (Chroma)
- Identify `<ProjectName>` and `<Prefix>` from `.agent/project/PROJECT_AGENT_CONFIG.md`.
- Search in `research_summaries` and `decisions` to avoid duplicates.

3) RAG (Strict Order)
**Step 0: Internal Canon Check**
- **Skill**: `resolve_canon_sources` (Handles hierarchy Custom > Template)
- Read the Canon Source. If the topic is Gold, use `markdownify` before proceeding.
A) Repo-first: Analyze code and local documentation.
B) Official Docs / Microsoft Learn / Context7.
C) Brave-search: Only for news or info outside the canon.
- **Massive Ingestion (Optimization)**:
  - For multi-axis searches, use the parallel aggregation tool:
  - `uv run --with aiohttp --with html2text --with beautifulsoup4 .agent/tools/deep_search.py --urls <url1> <url2> ... --output RESEARCH_BUNDLE.md`

4) Synthesis & Options (Dual-Persistence)
**A) Always: Research Summary**
- Generate `.agent/research_summaries/<Prefix>.research.YYYYMMDD.<slug>.md`.
- Contains: Main Learnings, Technical Proofs, Sources.
**B) Conditional: Architectural Decision (ADR)**
- If the task implies a binding choice, include: Options (2-4), Pro/Con Analysis, Choice, and Rationale.
- Save ADR details in Chroma (`decisions` collection).

5) Persistence & ID (MANDATORY)
- **ID Research**: `<Prefix>.research.YYYYMMDD.<slug>` (or `eval.metadata_gate` if CANARY).
- **ID Decision**: `<Prefix^^>-DEC-XXXX` (or `DEC-EVAL-0001` if CANARY).
- Metadata: `project=<ProjectName>, type=research|decision, ...`.

6) Post-check (REGRESSION GATE)
- **Skill**: `regression_gate` (Executes check_chroma on `research_summaries` or `decisions`).
- **FAIL-FAST**: If the checker fails, correct immediately before proceeding.

7) Final Output
- Research Synthesis + (Optional) Decision ID.
- **FILESYSTEM UPDATES**: Mandatory for every output (Leader Rule).
