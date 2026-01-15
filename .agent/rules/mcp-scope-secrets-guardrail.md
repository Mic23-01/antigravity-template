---
trigger: always_on
---

# MCP Scope & Secrets Guardrail (ALWAYS ON)

## Scopo
Questa regola impone confini e sicurezza quando l’Agent usa strumenti (MCP) e filesystem.

## Workspace Scope (OBBLIGATORIO)
- Considera come “root consentita” SOLO la root del workspace aperto.
- **INTERRUPT**: Se un’operazione richiede di uscire dal workspace, l'Agente **DEVE FERMARSI** e chiedere conferma esplicita motivata.

## Secrets & Sensitive Files (DIVIETO ASSOLUTO)
L'Agente **NON DEVE MAI** leggere, stampare o cercare contenuti in:
- Qualsiasi file `.env*` (`.env`, `.env.local`, ecc.)
- `**/mcp_secrets.env`
- `~/.ssh/**`, `**/id_rsa*`, `**/known_hosts`
- `**/secrets/**`, `**/*token*`, `**/*apikey*`, `**/*key*`

## Uso MCP: regole operative
- Usa `sequential-thinking` per pianificare ogni task non banale.
- Usa `brave-search` SOLO quando servono info esterne.
- Usa "context7" quando servono docs reali validati.
- Non inventare: se non trovi, dichiaralo e proponi il prossimo passo.

## Terminal safety
- Se un comando non è in Allow List, richiedi sempre review (ok).
- **INTERRUPT**: Non proporre comandi distruttivi (`rm`, `sudo`, `chmod -R`, ecc.) senza un piano dettagliato e conferma esplicita.