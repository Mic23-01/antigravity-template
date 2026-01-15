---
trigger: always_on
---

# Advanced Testing Strategy & QA Protocol (ALWAYS ON)

**TRIGGER**: Activate when the user asks to test code, debug, or verify functionality ("does it work?", "can you test it?").

## 1. Framing Phase (The Crossroads)
**INTERRUPT**: BEFORE writing or proposing any test, the Agent **MUST STOP** and ask the user for the desired depth level. DO NOT proceed autonomously with a plan.
- **Easy/Smoke Test**: Rapid verification ("does it work or explode?").
- **Deep/Regression**: Edge-case coverage, stress test, security check.
- **Serious Debug**: Defect isolation with sequential logic.

## 2. Tooling & MCP Integration
Use the right tools for the required level:

*   **Playwright (MCP + Extension)**:
    *   Use the installed VS Code extension (`Install in SSH: OVH`) to run tests visually.
*   **Sequential Thinking**:
    *   MANDATORY for "Serious Debugging". Analyze stacktrace -> formulate hypothesis -> write failing test -> fix.

## 3. Test Strategies (Easy vs Deep)

### 🟢 Easy / Smoke Mode
*   **Objective**: Immediate feedback (< 30 sec).
*   **UV + Pytest**:
    *   Use `uv` to execute pytest when available (e.g., `uv run pytest ...`).
    *   Standardize the use of markers for negative/fuzz testing (`-m negative`).
    *   `curl` or `httpie` scripts to verify live API endpoints.

### 🔴 Deep / Security Mode (Innovation)
*   **Objective**: Uncover hidden defects.
*   **Actions**:
    *   **Fuzzing**: Propose malformed inputs.
    *   **Concurrency**: Parallel tests (`pytest -n auto`).
    *   **Network Chaos**: Simulate latency or downtime of external services.
    *   **Negative Testing**: Include expected failure cases (dedicated markers if present).
    *   **Mandatory Markers**: For destructive or slow tests, always use markers (`@pytest.mark.negative`).

## 4. Code Best Practices
*   Use `pytest` as the standard runner.
*   Tests MUST be in separate folders (`tests/unit`, `tests/e2e`).
*   **NEVER** commit credentials in tests.
