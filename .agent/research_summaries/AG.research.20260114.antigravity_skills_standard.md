---
project: Antigravity
type: research
id: AG.research.20260114.antigravity_skills_standard
date: 2026-01-14
source: System Prompt + Cursor Best Practices
tags: [skills, architecture, standard, antigravity]
status: COMPLETED
---

# Research: Antigravity Skills Standard

## 1. Executive Summary
Questa ricerca definisce lo standard per l'implementazione delle **Skills** nel progetto Antigravity.
Le Skills rappresentano "capacità specializzate" modulari (tools + istruzioni + script) che estendono l'agente oltre le regole globali.
**Differenza chiave**: 
- **Workflows**: Processi procedurali (Step 1 -> Step 2).
- **Skills**: Domini di competenza (es. "Gestione Postgres", "Analisi Log") attivati su richiesta.

## 2. Definizione Ufficiale (System Protocol)
Basandosi sul protocollo interno Antigravity (System Prompt), una Skill è definita come una **directory autocontenuta** che fornisce capacità estese.

### 2.1 Struttura Filesystem
Le skills devono risiedere in `.agent/skills/`.
Ogni skill DEVE seguire questa struttura:

```text
.agent/skills/
└── <skill-name>/
    ├── SKILL.md          # Entry point OBBLIGATORIO (Istruzioni + YAML)
    ├── scripts/          # Script Python/Bash di supporto
    ├── examples/         # Snippet di codice o pattern di utilizzo
    └── resources/        # Template, assets statici
```

### 2.2 Formato `SKILL.md`
Il file principale deve contenere frontmatter YAML e istruzioni Markdown chiare.

```markdown
---
name: <human_readable_name>
description: <short_description>
version: 1.0.0
---

# Istruzioni Operative
Quando l'utente richiede task relativi a <skill-name>, segui queste direttive...

## Tools Disponibili
Descrizione degli script in `scripts/` e come invocarli (es. `run_command`).
```

## 3. Utilizzo nel Progetto
Per integrare le Skills nel flusso di lavoro Antigravity:

1.  **Discovery**: Prima di affrontare un task complesso, l'Agente controlla `.agent/skills` per competenze pertinenti.
2.  **Activation**: L'Agente legge `SKILL.md` tramite `view_file` per "imparare" la skill.
3.  **Standard**: Le Skills devono essere pure, senza dipendenze esterne non dichiarate (usare `uv` per ambienti isolati se necessario).

## 4. Skills vs Workflows vs Rules
| Componente | Scopo | Esempio | Quando Usare |
|------------|-------|---------|--------------|
| **Rules** | Governance & Sicurezza (Always On) | `mcp-scope-secrets-guardrail` | Sempre (Constraint) |
| **Workflows**| Processi Ripetibili (Step-by-Step) | `/research_rag` | Task definiti |
| **Skills** | Capacità di Dominio (Capabilities) | `sql_optimization`, `data_viz` | Task complessi/specifici |

## 5. Prossimi Passi (Actionable)
Per abilitare le Skills in "NOSTRO PROGETTO":
1.  Creare la directory `.agent/skills`.
2.  Migrare eventuali script sparsi in competenze strutturate.
3.  Definire la prima Skill pilota (es. `chroma_management` o `frontend_design`).
