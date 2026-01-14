# E09 — Chroma query by tag: trova solo topic=playwright

## Prompt
"Cerca nella memoria tecnica tutti i log che hanno il tag 'playwright'."

## Expected
- Utilizzo di `chroma_query_documents` con filtro `where_document={"$contains": "playwright"}` o metadata filter appropriato.
- Risultati filtrati correttamente per mostrare solo il topic richiesto.
PASS/FAIL: manuale/check Chroma.
