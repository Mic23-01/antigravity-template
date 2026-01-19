# 🧪 Antigravity Canary Scenarios

These scenarios define test cases to verify that the Agent is operating at 100% protocol precision.

## Scenario 1: The Smoke Test (Hygiene)
- **Objective**: Verify that `librarian` correctly detects the project state.
- **Workflow**: `/librarian`
- **Expected**: Detection of `docs_custom/` presence and consistency with `task.md`.

## Scenario 2: Deep Context (Cascade Verification)
- **Objective**: Verify that a technical request forces loading of hydrated documentation.
- **Workflow**: `/tech_rag`
- **Input**: "Modify the Dashboard CSS following the brand identity guide."
- **Expected**: The agent MUST execute a `view_file` on `docs_custom/brand_identity_guide.md` BEFORE making proposals.

## Scenario 3: Strategic Alignment (Research)
- **Objective**: Verify that research is tied to the Vision.
- **Workflow**: `/research_rag`
- **Input**: "Search for new patterns for agentic UI 2026."
- **Expected**: The agent MUST load `docs_custom/product_strategy.md` and cite how the found patterns help "Guide towards building the best operational templates".

## Scenario 4: Truth Conflict (Regression Gate)
- **Objective**: Verify adherence to the validation protocol by saving data to Chroma.
- **Input**: Any task with `CANARY` flag or `EVAL_MODE=1`.
- **Expected**: The agent MUST invoke `check_chroma.py` and present the Regression Gate outcome.
