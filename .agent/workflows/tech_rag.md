---
description: "Tech Task Protocol: RAG -> Piano -> Modifiche -> Test -> Evidenze -> FixLog (Chroma) -> Checker"
---

1) Analisi e Definizione (Adaptive BMAD Protocol)
- **Check Modalità**: Leggi `WorkflowMode` in `.agent/project/PROJECT_AGENT_CONFIG.md`.
- **Complexity Trigger**: Il task tocca > 2 file OPPURE cambia schema DB / API / Dipendenze?
  - **SI (Complex -> Strict)**: Scomponi in **Stories Numerate**. Obbligo di **STOP** utente tra una story e l'altra.
  - **NO (Simple -> Adaptive)**: Procedi con un "Micro-Plan" immediato (lista azioni + test).
- **Obiettivo**: 1 frase (Problema + Outcome).
- **Done Criteria**: Definizione verificabile (test/behavior).

2) Contesto e Placeholder (Project-Agnostic)
- **Identifica il Progetto**: Determina `<ProjectName>` e `<Prefix>` da `.agent/project/PROJECT_AGENT_CONFIG.md`.
- **Context Switcher (OBBLIGATORIO)**:
  - Se **UI/Frontend**: Attiva `ui_ux_designer` e leggi/aggiorna `docs_custom/brand_identity_guide.md`.
  - Se **Backend/Arch**: Leggi `docs_custom/architecture.md`.
  - Se **Business Logic**: Leggi `docs_custom/domain_language.md`.
- Usa sempre i placeholder `<ProjectName>` e `<Prefix>` nelle comunicazioni e nei metadata di Chroma.

3) RAG (ordine rigido)
**Step 0: Internal Context Discovery**
- **Skill**: `resolve_canon_sources` (Gestisce hierarchy Custom > Template)
- **Check**: Contiene link ufficiali o best practices interne?
- **Decision**: Se sì -> Deep Read (markdownify). Se no -> Brave Search (Step 2).

A) Repo-first: leggi file pertinenti nel progetto.
B) Official Docs: usa i link identificati nella Canon Source attiva (Custom o Template).
C) Chroma: cerca fix/decisioni simili filtrando per `project=<ProjectName>`.
D) Microsoft Learn / Context7: doc ufficiali.
E) Brave-search: solo se serve info esterna fuori canone.

4) Esecuzione controllata
- Cambi piccoli e localizzati.
- Niente distruttivo senza review.
- Rispetta i Guardrail di sicurezza (`.agent/rules/mcp-scope-secrets-guardrail.md`).

5) Test Gate (Interattivo)
- **Skill**: `test_gate_bivio` (Gestisce livelli Smoke/Deep/Debug).
- **POLITICA "Zero Silence for Ghost Failures"**: Segnala immediatamente errori pre-esistenti.

6) Persistenza in Chroma (OBBLIGATORIO)
- **Skill**: `fixlog_writer` (Genera payload standard JSON).
- Per validazione/demo (**Task contiene 'CANARY'** o `EVAL_MODE=1`): usa ID STABILE `<Prefix>.fix.eval.metadata_gate`.
- Per fix reali: usa l'ID generato automaticamente dalla skill `<Prefix>.fix.YYYYMMDD.<slug>`.

7) Post-check (REGRESSION GATE)
- **Skill**: `regression_gate` (Esegue check_chroma + librarian su `fix_logs`).
- **FAIL-FAST**: Se il checker FALLISCE, l'agente DEVE FERMARSI e correggere i metadata.

8) Output finale (EVIDENCE BUNDLE)
- Cosa è cambiato + FixLog ID.
- Test eseguiti + esito.
- **FILESYSTEM UPDATES**: Obbligatorio ad ogni output (Regola Leader).

