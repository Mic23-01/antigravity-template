# 🧪 Antigravity Canary Scenarios

Questi scenari definiscono i casi di test per verificare che l'Agente stia operando al 100% della precisione protocollo.

## Scenario 1: The Smoke Test (Hygiene)
- **Obiettivo**: Verificare che `librarian` rilevi correttamente lo stato del progetto.
- **Workflow**: `/librarian`
- **Aspettativa**: Rilevamento `docs_custom/` presente e coerenza con `task.md`.

## Scenario 2: Deep Context (Cascade Verification)
- **Obiettivo**: Verificare che una richiesta tecnica forzi il caricamento della documentazione idratata.
- **Workflow**: `/tech_rag`
- **Input**: "Modifica il CSS della Dashboard seguendo il brand identity guide."
- **Aspettativa**: L'agente DEVE eseguire un `view_file` su `docs_custom/brand_identity_guide.md` PRIMA di fare proposte.

## Scenario 3: Strategic Alignment (Research)
- **Obiettivo**: Verificare che la ricerca sia legata alla Vision.
- **Workflow**: `/research_rag`
- **Input**: "Cerca nuovi pattern per UI agentiche 2026."
- **Aspettativa**: L'agente DEVE caricare `docs_custom/product_strategy.md` e citare come i pattern trovati aiutano a "Guidare alla realizzazione dei migliori template operativi".

## Scenario 4: Truth Conflict (Regression Gate)
- **Obiettivo**: Verificare l'aderenza al protocollo di validazione salvando dati in Chroma.
- **Input**: Qualsiasi task con flag `CANARY` o `EVAL_MODE=1`.
- **Aspettativa**: L'agente DEVE invocare `check_chroma.py` e presentare l'esito del Regression Gate.
