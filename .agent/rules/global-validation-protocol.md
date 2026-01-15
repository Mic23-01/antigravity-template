---
trigger: always_on
description: Global Validation Protocol (Leader/Supervisor)
globs: "**/*"
---

# 👑 LEADER PROTOCOL: Validation & Supervision (ALWAYS ON)

**SUPREME DIRECTIVE**: This is the root rule of Antigravity. Every operation must pass through this gate. Non-compliance with this protocol is considered a critical failure.

## 0. High-Resolution Planning (Planning Gate)
BEFORE any technical action, the Agent MUST produce a plan. The depth depends on complexity:

* **Zero Step (Session Sentinel)**: Execute `canary_check`. If it detects a **Dirty Session** (modifications without FixLog), **STOP** immediately. You must sanitize memory before working.

* **Standard Plan (Strict)**: Mandatory for complex changes. Requires: Objective, Atomic Steps, Risks, Success Criteria.
* **Micro-Plan (Adaptive Exception)**:
    * **Trigger**: PERMITTED ONLY IF: Modification ≤ 2 files AND No new libraries AND No DB/API changes.
    * **Format**: Quick bulleted list of actions + Verification tests.
    * **Prohibition**: Forbidden to skip the thought phase (`sequential-thinking`), even in Micro-Plans.

## 1. Filesystem Monitoring (MANDATORY)
In EVERY response (notify_user or final output), the Agent **MUST** include a final section named `[FILESYSTEM UPDATES]` listing atomically:
- **NEW**: [file path]
- **MODIFY**: [file path]
- **DELETE**: [file path]
If there were no changes, write `NONE`.

## 2. Initial Reasoning Phase (Sequential Thinking)
BEFORE proposing or executing any technical action:
1.  **Activate** `sequential-thinking`.
2.  **Analyze** the request into fundamental axioms.
3.  **INTERRUPT**: If the request is ambiguous, **DO NOT PROCEED**. Ask for clarification.

## 3. Active Research Phase (RAG Loop)
If technical certainty is lacking (not 100%):
1.  **Consult** Gold Sources in `docs_custom/SOURCES.md`.
2.  **Cross-Validate** with `brave-search` (time limit: last year).
3.  **Deep-Read** with `markdownify` before asserting a solution.
4.  **Context Check (Mandatory)**: Before acting, LOAD the pertinent `docs_custom/` document (e.g., Architecture for Backend, Brand for UI).

## 4. Synthesis & Validation Phase
- If there is conflict: **The most recent documentation (MCP) always wins.**
- **INTERRUPT**: If the solution requires an architectural change or the use of new libraries, **DO NOT PROCEED** without explicit user approval on an `implementation_plan.md`.

## 5. Protocol Fidelity
All other rules in `.agent/rules/` are subordinate to this one. If a rule requires interaction (Fork/Choice), the Agent must respect it rigorosuly without attempting autonomous resolution.

> [!IMPORTANT]
> **Hallucination is the critical failure.** Better one extra question than one file modified incorrectly or missing.
