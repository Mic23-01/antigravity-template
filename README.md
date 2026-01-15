# Antigravity (AG) 🌌
> **The Deep Agentic Template for 2026**

Antigravity is an advanced, hybrid project template designed for building **Autonomous Agents** that are robust, replicable, and self-correcting. It bridges the gap between high-level reasoning (LLMs) and deterministic execution (Python/Node).

> **Mission**: To provide the "Gold Standard" operational foundation for AI Engineering, eliminating the fragility of traditional agent "demos".

## 🚀 Key Features

*   **Hybrid Architecture**: Seamlessly integrates Python (Backend/Tools), Node.js (Frontend), and Agentic Workflows.
*   **Dual Persistence Memory**: Combines **ChromaDB** (Vector Search) with **Filesystem Logs** (Human-readable markdown) for absolute recall and recoverability.
*   **Sequential Thinking**: Enforces "System 2" reasoning (Think -> Plan -> Act) before any critical operation.
*   **Strict Guardrails**: Pre-configured rules for Security (`secrets`), Testing (`regression`), and Quality (`linting`).
*   **Hydration Ready**: Designed to be cloned and "hydrated" into a custom project in minutes.

## 📂 Project Structure

```bash
.
├── .agent/                 # The "Brain": Memory, Rules, Skills, Workflows
│   ├── memory/             # Hot State (STATE.md) & Cold Logs
│   ├── rules/              # Active constraints (English-First)
│   ├── skills/             # executable toolkits (e.g., security_audit)
│   └── workflows/          # Standard Operating Procedures (.md)
├── docs_custom/            # 🧠 Project Intelligence (The "Soul")
│   ├── domain_language.md  # Ubiquitous Language & Definitions
│   ├── product_strategy.md # Vision, OKRs & Roadmap
│   ├── brand_identity.md   # UX/UI Guidelines
│   └── architecture.md     # Technical Design
├── .gitignore              # Pre-configured for Polyglot stacks
└── README.md               # This file
```

## 🛠️ Getting Started

### Prerequisites
*   **OS**: Ubuntu 22.04 / 24.04 (Recommended)
*   **Python**: Managed via `uv` (Fast Python package installer).
*   **Node.js**: LTS.

### Hydration (Creating a New Project)
To transform this template into your specific project (e.g., "SolarSystemBuilder"), run the **Custom Project Workflow**:

1.  Invoke the agent.
2.  Run the workflow: `@[/custom_project]`
3.  Follow the wizard to generate your specific `docs_custom/` and config.

## 🧠 Core Protocols

1.  **No "Raw" Thinking**: Every complex task starts with `sequential-thinking`.
2.  **English-First**: All Rules, Workflows, and System Logs must be in English for optimal AI comprehension.
3.  **Resume Capability**: The agent maintains a "Hot State" (`STATE.md`) to survive crashes.
4.  **Verify First**: Use `brave_search` or `markdownify` to validate libraries before coding.
5.  **Fail Fast**: Operations stop immediately if a "Regression Gate" or "Security Audit" fails.

## 🤝 Contributing
Refer to `.agent/rules/` for the strict contributor guidelines.

