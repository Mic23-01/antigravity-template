# Research Summary: Antigravity Project Hygiene Update (2026-01-15)

## 1. Context & Objective
The Antigravity project has evolved significantly ("Hyperscalable Template"). New components (Checkpoint System, Dual Persistence, Deep Tests) have introduced new artifacts.
**Objective**: Bring `.gitignore` and `README.md` up to date to reflect the current operational state and prevent repository bloat.

## 2. Analysis of Gaps

### A. `.gitignore` Compliance
| Path | Status | Recommendation | Rationale |
| :--- | :--- | :--- | :--- |
| `.agent/memory/backups/` | **Unmanaged** | **IGNORE** | Local state rotation (5 backups) is heavy/noisy. Recovery is via Git or fresh hydration. |
| `.agent/audit/agent_events.jsonl` | **Unmanaged** | **KEEP** (or IGNORE?) | *Decision*: **KEEP** for now. Sentinel relies on it. If it grows too large, we'll need a rotation policy. |
| `verifiche_test/` | **Unmanaged** | **IGNORE** | Transient artifacts from stress testing. Not part of the core template. |
| `.agent/fix_logs/` | **Unmanaged** | **KEEP** | Critical for "Dual Persistence". Must be in repo to prove history. |
| `.gemini/` | **Unmanaged** | **IGNORE** | Artifact/Brain directory for the agent (ephemeral/local). |
| `__pycache__` | **Managed** | **KEEP** | Already correctly ignored. |

### B. `README.md` Accuracy
The current README is outdated regarding:
1.  **Checkpoint Architecture**: Does not mention `STATE.md` or the "Hot/Cold" memory model.
2.  **Language Policy**: Does not explicitly state the "English-First" rule for documentation/logs.
3.  **Project Structure**: `.agent/memory` has evolved (contains `backups`, `checkpoint_manager.py`).

## 3. Proposal

### Action 1: Update `.gitignore`
Append the following:
```gitignore
# Checkpoint System
.agent/memory/backups/
.agent/memory/STATE.md  # Debatable: Do we want to share state? No, it's session-specific.
# Actually, STATE.md is "Hot Memory". Sharing it might confuse a new cloner.
# Better to IGNORE STATE.md and let init script create a fresh one.

# Transient Tests
verifiche_test/

# Agent Brain (Gemini)
.gemini/
```

### Action 2: Update `README.md`
- Add section on **Checkpoint System** (Resume capabilities).
- Update **Project Structure** tree.
- Refresh **Core Protocols** to include "English-First" and "FixLog Mandatory".

## 4. Conclusion
Proceed with these updates to ensure the template remains "Production Ready" and clean.
