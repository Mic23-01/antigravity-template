---
id: E12_triad_bugfix
type: capability_eval
version: 1.0.0
---

# E12: The Bugfix Challenge (Diagnostic Depth)

**Obiettivo**: Misurare la capacità dell'agente di individuare e correggere bug latenti (es. race conditions o logica errata).

**Scenario**:
- File di input: `.agent/evals/triad/bugfix_challenge.py`
- Contenuto: Un sistema di "Bank Account" con una race condition nel metodo `transfer`.
- Task: Fixare la race condition usando lock o logica atomica.

**Aspettativa**:
1.  Il test di concorrenza (`tests/test_bugfix.py`) che prima falliva/era instabile deve passare stabilmente.
2.  Nessun deadlock introdotto.
3.  Logging adeguato aggiunto per tracciare l'errore.

**Comando di validazione**:
`python3 .agent/evals/runner.py --id E12`
