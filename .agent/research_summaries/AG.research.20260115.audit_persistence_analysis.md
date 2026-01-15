# Research Summary: Antigravity Audit System Persistence

> **ID**: AG.research.20260115.audit_persistence_analysis
> **Type**: Technical Deep Dive
> **Context**: Spiegazione dei componenti del sistema Dual Layer Audit (JSONL + MD).

## 1. Analisi dei Componenti

### 1.1 `.agent/audit/.gitignore`
- **Funzionamento**: Definisce cosa deve "sporcare" il repository Git e cosa no.
- **Dettaglio**:
    - **Esclude `*.jsonl`**: I log granulari (migliaia di righe) non vengono committati per evitare di appesantire il repo con dati volatili.
    - **Include `audit_summary.md`**: Permette all'utente di vedere la cronologia delle azioni critiche direttamente su GitHub/GitLab.
- **Vantaggio**: Bilancia efficienza del repository e visibilità per l'uomo.

### 1.2 `agent_events.jsonl` (Machine Layer)
- **Funzionamento**: Archivio grezzo in formato JSON Lines (una riga = un oggetto JSON).
- **Logica di Aggiornamento**: **APPEND-ONLY**.
    - Utilizza la modalità `open(path, "a")` in Python. Ogni nuovo evento viene aggiunto in coda.
- **Contenuto**: Traccia ogni singola operazione, tool call, ed eval con metadati completi (timestamp, payload, project).
- **Perché JSONL?**: È ultra-resiliente. Se l'agente crasha a metà scrittura, le righe precedenti sono già scritte sul disco e integre.

### 1.3 `audit_summary.md` (Human Layer)
- **Funzionamento**: Tabella Markdown visualizzabile in tempo reale.
- **Logica di Aggiornamento**: **APPEND-ONLY**.
    - Filtra solo eventi "Pivot" (FixLogs, Evals complete).
    - Aggiunge nuove righe in fondo alla tabella esistente.
- **Vantaggio**: Consente una supervisione rapida senza dover parsare codice JSON.

---

## 2. Persistenza: Sovrascrittura vs Accumulo

| File | Strat di Scrittura | Rischio Sovrascrittura |
| :--- | :--- | :--- |
| **.gitignore** | Statica | Zero (scritto una volta). |
| **agent_events.jsonl** | Append (Coda) | **NESSUNA**. Il file cresce storicamente. |
| **audit_summary.md** | Append (Coda) | **NESSUNA**. La tabella si allunga. |

---

## 3. Considerazioni di Strategia
L'approccio segue il pilastro di **Robustezza** definito in `product_strategy.md`:
- **Truth Persistence**: Il filesystem è la fonte di verità.
- **Auditability**: Non si cancella mai il passato, si costruisce sopra.

> [!TIP]
> Per gestire file JSONL molto grandi in futuro, si consiglia una logica di **Log Rotation** (es. creare un nuovo file ogni 10MB), ma per l'attuale fase di sviluppo, l'accumulo garantisce la massima tracciabilità.

---
**Filesystem Evidence**: Verificato via `event_logger.py` e test di esecuzione.
