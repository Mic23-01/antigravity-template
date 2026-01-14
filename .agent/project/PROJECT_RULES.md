# Antigravity Project Rules (Template Laws)

Queste regole sono vincolanti per ogni Agente Antigravity e definiscono lo standard di qualità del template.

## ⚖️ ANTI-RULE-0001: Zero Silence for Ghost Failures
**Status**: ACTIVE
**Trigger**: Comandi di testing (`<SmokeTestCmd>`)

L'Agente **NON DEVE MAI** ignorare errori pre-esistenti nella suite di test, anche se palesemente non correlati al task corrente.
- Se all'inizio o durante un task vengono rilevati "fantasmi" (errori legacy), l'Agente deve segnalarli immediatamente all'utente.
- Il silenzio operativo in presenza di errori è considerato un fallimento critico del protocollo di sicurezza.

## 📦 ANTI-RULE-0002: Gold Sources First
**Status**: ACTIVE
**Trigger**: Fase di RAG / Research

Prima di ogni ricerca esterna, l'Agente deve prioritizzare le fonti elencate in `.agent/docs/SOURCES.md`.

## 🛠️ ANTI-RULE-0003: High-Frequency Performance 2026
**Status**: ACTIVE
**Trigger**: Refactoring di componenti UI ad alta intensità di dati

Per aggiornamenti UI rapidi (>100 nodi dinamici), prioritizzare pattern di stato reattivo (Proxy/Signals) rispetto all'immutabilità pura se i benchmark mostrano degradazione del frame rate.

## 🛡️ ANTI-RULE-0004: Mandatory Test Reporting (The Seal)
**Status**: ACTIVE
**Trigger**: Ogni output finale della chat (notify_user)

L'Agente **DEVE SEMPRE** terminare ogni comunicazione in chat con un riepilogo dello stato dei test:
## 🧹 ANTI-RULE-0005: Ephemeral Workspace (Auto-Cleanup)
**Status**: ACTIVE
**Trigger**: Ogni workflow che crea file temporanei (R&D, Sandbox, Prove tecniche)

L'Agente **DEVE** eliminare ogni file temporaneo o di test creato per scopi esplorativi non appena l'evidenza è stata raccolta o persistita in Chroma.
- È vietato lasciare "Ghost Files" (es. `rnd_*.py`, `test_*.tmp`) nel repository dopo il termine del task.
- La pulizia deve avvenire preferibilmente nello stesso turno di esecuzione o come azione finale obbligatoria del workflow.
- **DOPPIO CHECK**: L'agente DEVE eseguire un comando di verifica (es. `ls <path>`) immediatamente dopo la cancellazione per confermare l'avvenuta rimozione prima di dichiarare il workspace pulito.
- Questa regola serve a ricordare all'Agente e all'Utente che il codice non è "finito" finché non è "verificato".
- **FORMATO**: `[TEST] ✅ Pass: X/N | ❌ Fail: Y/N`
- Se non sono stati eseguiti test nel turno, deve comunque riportare l'ultimo stato noto salvato in Chroma (fix_logs).
- Questa regola serve a ricordare all'Agente e all'Utente che il codice non è "finito" finché non è "verificato".
