---
name: fixlog_writer
description: Standardizes FixLog writing and handles Chrome persistence.
version: 1.0.0
author: Antigravity
---

# Operational Instructions

## Triggers
- At the end of every workflow involving modifications (`tech_rag`, `refactor`).
- When a technical intervention needs to be tracked (Step 6 Persistence).

## Inputs
- **Prefix**: (from `PROJECT_AGENT_CONFIG.md`) Project prefix.
- **ProjectName**: (from `PROJECT_AGENT_CONFIG.md`) Project name.
- **Log Data**: JSON containing `id`, `document` (description), and `metadatas` (project, type, date, files, tests, result).

## Steps
1. **Prepare Data**: Collect intervention data.
2. **Format JSON**: Create a JSON structure compatible with Chroma.
3. **Persist (Dual Write)**:
    - Write to `.agent/fix_logs/<ID>.json`.
    - Upsert to ChromaDB collection `fix_logs`.
4. **Verification**: Confirm file exists and Chroma entry is searchable.

## Usage Example
```python
# Typically used via internal script or agent call
log_entry = {
    "id": "FIX-001",
    "document": "Fixed critical bug in auth",
    "metadatas": { ... }
}
persist_log(log_entry)
```
