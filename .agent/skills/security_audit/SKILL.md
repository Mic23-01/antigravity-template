---
name: security_audit
description: Scansione di sicurezza per segreti, file rischiosi e dipendenze vulnerabili.
version: 1.0.0 (Divine)
author: Antigravity
---

# Istruzioni Operative

Questa skill esegue un audit di sicurezza statico sul progetto. Identifica file pericolosi, credenziali esposte e dipendenze rotte.

## Trigger
- **Pre-Commit**: Prima di caricare codice sensibile.
- **Refactor**: Quando si toccano file di configurazione.
- **On-Demand**: Richiesta esplicita "Verifica sicurezza".

## Inputs
- **Target Logic**: Directory da scansionare (default: `.`).
- **Exclude Patterns**: File/Cartelle da ignorare (es. `.git`, `.venv`, `node_modules`).

## Steps
1. **Secret Scanning**: Cerca pattern Regex (AWS, GitHub, Generic Keys) nei file tracciati.
2. **Risky Files Audit**: Cerca estensioni proibite (`.exe`, `.p12`, `.key`) e file giganti (>50MB).
3. **Dependency Check**: Esegue `uv pip check` per verificare la coerenza dell'ambiente Python.
4. **Reporting**: Genera un output JSON/Markdown con status PASS/FAIL per ogni check.

## Outputs
- **Console**: Log colorato con esito immediato.
- **Report**: Lista dei file violati (se FAIL).

## Fail-Fast
- Se trova **Segreti Confermati** (High Confidence), l'audit FALLISCE e richiede intervento manuale.

## Comandi Suggeriti
```bash
python3 .agent/skills/security_audit/scripts/audit_runner.py
```
