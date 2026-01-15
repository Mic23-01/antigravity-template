# Research Summary: The Triple Gate Paradox (Resilience vs Integrity)

> **ID**: AG.research.20260115.triple_gate_analysis
> **Type**: Architectural Strategy
> **Context**: Valutazione dell'estensione del "Hard Gate" (Session Sentinel) a ChromaDB e Audit.

## 1. Analisi Comparativa dei "Cancelli"

| Layer | Natura | Costo | Affidabilità | Ruolo Attuale |
| :--- | :--- | :--- | :--- | :--- |
| **Filesystem** | Fisica / Atomica | Quasi Zero | 100% (Locale) | **Hard Gate** (Bloccante) |
| **ChromaDB** | Vettoriale / MCP | Medio (Rete/IO) | 90% (Network/Sync) | **Persistent Store** (Soft) |
| **Audit** | Sequenziale | Elevato (Parsing) | 95% (Stream) | **Observability** (Soft) |

---

## 2. Perché ChromaDB non è (ancora) un Hard Gate

### 2.1 Il Rischio di "Infrastructure Lock-out"
In informatica, legare l'esecuzione di un sistema a un database esterno per ogni azione crea un punto di fallimento singolo (**SPOF**).
- **Scenario**: Il server ChromaDB ha un picco di latenza o il tool MCP `mcp_chroma` crasha.
- **Conseguenza**: Il Sentinel bloccherebbe l'Agente. L'Agente non potrebbe più né lavorare, né (ironicamente) riparare ChromaDB perché il cancello è chiuso.
- **Verdetto**: Viola il principio di **Anti-fragilità**. Il sistema deve poter funzionare in emergenza anche "solo a freddo" (filesystem).

### 2.2 Il "Ghost Metadata" Problem
ChromaDB è flessibile: ID e Metadati possono variare. Un controllo "Hard" richiederebbe una query complessa ad ogni passo. Se facciamo 50 tool call in un task, aggiungiamo 50 query al DB solo per "permesso di procedere". Il rallentamento sarebbe percepibile.

---

## 3. La Proposta: "Verification, not Interdiction"

Invece di trasformare Chroma e Audit in Cancelli Bloccanti (che fermano il lavoro), la strategia vincente è integrarli nel **Canary Check (The Checker)**:

1.  **Hard Gate (Sentinel)**: Rimane sul Filesystem. Impedisce di dimenticare il FixLog locale (indispensabile per la sicurezza).
2.  **Soft Gate (Canary)**: Durante la validazione finale, il Canary interroga ChromaDB. Se l'ID del FixLog locale non esiste nel DB, il Canary riporta:
    `[DEGRADED] FixLog present on Disk but MISSING in ChromaDB.`
3.  **Audit Drift**: Il sistema confronta l'ultima riga del log con l'ultimo FixLog. Se non coincidono, segnale di avvertimento.

---

## 4. Conclusione: L'Agente deve essere "Self-Healing"
L'obiettivo non è bloccare l'Agente se sbaglia la persistenza (che è frustrante), ma fare in modo che l'Agente **controlli se stesso** prima di terminare. 

### Regola d'Oro Proposta
> "Il Filesystem garantisce la **Vita** (Sopravvivenza), ChromaDB garantisce la **Saggezza** (Memoria). Non puoi avere saggezza se sei morto, quindi la Vita viene prima."

---
**Filesystem Evidence**: Analisi basata sull'incidente di sincronizzazione del turno precedente.
