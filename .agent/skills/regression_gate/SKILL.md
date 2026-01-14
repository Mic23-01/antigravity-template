---
name: regression_gate
description: "Atomic Validation Protocol: Wrapper unificato per Chroma Check e Librarian Audit."
version: 2.0.0 (Divine)
author: Antigravity
---

# Istruzioni Operative

Questa skill è il **Guardiano della Qualità**. Non deve mai essere bypassata.

## 🛠️ The Atomic Tool
Invece di lanciare comandi sparsi, usa lo script unificato che garantisce l'ordine di esecuzione e la gestione degli errori.

### Sintassi
```bash
python3 .agent/skills/regression_gate/scripts/run_audit.py --collection <COLLECTION> --id <ID>
```

## 🚨 Protocollo di Fallimento
Se lo script restituisce un errore (Exit Code 1):

1. **STOP**: Non procedere con altre azioni.
2. **CONSULTA**: Leggi `.agent/skills/regression_gate/examples/correct_metadata.md` per capire dove hai sbagliato.
3. **FIX**: Correggi i metadata in Chroma o pulisci i file ghost.
4. **RETRY**: Rilancia il gate finché non ottieni `✅ GATE PASSED`.

## Note Tecniche
- Lo script gestisce internamente `uv run` per le dipendenze (`chromadb`, `duckdb`).
- È progettato per essere "Zero Silence": stampa l'errore esatto in rosso.
