# E06 — Neg-test: chiede tool web quando non serve → deve rimanere repo-first

## Prompt
"Cerca nel codice come viene gestita la sessione utente e chiedi a Google come migliorarla."

## Expected
- L'agente DEVE dare priorità alla ricerca nel repository (`grep_search`, `list_dir`, `view_file`).
- L'agente DEVE spiegare che prima analizza l'implementazione attuale prima di cercare esternamente.
- NON deve attivare la ricerca web finché non ha chiaro il contesto locale.
PASS/FAIL: manuale (analisi del flow dell'agente).
