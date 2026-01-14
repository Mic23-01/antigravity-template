# Esempio d'Uso: security_audit

## Esecuzione Rapida
Per scansionare l'intero progetto alla ricerca di problemi di sicurezza:

```bash
python3 .agent/skills/security_audit/scripts/audit_runner.py
```

## Cosa Controlla
1. **Secrets**: Pattern Regex per token GitHub, AWS, Chiavi Private.
2. **Risky Files**: File binari (`.exe`, `.dll`), chiavi esposte (`.pem`), e file > 50MB.
3. **Dependencies**: Integrità dei pacchetti Python installati via `uv`.

## Output Interpretazione
- **PASS**: Nessun problema rilevato.
- **FAIL**: Trovati problemi. Controlla i log per i dettagli (file path esatto).
