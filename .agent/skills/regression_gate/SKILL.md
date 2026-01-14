---
name: regression_gate
description: Validare la persistenza dei dati e l'igiene post-modifica
version: 1.0.0
---

# Istruzioni Operative

## Scopo
Assicurare che ogni modifica sia tracciata correttamente in Chroma e che la documentazione sia sincronizzata.

## Workflow
1. **Chroma Check**:
   - Esegui: `uv run --with chromadb python3 .agent/tools/check_chroma.py --collection <COLLECTION> --id <ID>`
2. **Librarian Audit**:
   - Esegui: `uv run python3 .agent/project/librarian.py`

## Fail-Fast Policy
- Se uno dei due comandi fallisce (exit code != 0), **INTERROMPI** il processo.
- Non procedere all'output finale finché i metadati non sono corretti.
