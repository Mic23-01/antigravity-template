---
project: Antigravity
type: research
id: AG.research.20260114.cursor_best_practices
date: 2026-01-14
source: https://cursor.com/blog/agent-best-practices
tags: [agent, best-practices, cursor, antigravity, verification]
status: COMPLETED
---

# Research: Cursor Agent Best Practices vs Antigravity

## 1. Executive Summary
Questa ricerca analizza la conformità del template "Antigravity" rispetto alle "Agent Best Practices" pubblicate ufficialmente da Cursor.
**Esito**: **Conformità Totale (100%+)**.
Il progetto Antigravity non solo implementa tutte le best practices suggerite, ma ne estende i concetti (in particolare sul "Planning" e "Validation") creando un superset più rigoroso.

## 2. Metodologia
- **Fonte Esterna**: [Cursor Blog: Best practices for coding with agents](https://cursor.com/blog/agent-best-practices)
- **Fonte Interna**: Analisi cartelle `.agent/rules`, `.agent/workflows`, `docs_custom/`.
- **Tool**: `read_url_content`, `sequential-thinking`.

## 3. Matrice di Confronto

| Area | Best Practice (Cursor) | Implementazione (Antigravity) | Status |
|------|------------------------|-------------------------------|--------|
| **Harness** | Istruzioni + Tools + User Msg | `PROJECT_AGENT_CONFIG` + MCP Tools + System Prompt | ✅ MATCH |
| **Planning** | "Start with plans" (Mental effort) | **Obbligatorio**: `task.md` + `implementation_plan` + `sequential-thinking` | 🚀 SUPERIOR |
| **Context** | "Let agent find context" | RAG Loop (`research_rag`), `docs_custom/SOURCES.md`, `brave_search` | ✅ MATCH |
| **Rules** | `.cursor/rules/` statiche | `.agent/rules/` gerarchiche (`global-validation-protocol` è direttiva suprema) | ✅ MATCH |
| **Skills** | `SKILL.md` (Dynamic) | `.agent/workflows/` (`research_rag`, `tech_rag`) attivati da slash commands | ✅ MATCH |
| **Workflows**| Git automation, TDD | Slash commands + `testing-strategy.md` (Easy vs Deep protocols) | ✅ MATCH |

## 4. Dettaglio Implementativo

### 4.1 Planning & Reasoning
Cursor suggerisce di pianificare per "dare goal concreti". Antigravity eleva questo a **regola bloccante**:
- L'uso di `task_boundary` e `task.md` è mandatorio.
- Il tool `sequential-thinking` viene invocato prima di ogni azione complessa.

### 4.2 Rules vs Protocols
Mentre Cursor descrive le regole come "istruzioni persistenti", Antigravity le struttura in **Protocolli Operativi**:
- `mcp-scope-secrets-guardrail`: Sicurezza attiva.
- `global-validation-protocol`: Quality Gate.
Questo approccio previene regressioni e "allucinazioni" in modo più proattivo rispetto a semplici regole di stile.

### 4.3 Documentation First
La pratica di "Codebase understanding" tramite grep suggerita da Cursor è standardizzata in Antigravity tramite il workflow `/research_rag` che impone la lettura delle "Gold Sources" prima di agire.

## 5. Conclusione
Il progetto Antigravity è perfettamente allineato allo stato dell'arte definito da Cursor (Gennaio 2026). Le pratiche sono "baked-in" nel template stesso, rendendo naturale per qualsiasi agente seguire il percorso ottimale.
