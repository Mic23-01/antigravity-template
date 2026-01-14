# Project Agent Configuration
> **AI Instruction**: This file is the Source of Truth for Workflow Variables.

- **ProjectName**: "Antigravity"
- **Prefix**: "AG"
- **WorkflowMode**: "Adaptive"
  - **Adaptive**: Attiva "Micro-Plan" per task semplici (< 3 file, no API/DB change).
  - **Strict**: Attiva protocollo completo (RAG profondo + Story Breakdown & Stop + FixLog dettagliato).
- **SmokeTestCmd**: "ls -la docs_custom/" (Default safe check for template integrity)
