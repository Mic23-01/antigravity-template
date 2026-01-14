# E03 — /research_rag salva research_summaries con sources+tags

## Prompt
"/research_rag: cerca la documentazione recente su Playwright 2025 e salva un sommario."

## Expected
- Ricerca esterna (Brave Search) eseguita.
- Salvataggio in Chroma: collection `research_summaries`.
- Metadata contenenti `sources` (URL validi) e `tags` (es. #playwright #research).
PASS/FAIL: manuale/check Chroma.
