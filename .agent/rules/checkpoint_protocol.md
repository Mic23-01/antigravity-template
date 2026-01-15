---
trigger: always_on
description: Checkpoint / Compaction Protocol (STATE + NEXT) to mitigate Double Penalty
globs: "**/*"
---

# 🛡️ CHECKPOINT PROTOCOL (Primitive)

**GOAL**: Mitigate "Double Penalty" (Human Context Re-download) by maintaining a compact, real-time narrative of the session state.

## 1. The Mechanic (Hot Path)
**TRIGGER**: Before every `notify_user` OR after every ~5 significant tool calls (e.g., end of a Phase).

**ACTION**: You MUST update the "Hippocampus" file `.agent/memory/STATE.md`.
Use the provided utility script for robustness (never edit raw if script is available).

```bash
python3 .agent/memory/checkpoint_manager.py update \
  --state "Brief narrative of WHERE we are (e.g., 'Analyzing AST for refactor')." \
  --context "Compacted history of last events (e.g., '1. Created file X. 2. Failed test Y. 3. Fixed bug Z')." \
  --next "Immediate next atomic step (e.g., 'Run pytest')."
```

## 2. The Format (Double Penalty Shield)
The content of `STATE.md` serves as a "Quick Resume" for the user/operator. It must be:
- **Narrative**: Not just a list of files, but the *reasoning* trajectory.
- **Compacted**: Do not dump logs. Summarize findings.
- **Forward-Looking**: `@NEXT` must be precise.

## 3. Storage (Cold Path)
When the session ends or you run `@[/librarian]`, the `STATE.md` is archived into the historical logs. This separation ensures `STATE.md` remains a lightweight "Runtime Cache".

> [!IMPORTANT]
> If you crash or the session resets, READ `.agent/memory/STATE.md` immediately to resume your thought process.
