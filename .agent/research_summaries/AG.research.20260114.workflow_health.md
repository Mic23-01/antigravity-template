# Research Summary: Workflow Documentation & Health Check Integration

## 1. Context
User requested a summary of Antigravity workflows and advice on integrating health checks (`canary_check`, `deep_search`, `check_chroma`) into the Librarian role.

## 2. Findings
- **Workflows Identified**: `/custom_project`, `/deep_rag`, `/librarian`, `/refactor`, `/research_rag`, `/tech_rag`.
- **Librarian Role**: Defined as "Hygiene Proactive" & "Structural Analysis".
- **Health Checks**: `canary_check.py` exists and validates system integrity (config files, workflows, scripts).

## 3. Decision (ADR)
**Decision**: Integrate `canary_check.py` into the `@/librarian` workflow.
**Rationale**: The Librarian is responsible for project hygiene. Removing files (ghost code) carries inherent risk. A mandatory run of `canary_check.py` in the Verification phase ensures no critical system component is broken by cleanup operations.
**Status**: Implemented in `.agent/workflows/librarian.md`.

## 4. Documentation
Created `docs/WORKFLOW_SUMMARY.md` as a quick reference guide appropriately.
