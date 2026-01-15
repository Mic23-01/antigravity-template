---
description: "Deep Refactoring Protocol (KILLER 2026): AST Analysis, Blast Radius, and Hard Interrupt"
---

1) Inquiry Phase (Structural AST Check)
- **Skill**: `resolve_canon_sources` (Handles hierarchy `docs_custom/` > Template).
- Consult the Leader Supervisor (`.agent/rules/global-validation-protocol.md`).
- **Structural Mapping**: Use `ast-grep` or `grep_search` to map every syntactic occurrence (not just textual).
- **Blast Radius Report**: Generate a summary indicating:
    - How many files and lines will be touched.
    - Which dependencies (imports/callers) will be impacted.
    - Estimated Risk (Low/Medium/High).

2) Hard Interrupt (Informed Consent)
- **MANDATORY BLOCK**: Present the *Blast Radius Report* and Detailed Modification Proposal (Forecasted Diff).
- **ASK FOR CONFIRMATION**: Call `notify_user` and wait for explicit "Proceed" before executing any edits.

3) Surgical Execution (AST Transformation)
- If refactoring is complex, use `uv run --with libcst` scripts for atomic transformations that preserve formatting.
- Execute changes incrementally.

4) SOLID Validation & Regression Gate
- **Skill**: `regression_gate` (Chroma + Librarian Validation).
- Verify formal quality post-modification.
- Execute the full module test suite (`testing-strategy.md`).
- **Zero Silence**: If refactoring breaks pre-existing tests, stop everything and report.

5) Persistence & Hygiene (Post-Refactor)
- Save a FixLog in Chroma (type=refactor).
- **Final Cleanup**: Delete any temporary transformation scripts or sandboxes.
- **Double Check**: Run `ls` to confirm workspace cleanliness.

6) Final Output (Evidence Bundle)
- Transformative synthesis + FixLog ID.
- **FILESYSTEM UPDATES**: Mandatory for every output (Leader Rule).
