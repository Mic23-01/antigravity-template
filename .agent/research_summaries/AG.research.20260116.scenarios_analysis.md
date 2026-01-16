# Research: Antigravity Scenarios Analysis
**ID**: AG.research.20260116.scenarios_analysis
**Status**: Complete
**Type**: Architectural Documentation
**Project**: Antigravity

---

## 1. Cosa Sono e Cosa Fanno?
Sono "Test Comportamentali" (Behavioral Unit Tests) per l'Agente stesso.
Definiscono delle **situazioni di prova** (`scenarios`) che l'Agente deve risolvere in un ambiente sandbox, complete di assertion per verificare se ha rispettato le regole.

### File Analizzati:
- `001_compliance.md`: Verifica che l'Agente crei un **FixLog** valido quando modifica codice Python. (Fondamentale per ANTI-RULE-0004).
- `002_ui_ux_link.md`: Verifica che l'Agente usi la skill `ui_ux_designer` per cercare colori reali invece di inventarli.

### Funzionano?
**SÌ**. Sono interpretati da `dynamic_agent.py`.
- Nello scenario 001, verifica che esista `math_dummy.py` e il FixLog JSON correlato.
- Nello scenario 002, verifica che `brand_identity_guide.md` contenga codici esadecimali specifici (`#F59E0B`, `#8B5CF6`) che provengono dal database della skill.

### Perché sono FONDAMENTALI?
Senza questi scenari, non possiamo sapere se l'Agente sta **imparando** o **regredendo** nelle sue capacità operative.
- Garantiscono che le "Regole" (es. "Scrivi sempre FixLog") siano rispettate tecnicamente.
- Servono come "Esame di Qualifica" per l'Agente prima di operare su progetti reali.

---

## 2. Chi li chiama?
- **Tool**: `dynamic_agent.py` (funzione `load_scenarios`).
- **Workflow**: Non direttamente in un workflow utente, ma parte della suite di **Self-Correction**.
- **Canary**: `canary_check.py` può eseguire `dynamic_agent.py` per validare l'intero stack.

---

## 3. Lancio Manuale?
**SÌ**, per testare le capacità dell'agente.

```bash
# Esegue tutti gli scenari (Dry-Run mode di default per ora)
python3 .agent/tools/dynamic_agent.py
```

### Best Practice
- **Quando crearne nuovi?**: Ogni volta che introduci una nuova **Regola Vincolante** (es. "Devi sempre aggiornare architecture.md").
- **Formato**: YAML frontmatter + descrizione task + assertions precise.

---

## 4. Top Ideas (AI + Python)

### 1. **Auto-Generation via LLM**
Tool che legge una nuova regola in `PROJECT_RULES.md` e genera automaticamente uno scenario di test corrispondente (`003_new_rule.md`).
- *Input*: "Regola: Non lasciare print() nel codice."
- *Output*: Scenario con task "Scrivi funzione con print" e assertion `file_content_does_not_contain: print`.

### 2. **Real-Mode Execution**
Attualmente `dynamic_agent.py` è spesso in "dry-run". Implementare un vero loop dove l'LLM (tu) riceve il prompt dello scenario ed esegue i tool **veramente** nella sandbox `.agent/sandbox/`.

### 3. **Scorecard Evolutiva**
Salvare i risultati degli scenari in ChromaDB (`collection: agent_evals`) per tracciare se l'Agente diventa "più intelligente" o "più pigro" nel tempo (es. smette di usare FixLog).

### 4. **Diff-Based Trigger**
Se modifico `ui_ux_designer.py`, esegui automaticamente solo `002_ui_ux_link.md` per regression testing mirato.

---

**FILESYSTEM UPDATES**:
- NEW: `.agent/research_summaries/AG.research.20260116.scenarios_analysis.md`
