---
description: "Project Hydration Wizard: Transforms Antigravity Templates into Living Documentation (`docs_custom/`)."
---

1) Context Discovery (The Automated Audit)
- **Goal**: Deduce everything technically possible without asking the user.
- **Action**: Execute deep structural analysis (Repo-first).
  - **Primary**: Read `package.json`, `requirements.txt`, `pyproject.toml` for the Stack.
  - **Fallback**: If configs are missing, use `find` or `grep` to deduce structure or search for import patterns.
  - **Active Check**: If necessary, run safe commands (`node -v`, `python --version`) or exploration scripts.
  - **Intervention**: If ambiguity persists (> 20%), **ASK** the user explicitly before inventing.
  - **Style Check**: Search for `tailwind.config.js` or root CSS variables to deduce the palette.
- **Tool**: `view_file`, `run_command` (safe), `librarian`.

2) Gap Analysis & Interview (The User Check)
- **Comparison**: Read placeholders in **Original Templates**:
  - `.agent/docs/architecture.md`
  - `.agent/docs/brand_identity_guide.md`
  - `.agent/docs/domain_language.md`
  - `.agent/docs/product_strategy.md`
  - `.agent/docs/SOURCES.md`
- **Interview**: Formulate a series of targeted questions for the user to bridge gaps (e.g., "What is the 12-month Vision?", "Define the term 'Player'").
- **Constraint**: Do NOT proceed to generation until the user has responded.

3) Hydration Generation (The Build)
- **Action**: Create the target directory `docs_custom/` (if it doesn't exist).
- **Skill**: Activate `ui_ux_designer` to find consistent palettes and fonts if undefined.
- **Action**: For each template:
  - Replace placeholders with collected data (Audit + Interview + UI Skill).
  - Remove "AI Instruction" sections.
  - Write the final file to `docs_custom/<filename>`.
- **Naming Convention**: Maintain the same filenames as the templates for consistency.

4) Validation & Binding (The Handshake)
- **Review**: Ask the user to validate the files in `docs_custom/`.
- **Commit**: Once approved, these files become the **Specific Source of Truth** for the project.
- **FILESYSTEM UPDATES**: Notification of new file creation.
