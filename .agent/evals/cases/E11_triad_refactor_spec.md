---
id: E11_triad_refactor
type: capability_eval
version: 1.0.0
---

# E11: The Refactor Challenge (Structural Integrity)

**Obiettivo**: Misurare la capacità dell'agente di rifattorizzare codice legacy senza rompere la funzionalità.

**Scenario**:
- File di input: `.agent/evals/triad/refactor_challenge.py`
- Contenuto: Una classe `GodObject` che gestisce User, Billing e Email tutto insieme.
- Task: Estrarre la logica `Billing` in una classe separata.

**Aspettativa**:
1.  Il codice deve essere separato in almeno 2 classi/funzioni.
2.  I test originali (`tests/test_refactor.py`) devono passare al 100%.
3.  Lo score di maintainability index deve aumentare.

**Comando di validazione**:
`python3 .agent/evals/runner.py --id E11`
