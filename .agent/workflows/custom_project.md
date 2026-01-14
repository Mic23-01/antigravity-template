---
description: "Project Hydration Wizard: Trasforma i Template Antigravity in Documentazione Viva (`docs_custom/`)."
---

1) Context Discovery (The Automated Audit)
- **Obiettivo**: Dedurre tutto ciò che è tecnicamente possibile senza chiedere all'utente.
- **Action**: Esegui analisi strutturale profonda (Repo-first).
  - **Primary**: Leggi `package.json`, `requirements.txt`, `pyproject.toml` per lo Stack.
  - **Fallback**: Se i config mancano, usa `find` o `grep` per dedurre la struttura o cercare pattern di import.
  - **Active Check**: Se necessario, lancia comandi safe (`node -v`, `python --version`) o script di esplorazione.
  - **Intervention**: Se l'ambiguità persiste (> 20%), **CHIEDI** esplicitamente all'utente prima di inventare.
  - **Style Check**: Cerca `tailwind.config.js` o variabili CSS root per dedurre la palette.
- **Tool**: `view_file`, `run_command` (safe), `librarian`.

2) Gap Analysis & Interview (The User Check)
- **Confronto**: Leggi i placeholder nei **Template Originali**:
  - `.agent/docs/architecture.md`
  - `.agent/docs/brand_identity_guide.md`
  - `.agent/docs/domain_language.md`
  - `.agent/docs/product_strategy.md`
  - `.agent/docs/SOURCES.md`
- **Intervista**: Formula una serie di domande mirate per l'utente per colmare i gap (es. "Qual è la Visione a 12 mesi?", "Definisci il termine 'Player'").
- **Constraint**: NON procedere alla generazione finché l'utente non ha risposto.

3) Hydration Generation (The Build)
- **Action**: Crea la directory target `docs_custom/` (se non esiste).
- **Skill**: Attiva `ui_ux_designer` per trovare palette e font coerenti se non definiti.
- **Action**: Per ogni template:
  - Sostituisci i placeholder con i dati raccolti (Audit + Intervista + UI Skill).
  - Rimuovi le sezioni "AI Instruction".
  - Scrivi il file finale in `docs_custom/<filename>`.
- **Naming Convention**: Mantieni gli stessi nomi file dei template per coerenza.

4) Validation & Binding (The Handshake)
- **Review**: Chiedi all'utente di validare i file in `docs_custom/`.
- **Commit**: Una volta approvati, questi file diventano la **Specific Source of Truth** del progetto.
- **FILESYSTEM UPDATES**: Notifica la creazione dei nuovi file.
