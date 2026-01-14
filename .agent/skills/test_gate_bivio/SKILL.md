---
name: test_gate_bivio
description: Gestisce l'interazione del test gate rispettando la profondità richiesta
version: 1.0.0
---

# Istruzioni Operative

## Scopo
Gestire l'interazione del test gate secondo protocollo `testing-strategy.md`.

## Logica
1. **Interrupt**: CHIEDI all'utente il livello di test desiderato (Easy, Deep, Debug).
2. **Easy/Smoke**:
   - Esegui comando `<SmokeTestCmd>` (definito in `.agent/project/PROJECT_AGENT_CONFIG.md`).
3. **Deep**:
   - Esegui test di regressione completi (`pytest`, `npm test`, etc).
4. **Debug**:
   - Attiva `sequential-thinking` per isolare il caso.

## Configurazione
Verifica `.agent/project/PROJECT_AGENT_CONFIG.md` per il comando Smoke di default.
