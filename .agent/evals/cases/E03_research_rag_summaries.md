# E03 — /research_rag saves research_summaries with sources+tags

## Prompt
"/research_rag: search for recent documentation on Playwright 2025 and save a summary."

## Expected
- External search (Brave Search) executed.
- Save to Chroma: collection `research_summaries`.
- Metadata containing `sources` (valid URLs) and `tags` (e.g., #playwright #research).
PASS/FAIL: manual/Chroma check.
