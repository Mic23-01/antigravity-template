# PROGETTO ANTIGRAVITY - Project Agent Configuration
> **AI Instruction**: This file is the Source of Truth for Workflow Variables and Project Metadata.

- **ProjectName**: "Antigravity"
- **Prefix**: "AG"
- **WorkflowMode**: "Adaptive"
  - **Adaptive**: Attiva "Micro-Plan" per task semplici (< 3 file, no API/DB change).
  - **Strict**: Attiva protocollo completo (RAG profondo + Story Breakdown & Stop + FixLog dettagliato).
- **SmokeTestCmd**: "ls -la docs_custom/" (Default safe check for template integrity)
- **DeepTestCmd**: "uv run pytest -q"
- **DebugTestCmd**: "uv run pytest -q -vv --maxfail=1 --pdb"
- **NegativeTestMarkers**: "negative, fuzz, chaos"
