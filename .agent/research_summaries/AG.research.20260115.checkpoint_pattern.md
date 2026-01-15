# Research Summary: Checkpoint & Compaction Primitive (Claude Code Pattern)

**Project**: Antigravity
**Type**: Research
**Date**: 2026-01-15
**Topic**: Adoption of "Checkpoint / Compaction" (STATE + NEXT) as a core primitive to mitigate Double Penalty.
**ID**: AG.research.20260115.checkpoint_pattern
**Tags**: [research, agentic-state, checkpoint, compaction, double-penalty, claude-code]

## 1. The Problem: "Double Penalty"
In autonomous agentic workflows (Agentic Engineering), a "Double Penalty" occurs when an agent fails or loses context:
1.  **Direct Cost**: The token/time cost of the failed attempt.
2.  **Cognitive/Recovery Cost**: The massive load on the Human Operator to "download" the agent's internal state (thousands of log lines) to resume work or fix the error.
*Source: Analysis of "Claude Code" agentic patterns and "Agentic Engineering" literature.*

## 2. The Solution: Checkpoint / Compaction (STATE + NEXT)
The "Claude Code" project (and similar advanced agents) mitigates this via a generic primitive:
*   **Checkpoint**: A hard save of the current "Mental State" (not just code matches).
*   **Compaction**: Summarizing the conversation/reasoning history into a concise block to free up context window while retaining direction.
*   **The Artifact**: A file (or structural rule) updated constantly (e.g., every 20-30 mins) containing:
    *   **STATE**: Where are we? (High-level narrative).
    *   **NEXT**: What is the immediate next step?

## 3. Gap Analysis: Antigravity 2026
Does Antigravity already have this?
*   **FixLog (`.json`)**: Persists *atomic code changes* and test results. (Excellent for Rollback, poor for Narrative Resumption).
*   **ChromaDB**: Persists *semantic vectors*. (Good for retrieval, invisible to human).
*   **Task.md**: Persists *To-Do list*. (Good for high-level tracking, lacks "Reasoning State").
*   **Audit (`events.jsonl`)**: Persists *event stream*. (Too granular for quick resumption).

**Verdict**: Antigravity lacks a specific **Narrative Compaction** primitive. If the session crashes, the "Thought Process" is lost, and the user must reconstruct it from granular logs.

## 4. Recommendation (ADR Preview)
**YES, adopt this primitive.**
It should not replace FixLogs but complement them.

### Proposed Implementation
Introduce a **`checkpoint.md`** (or `state.md`) in `.agent/current_state/` or root, updated via `task_boundary` or a dedicated skill/rule.
Structure:
```markdown
# Session State: [Timestamp]
## Current Goal
[Narrative Summary of WHAT we are trying to achieve right now]

## Last Outcome
[What happened in the last step? Success/Fail/Insight]

## Compaction
[Summary of previous 20 steps, flattened]

## NEXT (Immediate)
[Specific next action]
```
This reduces the "Double Penalty" to near zero: The human only needs to read `state.md` to resume.
