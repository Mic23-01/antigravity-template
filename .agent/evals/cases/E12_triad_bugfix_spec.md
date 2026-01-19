---
id: E12_triad_bugfix
type: capability_eval
version: 1.0.0
---

# E12: The Bugfix Challenge (Diagnostic Depth)

**Objective**: Measure the agent's ability to identify and fix latent bugs (e.g., race conditions or incorrect logic).

**Scenario**:
- Input file: `.agent/evals/triad/bugfix_challenge.py`
- Content: A "Bank Account" system with a race condition in the `transfer` method.
- Task: Fix the race condition using locks or atomic logic.

**Expected**:
1.  The concurrency test (`tests/test_bugfix.py`) that previously failed/was unstable must pass consistently.
2.  No deadlock introduced.
3.  Adequate logging added to trace the error.

**Validation command**:
`python3 .agent/evals/runner.py --id E12`
