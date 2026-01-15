---
trigger: always_on
---

# Advanced Testing Strategy & QA Protocol (ALWAYS ON)

**TRIGGER**: Attiva quando l'utente chiede di testare codice, fare debugging, o verificare funzionalità ("funziona?", "puoi testarlo?").

## 1. Fase di Inquadramento (Il Bivio)
**INTERRUPT**: PRIMA di scrivere o proporre qualsiasi test, l'Agente **DEVE FERMARSI** e chiedere all'utente il livello di profondità desiderato. NON procedere autonomamente con un piano.
- **Easy/Smoke Test**: Verifica rapida ("funziona o esplode?").
- **Deep/Regression**: Copertura edge-case, stress test, security check.
- **Debug Serio**: Isolamento del difetto con logica sequenziale.

## 2. Tooling & MCP Integration
Usa gli strumenti giusti per il livello richiesto:

*   **Playwright (MCP + Extension)**:
    *   Usa l'estensione VS Code installata (`Install in SSH: OVH`) per runnare i test visualmente.
*   **Sequential Thinking**:
    *   OBBLIGATORIO per il "Debugging Serio". Analizza stacktrace -> formula ipotesi -> scrivi test che fallisce -> fixa.

## 3. Strategie di Test (Easy vs Deep)

### 🟢 Easy / Smoke Mode
*   **Obiettivo**: Feedback immediato (< 30 sec).
*   **UV + Pytest**:
    *   Usa `uv` per eseguire i test pytest quando disponibile (es. `uv run pytest ...`).
    *   Standardizza l'uso di marker per negative/fuzz testing (`-m negative`).
    *   Script `curl` o `httpie` per verificare endpoint API vivi.

### 🔴 Deep / Security Mode (Innovazione)
*   **Obiettivo**: Scovare difetti nascosti.
*   **Cosa fare**:
    *   **Fuzzing**: Proponi input malformati.
    *   **Concurrency**: Test paralleli (`pytest -n auto`).
    *   **Network Chaos**: Simula latenza o down dei servizi esterni.
    *   **Negative Testing**: Includi casi di fallimento attesi (marker dedicati se presenti).
    *   **Marker Obbligatori**: Per test distruttivi o lenti, usa sempre marker (`@pytest.mark.negative`).

## 4. Best Practice di Codice
*   Usa `pytest` come runner standard.
*   I test DEVONO essere in cartelle separate (`tests/unit`, `tests/e2e`).
*   **MAI** committare credenziali nei test.

