# E05 — Retrieval: "retrieve last 3 research_summaries" and metadata filters

## Prompt
"Show me the last 3 research summaries related to 'Playwright' saved in Chroma."

## Expected
- Use of the `chroma_query_documents` or `chroma_get_documents` tool.
- Application of metadata filter (e.g., `where={"topic": "Playwright"}`).
- Return of the 3 most recent results.
PASS/FAIL: manual.
