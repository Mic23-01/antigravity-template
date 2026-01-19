---
id: E13_triad_feature
type: capability_eval
version: 1.0.0
---

# E13: The Feature Challenge (Product Alignment)

**Objective**: Measure the agent's ability to implement a feature while respecting domain and architectural constraints.

**Scenario**:
- Input file: `.agent/evals/triad/feature_challenge.py`
- Content: An API Skeleton service `UserService`.
- Task: Implement the method `anonymize_user(user_id)` according to GDPR.

**Expected**:
1.  The method must mask email and name.
2.  Must log the operation with structured JSON format (as per `domain_language.md`).
3.  Integration tests (`tests/test_feature.py`) must pass.

**Validation command**:
`python3 .agent/evals/runner.py --id E13`
