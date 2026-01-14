---
description: "Agente Bibliotecario: Igiene Proattiva, Sincronizzazione Documentale e Analisi Strutturale (DuckDB)"
---

1) Preparazione e Planning
- Consulta il Supervisore Leader (`.agent/rules/global-validation-protocol.md`).
- Obiettivo: Mantenere il progetto pulito, aggiornato e privo di "Ghost Code".

2) Analisi Strutturale (The SQL Eye)
- **DuckDB Audit**: Esegui l'audit strutturale automatizzato.
  `uv run --with duckdb python3 .agent/project/librarian.py --audit`
- Identifica:
    - **Ghost Files**: File non importati o duplicati orfani.
    - **Dead Code**: Funzioni/Classi senza referenze (usa `grep_search` per validare).
    - **Documentation Drift**: Verifica se `docs_custom/` è aggiornato rispetto al codice.
    - **Missing Context**: Segnala se mancano file core in `docs_custom/`.

3) Sincronizzazione Attiva (Active Sync)
- **Autorizzazione Obbligatoria**: Se il Bibliotecario individua documentazione mancante o obsoleta (es. README, ADR, DOCS), **DEVE** descrivere il contenuto proposto e chiedere il permesso tramite `notify_user` prima di creare o modificare i file.
- **README Update**: Proponi l'aggiornamento delle mappe dei file e delle descrizioni.
- **DOCS Sync**: Proponi il link di nuovi ADR o Research negli indici.
- **SSOT Check**: Verifica coerenza costanti/parametri tra frontend e backend.

4) Pulizia e Ottimizzazione
- Proponi la rimozione dei file identificati come "Ghost".
- Archivia i task completati da `task.md` nel changelog storico.
- Ottimizza i metadata di Chroma eliminando entry ridondanti o obsolete.

5) Verifica e Chiusura
- Esegui lo script `librarian.py` originale per la validazione dello schema.
- **Persistenza Chroma**: Salva l'esito nella collezione `fix_logs`.
    - **ID**: `<Prefix>.hygiene.YYYYMMDD.<slug>`
    - **Metadata**: `project=<ProjectName>, type=hygiene_log, date=YYYY-MM-DD, result=pass|fail, notes=...`
- **Regression Gate**: Esegui `check_chroma.py` sull'ID generato.

6) Output finale
- Report delle azioni di igiene eseguite.
- **FILESYSTEM UPDATES**: Obbligatorio ad ogni output (Regola Leader).
