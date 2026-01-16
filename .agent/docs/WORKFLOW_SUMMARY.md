# Antigravity Workflow Reference

This guide provides a concise summary of the operational workflows available in the project. Use **Slash Commands** (e.g., `@[/research_rag]`) to activate the Agent for specific tasks.

| Workflow | Slash CMD | When to Use | What it Does |
| :--- | :--- | :--- | :--- |
| **Project Hydration** | `@[/custom_project]` | At the start of a new project or to update core docs. | Transforms generic templates into living documentation (`docs_custom/`). Guides the compilation of Vision, Domain Language, and Strategy. |
| **Deep Research** | `@[/deep_rag]` | For complex, comparative research or future topics (2026+). | Recursive search across multiple axes (Official, Skeptical, Future). Generates impact scorecards and in-depth analysis. |
| **Librarian** | `@[/librarian]` | When the project feels "dirty" or disorganized. | **Hygiene & Structure**. Removes unused files (ghost code), syncs documentation, and verifies system integrity (Canary Check). |
| **Refactoring** | `@[/refactor]` | For risky structural changes or technical debt. | Analyzes AST and Blast Radius. Plans safe modifications with a mandatory rollback plan. |
| **Architect Research** | `@[/research_rag]` | For architectural decisions or setting up new technologies. | Precision RAG protocol: Cannon Source -> Internal Scan -> Synthesis. Generates specific Implementation Blueprints. |
| **Tech Task** | `@[/tech_rag]` | For standard implementation tasks (Feature/Bugfix). | Cycle: Research -> Plan -> Code -> Test -> Verification. Ideal for daily development. |

> [!TIP]
> **Canary Check**: The `@[/librarian]` workflow now includes an automated integrity check (`canary_check.py`) to ensure rules and workflows are healthy.
