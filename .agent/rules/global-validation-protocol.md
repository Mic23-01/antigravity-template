---
trigger: always_on
description: Global Validation Protocol (Leader/Supervisor)
globs: "**/*"
---

# 👑 PROTOCOLLO LEADER: Validazione & Supervisione (ALWAYS ON)

**DIRETTIVA SUPREMA**: Questa è la regola radice di Antigravity. Ogni operazione deve passare da questo gate. L'inottemperanza a questo protocollo è considerata un fallimento critico.

## 0. High-Resolution Planning (Planning Gate)
PRIMA di qualsiasi azione tecnica, l'Agente DEVE produrre un piano. La profondità dipende dalla complessità:

* **Zero Step (Session Sentinel)**: Esegui `canary_check`. Se rileva una **Dirty Session** (modifiche senza FixLog), **STOP** immediato. Devi sanare la memoria prima di lavorare.

* **Standard Plan (Strict)**: Obbligatorio per modifiche complesse. Richiede: Obiettivo, Step atomici, Rischi, Criteri di Successo.
* **Micro-Plan (Adaptive Exception)**:
    * **Trigger**: AMMESSO SOLO SE: Modifica ≤ 2 file AND Nessuna nuova libreria AND Nessun cambio DB/API.
    * **Formato**: Lista puntata rapida delle azioni + Test di verifica.
    * **Divieto**: Vietato saltare la fase di pensiero (`sequential-thinking`), anche nel

## 1. Monitoraggio Filesystem (MANDATORIO)
In OGNI risposta (notify_user o output finale), l'Agente **DEVE** includere una sezione finale denominata `[FILESYSTEM UPDATES]` che elenca in modo atomico:
- **NEW**: [file path]
- **MODIFY**: [file path]
- **DELETE**: [file path]
Se non ci sono stati cambiamenti, scrivere `NONE`.

## 2. Fase di Ragionamento Iniziale (Sequential Thinking)
PRIMA di proporre o eseguire qualsiasi azione tecnica:
1.  **Attiva** `sequential-thinking`.
2.  **Analizza** la richiesta in assiomi fondamentali.
3.  **INTERRUPT**: Se la richiesta è ambigua, **NON PROCEDERE**. Chiedi chiarimenti.

## 3. Fase di Ricerca Attiva (RAG Loop)
Se manca certezza tecnica (100%):
1.  **Consulta** le Gold Sources in `docs_custom/SOURCES.md`.
2.  **Cross-Valida** con `brave-search` (limite temporale: ultimo anno).
3.  **Deep-Read** con `markdownify` prima di asseverare una soluzione.
4.  **Context Check (Obbligatorio)**: Prima di agire, CARICA il documento `docs_custom/` pertinente (es. Architecture per Backend, Brand per UI).

## 4. Fase di Sintesi & Validazione
- Se c'è conflitto: **La documentazione più recente (MCP) vince sempre.**
- **INTERRUPT**: Se la soluzione richiede un cambio di architettura o l'uso di nuove librerie, **NON PROCEDERE** senza OK esplicito dell'utente su un `implementation_plan.md`.

## 5. Protocol Fidelity
Tutte le altre regole in `.agent/rules/` sono subordinate a questa. Se una regola richiede un'interazione (Bivio), l'Agente deve rispettarla rigorosamente senza tentare la risoluzione autonoma.

> [!IMPORTANT]
> **L'allucinazione è il fallimento critico.** Meglio una domanda in più che un file modificato in meno o in modo errato.

