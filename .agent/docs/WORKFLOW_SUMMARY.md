# Antigravity Workflow Reference

Questa guida fornisce un riepilogo sintetico dei workflow operativi disponibili nel progetto. Usa i **Slash Command** (es. `@[/research_rag]`) per attivare l'Agent su compiti specifici.

| Workflow | Slash CMD | Quando usarlo | Cosa fa |
| :--- | :--- | :--- | :--- |
| **Project Hydration** | `@[/custom_project]` | All'avvio di un nuovo progetto o per aggiornare docs core. | Trasforma i template generici in documentazione viva (`docs_custom/`). Guida la compilazione di Vision, Domain Language e Strategy. |
| **Deep Research** | `@[/deep_rag]` | Per ricerche complesse, comparative o su argomenti futuri (2026+). | Ricerca ricorsiva su più assi (Official, Skeptical, Future). Genera Scorecard di impatto e analisi approfondita. |
| **Librarian** | `@[/librarian]` | Quando il progetto sembra "sporco" o disordinato. | **Igiene & Struttura**. Rimuove file inutilizzati (ghost code), sincronizza la documentazione e verifica l'integrità del sistema (Canary Check). |
| **Refactoring** | `@[/refactor]` | Per modifiche strutturali rischiose o debito tecnico. | Analizza l'AST e il Blast Radius. Pianifica modifiche sicure con rollback plan obbligatorio. |
| **Unified RAG** | `@[/research_rag]` | Per decisioni architetturali o setup di nuove tecnologie. | Protocollo RAG standard: Source Canon -> Web -> Sintesi. Genera Architectural Decision Records (ADR). |
| **Tech Task** | `@[/tech_rag]` | Per task di implementazione standard (Feature/Bugfix). | Ciclo: Ricerca -> Piano -> Codice -> Test -> Verifica. Ideale per sviluppo quotidiano. |

> [!TIP]
> **Canary Check**: Il workflow `@[/librarian]` include ora un controllo di integrità automatico (`canary_check.py`) per garantire che le regole e i workflow siano sani.
