---
id: E11_triad_refactor
type: capability_eval
version: 1.0.0
---

# E11: The Refactor Challenge (Structural Integrity)

**Objective**: Measure the agent's ability to refactor legacy code without breaking functionality.

**Scenario**:
- Input file: `.agent/evals/triad/refactor_challenge.py`
- Content: A `GodObject` class that manages User, Billing, and Email all together.
- Task: Extract the `Billing` logic into a separate class.

**Expected**:
1.  The code must be separated into at least 2 classes/functions.
2.  Original tests (`tests/test_refactor.py`) must pass at 100%.
3.  The maintainability index score must increase.

**Validation command**:
`python3 .agent/evals/runner.py --id E11`
