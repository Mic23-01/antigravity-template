# Esempio d'Uso: fixlog_writer

Questa skill standardizza la creazione dei FixLog per ridurre errori di formato e garantire che meta-dati critici (come `result` o `files`) siano sempre presenti.

## Generazione Payload (Dry Run)
Usa lo script per generare il JSON corretto da incollare nel tool `chroma_add_documents`.

```bash
python3 .agent/skills/fixlog_writer/scripts/write_log.py \
  --project "Antigravity" \
  --desc "Standardized all skill definitions" \
  --files ".agent/skills/resolve_canon_sources/SKILL.md, .agent/skills/test_gate_bivio/SKILL.md" \
  --test "Canary Check passed" \
  --result "pass" \
  --dry-run
```

## Integrazione nei Workflow
In `tech_rag.md` (Step 6), invece di scrivere "Salva un documento...", ora si invoca:

> **Skill**: `fixlog_writer` (Standardizza il payload JSON).

## Output Atteso
Un JSON valido pronto per l'ingestione:
```json
{
  "id": "AG.fix.20260114.a1b2c3d4",
  "document": "Standardized all skill definitions",
  "metadatas": {
    "project": "Antigravity",
    "type": "fix_log",
    "date": "2026-01-14",
    ...
  }
}
```
