# Architecture & Technical Design 🏗️

## 1. System Overview
**Antigravity** is a Python-centric agentic framework designed to minimize the fragility of LLM-based systems through strict protocol enforcement and dual-persistence memory.

## 2. Technology Stack
- **Primary Runtime**: Python 3.12+
- **Dependency Management**: `uv` (Fastest resolver and manager).
- **Persistence**: 
    - **Vector Memory**: ChromaDB (Active search and context).
    - **Human Logs**: Filesystem-based Markdown (.agent/fix_logs).
- **Communication Layer**: MCP (Model Context Protocol) for tool and service integration.
- **Frontend (Optional)**: Node.js/Vite for visualization components.

## 3. High-Level Modular Design
- **Brain (`.agent/`)**: Orchestration of rules, skills, and memory.
- **Sentinel**: Hard-gated session integrity tracker.
- **Runner**: Automated capability evaluation suite.

## 4. Integration Strategy
No external dedicated databases are planned. All specialized services and data connections are handled via **MCP Servers**, ensuring a decoupled and highly modular architecture.
