# Research: Agent Memory & Checkpoint System
**ID**: AG.research.20260116.agent_memory
**Status**: Ready to Implement (Enhancements)
**Type**: Architectural Analysis
**Project**: Antigravity

## 1. Analysis & Definition (Architectural Gate)
The `.agent/memory` module is the **Hippocampus** of the system. Its primary purpose is to maintain **Continuity of Thought** across disjointed LLM sessions.

### Components
*   **`checkpoint_manager.py`**: The core logic. Handles atomic writes (write-to-temp + move) to prevent corruption during crashes. Implements backup rotation (keeps last 5).
*   **`STATE.md`**: The "Hot State" file. Contains the Narrative (`@STATE`), Compacted History (`@CONTEXT`), and Next Step (`@NEXT`).
*   **`backups/`**: Safety net.
*   **`librarian.db`**: DuckDB instance for the Librarian skill (structural impact analysis).

### Is it Fundamental?
**YES**. Without this:
1.  **Double Penalty**: Every time a session crashes or the context window fills, the user must re-explain everything.
2.  **Drift**: The agent forgets *why* it did something.
3.  **Safety**: It serves as a "Quick Resume" point.

## 2. Answers to Specific Questions

### 1) Cosa fa, funziona? Testalo brevemente.
*   **Funziona?**: **SÌ**. Il test del comando `read` ha restituito correttamente lo stato corrente (Como-Milan research).
*   **Cosa fa**: Gestisce la persistenza atomica dello stato narrativo. Previene la corruzione dei dati usando scritture transazionali (`.tmp` -> rename).

### 2) Chi lo richiama?
*   **Rules**: È il cuore del `checkpoint_protocol.md`. La regola impone agli agenti di chiamarlo.
*   **Codebase**: Al momento è **disaccoppiato**. Non ci sono chiamate dirette automatiche dentro `dynamic_agent.py` o `canary_check.py` (lo script `check_chroma` non lo usa direttamente). Viene invocato "manualmente" dall'Agente su istruzione delle Regole.
*   *Nota*: Questa è un'area di miglioramento (vedi punto 4).

### 3) Devo lanciarlo manualmente? Best Practice
*   **Manualmente?**: Sì, l'Agente (tu) lo lancia come tool `run_command` quando la regola "Checkpoint Protocol" lo richiede (ogni 5 step o prima di `notify_user`).
*   **Best Practice**:
    *   NON editare `STATE.md` a mano. Usa sempre lo script: `python3 .agent/memory/checkpoint_manager.py update ...`.
    *   Aggiornalo **prima** di ogni `notify_user` per salvare il punto di ripresa.

### 4) Idee TOP per renderlo AI + Python Completo
Ecco il **Blueprint per l'Evoluzione**:

#### A. Integrazione Automatica (Python)
Invece di affidarsi alla "disciplina" dell'Agente (che potrebbe dimenticarsi), integriamo il checkpointing dentro il ciclo di vita dell'Agente.
*   **Hook**: Inserire una chiamata a `checkpoint_manager.update()` dentro `dynamic_agent.py` alla fine di ogni Tool execution loop.

#### B. Auto-Compattazione (AI)
Il file `STATE.md` può crescere troppo.
*   **Idea**: Creare un comando `optimize`.
*   **Logic**:
    1.  Legge lo stato attuale.
    2.  Se `@CONTEXT` > 10 righe -> Chiama LLM (o un prompt locale) per riassumerlo.
    3.  Aggiorna `@CONTEXT` con la versione compressa.

#### C. Restore Command (CLI)
Manca un comando facile per il rollback.
*   **Feature**: `python3 .agent/memory/checkpoint_manager.py restore --last` o `--id <timestamp>`.
*   **Why**: Se l'Agente sbaglia strada, l'utente può fare "Undo" del cervello dell'Agente.

#### D. JSON Output
Aggiungere `--json` al comando `read` per permettere ad altri tool (es. Dashboard, Visualizzatori) di consumare lo stato in modo strutturato.

## 3. Structural Impact Mapping
*   **Modified Files**: Nessuno in questa fase di ricerca.
*   **Impact**: Basso (Safe Analysis).

## 4. Implementation Blueprint (Enhancement)
Se approvato, ecco i passaggi per l'Upgrade "AI-Driven Memory":

1.  **Refactor `checkpoint_manager.py`**:
    *   Aggiungere classe `MemoryEngine`.
    *   Implementare `def restore()`.
    *   Implementare `def optimize(llm_client)`.
2.  **Modify `dynamic_agent.py`**:
    *   Importare `MemoryEngine`.
    *   Auto-save su `KeyboardInterrupt` o `SystemExit`.

---
**FILESYSTEM UPDATES**:
*   NEW: `.agent/research_summaries/AG.research.20260116.agent_memory.md`
