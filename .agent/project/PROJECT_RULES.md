# Antigravity Project Rules (Template Laws)

These rules are binding for every Antigravity Agent and define the template's quality standard.

## ⚖️ ANTI-RULE-0001: Zero Silence for Ghost Failures
**Status**: ACTIVE
**Trigger**: Testing commands (`<SmokeTestCmd>`)

The Agent **MUST NEVER** ignore pre-existing errors in the test suite, even if clearly unrelated to the current task.
- If "ghosts" (legacy errors) are detected at the start or during a task, the Agent must notify the user immediately.
- Operational silence in the presence of errors is considered a critical failure of the safety protocol.

## 📦 ANTI-RULE-0002: Gold Sources First
**Status**: ACTIVE
**Trigger**: RAG / Research phase

Before any external search, the Agent must prioritize the sources listed in `.agent/docs/SOURCES.md`.

## 🛠️ ANTI-RULE-0003: High-Frequency Performance 2026
**Status**: ACTIVE
**Trigger**: Refactoring of data-intensive UI components

For rapid UI updates (>100 dynamic nodes), prioritize reactive state patterns (Proxy/Signals) over pure immutability if benchmarks show frame rate degradation.

## 🛡️ ANTI-RULE-0004: Mandatory Test Reporting (The Seal)
**Status**: ACTIVE
**Trigger**: Every final chat output (notify_user)

The Agent **MUST ALWAYS** end every chat communication with a summary of the test status:
- **FORMAT**: `[TEST] ✅ Pass: X/N | ❌ Fail: Y/N`
- If no tests were run in the turn, it must still report the last known state saved in Chroma (fix_logs).
- This rule serves to remind both the Agent and the User that code is not "finished" until it is "verified."

## 🧹 ANTI-RULE-0005: Ephemeral Workspace (Auto-Cleanup)
**Status**: ACTIVE
**Trigger**: Every workflow that creates temporary files (R&D, Sandbox, Technical Prototyping)

The Agent **MUST** delete every temporary or test file created for exploratory purposes as soon as evidence has been collected or persisted in Chroma.
- It is forbidden to leave "Ghost Files" (e.g., `rnd_*.py`, `test_*.tmp`) in the repository after the task is finished.
- Cleanup should preferably occur in the same execution turn or as a mandatory final workflow action.
- **DOUBLE CHECK**: The agent MUST run a verification command (e.g., `ls <path>`) immediately after deletion to confirm removal before declaring the workspace clean.
