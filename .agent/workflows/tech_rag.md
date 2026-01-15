---
description: "Tech Task Protocol: RAG -> Plan -> Edits -> Test -> Evidence -> FixLog (Chroma) -> Checker"
---

1) Analysis & Definition (Adaptive BMAD Protocol)
- **Mode Check**: Read `WorkflowMode` in `.agent/project/PROJECT_AGENT_CONFIG.md`.
- **Complexity Trigger**: Does the task touch > 2 files OR change DB schema / API / Dependencies?
  - **YES (Complex -> Strict)**: Break down into **Numbered Stories**. Mandatory User **STOP** between stories.
  - **NO (Simple -> Adaptive)**: Proceed with an immediate "Micro-Plan" (Action List + Test).
- **Objective**: 1 sentence (Problem + Outcome).
- **Done Criteria**: Verifiable definition (test/behavior).

2) Context & Placeholders (Project-Agnostic)
- **Identify Project**: Determine `<ProjectName>` and `<Prefix>` from `.agent/project/PROJECT_AGENT_CONFIG.md`.
- **Context Switcher (MANDATORY)**:
  - If **UI/Frontend**: Activate `ui_ux_designer` and read/update `docs_custom/brand_identity_guide.md`.
  - If **Backend/Arch**: Read `docs_custom/architecture.md`.
  - If **Business Logic**: Read `docs_custom/domain_language.md`.
- Always use placeholders `<ProjectName>` and `<Prefix>` in communications and Chroma metadata.

3) RAG (Strict Order)
**Step 0: Internal Context Discovery**
- **Skill**: `resolve_canon_sources` (Handles hierarchy Custom > Template)
- **Check**: Does it contain official links or internal best practices?
- **Decision**: If yes -> Deep Read (markdownify). If no -> Brave Search (Step 2).

A) Repo-first: Read pertinent files in the project.
B) Official Docs: Use links identified in the active Canon Source (Custom or Template).
C) Chroma: Search for similar fixes/decisions filtering by `project=<ProjectName>`.
D) Microsoft Learn / Context7: Official docs.
E) Brave-search: Only if external info outside canon is needed.

4) Controlled Execution
- Small, localized changes.
- Nothing destructive without review.
- Respect Security Guardrails (`.agent/rules/mcp-scope-secrets-guardrail.md`).

5) Test Gate (Interactive)
- **Skill**: `test_gate_bivio` (Handles Smoke/Deep/Debug levels).
- **POLICY "Zero Silence for Ghost Failures"**: Report pre-existing errors immediately.

6) Chroma Persistence (MANDATORY)
- **Skill**: `fixlog_writer` (Generates standard JSON payload).
- For validation/demo (**Task contains 'CANARY'** or `EVAL_MODE=1`): use STABLE ID `<Prefix>.fix.eval.metadata_gate`.
- For real fixes: use automatically generated ID from skill `<Prefix>.fix.YYYYMMDD.<slug>`.

7) Post-check (REGRESSION GATE)
- **Skill**: `regression_gate` (Executes check_chroma + librarian on `fix_logs`).
- **FAIL-FAST**: If the checker FAILS, the Agent MUST STOP and fix metadata.

8) Final Output (EVIDENCE BUNDLE)
- What changed + FixLog ID.
- Tests executed + outcome.
- **FILESYSTEM UPDATES**: Mandatory for every output (Leader Rule).
