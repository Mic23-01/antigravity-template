---
name: resolve_canon_sources
description: Risolve la gerarchia delle fonti (Custom > Template)
version: 1.0.0
---

# Istruzioni Operative

## Scopo
Centralizzare la logica di ricerca tra fonti custom e template.

## Logica di Risoluzione
1. **Primary Check**: Verifica esistenza `docs_custom/SOURCES.md`.
2. **Fallback Check**: Se Custom non esiste, usa `.agent/docs/SOURCES.md`.
3. **Execution**:
   - Leggi il file identificato (`view_file`).
   - Se l'argomento è "Gold" (definito nel file), attiva `markdownify` per deep reading.
   - Altrimenti procedi con `brave_search` se necessario.

## Comandi Suggeriti
```bash
ls -F docs_custom/SOURCES.md 2>/dev/null || ls -F .agent/docs/SOURCES.md
```
