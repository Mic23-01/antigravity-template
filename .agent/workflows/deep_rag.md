---
description: "Agente R&D 2026: Ricerca Deep con Recursive Loop (Gemini-Level), Analisi Negativa (Skeptical) e Impact Scorecard."
---

1) Context & Deep Mapping (The Network)
- **Mapping Esterno**: Usa `context7` per comprendere le librerie target e le loro alternative moderne.
- **Mapping Interno**: Usa `grep_search` o `duckdb` (via `.agent/project/librarian.py --audit`) per mappare l'impatto strutturale sulle dipendenze locali.
- **Obiettivo**: Capire non solo "cosa" fa la tecnologia, ma "dove" toccherà il progetto.

2) Recursive Deep Search Loop (The Gemini-Cycle)
- **Fase A: Query Expansion (Divergenza)**
  - Genera 5 assi di ricerca paralleli:
    1. **Official**: Doc e Changelog.
    2. **Skeptical**: "Why [X] sucks", "Performance issues", "Alternatives".
    3. **Comparative**: Benchmark vs Competitor Y.
    4. **Migration**: "Migration from [Current] to [X]", "Breaking changes".
    5. **Future**: "Roadmap 2026", "Deprecation warnings".
- **Fase B: Massive Ingestion (Automated)**
  - **Action**: Raccogli i 3-5 URL migliori per asse.
  - **Tool**: Esegui `uv run --with aiohttp --with html2text --with beautifulsoup4 .agent/tools/deep_search.py --urls <url1> <url2> ... --output RESEARCH_BUNDLE.md`
  - **Read**: Leggi SOLO `RESEARCH_BUNDLE.md` (Risparmia token e tempo).
- **Fase C: Reflection & Convergence**
  - Usa `sequential-thinking` per chiederti: "Le fonti sono concordi?".
  - Se c'è conflitto o gap, lancia un Loop Ricorsivo mirato.

3) Ephemeral Sandbox (The PoC)
- **Regola Aurea**: Usa `uv run --with <libs>` per usare il top delle librerie senza inquinare l'ambiente.
- **ANTI-RULE-0005**: 
    - Crea script in `verifiche_test/RND_<slug>.py`.
    - Esegui e cattura l'output quantitativo.
    - **CANCELLA SUBITO**: `rm verifiche_test/RND_<slug>.py`.
    - **DOPPIO CHECK**: Esegui `ls` per confermare la pulizia.

4) Impact Analysis (The Scorecard)
- Produci una tabella di impatto obbligatoria per ogni ricerca:

| Metrica | Rating (1-5) | Descrizione Impatto |
| :--- | :--- | :--- |
| **Simplification** | 1-5 | Quanto codice/complessità rimuove? |
| **Performance** | 1-5 | Impatto su velocità/memoria. |
| **Blast Radius** | 1-5 | Quanti file tocca? (1=Pochi, 5=Tutto) |
| **Canon Compliance** | Si/No | Rispetta gli standard del progetto? |
| **Depth of Field** | N Fonti | Numero totale fonti uniche consultate. |

5) Persistenza e Decisione
- **Research Summary**: Salva in `.agent/research_summaries/` (ID: `<Prefix>.deep_rag.YYYYMMDD.<slug>`).
- **Chroma**: Persisti con tag `type=deep_search`.
- **ADR condizionale**: Se il punteggio Simplification > 4 e Risk < 3, proponi direttamente l'adozione.

6) Output Finale
- Includi esplicitamente: "Processate X fonti su 5 assi (Recursive Deep Search)".
- Scorecard completata.
- Link al Summary.
- **FILESYSTEM UPDATES**: Obbligatorio ad ogni output (Regola Leader).
