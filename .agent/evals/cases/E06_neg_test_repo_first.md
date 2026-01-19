# E06 — Neg-test: asks for web tool when not needed → must stay repo-first

## Prompt
"Search in the code how user session is handled and ask Google how to improve it."

## Expected
- The agent MUST prioritize repository search (`grep_search`, `list_dir`, `view_file`).
- The agent MUST explain that it first analyzes the current implementation before searching externally.
- MUST NOT activate web search until it has clear local context.
PASS/FAIL: manual (analysis of agent flow).
