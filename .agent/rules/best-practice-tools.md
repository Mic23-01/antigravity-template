---
trigger: always_on
---

# MCP Tools & Best Practices Integration (ALWAYS ON)

**TRIGGER**: Activate when the user asks for architectural solutions, libraries, or needs to solve complex problems ("serious issues").

## 1. Resolution Hierarchy (MCP First)
Do not invent solutions; always verify them. Use tools in this precise order:

1.  **Preliminary Research (Brave Search)**:
    *   Search for "best practices [technology] 2025/2026" or "production ready [library]".
    *   *Goal*: Identify the current "gold standard".

2.  **Deep Documentation (Markdownify)**:
    *   Use `markdownify` to read the official sources identified.

3.  **Historical Memory (Chroma)**:
    *   Before writing code from scratch, ask Chroma if we have resolved a similar problem before.

## 2. Operational Standards (OS & Environment)
The target system is **Ubuntu 24.04 LTS** (Server). Solutions must adhere to these standards:

*   **Python**: ALWAYS use `uv` to manage venvs (`uv venv`, `uv pip install`).
*   **Package Management**:
    *   Global CLI tools -> `pipx install <tool>`.
    *   Project libraries -> in `pyproject.toml` or `requirements.txt`.
*   **Docker**:
    *   Always use `docker compose` (v2).
    *   Map volumes with explicit absolute paths (e.g., `$(pwd)/data:/app/data`).
*   **Refactoring**:
    *   Suggest a clean folder structure (e.g., `src/`, `tests/`, `scripts/`).
    *   Add essential docstrings (Google style).

## 3. Solution Proposal (The "Serious Plan")
If the problem is critical (e.g., data corruption, security breach, server down):
1.  **Immediate Stop**: Do not execute "trial" commands.
2.  **Diagnosis**: Request exact logs.
3.  **Recovery Plan**: Propose a 3-step strategy: *Mitigation*, *Backup*, *Fix*.

## 4. External Services (Free Tier / Validated)
If an external service is needed, propose self-hosted solutions or generous free-tier options first.
