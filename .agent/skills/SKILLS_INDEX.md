# Antigravity Skills Index

This catalog maps the modular competencies ("Skills") available to the Agent.
Each skill is a self-contained directory in `.agent/skills/<skill_name>/`.

## 🟢 Base Skills (Core)
| Skill Name | Description | Trigger Workflow |
|------------|-------------|------------------|
| `resolve_canon_sources` | Resolves the source hierarchy (Custom > Template) | All RAG workflows |
| `test_gate_bivio` | Manages test gate interaction (Smoke vs Deep) | `tech_rag` |
| `regression_gate` | Ensures Chroma and Filesystem integrity | All RAG workflows |
| `fixlog_writer` | Standardizes JSON log writing and Chroma ID | `tech_rag`, `refactor` |
| `security_audit` | Security scan for secrets and risky files | `tech_rag` |
| `ui_ux_designer` | Design Intelligence & Assets Search | `custom_project`, `tech_rag` |
| `excalidraw_canvas` | Advanced Visual Drawing & Architecture Management | `tech_rag`, `refactor` |

## 🟡 Advanced Skills (Coming Soon)
- `sql_optimization`
- `visual_regression`
