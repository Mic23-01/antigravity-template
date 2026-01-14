---
name: resolve_canon_sources
description: Risolve la gerarchia delle fonti (Custom > Template)
version: 1.1.0
author: Antigravity
---

# Istruzioni Operative

## Trigger
- All'inizio di `tech_rag` (Step 0 Internal Context Discovery).
- All'inizio di `research_rag` (Step 0 Internal Canon Check).
- Ogni volta che è necessario stabilire la "Gold Source" di verità.

## Inputs
- **Environment**: File system locale.
- **Constraints**: Nessuno.

## Steps
1. **Primary Check**: Verifica esistenza `docs_custom/SOURCES.md`.
2. **Fallback Check**: Se Custom non esiste, usa `.agent/docs/SOURCES.md`.
3. **Execution**:
   - Leggi il file identificato (`view_file`).
   - Se l'argomento è "Gold" (definito nel file), attiva `markdownify` per deep reading.
   - Altrimenti procedi con `brave_search` se necessario.

## Outputs
- **Path**: Il path del file sorgente identificato.
- **Content**: Il contenuto letto da usare come contesto.

## Comandi Suggeriti
```bash
ls -F docs_custom/SOURCES.md 2>/dev/null || ls -F .agent/docs/SOURCES.md
```
