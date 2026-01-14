---
name: fixlog_writer
description: Standardizza la scrittura dei FixLog e gestisce la persistenza in Chroma.
version: 1.0.0
author: Antigravity
---

# Istruzioni Operative

## Trigger
- Alla fine di ogni workflow che implica modifiche (`tech_rag`, `refactor`).
- Quando si deve salvare traccia di un intervento tecnico (Step 6 Persistenza).

## Inputs
- **Prefix**: (da `PROJECT_AGENT_CONFIG.md`) Prefisso del progetto.
- **ProjectName**: (da `PROJECT_AGENT_CONFIG.md`) Nome del progetto.
- **Log Data**: JSON contenente `id`, `document` (descrizione), e `metadatas` (project, type, date, files, tests, result).

## Steps
1. **Prepare Data**: Raccogli i dati dell'intervento.
2. **Generate JSON**: Usa lo script `write_log.py` per generare e (opzionalmente) salvare il log.
3. **Verify**: Il protocollo delega la validazione a `regression_gate`.

## Outputs
- **Chroma Entry**: Nuovo documento nella collezione `fix_logs`.
- **Log ID**: L'ID univoco assegnato al log.

## Comandi Suggeriti
```bash
python3 .agent/skills/fixlog_writer/scripts/write_log.py --project "<ProjectName>" --desc "Fixed X" --files "file1.py" --test "pytest ok" --result "pass"
```
