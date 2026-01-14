---
name: ui_ux_designer
description: "AI Design Lead: Accesso a database di stili, palette e tipografia."
version: 1.0.0
---

# UI/UX Designer Skill

Attiva questa skill quando devi prendere decisioni estetiche, generare CSS o definire lo stile del progetto.

## 🛠️ Tools
### Ricerca Stile
Usa questo comando per trovare configurazioni reali (non inventate):
`python3 .agent/skills/ui_ux_designer/scripts/search_design.py --query "<keywords>" --type <colors|typography|styles|products|ux|landing|charts>`

## 📋 Protocollo Operativo
1. **Search**: Cerca sempre nel database prima di proporre un colore.
2. **Apply**: Se stai idratando un progetto (`custom_project`), usa i valori trovati per compilare `docs_custom/brand_identity_guide.md`.
3. **Fallback**: Se il database non restituisce risultati, usa lo stile "Minimal Monochrome".

## 🚫 Divieti
- Non inventare codici Hex (es. `#123456`) se non presenti nel database o nel `brand_identity_guide.md` (a meno che non siano sfumature calcolate).
- Non hardcodare stili nei componenti React senza prima averli definiti nei token globali.
