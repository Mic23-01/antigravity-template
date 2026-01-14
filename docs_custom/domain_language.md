# Domain Language (Ubiquitous Language): Antigravity

> **AI Instruction**: Binding glossary for the Antigravity Project.

## 1. Core Entities (Nouns)
| Termine | Definizione Business (User) | Definizione Tecnica (AI) | Vincoli / Invarianti |
| :--- | :--- | :--- | :--- |
| **Agent** | L'entità autonoma che esegue i compiti. | `Models.Agent` / Process | Deve avere accesso a `.agent` root. |
| **Template** | La struttura base replicabile per nuovi progetti. | `docs/*.md` | Deve contenere placeholder iniziali. |
| **Hydration** | Il processo di compilazione di un Template in un Progetto. | `Workflow: custom_project` | Irreversibile su `docs_custom`. |
| **Workflow** | Sequenza operativa codificata. | `.agent/workflows/*.md` | Deve essere atomico e testabile. |

## 2. Processi Chiave (Verbs)
| Azione | Input | Output | Side Effects Importanti |
| :--- | :--- | :--- | :--- |
| **Hydrate** | User Context (Stack, Vision) | `docs_custom/` files | Crea nuova Source of Truth. |
| **Research** | Query | `research_summaries/` | Consuma token, aggiorna Chroma. |

## 3. Ambiguities & Anti-patterns
> Termini che NON dobbiamo usare o che creano confusione.
- **"Bot"**: Non usare. Usa invece **"Agent"**.
- **"Script"**: Se è un workflow strutturato, usa **"Workflow"**.
