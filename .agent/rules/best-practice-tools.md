---
trigger: always_on
---

# MCP Tools & Best Practices Integration (ALWAYS ON)

**TRIGGER**: Attiva sempre quando l'utente chiede soluzioni architetturali, librerie, o deve risolvere problemi complessi ("problemi seri").

## 1. Gerarchia di Risoluzione (MCP First)
Non inventare soluzioni ma verificale sempre. Usa i tool in questo ordine:

1.  **Ricerca Preliminare (Brave Search)**:
    *   Cerca "best practices [tecnologia] 2025/2026" o "production ready [libreria]".
    *   *Obiettivo*: Identificare il "gold standard" attuale.

2.  **Documentazione Profonda (Markdownify)**:
    *   Usa `markdownify` per leggere le fonti ufficiali identificate.

3.  **Memoria Storica (Chroma)**:
    *   Prima di scrivere codice da zero, chiedi a Chroma se abbiamo già risolto un problema simile.

## 2. Standard Operativi (OS & Environment)
Il sistema target è **Ubuntu 24.03+ LTS** (Server). Le soluzioni devono rispettare questi standard:

*   **Python**: Usa SEMPRE `uv` per gestire i venv (`uv venv`, `uv pip install`).
*   **Gestione Pacchetti**:
    *   Tool CLI globali -> `pipx install <tool>`.
    *   Librerie di progetto -> nel `pyproject.toml` o `requirements.txt`.
*   **Docker**:
    *   Usa sempre `docker compose` (v2).
    *   Mappa i volumi con path assoluti espliciti (`/home/ubuntu/Progetti/...`).
*   **Refactoring**:
    *   Suggerisci una struttura a cartelle pulita (es. `src/`, `tests/`, `scripts/`).
    *   Aggiungi docstring essenziali (Google style).

## 3. Proposta di Soluzioni (Il "Piano Serio")
Se il problema è critico (es. data corruption, security breach, server down):
1.  **Stop immediato**: Non dare comandi "tentativo".
2.  **Diagnosi**: Chiedi i log esatti.
3.  **Piano di recupero**: Proponi una strategia in 3 step: *Mitigazione*, *Backup*, *Fix*.

## 4. Servizi Esterni (Free Tier / Validati)
Se serve un servizio esterno, proponi prima soluzioni self-hosted o con free-tier generoso.

