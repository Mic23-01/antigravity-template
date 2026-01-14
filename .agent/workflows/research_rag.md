---
description: "Unified RAG Protocol: Research -> (Optional) Decision -> Dual Persistence (Chroma + MD)"
---

1) Analisi e Definizione (Planning Gate)
- Consulta il Supervisore Leader (`.agent/rules/global-validation-protocol.md`).
- **Strategic Alignment**: Verifica `docs_custom/product_strategy.md` (Vision) e `docs_custom/domain_language.md` (Termini) per evitare derive.
- Determina l'obiettivo: Pura ricerca (Discovery) o Decisione Architetturale (Commitment).

2) Check Memoria (Chroma)
- Identifica `<ProjectName>` e `<Prefix>` da `.agent/project/PROJECT_AGENT_CONFIG.md`.
- Cerca in `research_summaries` e `decisions` per evitare duplicati.

14) 3) RAG (ordine rigido)
**Step 0: Internal Canon Check**
- **Skill**: `resolve_canon_sources` (Gestisce hierarchy Custom > Template)
- Leggi la Canon Source. Se l'argomento è Gold, usa `markdownify` prima di procedere.
A) Repo-first: Analisi codice e documentazione locale.
B) Official Docs / Microsoft Learn / Context7.
C) Brave-search: Solo per news o informazioni fuori canone.
- **Massive Ingestion (Optimization)**:
  - Per ricerche su più assi, usa il tool di aggregazione parallela:
  - `uv run --with aiohttp --with html2text --with beautifulsoup4 .agent/tools/deep_search.py --urls <url1> <url2> ... --output RESEARCH_BUNDLE.md`

4) Sintesi e Opzioni (Dual-Persistence)
**A) Sempre: Research Summary**
- Genera `.agent/research_summaries/<Prefix>.research.YYYYMMDD.<slug>.md`.
- Contiene: Apprendimenti principali, Prove tecniche, Fonti.
**B) Condizionale: Architectural Decision (ADR)**
- Se il task implica una scelta vincolante, includi: Opzioni (2-4), Analisi Pro/Contro, Scelta e Motivazione.
- Salva i dettagli dell'ADR in Chroma (collezione `decisions`).

5) Persistenza e ID (OBBLIGATORIO)
- **ID Research**: `<Prefix>.research.YYYYMMDD.<slug>` (o `eval.metadata_gate` se CANARY).
- **ID Decision**: `<Prefix^^>-DEC-XXXX` (o `DEC-EVAL-0001` se CANARY).
- Metadata: `project=<ProjectName>, type=research|decision, ...`.

6) Post-check (REGRESSION GATE)
- **Skill**: `regression_gate` (Esegue check_chroma su `research_summaries` o `decisions`).
- **FAIL-FAST**: Se il checker fallisce, correggere immediatamente prima di procedere.

7) Output finale
- Sintesi Research + (Opzionale) Decision ID.
- **FILESYSTEM UPDATES**: Obbligatorio ad ogni output (Regola Leader).
