# E02 — /tech_rag scrive fix_logs con metadata

## Prompt
"/tech_rag: fai una modifica minuscola e safe (es. commento in README) e lancia lo smoke test."

## Expected
- Esecuzione di uno smoke test (es. build o test e2e).
- Inserimento/Aggiornamento in Chroma: collection `fix_logs`.
- Metadata presenti e completi: `project`, `type`, `date`, `files`, `tests`, `result`.
PASS/FAIL: semi-automatico (verifica tramite Chroma).
