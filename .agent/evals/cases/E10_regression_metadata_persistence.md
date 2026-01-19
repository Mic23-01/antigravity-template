# E10 — Regression: repeat E02 and compare metadata

## Prompt
"Repeat the /tech_rag workflow to add another comment to the README and verify that the metadata in Chroma is still complete."

## Expected
- `/tech_rag` workflow completed.
- Metadata in Chroma (`fix_logs`) populated consistently with E02.
- No loss of structure in metadata (must not be null).
PASS/FAIL: semi-automatic (Chroma log comparison).
