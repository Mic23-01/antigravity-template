---
description: "The Project Architect: Context-Aware Research, Structural Impact (DuckDB), and Implementation Blueprint."
---

1) Analysis & Definition (Architectural Gate)
- Consult the Leader Supervisor (`.agent/rules/global-validation-protocol.md`).
- **Strategic Alignment**: Verify `docs_custom/product_strategy.md` (Vision) and `docs_custom/domain_language.md` (Terms) to ensure the solution fits the project's long-term goals.
- **Objective**: Determine if this is a **Fix** (Correction), **Enhancement** (Evolution), or **Optimization** (Performance).

2) Structural Impact Mapping (The DuckDB Internal Scan)
- **Action**: Analyze the *current* state of the project before searching externally.
- **Tool**: `uv run --with duckdb .agent/project/librarian.py --audit`
- **Deep Scan**: Search for related components, data flows, or similar logic blocks in the codebase to avoid redundancy.
- **Dependency Check**: Identify if the proposed research area touches critical "Blast Radius" files (Check `architecture.md`).

3) Targeted RAG (Precision Search)
**Step 0: Internal Canon Check**
- **Skill**: `resolve_canon_sources` (Custom > Template).
- Read the Canon Source. If the topic is Gold, use `markdownify` before proceeding.
A) Official Docs: Prioritize official documentation for libraries already in the project.
B) Microsoft Learn / Context7: Resolve SDK/API specifics.
C) Brave-search: Only for specific technical "how-to" if official docs are insufficient.

4) Synthesis & Implementation Blueprint (The Blueprint)
**A) Always: Research Summary**
- Generate `.agent/research_summaries/<Prefix>.research.YYYYMMDD.<slug>.md`.
- **MANDATORY**: Include a "Structural Impact" section explaining *where* and *how* this change fits into the existing code.
**B) The Blueprint (Actionable Impact)**
- Provide a concrete **Implementation Blueprint**:
  - Suggested CLI commands (`uv run`, `npm run`, etc.).
  - Code snippets following the project's style (Ref: `brand_identity_guide.md` Persona).
  - List of files to be modified/created.

5) Persistence & ID (MANDATORY)
- **ID Research**: `<Prefix>.research.YYYYMMDD.<slug>`
- **Metadata**: `project=<ProjectName>, type=architect_research, status=ready_to_implement`.

6) Final Output (The Handover)
- Synthesis + Implementation Blueprint.
- **FILESYSTEM UPDATES**: Mandatory for every output (Leader Rule).
