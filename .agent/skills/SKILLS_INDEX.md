# Antigravity Skills Index

Questo catalogo mappa le competenze modulari ("Skills") disponibili per l'Agente.
Ogni skill è una directory autocontenuta in `.agent/skills/<skill_name>/`.

## 🟢 Base Skills (Core)
| Skill Name | Descrizione | Trigger Workflow |
|------------|-------------|------------------|
| `resolve_canon_sources` | Risolve la gerarchia delle fonti (Custom > Template) | All RAG workflows |
| `test_gate_bivio` | Gestisce l'interazione Test (Smoke vs Deep) | `tech_rag` |
| `regression_gate` | Assicura integrità Chroma e Filesystem | All RAG workflows |
| `fixlog_writer` | Standardizza scrittura log JSON e Chroma ID | `tech_rag`, `refactor` |

## 🟡 Advanced Skills (Coming Soon)
- `sql_optimization`
- `frontend_design_system`
