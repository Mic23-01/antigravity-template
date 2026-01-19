![Python](https://img.shields.io/badge/python-3.10+-blue)
![uv](https://img.shields.io/badge/uv-native-blueviolet)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-production--ready-success)
![Agentic](https://img.shields.io/badge/architecture-agentic-orange)

# Antigravity (AG) 🌌

> [!NOTE]
> **Disclaimer**: This project, "Antigravity (AG)", is an independent template for Agentic AI development and is **not** affiliated with, endorsed by, or connected to Google's "Antigravity" project or deep research initiatives. "Antigravity" here refers to the concept of lifting the burden of maintenance through AI.

## About

🚀 **Antigravity**: The definitive template for building production-grade Autonomous Agents. Hybrid architecture, dual-layer memory (ChromaDB + Filesystem), sequential thinking, and battle-tested guardrails. From concept to deployment in minutes.

## Project Overview

Advanced project template designed for building **robust, replicable, and self-correcting AI Agents**. Bridges high-level LLM reasoning with deterministic Python/Node execution. Features dual persistence memory, strict security protocols, and a complete toolkit of workflows, skills, and evaluators.

> **Mission**: Provide the "Gold Standard" operational foundation for AI Engineering, eliminating the fragility of traditional agent "demos".

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **Hybrid Architecture** | Seamlessly integrates Python (Backend/Tools), Node.js (Frontend), and Agentic Workflows |
| **Dual Persistence Memory** | Combines **ChromaDB** (Vector Search) with **Filesystem Logs** (Human-readable JSON/Markdown) |
| **Sequential Thinking** | Enforces "System 2" reasoning (Think → Plan → Act) before any critical operation |
| **Strict Guardrails** | Pre-configured rules for Security, Testing (Regression Gate), and Quality |
| **Hydration Ready** | Clone and customize for any project via interactive wizard in minutes |
| **Resume Capability** | Hot State persistence (`STATE.md`) survives crashes and context resets |
| **English-First** | All rules, workflows, and logs in English for optimal AI comprehension |

## 📂 Project Structure

```bash
.
├── .agent/                 # The "Brain": Memory, Rules, Skills, Workflows
│   ├── memory/             # Hot State (STATE.md) & Cold Logs
│   ├── audit/              # Machine Logs & Human Summaries (JSONL + MD)
│   ├── fix_logs/           # Persistent technical fix records (JSON)
│   ├── evals/              # Capability evaluation suite (Triad: Refactor/Bugfix/Feature)
│   ├── rules/              # Active constraints & protocols
│   ├── skills/             # Executable toolkits (security_audit, fixlog_writer, etc.)
│   ├── tools/              # Python utilities (canary_check, librarian, etc.)
│   └── workflows/          # Standard Operating Procedures (.md)
├── docs_custom/            # 🧠 Project Intelligence (The "Soul")
│   ├── SOURCES.md          # Canon Source hierarchy & Gold references
│   ├── domain_language.md  # Ubiquitous Language & definitions
│   ├── product_strategy.md # Vision, OKRs & Roadmap
│   ├── brand_identity_guide.md # UX/UI Guidelines & tokens
│   └── architecture.md     # Technical design & ADRs
├── LICENSE                 # MIT License
└── README.md               # This file
```

## 🛠️ Quick Start

### Prerequisites
- **OS**: Ubuntu 22.04 / 24.04 LTS (Recommended)
- **Python**: Managed via [`uv`](https://docs.astral.sh/uv/) (Fast Python package manager)
- **Node.js**: LTS (Optional, for frontend projects)

### 1. Clone the Template

```bash
git clone https://github.com/Mic23-01/antigravity-template.git my-project
cd my-project
```

### 2. Run Canary Check

```bash
uv run .agent/tools/canary_check.py --no-sentinel
```

### 3. Hydrate Your Project

Invoke your AI agent and run:
```
@[/custom_project]
```
Follow the interactive wizard to generate your `docs_custom/` and project-specific configuration.

## 🧠 Core Protocols

| # | Protocol | Description |
|---|----------|-------------|
| 1 | **No "Raw" Thinking** | Every complex task starts with `sequential-thinking` |
| 2 | **English-First** | All Rules, Workflows, and System Logs in English |
| 3 | **Resume Capability** | Agent maintains "Hot State" (`STATE.md`) to survive crashes |
| 4 | **Verify First** | Use RAG tools (`brave_search`, `markdownify`) to validate before coding |
| 5 | **Fail Fast** | Operations halt immediately if Regression Gate or Security Audit fails |
| 6 | **Dual Persistence** | Every fix logged to both ChromaDB and filesystem for recoverability |

## 🔧 Included Workflows

| Workflow | Purpose |
|----------|---------|
| `/tech_rag` | Technical tasks with adaptive complexity (Strict/Adaptive modes) |
| `/research_rag` | Deep research with structural impact analysis (DuckDB) |
| `/refactor` | Large-scale refactoring with AST analysis and blast radius |
| `/custom_project` | Interactive hydration wizard for new projects |
| `/librarian` | Proactive hygiene, ghost code detection, documentation sync |

## 🛡️ Built-in Skills

| Skill | Function |
|-------|----------|
| `regression_gate` | Unified validator for Chroma & Filesystem integrity |
| `fixlog_writer` | Standardized JSON log generation with ChromaDB persistence |
| `security_audit` | Secret scanning, risky file detection, dependency checks |
| `test_gate_bivio` | Interactive test depth selector (Smoke/Deep/Debug) |
| `resolve_canon_sources` | Source hierarchy resolution (Custom > Template) |
| `ui_ux_designer` | Design database access for colors, typography, styles |

## 🏆 Best Practices Enforced

- ✅ **Zero Silence Policy**: Pre-existing errors reported immediately
- ✅ **Atomic Changes**: Small, localized, verifiable modifications
- ✅ **Security Guardrails**: No `.env` leakage, secrets scanning, scope limits
- ✅ **Evidence Bundle**: Every task outputs what changed, tests run, and FixLog ID

## Requirements

- Python 3.10+
- `uv` (recommended) or `pip`
- ChromaDB (optional, for vector memory)

## Support & Community

- **GitHub Issues**: Bug reports and feature requests
- **Workflows Documentation**: Complete guides in `.agent/workflows/`
- **Contributions**: Welcome! Follow the English-First policy for PRs

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Project Founder**: MIC | **Version**: 2.0.0 | **Status**: Production Ready
