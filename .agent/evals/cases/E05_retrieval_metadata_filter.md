# E05 — Retrieval: “recupera ultimi 3 research_summaries” e filtri metadata

## Prompt
"Mostrami gli ultimi 3 sommari di ricerca relativi a 'Playwright' salvati in Chroma."

## Expected
- Utilizzo del tool `chroma_query_documents` o `chroma_get_documents`.
- Applicazione del filtro metadata (es. `where={"topic": "Playwright"}`).
- Restituzione dei 3 risultati più recenti.
PASS/FAIL: manuale.
