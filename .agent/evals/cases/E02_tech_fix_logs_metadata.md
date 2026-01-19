# E02 — /tech_rag writes fix_logs with metadata

## Prompt
"/tech_rag: make a tiny and safe modification (e.g., comment in README) and run the smoke test."

## Expected
- Execution of a smoke test (e.g., build or e2e test).
- Insert/Update in Chroma: collection `fix_logs`.
- Metadata present and complete: `project`, `type`, `date`, `files`, `tests`, `result`.
PASS/FAIL: semi-automatic (verification via Chroma).
