---
description: "Librarian Agent: Proactive Hygiene, Document Sync, and Structural Analysis (DuckDB)"
---

1) Preparation & Planning
- Consult the Leader Supervisor (`.agent/rules/global-validation-protocol.md`).
- Goal: Keep the project clean, updated, and free of "Ghost Code".

2) Structural Analysis (The SQL Eye)
- **DuckDB Audit**: Execute automated structural audit.
  `uv run --with duckdb python3 .agent/project/librarian.py --audit`
- Identify:
    - **Ghost Files**: Unimported files or orphan duplicates.
    - **Dead Code**: Functions/Classes without references (use `grep_search` to validate).
    - **Documentation Drift**: Verify if `docs_custom/` is up-to-date with code.
    - **Missing Context**: Flag if core files are missing in `docs_custom/`.

3) Active Sync
- **Mandatory Authorization**: If the Librarian identifies missing or obsolete documentation (e.g., README, ADR, DOCS), it **MUST** describe the proposed content and ask for permission via `notify_user` before creating or modifying files.
- **README Update**: Propose updates to file maps and descriptions.
- **DOCS Sync**: Propose links for new ADRs or Research in indices.
- **SSOT Check**: Verify coherence of constants/parameters between frontend and backend.

3.5) Checkpoint Archiving (Memory Consolidation)
- **State Archiving**: Read `.agent/memory/STATE.md` (if exists).
- **Append**: Append the content to the session history in `docs_custom/session_history.md` (if exists) or Chroma logs with tag `session_summary`.
- **Reset**: (Optional) If the session is concluded, rotate `.agent/memory/STATE.md` to clear context for the next startup.

4) Cleaning & Optimization
- Propose removal of files identified as "Ghost".
- Archive completed tasks from `task.md` into the historical changelog.
- Optimize Chroma metadata by eliminating redundant or obsolete entries.

5) Verification & Closure
- Execute original `librarian.py` script for schema validation.
- **Chroma Persistence**: Save the result in the `fix_logs` collection.
    - **ID**: `<Prefix>.hygiene.YYYYMMDD.<slug>`
    - **Metadata**: `project=<ProjectName>, type=hygiene_log, date=YYYY-MM-DD, result=pass|fail, notes=...`
- **Regression Gate**: Execute `check_chroma.py` on the generated ID.
- **System Integrity**: Execute `.agent/tools/canary_check.py` to ensure hygiene didn't break anything.

6) Final Output
- Report of hygiene actions performed.
- **FILESYSTEM UPDATES**: Mandatory for every output (Leader Rule).
