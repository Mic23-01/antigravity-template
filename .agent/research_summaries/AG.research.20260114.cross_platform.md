# Research Summary: Cross-Platform & Dependency Audit
> **ID**: AG.research.20260114.cross_platform
> **Project**: Antigravity
> **Date**: 2026-01-14

## Findings
1.  **Hardcoded Paths**: `dynamic_agent.py` uses `/tmp/ag_dynamic_sandbox`. This fails on native Windows.
2.  **Hidden Dependency**: `dynamic_agent.py` imports `yaml` but `canary_check.py` calls it with system `python3`. This causes "ModuleNotFoundError" on clean systems.

## Solution Analysis
*   **Pathing**: Use `tempfile.gettempdir()` for OS-agnostic temp locations.
*   **Execution**: Wrap subprocess calls with `uv run --with PyYAML`. This aligns with the "Gold Standard" of ephemeral environments.

## Evidence
- `dynamic_agent.py` Line 19: `SANDBOX_ROOT = Path("/tmp/ag_dynamic_sandbox")`
- `canary_check.py` Line 147: `dyn_cmd = ["python3", ...]`
