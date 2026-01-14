---
name: test_gate_bivio
description: Gestisce l'interazione del test gate rispettando la profondità richiesta
version: 1.1.0
author: Antigravity
---

# Istruzioni Operative

## Trigger
- All'interno di `tech_rag` (Step 5 Test Gate).
- Ogni volta che è necessaria una validazione interattiva prima di procedere.

## Inputs
- **User Config**: `<SmokeTestCmd>` in `.agent/project/PROJECT_AGENT_CONFIG.md`.
- **User Choice**: Interazione diretta (Easy/Deep/Debug).

## Steps
1. **Interrupt**: CHIEDI all'utente il livello di test desiderato.
2. **Easy/Smoke**:
   - Esegui comando `<SmokeTestCmd>`.
3. **Deep**:
   - Esegui test di regressione completi (`pytest`, `npm test`, etc).
4. **Debug**:
   - Attiva `sequential-thinking` per isolare il caso.

## Outputs
- **Result**: `PASS` (proceed) o `FAIL` (fix required).

## Configurazione
Verifica `.agent/project/PROJECT_AGENT_CONFIG.md` per il comando Smoke di default.
