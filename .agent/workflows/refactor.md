---
description: "Deep Refactoring Protocol (KILLER 2026): Analisi AST, Blast Radius e Hard Interrupt"
---

1) Fase di Inquiry (Structural AST Check)
- **Skill**: `resolve_canon_sources` (Gestisce hierarchy `docs_custom/` > Template).
- Consulta il Supervisore Leader (`.agent/rules/global-validation-protocol.md`).
- **Mappatura Strutturale**: Usa `ast-grep` o `grep_search` per mappare ogni occorrenza sintattica (non solo testuale).
- **Blast Radius Report**: Genera un riepilogo che indichi:
    - Quanti file e righe saranno toccati.
    - Quali dipendenze (import/callers) verranno impattate.
    - Rischio stimato (Basso/Medio/Alto).

2) Hard Interrupt (Consenso Informato)
- **BLOCCO OBBLIGATORIO**: Presenta il *Blast Radius Report* e la proposta di modifica dettagliata (Diff previsto).
- **CHIEDERE CONFERMA**: Chiama `notify_user` e attendi il "Procedi" esplicito prima di eseguire qualsiasi edit.

3) Esecuzione Chirurgica (AST Transformation)
- Se il refactoring è complesso, usa script `uv run --with libcst` per trasformazioni atomiche che preservano la formattazione.
- Esegui i cambiamenti in modo incrementale.

4) Validazione SOLID & Regression Gate
- **Skill**: `regression_gate` (Validazione Chroma + Librarian).
- Verifica la qualità formale post-modifica.
- Esegui la suite di test completa del modulo (`testing-strategy.md`).
- **Zero Silence**: Se il refactoring rompe test pre-esistenti, ferma tutto e rapporta.

5) Persistenza e Igiene (Post-Refactor)
- Salva un FixLog in Chroma (type=refactor).
- **Cleanup Finale**: Elimina ogni script di trasformazione temporaneo o sandbox.
- **Doppio Check**: Esegui `ls` per confermare la pulizia del workspace.

6) Output finale (Evidence Bundle)
- Sintesi trasformativa + FixLog ID.
- **FILESYSTEM UPDATES**: Obbligatorio ad ogni output (Regola Leader).
